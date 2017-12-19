from PyQt5 import uic, QtWidgets, QtCore, QtGui
import matplotlib.pyplot as plt
import numpy as np
import sys
import pandas as pd
from scipy.optimize import curve_fit as cf
import functions
import os
import re
from textwrap import wrap
from collections import OrderedDict

file_name = ""
lenax = 0
abol = True
global_idz = 0
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
        self.setWindowTitle('Quick Fit Ver 0.27')

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

        self.actionLoad_File.triggered.connect(self.loadfile)

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
            for button, path, idz in buttonDict.values():
                self.connect_load(button, path, idz)
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

    def createbox(self, file, idz):
        global df
        global global_idz
        with open(file, 'r') as data:
            aa = data.readline()
        data.close()
        with open(file, 'r') as data:
            fildat = data.read()
            if len(aa.split("\t")) == 1:
                if len(aa.split(" ")) == 1:
                    df = pd.read_csv(pd.compat.StringIO(fildat), sep=",")
                else:
                    df = pd.read_csv(pd.compat.StringIO(fildat), sep=" ")
            else:
                df = pd.read_csv(pd.compat.StringIO(fildat), sep="\t")

            self.titleLineEdit.setText(re.split('\\\\', file)[-1])
            self.fileNameLineEdit.setText(re.split('\\\\', file)[-1])
        global_idz = idz
        self.reload(False)

        for idx, column in enumerate(df):
            variable1 = column + str(1)
            variable2 = column + str(2)
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

        mark = self.markersLineEdit.text().split(",")
        mark = [l.strip(" ") for l in mark]
        global lenax
        lenax = 0
        # plt.style.use("ggplot")

        for idx, columnx in enumerate(df):
            if boxDict[columnx + str(1)].isChecked():
                pa = df[columnx].tolist()

                if self.xLabelLineEdit.text() == "":
                    xlab = columnx
                else:
                    xlab = self.xLabelLineEdit.text()

                for idy, columny in enumerate(df):
                    variableplt = str(idx) + str(idy) + "plot" + str(
                                                                global_idz)
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
                    else:
                        if variableplt in plotDict:
                            try:
                                plotDict[variableplt][0].remove()
                                plotDict.pop(variableplt)
                            except Exception:
                                pass

            else:
                for idy, columny in enumerate(df):
                    variableplt = str(idx) + str(idy) + "plot" + str(global_idz)
                    if variableplt in plotDict:
                        try:
                            plotDict[str(idx) + str(idy) + "plot" + str(global_idz)][0].remove()
                            plotDict.pop(variableplt)
                        except Exception:
                            pass
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
        for idx, columnx in enumerate(df):
            if boxDict[columnx + str(1)].isChecked():
                pa = df[columnx].tolist()
                for idy, columny in enumerate(df):
                    variablefit = str(idx) + str(idy) + "poly2_fit" + str(
                                                                global_idz)
                    if boxDict[columny + str(2)].isChecked():
                        try:
                            fitDict[variablefit][0].remove()
                        except Exception:
                            pass
                        pb = df[columny].tolist()
                        fit = np.polyfit(pa, pb, 2)
                        pb = [(i**2)*fit[0] + i*fit[1] + fit[2] for i in
                              np.linspace(pa[0], pa[-1], 1000)]
                        fitDict[variablefit] = plt.plot(np.linspace(pa[0],
                                                        pa[-1], 1000), pb, "-",
                                                        color="red")
                        self.textBrowser.append("Poly2 fit: " + "A = " +
                                                str(fit[0]) + ", B = " +
                                                str(fit[1]) +
                                                ", C = " + str(fit[2]) +
                                                " for " + str(columnx)
                                                + " x " + str(columny))

        self.reloadpictrue()

    def fitpoly3(self):
        for idx, columnx in enumerate(df):
            if boxDict[columnx + str(1)].isChecked():
                pa = df[columnx].tolist()
                for idy, columny in enumerate(df):
                    variablefit = str(idx) + str(idy) + "poly3_fit"
                    if boxDict[columny + str(2)].isChecked():
                        try:
                            fitDict[variablefit][0].remove()
                        except Exception:
                            pass
                        pb = df[columny].tolist()
                        fit = np.polyfit(pa, pb, 3)
                        pb = [(i**3)*fit[0] + (i**2)*fit[1] + i*fit[2]
                              + fit[3] for i in
                              np.linspace(pa[0], pa[-1], 1000)]
                        fitDict[variablefit] = plt.plot(np.linspace(pa[0],
                                                        pa[-1], 1000), pb, "-",
                                                        color="red")
                        self.textBrowser.append("Poly3 fit: " + "A = "
                                                + str(fit[0]) + ", B = "
                                                + str(fit[1]) +
                                                ", C = " + str(fit[2])
                                                + ", D = " + str(fit[3])
                                                + " for "
                                                + str(columnx)
                                                + " x " + str(columny))

        self.reloadpictrue()

    def fitline(self):
        for idx, columnx in enumerate(df):
            if boxDict[columnx + str(1)].isChecked():
                pa = df[columnx].tolist()
                for idy, columny in enumerate(df):
                    variablefit = str(idx) + str(idy) + "line_fit"
                    if boxDict[columny + str(2)].isChecked():
                        try:
                            fitDict[variablefit][0].remove()
                        except Exception:
                            pass
                        pb = df[columny].tolist()
                        try:
                            fit = np.polyfit(pa, pb, 1)
                            pb = [i*fit[0] + fit[1] for i in
                                  np.linspace(pa[0], pa[-1], 1000)]
                            fitDict[variablefit] = plt.plot(np.linspace(pa[0],
                                                            pa[-1], 1000), pb, 
                                                            "-", color="red")
                            self.textBrowser.append("Line fit: "
                                                    + "A = " + str(fit[0])
                                                    + ", B = " + str(fit[1])
                                                    + " for " + str(columnx)
                                                    + " x " + str(columny))
                        except Exception:
                            pass

        self.reloadpictrue()

    def gaussfit(self):
        for idx, columnx in enumerate(df):
            if boxDict[columnx + str(1)].isChecked():
                pa = df[columnx].tolist()
                for idy, columny in enumerate(df):
                    variablefit = str(idx) + str(idy) + "gauss_fit"
                    if boxDict[columny + str(2)].isChecked():
                        try:
                            fitDict[variablefit][0].remove()
                        except:
                            pass
                        pb = df[columny].tolist()
                        pstart = [1., 0., 1.]
                        coeff, var_matrix = cf(functions.gauss, pa, pb,
                                               p0=pstart)
                        fitDict[variablefit] = plt.plot(np.linspace(pa[0],
                                                                    pa[-1],
                                                                    1000),
                                                        functions.gauss(
                                     np.linspace(pa[0], pa[-1], 1000),
                                     coeff[0], coeff[1], coeff[2]),
                                 "-", color="red")
                        self.textBrowser.append("Line fit: "
                                                + "a = " + str(coeff[0])
                                                + ", mu = " + str(coeff[1])
                                                + ", sigma = " + str(coeff[2])
                                                + " for " + str(columnx)
                                                + " x " + str(columny))

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
        # if self.labelsBox.isChecked():
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
                                    if str(idx) + str(idy) + "plot" + str(global_idz) in plotDict:
                                        plotDict[str(idx) + str(idy) + "plot" +     str(global_idz)][0].\
                                            set_label(labels[labidx])
                                        labidx += 1
                                    else:
                                        return 0
                                    continue
                                except TypeError:
                                    pass

                            else:
                                try:
                                    plotDict[str(idx) + str(idy) + "plot" + str(global_idz)][0].\
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

            try:
                plt.legend()
            except UserWarning:
                plt.legend("")
        else:
            abol = not abol
            try:
                plt.legend()
                ax.legend_.set_visible(False)
            except UserWarning:
                plt.legend("")

        self.reloadpictrue()

    def loadmultifiles(self, file):
        with open(file, 'r') as data:
            lines = data.readlines()
            for idx, line in enumerate(lines):
                button_var = "button" + str(idx)
                line = os.path.normpath(line.rstrip())
                buttonDict[button_var] = (QtWidgets.QPushButton("Load"),
                                                                    line, idx)
                buttonDict[button_var][0].setMaximumWidth(50)
                self.gridLayout_files.addWidget(QtWidgets.QLabel("\n".join(wrap(
                                        re.split('\\\\', line)[-1], 45))), idx, 0)
                self.gridLayout_files.addWidget(buttonDict[button_var][0],
                                                                    idx, 1)
                self.gridLayoutWidget_2.setGeometry(QtCore.QRect(10, 15, 350,
                                                                20 + 42 * idx))
                self.gridLayout_files.setColumnMinimumWidth(0, 250)
                self.gridLayout_files.setColumnMinimumWidth(1, 65)
                self.gridLayout_files.setColumnStretch(1, 1)
                self.scrollAreaWidgetContents_2.setGeometry(
                QtCore.QRect(10, 15, 350, 40 + 42 * idx))

    def connect_load(self, button, path, idz):
        button.clicked.connect(lambda: self.createbox(path, idz))

    def setlimits(self):
        try:
            try:
                astr = self.xminLineEdit.text().replace(",", ".")
                a = float(astr)
            except Exception:
                a = float(self.xminLineEdit.text())
            try:
                bstr = self.xmaxLineEdit.text().replace(",", ".")
                b = float(bstr)
            except Exception:
                b = float(self.xmaxLineEdit.text())
            try:
                cstr = self.yminLineEdit.text().replace(",", ".")
                c = float(cstr)
            except Exception:
                c = float(self.yminLineEdit.text())
            try:
                dstr = self.ymaxLineEdit.text().replace(",", ".")
                d = float(dstr)
            except Exception:
                d = float(self.ymaxLineEdit.text())
            plt.axis([a, b, c, d])
        except Exception:
            pass
        self.reloadpictrue()

    def clearplot(self):
        try:
            list(plotDict.values())[-1][0].remove()
            plotDict.popitem(last=True)
            self.reloadpictrue()
        except IndexError as e:
            pass        

    def clearallplots(self):         
        for idx, columnx in enumerate(df):
                for idy, columny in enumerate(df):
                    for key, value in enumerate(buttonDict):
                        variablefit = str(idx) + str(idy) + "plot" + str(key)
                        try:
                            plotDict[variablefit][0].remove()
                            plotDict.pop(variablefit)
                        except Exception:
                            pass

        self.textBrowser.setText("Cleared")
        self.reloadpictrue()

    def clearfit(self):
        try:
            list(fitDict.values())[-1][0].remove()
            plotDict.popitem(last=True)
            self.reloadpictrue()
        except IndexError as e:
            pass          

        self.textBrowser.setText("Output: Fit removed!")
        self.textBrowser.setText("Output: No fits to clear!")
        self.reloadpictrue()

    def clearallfits(self):         
        for idx, columnx in enumerate(df):
                for idy, columny in enumerate(df):
                        for s in ("poly2", "poly3", "line", "gauss"):
                            variablefit = str(idx) + str(idy) + "%s_fit" % s
                            try:
                                fitDict[variablefit][0].remove()
                                fitDict.pop(variablefit)
                            except Exception:
                                pass

        self.textBrowser.setText("Cleared")
        self.reloadpictrue()

    def reloadpictrue(self):
        plt.savefig(os.path.dirname(
            os.path.realpath(__file__)) + "\\temp.jpg", dpi=300)
        pixmap = QtGui.QPixmap(os.path.dirname(
            os.path.realpath(__file__)) + "\\temp.jpg")
        self.pixlabel.setPixmap(pixmap)
        self.pixlabel.setScaledContents(True)
        self.pixlabel.show()

    def savefile(self):
        savename = self.fileNameLineEdit.text()
        pixmap = QtGui.QPixmap("temp.jpg")
        pixmap.save(savename + ".png", "PNG")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    GUI = UiWindow()
    sys.exit(app.exec_())
