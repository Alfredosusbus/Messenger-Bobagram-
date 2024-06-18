import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import emoji


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(570, 702)
        font = QtGui.QFont()
        font.setPointSize(8)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet("background-color: #2F4F4F;")
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(10, 640, 371, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.textEdit.setFont(font)
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setStyleSheet("background-color: #5F9EA0;")
        
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(10, 61, 551, 561))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.listWidget.setFont(font)
        self.listWidget.setObjectName("listWidget")
        self.listWidget.setStyleSheet("background-color: #708090;")
        
        self.emojiButton = QtWidgets.QPushButton(self.centralwidget)
        self.emojiButton.setGeometry(QtCore.QRect(390, 640, 41, 41))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.emojiButton.setFont(font)
        self.emojiButton.setObjectName("emojiButton")
        self.emojiButton.setStyleSheet("background-color: #696969;")
        self.emojiButton.setText("😊")
        self.emojiButton.clicked.connect(self.showEmojiMenu)
        
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(440, 640, 81, 41))
        font = QtGui.QFont()
        font.setPointSize(31)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setStyleSheet("background-color: #696969;")
        
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 291, 51))
        font = QtGui.QFont()
        font.setPointSize(31)
        self.label.setFont(font)
        self.label.setObjectName("label")
        
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(430, 10, 131, 51))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setStyleSheet("background-color: #800000;")
        
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Messenger"))
        self.textEdit.setPlaceholderText(_translate("MainWindow", "Enter message"))
        self.pushButton.setText(_translate("MainWindow", ">"))
        self.label.setText(_translate("MainWindow", "Bobagram"))
        self.pushButton_2.setText(_translate("MainWindow", "Exit"))

    def showEmojiMenu(self):
        menu = QtWidgets.QMenu()
        emojis = ["😀", "😂", "😊", "😍", "😒", "😭", "😡", "👍", "👎", "🙏", "👏", "👌", "🙌", "🤔", "❤️"]
        
        for em in emojis:
            action = menu.addAction(em)
            action.triggered.connect(lambda checked, em=em: self.insertEmoji(em))
        
        menu.exec_(QtGui.QCursor.pos())

    def insertEmoji(self, emoji_char):
        cursor = self.textEdit.textCursor()
        cursor.insertText(emoji_char)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
