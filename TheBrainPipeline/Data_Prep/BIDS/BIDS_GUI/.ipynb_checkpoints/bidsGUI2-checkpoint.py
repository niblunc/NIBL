from PyQt5.QtWidgets import QWidget, QLabel,  QAction, QMessageBox, QPushButton, QLineEdit, QInputDialog, QApplication, QFileDialog, QComboBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import sys
import BIDSConversion
import os, glob

class App(QWidget):


    def __init__(self):
        super().__init__()
        self.title = 'DICOM TO BIDS CONVERTER'
        self.left = 5
        self.top = 5
        self.width = 550
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.guiTitle = QLabel("DICOM to BIDS Converter", self)
        self.guiTitle.move(20, 50)
        # Here is the button for the Study/Experiment Name

        
        self.inputdir_btn = QPushButton("Input Directory", self)
        self.inputdir_btn.move(15, 100)
        self.inputdir_btn.clicked.connect(self.getInputDir)

        self.outputdir_btn = QPushButton("Output Directory", self)
        self.outputdir_btn.move(175, 100)
        self.outputdir_btn.clicked.connect(self.getOutputDir)

        self.heuristic_btn = QPushButton("Heuristic File", self)
        self.heuristic_btn.move(350, 100)
        self.heuristic_btn.clicked.connect(self.getHeuristicFile)


        self.textA = QLabel("Dicom Extension:", self)
        self.textA.move(20, 150)
        # Menu, or "combo box" for multi-session parameter
        self.dicom = QComboBox(self)
        self.dicom.addItem("")
        self.dicom.addItem("dcm")
        self.dicom.addItem("IMA")
        self.dicom.move(130, 145)
        default = str(self.dicom.currentText())
        self.dicom.activated.connect(self.setDICOM)
        



        self.textA = QLabel("Multiple sessions:", self)
        self.textA.move(210, 150)
        # Menu, or "combo box" for multi-session parameter
        self.multiSess = QComboBox(self)
        self.multiSess.addItem("")
        self.multiSess.addItem("No")
        self.multiSess.addItem("Yes")
        self.multiSess.move(325, 145)
        default = str(self.multiSess.currentText())
        self.multiSess.activated.connect(self.multiSession)

        self.sessID = QLineEdit(self)
        self.sessID.move(330,180)
        self.sessID.resize(50,20)
        self.sess_btn = QPushButton("Session", self)
        self.sess_btn.move(380,175)
        self.sess_btn.clicked.connect(self.getSession)

        self.startProcess_btn = QPushButton("CONVERT", self)
        self.startProcess_btn.move(200, 240)
        self.startProcess_btn.clicked.connect(self.runConversion)

        
        
        self.show()
        
        
##################################################
##################################################
# Below are the methods used to gather information from above

####### Get the heuristic file

    def getHeuristicFile(self):
        HEURISTICTUPLE = QFileDialog.getOpenFileName(self, "Select File")#get existing file
        HEURISTICFILE = HEURISTICTUPLE[0]
        #print(type(HEURISTICFILE[0]))
        BIDSConversion.setHEURISTICFILE(HEURISTICFILE)

####### Get output directory

    def getOutputDir(self):
        OUTPUTDIR = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        BIDSConversion.setOUTPUTDIR(OUTPUTDIR)
        #self.setPixmap(QPixmap(OUTPUTDIR))

####### Get input directory and

    def showSubjects(self,INPUT_DIR):
        msg = QMessageBox()
        
        SUBS = sorted(glob.glob(os.path.join(INPUT_DIR, "sub-*")))
        SUBS = [i.split("/")[-1] for i in SUBS]
        
        if not SUBS:
            msg.setIcon(QMessageBox.Warning)
            msg.setInformativeText("NO SUBJECTS WERE FOUND.")
        else:
            msg.setIcon(QMessageBox.Information)
            msg.setInformativeText("The following subjects were found:")
            string = ' , '.join(SUBS)
            msg.setDetailedText(string)
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        reply = msg.exec_()
        if reply == QMessageBox.Yes:
            BIDSConversion.setSUBJECTS(SUBS)
        else:
            print("value pressed was no")
            ### NEED TO PUT SOMETHING HERE
    def getInputDir(self):
        INPUTDIR = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.showSubjects(INPUTDIR)
        BIDSConversion.setINPUTDIR(INPUTDIR)
    @pyqtSlot()
    
###### Get multisession 

    def multiSession(self):
        MULTISESS = self.multiSess.currentText()
        if MULTISESS == 'Yes':
            BIDSConversion.setMULTISESS(True)
        else:
            BIDSConversion.setMULTISESS(False)
            
            
    def getSession(self):
        SESS_ID = self.sessID.text()
        BIDSConversion.setSESSIONID(SESS_ID)

    def setDICOM(self):
        MULTISESS = self.dicom.currentText()
        if MULTISESS == 'dcm':
            BIDSConversion.setDICOM('dcm')
        else:
            BIDSConversion.setDICOM('IMA')
            
    def runConversion(self):
        BIDSConversion.runConversion()
        

        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()

    sys.exit(app.exec_())
