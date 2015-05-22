import sys
from powell import *
from powellConstraints import *
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
    deltas = []
    thetas = []
    xStart = 0
    maxIterations = 0
    epsilonPowell = 1e-6
    # Parameters for powell with constraints
    m1 = 0.250
    m2 = 10
    cMin = 0.1
    # Parameters and options for searching in direction
    bracketStep = 0.0001
    goldenSearchWindow = 0.0001
    bracketing = True
    epsilonGoldenSearch = 1e-9

    def __init__(self):
        super(MainWindow, self).__init__()
        QToolTip.setFont(QFont('SansSerif', 10))
        # Set up the user interface from Designer.
        self.setupUi(self)

        # Make some local modifications.
        self.btnSearch.setToolTip("Click to start the program \u03B4 \u03B8")
        self.cmbVariables.setCurrentIndex(1)
        self.cmbPowellEpsilon.setCurrentIndex(3)
        self.cmbGoldenSearchEpsilon.setCurrentIndex(6)

        # Set lbl for sigma (\u03B4) and theta (\u03B8)
        self.lblConstrDelta1.setText("\u03B41")
        self.lblConstrDelta2.setText("\u03B42")
        self.lblConstrDelta3.setText("\u03B43")
        self.lblConstrDelta4.setText("\u03B44")
        self.lblConstrDelta5.setText("\u03B45")

        self.lblConstrTheta1.setText("\u03B81")
        self.lblConstrTheta2.setText("\u03B82")
        self.lblConstrTheta3.setText("\u03B83")
        self.lblConstrTheta4.setText("\u03B84")
        self.lblConstrTheta5.setText("\u03B85")

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

        # Connect constraints equations inputs:
        self.inputConstraint1.editingFinished.connect(self.constraintsChanged)
        self.inputConstraint2.editingFinished.connect(self.constraintsChanged)
        self.inputConstraint3.editingFinished.connect(self.constraintsChanged)
        self.inputConstraint4.editingFinished.connect(self.constraintsChanged)
        self.inputConstraint5.editingFinished.connect(self.constraintsChanged)

        # Connect constraints parameters:
        self.dsbConstrDelta1.valueChanged.connect(self.constraintsChanged)
        self.dsbConstrDelta2.valueChanged.connect(self.constraintsChanged)
        self.dsbConstrDelta3.valueChanged.connect(self.constraintsChanged)
        self.dsbConstrDelta4.valueChanged.connect(self.constraintsChanged)
        self.dsbConstrDelta5.valueChanged.connect(self.constraintsChanged)
        self.dsbConstrTheta1.valueChanged.connect(self.constraintsChanged)
        self.dsbConstrTheta2.valueChanged.connect(self.constraintsChanged)
        self.dsbConstrTheta3.valueChanged.connect(self.constraintsChanged)
        self.dsbConstrTheta4.valueChanged.connect(self.constraintsChanged)
        self.dsbConstrTheta5.valueChanged.connect(self.constraintsChanged)

        # Connect Powell parameters:
        self.dSBM1.valueChanged.connect(self.m1ChangedDSBox)
        self.hSldM1.valueChanged.connect(self.m1ChangedHSld)
        self.dSBM2.valueChanged.connect(self.m2ChangedDSBox)
        self.hSldM2.valueChanged.connect(self.m2ChangedHSld)
        self.dSBcMin.valueChanged.connect(self.cMinChangedDSBox)
        self.hSldcMin.valueChanged.connect(self.cMinChangedHSld)

        # Connect searching in direction parameters:
        self.dsbBracketStep.valueChanged.connect(self.bracketStepChanged)
        self.dsbGoldenSearchWindow.valueChanged.connect(self.goldenSearchWindowChanged)
        self.checkBoxBracketing.stateChanged.connect(self.bracketingOptionChanged)
        self.cmbGoldenSearchEpsilon.activated.connect(self.goldenSearchEpsilonChanged)

        # Set up variables and constrains inputs:
        self.setActiveConstrainInputs(self.numberOfConstraints)
        self.setActiveVariableInputs(int(self.cmbVariables.currentText()))
        self.meritum = str2fun(self.cmbObjFun.currentText())
        self.setXStart(self.numberOfVariables)
        self.setMaxInterations(int(self.cmbMaxIterations.currentText()))
        self.setPowellEpsilon(float(self.cmbPowellEpsilon.currentText()))

        # Set up states for searching in direction
        self.dsbBracketStep.setDisabled(False)
        self.lblBracketStep.setDisabled(False)
        self.dsbGoldenSearchWindow.setDisabled(True)
        self.lblGoldenSearchWindow.setDisabled(True)

        # Show the window at the end
        self.show()

    # Methods for constraints
    def nbConstrChanged(self):
        self.numberOfConstraints = int((self.cmbConstraints.currentText()))
        self.setActiveConstrainInputs(self.numberOfConstraints)
        self.setConstrEquations(self.numberOfConstraints)
        self.setConstrParameters(self.numberOfConstraints)

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
        self.lblConstraint1_2.setDisabled(True)
        self.lblConstraint2_2.setDisabled(True)
        self.lblConstraint3_2.setDisabled(True)
        self.lblConstraint4_2.setDisabled(True)
        self.lblConstraint5_2.setDisabled(True)
        self.lblConstrEq1.setDisabled(True)
        self.lblConstrEq2.setDisabled(True)
        self.lblConstrEq3.setDisabled(True)
        self.lblConstrEq4.setDisabled(True)
        self.lblConstrEq5.setDisabled(True)
        self.lblConstrDelta1.setDisabled(True)
        self.lblConstrDelta2.setDisabled(True)
        self.lblConstrDelta3.setDisabled(True)
        self.lblConstrDelta4.setDisabled(True)
        self.lblConstrDelta5.setDisabled(True)
        self.lblConstrTheta1.setDisabled(True)
        self.lblConstrTheta2.setDisabled(True)
        self.lblConstrTheta3.setDisabled(True)
        self.lblConstrTheta4.setDisabled(True)
        self.lblConstrTheta5.setDisabled(True)
        self.dsbConstrDelta1.setDisabled(True)
        self.dsbConstrDelta2.setDisabled(True)
        self.dsbConstrDelta3.setDisabled(True)
        self.dsbConstrDelta4.setDisabled(True)
        self.dsbConstrDelta5.setDisabled(True)
        self.dsbConstrTheta1.setDisabled(True)
        self.dsbConstrTheta2.setDisabled(True)
        self.dsbConstrTheta3.setDisabled(True)
        self.dsbConstrTheta4.setDisabled(True)
        self.dsbConstrTheta5.setDisabled(True)



        if nbrOfConstr >= 1:
            self.inputConstraint1.setDisabled(False)
            self.lblConstraint1.setDisabled(False)
            self.lblConstraint1_2.setDisabled(False)
            self.lblConstrEq1.setDisabled(False)
            self.lblConstrDelta1.setDisabled(False)
            self.lblConstrTheta1.setDisabled(False)
            self.dsbConstrDelta1.setDisabled(False)
            self.dsbConstrTheta1.setDisabled(False)
        if nbrOfConstr >= 2:
            self.inputConstraint2.setDisabled(False)
            self.lblConstraint2.setDisabled(False)
            self.lblConstraint2_2.setDisabled(False)
            self.lblConstrEq2.setDisabled(False)
            self.lblConstrDelta2.setDisabled(False)
            self.lblConstrTheta2.setDisabled(False)
            self.dsbConstrDelta2.setDisabled(False)
            self.dsbConstrTheta2.setDisabled(False)
        if nbrOfConstr >= 3:
            self.inputConstraint3.setDisabled(False)
            self.lblConstraint3.setDisabled(False)
            self.lblConstraint3_2.setDisabled(False)
            self.lblConstrEq3.setDisabled(False)
            self.lblConstrDelta3.setDisabled(False)
            self.lblConstrTheta3.setDisabled(False)
            self.dsbConstrDelta3.setDisabled(False)
            self.dsbConstrTheta3.setDisabled(False)
        if nbrOfConstr >= 4:
            self.inputConstraint4.setDisabled(False)
            self.lblConstraint4.setDisabled(False)
            self.lblConstraint4_2.setDisabled(False)
            self.lblConstrEq4.setDisabled(False)
            self.lblConstrDelta4.setDisabled(False)
            self.lblConstrTheta4.setDisabled(False)
            self.dsbConstrDelta4.setDisabled(False)
            self.dsbConstrTheta4.setDisabled(False)
        if nbrOfConstr >= 5:
            self.inputConstraint5.setDisabled(False)
            self.lblConstraint5.setDisabled(False)
            self.lblConstraint5_2.setDisabled(False)
            self.lblConstrEq5.setDisabled(False)
            self.lblConstrDelta5.setDisabled(False)
            self.lblConstrTheta5.setDisabled(False)
            self.dsbConstrDelta5.setDisabled(False)
            self.dsbConstrTheta5.setDisabled(False)

    def constraintsChanged(self):
        self.setConstrEquations(self.numberOfConstraints)
        self.setConstrParameters(self.numberOfConstraints)

    def setConstrEquations(self, nbrOfConstr):
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

    def setConstrParameters(self, nbrOfConstr):
        self.deltas = []
        self.thetas = []
        if nbrOfConstr >= 1:
            self.deltas.append(self.dsbConstrDelta1.value())
            self.thetas.append(self.dsbConstrTheta1.value())
        if nbrOfConstr >= 2:
            self.deltas.append(self.dsbConstrDelta2.value())
            self.thetas.append(self.dsbConstrTheta2.value())
        if nbrOfConstr >= 3:
            self.deltas.append(self.dsbConstrDelta3.value())
            self.thetas.append(self.dsbConstrTheta3.value())
        if nbrOfConstr >= 4:
            self.deltas.append(self.dsbConstrDelta4.value())
            self.thetas.append(self.dsbConstrTheta4.value())
        if nbrOfConstr >= 5:
            self.deltas.append(self.dsbConstrDelta5.value())
            self.thetas.append(self.dsbConstrTheta5.value())

    # Methods for variables
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

    # Set and get parameter M1
    def setM1(self, newM1):
        self.m1 = newM1
        self.hSldM1.setValue(newM1*1000)
        self.dSBM1.setValue(newM1)

    def m1ChangedDSBox(self):
        self.setM1(self.dSBM1.value())

    def m1ChangedHSld(self):
        self.setM1(self.hSldM1.value()/1000)

    # Set and get parameter M2
    def setM2(self, newM2):
        self.m2 = newM2
        self.hSldM2.setValue(newM2*10)
        self.dSBM2.setValue(newM2)

    def m2ChangedDSBox(self):
        self.setM2(self.dSBM2.value())

    def m2ChangedHSld(self):
        self.setM2(self.hSldM2.value()/10)

    # Set and get parameter cMin
    def setcMin(self, newcMin):
        self.cMin = newcMin
        self.hSldcMin.setValue(newcMin*1000000)
        self.dSBcMin.setValue(newcMin)

    def cMinChangedDSBox(self):
        self.setcMin(self.dSBcMin.value())

    def cMinChangedHSld(self):
        self.setcMin(self.hSldcMin.value()/1000000)

    # Set option for searching in direction

    def setBracketStep(self, newBracketStep):
        self.bracketStep = newBracketStep

    def bracketStepChanged(self):
        self.setBracketStep(self.dsbBracketStep.value())

    def setGoldenSearchWindow(self, newGoldenSearchWindow):
        self.goldenSearchWindow = newGoldenSearchWindow

    def bracketingOptionChanged(self):
        self.bracketing = self.checkBoxBracketing.isChecked()
        if self.checkBoxBracketing.isChecked():
            self.dsbBracketStep.setDisabled(False)
            self.lblBracketStep.setDisabled(False)
            self.dsbGoldenSearchWindow.setDisabled(True)
            self.lblGoldenSearchWindow.setDisabled(True)
        else:
            self.dsbBracketStep.setDisabled(True)
            self.lblBracketStep.setDisabled(True)
            self.dsbGoldenSearchWindow.setDisabled(False)
            self.lblGoldenSearchWindow.setDisabled(False)

    def goldenSearchWindowChanged(self):
        self.setGoldenSearchWindow(self.dsbGoldenSearchWindow.value())

    def goldenSearchEpsilonChanged(self):
        self.setGoldenSearchEpsilon(float(self.cmbGoldenSearchEpsilon.currentText()))

    def setGoldenSearchEpsilon(self, newEpsilon):
        self.epsilonGoldenSearch = newEpsilon
        print("New epsilon:", newEpsilon)


    # Powell algorithm
    def startSearch(self):
        self.statusBar().showMessage("Searching for minimum of: " + str(self.cmbObjFun.currentText())
                                     + " With xStart: " + str(self.xStart))

        self.logResults.insertPlainText('_'*80 + '\n')
        self.logResults.insertPlainText("Searching for minimum of: " + str(self.cmbObjFun.currentText()) +'\n')
        self.logResults.insertPlainText("Starting x: " + str(self.xStart) + '\n')

        powellConstr(self.meritum, self.xStart, constrains=self.constraints, deltas=self.deltas, thetas=self.thetas,
                     cMin=self.cMin, m2=self.m2, m1=self.m1)

        xMin, nIter, success = powell(self.meritum, self.xStart, epsilon=self.epsilonPowell,
                                      iterations=self.maxIterations, bracketing=self.bracketing,
                                      bracketStep=self.bracketStep, goldenSearchWindow=self.goldenSearchWindow,
                                      epsilonGoldenSearch=self.epsilonGoldenSearch)
        if success:
            self.logResults.insertPlainText('Minimum found at x: ' + str(xMin) + '\n')
        else:
            self.logResults.insertPlainText('Minimum not found \nMax number of iterations exceeded\n')
        self.logResults.insertPlainText("F(x) = " + str(self.meritum(xMin)) + '\n')
        self.logResults.insertPlainText("Number of cycles = " + str(nIter) + '\n')

        sb = self.logResults.verticalScrollBar()
        sb.setValue(sb.maximum())






if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    sys.exit(app.exec_())