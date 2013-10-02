import sys
from PyQt4.QtGui import *

class MainWindow(QMainWindow):

    def __init__(self, *args):
        apply(QMainWindow.__init__, (self, ) + args)
        self.setCaption("Network Client")

        self.actionInformation=QAction(self, "Information")
        self.actionInformation.setText("Informational Message")
        self.actionInformation.setMenuText("&Information")
        self.actionInformation.setStatusTip("Show an informational mesagebox.")

        self.connect(self.actionInformation,
                     SIGNAL("activated()"),
                     self.slotInformation)


        self.actionWarning=QAction(self, "Warning")
        self.actionWarning.setText("Warning Message")
        self.actionWarning.setMenuText("&Warning")
        self.actionWarning.setStatusTip("Show a warning mesagebox.")

        self.connect(self.actionWarning,
                     SIGNAL("activated()"),
                     self.slotWarning)

        self.actionCritical=QAction(self, "Critical")
        self.actionCritical.setText("Critical Message")
        self.actionCritical.setMenuText("&Critical")
        self.actionCritical.setStatusTip("Show an informational mesagebox.")


        self.connect(self.actionCritical,
                     SIGNAL("activated()"),
                     self.slotCritical)

        self.actionAbout=QAction(self, "About")
        self.actionAbout.setText("About")
        self.actionAbout.setMenuText("&About")
        self.actionAbout.setStatusTip("Show an about box.")

        self.connect(self.actionAbout,
                     SIGNAL("activated()"),
                     self.slotAbout)


        self.actionAboutQt=QAction(self, "AboutQt")
        self.actionAboutQt.setText("About Qt Message")
        self.actionAboutQt.setMenuText("About &Qt")
        self.actionAboutQt.setStatusTip("Show an about box for Qt.")

        self.connect(self.actionAboutQt,
                     SIGNAL("activated()"),
                     self.slotAboutQt)



        self.actionFile=QAction(self, "OpenFile")
        self.actionFile.setText("Open File")
        self.actionFile.setMenuText("&Open")
        self.actionFile.setStatusTip("Open a file.")

        self.connect(self.actionFile,
                     SIGNAL("activated()"),
                     self.slotFile)



        self.actionFont=QAction(self, "Font")
        self.actionFont.setText("Select a font")
        self.actionFont.setMenuText("&Font")
        self.actionFont.setStatusTip("Select a font")

        self.connect(self.actionFont,
                     SIGNAL("activated()"),
                     self.slotFont)



        self.actionColor=QAction(self, "Color")
        self.actionColor.setText("Select a color")
        self.actionColor.setMenuText("&Color")
        self.actionColor.setStatusTip("Select a color")

        self.connect(self.actionColor,
                     SIGNAL("activated()"),
                     self.slotColor)


        # Statusbar
        self.statusBar=QStatusBar(self)

        # Define menu

        self.messageMenu=QPopupMenu()

        self.actionInformation.addTo(self.messageMenu)
        self.actionWarning.addTo(self.messageMenu)
        self.actionCritical.addTo(self.messageMenu)

        self.dialogMenu=QPopupMenu()
        self.actionFile.addTo(self.dialogMenu)
        self.actionFont.addTo(self.dialogMenu)
        self.actionColor.addTo(self.dialogMenu)

        self.helpMenu=QPopupMenu()
        self.actionAbout.addTo(self.helpMenu)
        self.actionAboutQt.addTo(self.helpMenu)

        self.menuBar().insertItem("&Messages", self.messageMenu)
        self.menuBar().insertItem("&Standard dialogs", self.dialogMenu)
        self.menuBar().insertItem("&Help", self.helpMenu)

    def slotInformation(self):
        QMessageBox.information(self,
                                "Information",
                                "A plain, informational message")

    def slotWarning(self):
        QMessageBox.warning(self,
                            "Warning",
                            "What you are about to do will do some serious harm .")


    def slotCritical(self):
        QMessageBox.critical(self,
                                "Critical",
                                "A critical error has occurred.\nProcessing will be stopped!")

    def slotAbout(self):
        QMessageBox.about(self,
                          "About me",
                          "A demo of message boxes and standard dialogs.")

    def slotAboutQt(self):
        QMessageBox.aboutQt(self)


    def slotFile(self):
        filename=QFileDialog.getOpenFileName("", "*.py", self, "FileDialog")

    def slotFont(self):
        (font, ok) = QFontDialog.getFont(self, "FontDialog")

    def slotColor(self):
        color=QColorDialog.getColor(QColor("linen"), self, "ColorDialog")


def main(args):
    app=QApplication(args)
    win=MainWindow()
    win.show()
    app.connect(app, SIGNAL("lastWindowClosed()")\
                , app\
                , SLOT("quit()")\
                )
    app.exec_loop()

if __name__=="__main__":
        main(sys.argv)