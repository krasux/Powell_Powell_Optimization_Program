import sys
from powell import *
from numpy import array

from PyQt5.QtWidgets import (QMainWindow, QWidget, QToolTip, QPushButton, QApplication)
from PyQt5.QtGui import QFont
from program_ui import Ui_MainWindow
from funStrUtils import str2fun

class MainWindow(QMainWindow, Ui_MainWindow):
    numberOfConstraints = 0
    numberOfVariables = 2
    meritum = 0
    constraints = []
    xStart = 0
    maxIterations = 0
    epsilonPowell = 10e-6
    def __init__(self):
        super(MainWindow, self).__init__()
        QToolTip.setFont(QFont('SansSerif', 10))
        # Set up the user interface from Designer.
        self.setupUi(self)

        # Make some local modifications.
        self.btnSearch.setToolTip("Click to start the program")
        self.cmbVariables.setCurrentIndex(1)
        self.cmbPowellEpsilon.setCurrentIndex(4)


        # Connect up the buttons and combo boxes.
        self.cmbConstraints.activated.connect(self.nbConstrChanged)
        self.cmbVariables.activated.connect(self.nbVarChanged)
        self.cmbObjFun.activated.connect(self.setMeritum)
        self.cmbMaxIterations.activated.connect(self.maxIterationsChanged)
        self.cmbPowellEpsilon.activated.connect(self.powellEpsilonChanged)
        self.btnSearch.clicked.connect(self.startSearch)
        self.btnSearch2.clicked.connect(self.startSearch)
        self.btnClearLog.clicked.connect(self.logResults.clear)


        # Connect x0 inputs:
        self.inputX0_1.editingFinished.connect(self.x0Changed)
        self.inputX0_2.editingFinished.connect(self.x0Changed)
        self.inputX0_3.editingFinished.connect(self.x0Changed)
        self.inputX0_4.editingFinished.connect(self.x0Changed)
        self.inputX0_5.editingFinished.connect(self.x0Changed)

        # Connect constraints inputs:
        self.inputConstraint1.editingFinished.connect(self.constraintsChanged)
        self.inputConstraint2.editingFinished.connect(self.constraintsChanged)
        self.inputConstraint3.editingFinished.connect(self.constraintsChanged)
        self.inputConstraint4.editingFinished.connect(self.constraintsChanged)
        self.inputConstraint5.editingFinished.connect(self.constraintsChanged)


        # Set up variables and constrains inputs:
        self.setActiveConstrainInputs(self.numberOfConstraints)
        self.setActiveVariableInputs(int(self.cmbVariables.currentText()))
        self.meritum = str2fun(self.cmbObjFun.currentText())
        self.setXStart(self.numberOfVariables)
        self.setMaxInterations(int(self.cmbMaxIterations.currentText()))
        self.setPowellEpsilon(float(self.cmbPowellEpsilon.currentText()))
        # Show the window at the end
        self.show()

    def nbConstrChanged(self):
        self.numberOfConstraints = int((self.cmbConstraints.currentText()))
        self.setActiveConstrainInputs(self.numberOfConstraints)
        self.setConstraints(self.numberOfConstraints)

    def setActiveConstrainInputs(self, nbrOfConstr):
        self.inputConstraint1.setDisabled(True)
        self.inputConstraint2.setDisabled(True)
        self.inputConstraint3.setDisabled(True)
        self.inputConstraint4.setDisabled(True)
        self.inputConstraint5.setDisabled(True)
        self.lblConstraint1.setDisabled(True)
        self.lblConstraint2.setDisabled(True)
        self.lblConstraint3.setDisabled(True)
        self.lblConstraint4.setDisabled(True)
        self.lblConstraint5.setDisabled(True)

        if nbrOfConstr >= 1:
            self.inputConstraint1.setDisabled(False)
            self.lblConstraint1.setDisabled(False)
        if nbrOfConstr >= 2:
            self.inputConstraint2.setDisabled(False)
            self.lblConstraint2.setDisabled(False)
        if nbrOfConstr >= 3:
            self.inputConstraint3.setDisabled(False)
            self.lblConstraint3.setDisabled(False)
        if nbrOfConstr >= 4:
            self.inputConstraint4.setDisabled(False)
            self.lblConstraint4.setDisabled(False)
        if nbrOfConstr >= 5:
            self.inputConstraint5.setDisabled(False)
            self.lblConstraint5.setDisabled(False)


    def nbVarChanged(self):
        self.numberOfVariables = int((self.cmbVariables.currentText()))
        self.setActiveVariableInputs(self.numberOfVariables)
        self.setXStart(self.numberOfVariables)


    def setActiveVariableInputs(self, nbrOfVar):
        self.inputX0_2.setDisabled(True)
        self.inputX0_3.setDisabled(True)
        self.inputX0_4.setDisabled(True)
        self.inputX0_5.setDisabled(True)
        self.lbX0_2.setDisabled(True)
        self.lbX0_3.setDisabled(True)
        self.lbX0_4.setDisabled(True)
        self.lbX0_5.setDisabled(True)

        if nbrOfVar >= 2:
            self.inputX0_2.setDisabled(False)
            self.lbX0_2.setDisabled(False)
        if nbrOfVar >= 3:
            self.inputX0_3.setDisabled(False)
            self.lbX0_3.setDisabled(False)
        if nbrOfVar >= 4:
            self.inputX0_4.setDisabled(False)
            self.lbX0_4.setDisabled(False)
        if nbrOfVar >= 5:
            self.inputX0_5.setDisabled(False)
            self.lbX0_5.setDisabled(False)



    def setMeritum(self):
        self.meritum = str2fun(self.cmbObjFun.currentText())

    def x0Changed(self):
        self.setXStart(self.numberOfVariables)

    def setXStart(self, nbrOfVar):
        if nbrOfVar == 1:
            self.xStart = float(self.inputX0_1.text())
        if nbrOfVar == 2:
            self.xStart = [self.inputX0_1.text(), self.inputX0_2.text()]
        if nbrOfVar == 3:
            self.xStart = [self.inputX0_1.text(), self.inputX0_2.text(), self.inputX0_3.text()]
        if nbrOfVar == 4:
            self.xStart = [self.inputX0_1.text(), self.inputX0_2.text(),
                           self.inputX0_3.text(), self.inputX0_4.text()]
        if nbrOfVar == 5:
            self.xStart = [self.inputX0_1.text(), self.inputX0_2.text(), self.inputX0_3.text(),
                           self.inputX0_4.text(), self.inputX0_5.text()]
        if nbrOfVar > 1:
            self.xStart = [float(i) for i in self.xStart]


    def maxIterationsChanged(self):
        self.setMaxInterations(int(self.cmbMaxIterations.currentText()))

    def setMaxInterations(self, nbrOfIter):
        self.maxIterations = nbrOfIter

    def powellEpsilonChanged(self):
        self.setPowellEpsilon(float(self.cmbPowellEpsilon.currentText()))

    def setPowellEpsilon(self, newEpsilon):
        self.epsilonPowell = newEpsilon

    def constraintsChanged(self):
        self.setConstraints(self.numberOfConstraints)

    def setConstraints(self, nbrOfConstr):
        self.constraints = []
        if nbrOfConstr >= 1:
            self.constraints.append(str2fun(self.inputConstraint1.text()))
        if nbrOfConstr >= 2:
            self.constraints.append(str2fun(self.inputConstraint2.text()))
        if nbrOfConstr >= 3:
            self.constraints.append(str2fun(self.inputConstraint3.text()))
        if nbrOfConstr >= 4:
            self.constraints.append(str2fun(self.inputConstraint4.text()))
        if nbrOfConstr >= 5:
            self.constraints.append(str2fun(self.inputConstraint5.text()))

    def startSearch(self):
        self.statusBar().showMessage("Searching for minimum of: " + str(self.cmbObjFun.currentText())
                                     + " With xStart: " + str(self.xStart))

        self.logResults.insertPlainText('_'*80 + '\n')
        self.logResults.insertPlainText("Searching for minimum of: " + str(self.cmbObjFun.currentText()) +'\n')
        self.logResults.insertPlainText("Starting x: " + str(self.xStart) + '\n')

        xMin, nIter, success = powell(self.meritum, self.xStart, epsilon=self.epsilonPowell,
                                      iterations=self.maxIterations, searchRanges=self.xSearchRanges)
        if success:
            self.logResults.insertPlainText('Minimum found at x: ' + str(xMin) + '\n')
        else:
            self.logResults.insertPlainText('Minimum not found \n Max number of iterations exceeded\n')
        self.logResults.insertPlainText("F(x) = " + str(self.meritum(xMin)) + '\n')
        self.logResults.insertPlainText("Number of cycles = " + str(nIter) + '\n')

        sb = self.logResults.verticalScrollBar()
        sb.setValue(sb.maximum())










if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    sys.exit(app.exec_())