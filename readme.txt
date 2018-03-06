Quick Fitter Ver. 0.33


1. Introduction

	Quick Fitter is used to load files with data and plot simple curves from given columns in file. Program is written in python 3.x.x using GUI from PyQt5. 

2. Running program
	
	To run program execute run.bat file. In order to run program properly you need to have Python 3.x.x installed in your machine and had python interpreter 
	added in your PATH variable.

3. Using Quick Fitter

	3.1 Loading Files

		Before loading files to program prepare a *.txt file with absolute paths to files you want to load. Every path must be in new line. 
		In order to load a file open File tab in context menu and select "Load File". Find your *.txt file and click "Open". 
		Next select your file from bottom of menu and click "Load" button. This will read file and create check boxes of columns in file. 
		This action will also set default Title and File name of plot the same as loaded file.

	3.2 Plotting basic data

		To plot some data check X and Y checkboxes (You can check multiple X and Y checkboxes) to determine what will be on OX and OY. Then click "Plot" button. 
		Axis names are taken from last checked boxes.

	3.3 Changing plot properties
		
		Properties that you can change are: Title, X Axis name, Y Axis name, File name, Legend, Markers, Line width, plot limits.
 
		Title: To change title, write your title in title text field and click "Plot" button.
		X Axis and Y Axis: Inherit from Title.
		File name: Inherit from Title
		Legend: To set Legend to plots write legend in Legend text field (each legend separated by coma for every plot). 
		You can also set legend 1 by 1 by plotting plots one by one and adding legend to them. To reload Legend click two times on "Legend" button. 
		To turn of click only once.
		Markers: Symbol or line you want to use in plot. Also determine color for plot. Available  markers:
					"."	point
					","	pixel
					"o"	circle
					"v"	triangle_down
					"^"	triangle_up
					"<"	triangle_left
					">"	triangle_right
					"1"	tri_down
					"2"	tri_up
					"3"	tri_left
					"4"	tri_right
					"8"	octagon
					"s"	square
					"p"	pentagon
					"P"	plus (filled)
					"*"	star
					"h"	hexagon1
					"H"	hexagon2
					"+"	plus
					"x"	x
					"X"	x (filled)
					"D"	diamond
					"d"	thin_diamond
					"|"	vline
					"_"	hline 
		Avilable colors:	
					'b' blue
					'g' green
					'r' read
					'c' cyan
					'm' magneta 
					'y' yellow
					'k' black
					'w' white
		To change marker and corol write colorsymbol markersymbol without any spaces between them. For every plot markers must be separated by coma. 
		To change marker of plot you need to clear plot and plot it again.
		Line width: In pixels. Works only when marker is "-".
		Set limits: As name. To reset to base click "Plot".

		3.4 Clearing plots
				
			Clear plot clears last plottet plot. Clear All plears all plots.

		3.5 Fitting functions

			To fit function chose function from function menu and click fit. Function is fitted to checked boxes.
			
			Clear Fit/Clear All fits. Same as clear plot and all plots but applies fits. 

			If you want to fit only to partial data without stretching to whole plot just zoom to area and fit. If you want to stretch
			write values in Set Limits but don't click button. Just click Fit. It will work.

		3.6 Error bars

			Does not work properly yet.

		3.7 Saving plot

			To save plot open "File" menu from context menu and select "Save File". File is saved in program folder.

4. Help

	For help contact Arkadiusz Popczak (arepop@arepop.com) on mail. 