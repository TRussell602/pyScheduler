# for getting the local time
# needed for the calendar display
# WARNING: This module considers Monday to be the first day of the week
import time

# Qt holds Qt namespace constants
# constants so far used for color and box layout alignment
# QSize class holds width & height ints
# QDate holds a date, so far used to initialize a QDateTimeEdit
# QStringListModel contains a list of strings formatted so that a QListView can display them
# pyqtSignal is used for creating custom messages (event-responses)
from PyQt5.QtCore import Qt, QSize, QDate, QStringListModel#, pyqtSignal

# QBrush used to color in selected regions
# QPen used for drawing lines and outlines
# QColor can be used for customizing QGraphics item colors
# QFont used for customizing fonts, including QGraphicsScene text fonts
from PyQt5.QtGui import QBrush, QPen, QColor, QFont

# QApplication is application object, holds event loop
# QWidget is the basic control class
# QVBoxLayout used for setting window vertical layout
# QHBoxLayout used for setting window horizontal layout
# QGraphicsScene is a region where graphics are rendered
# QGraphicsView is the QGraphicsScene renderer
# QGraphicsRectItem used for drawing rects in a QGraphicsScene
# QPushButton is a simple button class
# QLabel used for displaying static text
# QLineEdit is a text field
# QDateTimeEdit is a LineEdit specifically for getting date and time
# QListView is a control that displays a list of items organised in a column
from PyQt5.QtWidgets import (
    QApplication, 
    QWidget,
    QVBoxLayout, QHBoxLayout,
    QGraphicsScene, QGraphicsView, QGraphicsLineItem, QGraphicsRectItem,
    QPushButton, QLabel, QLineEdit, QDateTimeEdit, QListView
)

# custom main window class used to host a QGraphicsScene, can host other controls
class MainWindow(QWidget):

    # localtime() returns a struct_time object
    # if input is none, returns the exact local time
    # the important struct_time members are tm_year, tm_mon, tm_mday, tm_wday (Monday is 0)
    currentDate = time.localtime()

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
        itemListButton = QPushButton("Item List")
        itemListButton.setFixedSize(QSize(75, 24))
        itemListButton.clicked.connect(self.itemList)
        topRowBox.addWidget(itemListButton, 20)
        topRowBox.addStretch(33)

        self.monthNameMap = ( "January", "February", "March", "April", "May", "June",
                        "July", "August", "September", "October", "November", "December")
        self.monthNumDaysMap = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

        # init label font
        font = QFont()
        font.setBold(True)
        font.setPointSizeF(9)

        #create month label and add it to horizontal layout
        monthLabel = QLabel(self.monthNameMap[self.currentDate.tm_mon - 1])
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
        for i in range(8):
            if (i != 7):
                line = QGraphicsLineItem(i * DAY_WIDTH, 0, i * DAY_WIDTH, CALENDAR_HEIGHT)
            else: # needs a correction of 1 here due to floating point math issue
                line = QGraphicsLineItem(i * DAY_WIDTH + 1, 0, i * DAY_WIDTH + 1, CALENDAR_HEIGHT)
            line.setPen(pen)
            self.scene.addItem(line)

        # add horizontal lines
        vStart = DAY_LABEL_HEIGHT + DAY_HEIGHT
        for i in range(5):
            line = QGraphicsLineItem(0, vStart + i * DAY_HEIGHT, CALENDAR_WIDTH, vStart + i * DAY_HEIGHT)
            line.setPen(pen)
            self.scene.addItem(line)

        # set weekday to follow anglosphere ordering
        weekday = self.currentDate.tm_wday
        if (weekday == 6): 
            weekday = 0
        else:
            weekday += 1

        # find weekday of first day of month
        dayColumn = self.currentDate.tm_mday % 7
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
        dayNumX = DAY_WIDTH / 100 * 88
        dayNumY = DAY_LABEL_HEIGHT
        numDays = self.monthNumDaysMap[self.currentDate.tm_mon - 1]
        for day in range(1, numDays + 1):
            if (day == 10):
                dayNumX = DAY_WIDTH / 100 * 80
            
            textItem = self.scene.addText(str(day), font)
            textItem.setPos(dayNumX + weekday * DAY_WIDTH, dayNumY)
            
            if (weekday == 6):
                weekday = 0
                dayNumY += DAY_HEIGHT
            else:
                weekday += 1

        # create view for the scene and add it to horizontal layout
        view = QGraphicsView(self.scene)
        vbox.addWidget(view)

        # initialize window layout
        self.setLayout(vbox)

    # opens item list dialog
    def itemList(self):
        self.dlg = itemListDlg()
        self.dlg.setWindowModality(Qt.ApplicationModal)
        #self.dlg.closeMsg.connect(self.onItemListClosed) # used for receiving msg from child
        self.dlg.show()

    #def onItemListClosed(self):
        #self.drawCalendar()
    
    # event handler for the main window
    # since it is called so frequently, it is used to track the current date
    def event(self, e):
        
        # update current date if necessary
        if (self.currentDate.tm_mday != time.localtime().tm_mday): 
            self.currentDate.tm_mday = time.localtime()

        # handle events
        return super().event(e)

class itemListDlg(QWidget):
#    currently unused
#    closeMsg = pyqtSignal()

    def __init__(self):
        super().__init__() # import base class members

        # set dialog caption and dims
        self.setWindowTitle("Item List")
        self.setFixedSize(481, 356)

        # create local vertical layout
        itemListVBox = QVBoxLayout(self)

        # create horizontal layout for the two buttons
        buttonHBox = QHBoxLayout()

        # create add items button
        addItemButton = QPushButton("Add Items")
        addItemButton.setFixedSize(QSize(80, 24))
        addItemButton.clicked.connect(self.addItems)
        buttonHBox.addWidget(addItemButton)

        # create button for manually saving class/dates
        saveButton = QPushButton("Save Changes")
        saveButton.setFixedSize(QSize(80, 24))
        saveButton.clicked.connect(self.saveChanges)
        buttonHBox.addWidget(saveButton)

        # preset string list model for demonstrating the QListView
        strings = ("Junk Class Name : 2026/10/26 12:00AM : This is one possible format", 
                   "Class : Date/Time : Comment",
                   "We could always use a different delimeter (; , - |)")
        listModel = QStringListModel(strings)

        # init item listview
        itemList = QListView()
        itemList.setModel(listModel)

        # init dialog display
        itemListVBox.addLayout(buttonHBox)
        itemListVBox.addWidget(itemList)
        self.setLayout(itemListVBox)

    # opens add items dialog
    def addItems(self):
        self.addItems = AddItemsDlg()
        self.addItems.setWindowModality(Qt.ApplicationModal)
        self.addItems.show()

    # saves additions, edits and deletions of dates/classes
    # note: currently does nothing as of yet
    def saveChanges(self):
        print("Nothing to save yet")

# proof of concept for propagating messages between dialogs
#    def closeEvent(self, QCloseEvent):
#        self.closeMsg.emit()
#        super().closeEvent(QCloseEvent)

class AddItemsDlg(QWidget):
    def __init__(self):
        super().__init__() # inherit base class members

        # init dialog caption and dims
        self.setWindowTitle("Add Item")
        self.setFixedSize(QSize(300, 250))

        # create main dialog layout box
        mainLayout = QHBoxLayout(self)

        # create column layout boxes
        leftCol = QVBoxLayout()
        rightCol = QVBoxLayout()

        # first row
        labelClass = QLabel("Class:")
        labelClass.setFixedSize(QSize(130, 20))
        leftCol.addWidget(labelClass)
        nameField = QLineEdit()
        nameField.setFixedSize(QSize(130, 20))
        rightCol.addWidget(nameField)

        # second row
        labelDate = QLabel("Date:")
        labelDate.setFixedSize(QSize(130, 20))
        leftCol.addWidget(labelDate)
        presentDate = time.localtime() # default to current date
        datePicker = QDateTimeEdit(QDate(presentDate.tm_year, presentDate.tm_mon, presentDate.tm_mday))
        datePicker.setFixedSize(QSize(130, 20))
        rightCol.addWidget(datePicker)

        # third row
        labelDesc = QLabel("Item Description:")
        labelDesc.setFixedSize(QSize(130, 20))
        leftCol.addWidget(labelDesc)
        commentField = QLineEdit()
        commentField.setFixedSize(QSize(130, 20))
        rightCol.addWidget(commentField)

        # fourth row
        addItemButton = QPushButton("Add To List")
        addItemButton.setFixedSize(QSize(130, 20))
        leftCol.addWidget(addItemButton)
        exitAddItem = QPushButton("Exit")
        exitAddItem.setFixedSize(QSize(130, 20))
        rightCol.addWidget(exitAddItem)

        # init dialog layout
        mainLayout.addLayout(leftCol)
        mainLayout.addLayout(rightCol)
        self.setLayout(mainLayout)

# create application instance
application = QApplication([])

# create main window
mainWindow = MainWindow()

# display main window
mainWindow.show()

# run (start?) event loop
application.exec()