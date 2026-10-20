# for getting the local time
# needed for the calendar display
# WARNING: This module considers Monday to be the first day of the week
import time

# Qt holds Qt namespace constants
# constants so far used for color and box layout alignment
# QSize class holds width & height ints
from PyQt5.QtCore import Qt, QSize

# QBrush used to color in selected regions
# QPen used for drawing lines and outlines
# QColor can be used for customizing QGraphics item colors
# QFont used for customizing fonts, including QGraphicsScene text fonts
from PyQt5.QtGui import QBrush, QPen, QColor, QFont

# QApplication is application object, holds event loop
# QWidget is the basic control class
# QDialog is a simple dialog/window class
# QVBoxLayout used for setting window vertical layout
# QHBoxLayout used for setting window horizontal layout
# QGraphicsScene is a region where graphics are rendered
# QGraphicsView is the QGraphicsScene renderer
# QGraphicsRectItem used for drawing rects in a QGraphicsScene
# QPushButton is a simple button class
# QLabel used for displaying static text
from PyQt5.QtWidgets import (
    QApplication, 
    QWidget, QDialog,
    QVBoxLayout, QHBoxLayout,
    QGraphicsScene, QGraphicsView, QGraphicsLineItem, QGraphicsRectItem,
    QPushButton, QLabel
)

# custom main window class used to host a QGraphicsScene, can host other controls
class MainWindow(QWidget):
    def __init__(self):
        # inherit base class members
        super().__init__()

        # set main window caption
        self.setWindowTitle("Key Item Schedule")

        # set window dims and disable resizing
        self.setFixedSize(QSize(851, 679))
        
        # create vertical layout box
        vbox = QVBoxLayout(self)

        CALENDAR_WIDTH = 826
        CALENDAR_HEIGHT = 625

        # create top row control layout box
        topRowBox = QHBoxLayout()

        # create add item/date button and add it to horizontal layout box
        addItemButton = QPushButton("Add Item")
        addItemButton.setFixedSize(QSize(75, 24))
        addItemButton.clicked.connect(self.addItem)
        topRowBox.addWidget(addItemButton, 20)
        topRowBox.addStretch(33)

        # localtime() returns a struct_time object
        # if input is none, returns the exact local time
        # the important struct_time members are tm_year, tm_mon, tm_mday, tm_wday (Monday is 0)
        currentDate = time.localtime()

        self.monthNameMap = ( "January", "February", "March", "April", "May", "June",
                        "July", "August", "September", "October", "November", "December")
        self.monthNumDaysMap = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

        # init label font
        font = QFont()
        font.setBold(True)
        font.setPointSizeF(9)

        #create month label and add it to horizontal layout
        monthLabel = QLabel(self.monthNameMap[currentDate.tm_mon - 1])
        monthLabel.setFont(font)
        topRowBox.addWidget(monthLabel, 47)

        # add horizontal layout box to vertical layout
        vbox.addLayout(topRowBox)

        # configure pen for drawing the day lines
        pen = QPen(Qt.black)
        pen.setWidth(2)

        # create QColor instance
        color = QColor()

        # each day gets a label (ex. Sunday for the first column)
        DAY_LABEL_HEIGHT = 20

        # dims for individual day rectangles in the calendar
        DAY_WIDTH = CALENDAR_WIDTH / 7
        DAY_HEIGHT = (CALENDAR_HEIGHT - DAY_LABEL_HEIGHT) / 5

        # create graphics scene
        self.scene = QGraphicsScene(0, 0, CALENDAR_WIDTH, CALENDAR_HEIGHT)

        # give the day labels a different background color from the rest of the calendar
        dayLabelRect = QGraphicsRectItem(0, 0, CALENDAR_WIDTH, DAY_LABEL_HEIGHT)
        color.setRgb(0xCC, 0xCC, 0xCC)
        dayLabelRect.setBrush(QBrush(color))
        self.scene.addItem(dayLabelRect)

        # add day labels
        textItem = self.scene.addText("Sunday", font)
        textItem.setPos(30, 0)
        textItem = self.scene.addText("Monday", font)
        textItem.setPos(30 + DAY_WIDTH, 0)
        textItem = self.scene.addText("Tuesday", font)
        textItem.setPos(29 + DAY_WIDTH * 2, 0)
        textItem = self.scene.addText("Wednesday", font)
        textItem.setPos(19 + DAY_WIDTH * 3, 0)
        textItem = self.scene.addText("Thursday", font)
        textItem.setPos(24 + DAY_WIDTH * 4, 0)
        textItem = self.scene.addText("Friday", font)
        textItem.setPos(35 + DAY_WIDTH * 5, 0)
        textItem = self.scene.addText("Saturday", font)
        textItem.setPos(28 + DAY_WIDTH * 6, 0)

        # add line that divides the day labels from their respective columns
        dividerLine = QGraphicsLineItem(0, DAY_LABEL_HEIGHT, CALENDAR_WIDTH, DAY_LABEL_HEIGHT)
        dividerLine.setPen(pen)
        self.scene.addItem(dividerLine)

        # add vertical lines
        for i in range(6):
            line = QGraphicsLineItem(DAY_WIDTH + i * DAY_WIDTH, 0, DAY_WIDTH + i * DAY_WIDTH, CALENDAR_HEIGHT)
            line.setPen(pen)
            self.scene.addItem(line)

        # add horizontal lines
        vStart = DAY_LABEL_HEIGHT + DAY_HEIGHT
        for i in range(4):
            line = QGraphicsLineItem(0, vStart + i * DAY_HEIGHT, CALENDAR_WIDTH, vStart + i * DAY_HEIGHT)
            line.setPen(pen)
            self.scene.addItem(line)

        # set weekday to follow anglosphere ordering
        weekday = currentDate.tm_wday
        if (weekday == 6): 
            weekday = 0
        else:
            weekday += 1

        # find weekday of first day of month
        dayColumn = currentDate.tm_mday % 7
        if (dayColumn != 1):
            if (dayColumn == 0):
                dayColumn = 6
            else:
                dayColumn -= 1
            if (weekday - dayColumn < 0):
                weekday += 7 - dayColumn
            else:
                weekday -= dayColumn     

        # add day numbers
        dayNumX = DAY_WIDTH / 100 * 84
        dayNumY = DAY_LABEL_HEIGHT
        numDays = self.monthNumDaysMap[currentDate.tm_mon - 1]
        for day in range(1, numDays):
            textItem = self.scene.addText(str(day))
            textItem.setPos(dayNumX + weekday * DAY_WIDTH, dayNumY)
            if (weekday == 6):
                weekday = 0
                dayNumX = DAY_WIDTH / 100 * 84
                dayNumY += DAY_HEIGHT
            else:
                weekday += 1

        # create view for the scene and add it to horizontal layout
        view = QGraphicsView(self.scene)
        vbox.addWidget(view)

        # initialize window layout
        self.setLayout(vbox)

    def addItem(self):
        dlg = AddItemDlg()
        dlg.exec()

class AddItemDlg(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Item")
        self.setFixedSize(481, 356)

# create application instance
application = QApplication([])

# create main window
mainWindow = MainWindow()

# display main window
mainWindow.show()

# run (start?) event loop
application.exec()