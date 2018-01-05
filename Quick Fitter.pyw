from PyQt5 import uic, QtWidgets, QtCore, QtGui
import matplotlib.pyplot as plt
import numpy as np
import sys
import pandas as pd
from scipy.optimize import curve_fit
import functions
import os
from textwrap import wrap
from collections import OrderedDict

file_name = ""
lenax = 0
abol = True
global_plt_index = 0
boxDict = {}
buttonDict = {}
plotDict = OrderedDict()
fitDict = OrderedDict()

class Label(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.p = None

    def setPixmap(self, p):
        self.p = p

    def paintEvent(self, event):
        if self.p:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.SmoothPixmapTransform)
            painter.drawPixmap(self.rect(), self.p)


class UiWindow(QtWidgets.QMainWindow, QtWidgets.QWidget):

    def __init__(self):
        super(UiWindow, self).__init__()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        uic.loadUi(dir_path + "\\a.ui", self)

        # Windows options
        self.setWindowTitle('Quick Fit Ver 0.30')

        # Buttons
        self.clearplotButton.setEnabled(False)
        self.clearplotButton.clicked.connect(self.clearplot)

        self.clearallplotsButton.setEnabled(False)
        self.clearallplotsButton.clicked.connect(self.clearallplots)

        self.plotButton.setEnabled(False)
        self.plotButton.clicked.connect(self.plotcolumns)

        self.fitButton.setEnabled(False)
        self.fitButton.clicked.connect(self.fit)

        self.clearButton.setEnabled(False)
        self.clearButton.clicked.connect(self.clearfit)

        self.clearallButton.setEnabled(False)
        self.clearallButton.clicked.connect(self.clearallfits)

        self.setLabelsButton.setEnabled(False)
        self.setLabelsButton.clicked.connect(self.addlabels)

        self.setLimitsButton.setEnabled(False)
        self.setLimitsButton.clicked.connect(self.setlimits)

        self.errorBarButton.setEnabled(False)
        self.errorBarButton.clicked.connect(self.adderrors)

        # Text fields i other areas
        self.scrollArea.setWidgetResizable(False)
        self.scrollArea_files.setWidgetResizable(False)
        self.textBrowser.setText("Output: ")

        # Tollbar actions
        self.actionSave_Plot.setEnabled(False)
        self.actionSave_Plot.triggered.connect(self.savefile)
        self.actionReadme.triggered.connect(self.readme)

        self.actionLoad_File.triggered.connect(self.loadfile)
        self.pixlabel.mousePressEvent = self.mouseclicked

        # Rest
        self.show()

    # Methods definitios

    def loadfile(self):
        global file_name
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        try:
            file_name, _ \
                = QtWidgets.QFileDialog.getOpenFileName(self, "Choose file",
                                                        "", "All Files (*);;" 
                                                        "Excel Files ("
                                                        "*.csv)",
                                                        options=options)
            self.reload()

        except TypeError:
            pass

        try:

            self.loadmultifiles(file_name)
            for button, path, plt_index, name in buttonDict.values():
                self.connect_load(button, path, plt_index)
        except Exception:
            pass

    def reload(self, x=True):

        if x:
            while self.gridLayout.count():
                child = self.gridLayout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
            while self.gridLayout_files.count():
                child = self.gridLayout_files.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

            lenax = 0
            boxDict.clear()
            plotDict.clear()
            fitDict.clear()
            buttonDict.clear()
            plt.clf()

        else:
            
            lenax = 0
            boxDict.clear()
            fitDict.clear()

            while self.gridLayout.count():
                child = self.gridLayout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

    def createbox(self, file, plt_index):
        global df
        global global_plt_index
        try:
            with open(file, 'r') as data:
                aa = data.readline()
        except Exception:
            return 0
        with open(file, 'r') as data:
            fildat = data.read()
            if len(aa.split("\t")) == 1:
                if len(aa.split(" ")) == 1:
                    df = pd.read_csv(pd.compat.StringIO(fildat), sep=",")
                else:
                    df = pd.read_csv(pd.compat.StringIO(fildat), sep=" ")
            else:
                df = pd.read_csv(pd.compat.StringIO(fildat), sep="\t")

            self.titleLineEdit.setText(os.path.basename(file))
            self.fileNameLineEdit.setText(os.path.basename(file))
        buttonDict['button'+str(global_plt_index)][3].setStyleSheet('color: black')
        buttonDict['button'+str(plt_index)][3].setStyleSheet('color: green')
        global_plt_index = plt_index
        self.reload(False)
        

        for idx, column in enumerate(df):
            variable1, variable2 = column + str(1), column + str(2)
            boxDict[variable1] = QtWidgets.QCheckBox("",
                                                     self.gridLayoutWidget)
            boxDict[variable2] = QtWidgets.QCheckBox(column,
                                                     self.gridLayoutWidget)
            self.gridLayout.addWidget(boxDict[variable1], idx + 2, 0)
            self.gridLayout.addWidget(boxDict[variable2], idx + 2, 1)
            self.gridLayoutWidget.setGeometry(QtCore.QRect(5, 24, 320,
                                                           18 * (idx + 2)))
            self.gridLayout.setColumnMinimumWidth(10, 0)
            self.gridLayout.setColumnStretch(1, 1)
            self.scrollAreaWidgetContents.setGeometry(
                QtCore.QRect(0, 0, 320, 39 + 18 * (idx + 2)))

        self.plotButton.setEnabled(True)

    def plotcolumns(self):

        mark = [l.strip(" ") for l in self.markersLineEdit.text().split(",")]
        global lenax
        lenax = 0

        for idx, columnx in enumerate(df):
            if boxDict[columnx + str(1)].isChecked():
                pa = df[columnx].tolist()

                if self.xLabelLineEdit.text() == "":
                    xlab = columnx
                else:
                    xlab = self.xLabelLineEdit.text()

                for idy, columny in enumerate(df):
                    variableplt = str(idx) + str(idy) + "plot" + str(
                                                                global_plt_index)
                    if boxDict[columny + str(2)].isChecked():
                        if self.yLabelLineEdit.text() == "":
                            ylab = columny
                        else:
                            ylab = self.yLabelLineEdit.text()

                        if variableplt in plotDict:
                            continue
                        pb = df[columny].tolist()

                        try:
                            if self.linewidthText.text() == '':
                                    linew = 2.0
                            else:
                                try:
                                    linew = float(self.linewidthText.text())
                                except ValueError as e:
                                    linew = 2.0

                            if mark[0] == '':
                                plotDict[variableplt] = plt.plot(pa, pb, ".", linewidth=linew)
                            else:
                                mark.append(".")
                                plotDict[variableplt] = plt.plot(pa, pb, mark[
                                                                   lenax], linewidth=linew)
                                lenax += 1
                        except Exception:
                            return 0

        ax = plt.gca()
        lenax = len(ax.lines)
        title = self.titleLineEdit.text()

        if self.xLabelLineEdit.text() == "":
            pass
        else:
            xlab = self.xLabelLineEdit.text()       

        if self.yLabelLineEdit.text() == "":
            pass
        else:
            ylab = self.yLabelLineEdit.text()       

        plt.grid(True)

        try:
            plt.title("\n".join(wrap(title, 62)))
            plt.ylabel(ylab)
            plt.xlabel(xlab)
        except Exception:
            pass
        ax.relim()
        ax.autoscale()

        self.reloadpictrue()
        self.actionSave_Plot.setEnabled(True)
        self.clearplotButton.setEnabled(True)
        self.clearallplotsButton.setEnabled(True)
        self.fitButton.setEnabled(True)
        self.setLabelsButton.setEnabled(True)
        self.setLimitsButton.setEnabled(True)
        self.errorBarButton.setEnabled(True)

    def fitpoly2(self):
        ax = plt.gca()
        x1, x2 = ax.get_xlim()
        for idx, columnx in enumerate(df):
            if boxDict[columnx + str(1)].isChecked():
                for idy, columny in enumerate(df):
                    variablefit = str(idx) + str(idy) + "poly2_fit" + str(
                                                                global_plt_index)
                    if boxDict[columny + str(2)].isChecked():
                        pa, pb = zip(*[(x,y) for x,y in zip(df[columnx].tolist(), df[columny].tolist()) if x >= x1 and x <= x2])
                        fit = np.polyfit(pa, pb, 2)
                        pb = [(i**2)*fit[0] + i*fit[1] + fit[2] for i in
                              np.linspace(x1, x2, 1000)]
                        fitDict[variablefit] = plt.plot(np.linspace(x1,
                                                        x2, 1000), pb, "-",
                                                        color="red")
                        self.textBrowser.append("Poly2 fit: " + "A = " +
                                                str(fit[0]) + ", B = " +
                                                str(fit[1]) +
                                                ", C = " + str(fit[2]) +
                                                " for " + str(columnx)
                                                + " x " + str(columny))
        ax.set_xlim(x1, x2)
        self.reloadpictrue()

    def fitpoly3(self):
        ax = plt.gca()
        x1, x2 = ax.get_xlim()
        for idx, columnx in enumerate(df):
            if boxDict[columnx + str(1)].isChecked():
                for idy, columny in enumerate(df):
                    variablefit = str(idx) + str(idy) + "poly3_fit" + str(
                                                                global_plt_index)
                    if boxDict[columny + str(2)].isChecked():
                        pa, pb = zip(*[(x,y) for x,y in zip(df[columnx].tolist(), df[columny].tolist()) if x >= x1 and x <= x2])
                        fit = np.polyfit(pa, pb, 3)
                        pb = [(i**3)*fit[0] + (i**2)*fit[1] + i*fit[2]
                              + fit[3] for i in
                              np.linspace(x1, x2, 1000)]
                        fitDict[variablefit] = plt.plot(np.linspace(x1,
                                                        x2, 1000), pb, "-",
                                                        color="red")
                        self.textBrowser.append("Poly3 fit: " + "A = "
                                                + str(fit[0]) + ", B = "
                                                + str(fit[1]) +
                                                ", C = " + str(fit[2])
                                                + ", D = " + str(fit[3])
                                                + " for "
                                                + str(columnx)
                                                + " x " + str(columny))
        ax.set_xlim(x1, x2)
        self.reloadpictrue()

    def fitline(self):
        ax = plt.gca()
        x1, x2 = ax.get_xlim()
        for idx, columnx in enumerate(df):
            if boxDict[columnx + str(1)].isChecked():
                for idy, columny in enumerate(df):
                    variablefit = str(idx) + str(idy) + "line_fit" + str(
                                                                global_plt_index)
                    if boxDict[columny + str(2)].isChecked():
                        pa, pb = zip(*[(x,y) for x,y in zip(df[columnx].tolist(), df[columny].tolist()) if x >= x1 and x <= x2])
                        try:
                            fit = np.polyfit(pa, pb, 1)
                            pb = [i*fit[0] + fit[1] for i in
                                  np.linspace(x1, x2, 1000)]
                            fitDict[variablefit] = plt.plot(np.linspace(x1,
                                                            x2, 1000), pb, 
                                                            "-", color="red")
                            self.textBrowser.append("Line fit: "
                                                    + "A = " + str(fit[0])
                                                    + ", B = " + str(fit[1])
                                                    + " for " + str(columnx)
                                                    + " x " + str(columny))
                        except Exception:
                            pass
        ax.set_xlim(x1, x2)
        self.reloadpictrue()

    def gaussfit(self):
        ax = plt.gca()
        x1, x2 = ax.get_xlim()
        for idx, columnx in enumerate(df):
            if boxDict[columnx + str(1)].isChecked():
                for idy, columny in enumerate(df):
                    variablefit = str(idx) + str(idy) + "gauss_fit" + str(
                                                                global_plt_index)
                    if boxDict[columny + str(2)].isChecked():
                        pa, pb = zip(*[(x,y) for x,y in zip(df[columnx].tolist(), df[columny].tolist()) if x >= x1 and x <= x2])
                        pstart = [1., 0., 1.]
                        try:
                            coeff, var_matrix = curve_fit(functions.gauss, pa, pb,
                                                p0=pstart)
                            fitDict[variablefit] = plt.plot(np.linspace(x1,
                                                                        x2,
                                                                        1000),
                                                            functions.gauss(
                                        np.linspace(x1, x2, 1000),
                                        coeff[0], coeff[1], coeff[2]),
                                    "-", color="red")
                            self.textBrowser.append("Line fit: "
                                                    + "a = " + str(coeff[0])
                                                    + ", mu = " + str(coeff[1])
                                                    + ", sigma = " + str(coeff[2])
                                                    + " for " + str(columnx)
                                                    + " x " + str(columny))
                        except RuntimeError:
                            self.textBrowser.setText("Fit not found")
        ax.set_xlim(x1, x2)
        self.reloadpictrue()

    def fit(self):
        if self.comboBox.currentText() == "Line":
            self.fitline()
        elif self.comboBox.currentText() == "Polynominal (2)":
            self.fitpoly2()
        elif self.comboBox.currentText() == "Polynominal (3)":
            self.fitpoly3()
        elif self.comboBox.currentText() == "Gauss":
            self.gaussfit()
        else:
            self.textBrowser.setText("Output: None!")
        self.clearButton.setEnabled(True)
        self.clearallButton.setEnabled(True)

    def adderrors(self):
        # Ok... This should add an errorbars to plot, but... It have some
        # bugs still so...        
        for idx, columnx in enumerate(df):
            for idy, columny in enumerate(df):
                variableplt = str(idx) + str(idy) + "plot"
                if variableplt in plotDict:
                    if boxDict[columnx + str(1)].isChecked() and boxDict[
                                                        columny + str(2)
                    ].isChecked():
                        xpoint = plotDict[variableplt][0].get_xdata()
                        ypoint = plotDict[variableplt][0].get_ydata()
                        for idxer, columnxer in enumerate(df):
                            if boxDict[columnxer + str(1)].isChecked() and \
                                    boxDict[columnxer + str(1)] != boxDict[
                                                columnx + str(1)]:
                                xerror = df[columnxer].tolist()
                                break
                            else:
                                xerror = 0
                        for idyer, columnyer in enumerate(df):
                            if boxDict[columnyer + str(2)].isChecked() and \
                                    boxDict[columnyer + str(2)] != boxDict[
                                            columny + str(2)]:
                                yerror = df[columnyer].tolist()
                                break
                            else:
                                yerror = 0

                        if str(idx) + str(idy) + "err" not in plotDict:
                            plotDict[str(idx) + str(idy) + "err"] = \
                                plt.errorbar(xpoint, ypoint, xerr=xerror,
                                             yerr=yerror, fmt=".",
                                             ecolor='blue')
                    else:
                        if str(idx) + str(idy) + "err" in plotDict:
                            try:
                                plotDict[str(idx) + str(idy) + "err"].remove()
                                plotDict.pop(str(idx) + str(idy) + "err")
                            except Exception:
                                pass

        self.reloadpictrue()

    def addlabels(self):
        labidx = 0
        global abol
        ax = plt.gca()
        labels = self.labelsLineEdit.text().split(",")
        labels = [l.strip(" ") for l in labels]
        if abol:
            abol = not abol
            for idx, columnx in enumerate(df):
                if boxDict[columnx + str(1)].isChecked():
                    for idy, columny in enumerate(df):
                        if boxDict[columny + str(2)].isChecked():
                            if self.labelsLineEdit.text() != '':
                                if len(labels) == labidx:
                                    labels.append("_nolabel_")
                                try:
                                    if str(idx) + str(idy) + "plot" + str(global_plt_index) in plotDict:
                                        plotDict[str(idx) + str(idy) + "plot" +     str(global_plt_index)][0].\
                                            set_label(labels[labidx])
                                        labidx += 1
                                    else:
                                        return 0
                                    continue
                                except TypeError:
                                    pass

                            else:
                                try:
                                    plotDict[str(idx) + str(idy) + "plot" + str(global_plt_index)][0].\
                                        set_label('_nolabel_')
                                except TypeError:
                                    pass

            try:
                for elem in fitDict.keys():
                    try:
                        fitDict[elem][0].set_label(labels[
                                                       labidx])
                        labidx += 1
                    except Exception:
                        fitDict[elem][0].set_label("_nolabel_")

            except Exception:
                pass

            plt.legend()

        else:
            abol = not abol
            plt.legend()
            try:
                ax.legend_.set_visible(False)
            except Exception as e:
                pass

        self.reloadpictrue()

    def loadmultifiles(self, file):
        try:
            with open(file, 'r') as data:
                lines = data.readlines()
                for idx, line in enumerate(lines):
                    button_var = "button" + str(idx)
                    line = os.path.normpath(line.rstrip())
                    name = QtWidgets.QLabel("\n".join(wrap(os.path.basename(line), 45)))
                    buttonDict[button_var] = (QtWidgets.QPushButton("Load"),
                                                                        line, idx, name)
                    buttonDict[button_var][0].setMaximumWidth(50)
                    self.gridLayout_files.addWidget(buttonDict[button_var][0],
                                                                        idx, 1)
                    self.gridLayout_files.addWidget(buttonDict[button_var][3],                                                     idx, 0)
                    self.gridLayoutWidget_2.setGeometry(QtCore.QRect(10, 15, 340, 20 + 42 * idx))
                    self.gridLayout_files.setColumnMinimumWidth(0, 240)
                    self.gridLayout_files.setColumnMinimumWidth(1, 65)
                    self.gridLayout_files.setColumnStretch(1, 1)
                    self.scrollAreaWidgetContents_2.setGeometry(
                    QtCore.QRect(10, 15, 340, 40 + 42 * idx))
        except Exception:
            return 0

    def connect_load(self, button, path, plt_index):
        button.clicked.connect(lambda: self.createbox(path, plt_index))

    def setlimits(self):
        ax = plt.gca()
        try:
            a = float(self.xminLineEdit.text())
        except Exception:
            a, x2 = ax.get_xlim()
        finally:
            x1, x2 = ax.get_xlim()
            ax.set_xlim(a, x2)
        try:
            b = float(self.xmaxLineEdit.text())
        except Exception:
            x1, b = ax.get_xlim()
        finally:
            x1, x2 = ax.get_xlim()
            ax.set_xlim(x1, b)       
        try:
            c = float(self.yminLineEdit.text())
        except Exception:
            c, y2 = ax.get_ylim()
        finally:
            y1, y2 = ax.get_ylim()
            ax.set_ylim(c, y2)                
        try:
            d = float(self.ymaxLineEdit.text())
        except Exception:
            y1, d = ax.get_ylim()
        finally:
            y1, y2 = ax.get_ylim()
            ax.set_ylim(y1, d)
        self.reloadpictrue()

    def clearplot(self):
        try:
            list(plotDict.values())[-1][0].remove()
            plotDict.popitem(last=True)
            self.reloadpictrue()
        except IndexError as e:
            pass

    def clearallplots(self):         
        for value in plotDict.values():
            value[0].remove()
        for box in boxDict.values():
            if box.isChecked():
                box.setChecked(False)

        plotDict.clear()
        
        self.textBrowser.setText("Cleared")
        self.reloadpictrue()

    def clearfit(self):
        try:
            list(fitDict.values())[-1][0].remove()
            fitDict.popitem(last=True)
            self.textBrowser.setText("Output: Fit removed!")
            self.reloadpictrue()
        except IndexError as e:
            self.textBrowser.setText("Output: No fits to clear!")
            return 0


    def clearallfits(self):         
        for value in fitDict.values():
            value[0].remove()
        
        fitDict.clear()

        self.textBrowser.setText("Cleared")
        self.reloadpictrue()

    def reloadpictrue(self):
        plt.savefig(os.path.dirname(
            os.path.realpath(__file__)) + "\\temp.png", dpi=300)
        pixmap = QtGui.QPixmap(os.path.dirname(
            os.path.realpath(__file__)) + "\\temp.png")
        self.pixlabel.setPixmap(pixmap)
        self.pixlabel.setScaledContents(True)
        self.pixlabel.show()

    def mouseclicked(self, event):
        ax = plt.gca()
        x_0, x_1 = ax.get_xlim()
        y_0, y_1 = ax.get_ylim()
        self.x = int(event.x())
        xoff = int(self.pixlabel.width())
        xgood = functions.map_an(self.x, 0.125*xoff , 0.875*xoff, x_0, x_1)
        self.y = int(event.y())
        yoff = int(self.pixlabel.height())
        ygood = functions.map_an(self.y, 0.125*yoff , 0.875*yoff, y_1, y_0)

        self.textBrowser.setText(str(int(xgood)) + ", " + str(int(ygood)))

    def savefile(self):
        savename = self.fileNameLineEdit.text()
        pixmap = QtGui.QPixmap("temp.png")
        pixmap.save(savename + ".png", "PNG")

    def readme(self):
        try:
            os.startfile("readme.txt")
        except Exception:
            pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    GUI = UiWindow()
    sys.exit(app.exec_())

