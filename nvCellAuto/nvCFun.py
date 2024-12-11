from PyQt5 import QtWidgets, QtCore, QtGui
import sys, os, traceback
import configparser as cp

def nSysHook(type, value, trac):
    nn = traceback.format_tb(trac)
    nStr = f"Type: {type}<br/>Value: {value}<br/>Trace: {str(nn).replace('[', '').replace(']', '')}"
    emsg = QtWidgets.QErrorMessage()
    emsg.setFixedWidth(900)
    emsg.setFixedHeight(300)
    emsg.showMessage(nStr.strip("'.~").replace('\\n', '<br/>'))
    emsg.exec_()
    emsg.close()

def nDefault(self):
    fName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", os.getcwd(),
                                                                         "*.ini *.cfg *.conf")
    self.fp = open(fName)
    self.nSec = 'DEFAULT'

def fOpen(self, sStr):
    fName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File",
                                                     os.getcwd(), "*.ini *.cfg *.conf")
    self.fp = open(fName)
    self.nSec = 'Value'

def nParser(self, nFName='nvInit.ini', nSec='Value'):
    cfg = cp.ConfigParser()
    try:
        self.fp = open(nFName)
        self.nSec = nSec
    except Exception as err:
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("ERROR")
        msg.setText(str(err))
        b_def = QtWidgets.QPushButton("Default")
        b_can = QtWidgets.QPushButton("Value")
        msg.addButton(b_def, QtWidgets.QMessageBox.YesRole)
        msg.addButton(b_can, QtWidgets.QMessageBox.YesRole)
        b_def.setFocus()
        b_can.clicked.connect(lambda x: fOpen(self, str(err)))
        b_def.clicked.connect(lambda: nDefault(self))
        msg.exec_()
        msg.close()
    return cfg

class nGraphicsScene(QtWidgets.QGraphicsScene):
    def __init__(self, nWin, parent=None):
        QtWidgets.QGraphicsScene.__init__(self, parent)
        self.nWin = nWin
        self.opt = "Generate"
#===========================================================
        self._start = QtCore.QPointF()
        self._current_rect_item = None
#        self.setSceneRect(0, 0, self.nWin.WIN_WIDTH, self.nWin.WIN_HEIGHT)

    def setOption(self, opt):
        self.opt = opt

    def mousePressEvent(self, event):
        super(nGraphicsScene, self).mousePressEvent(event)
        rect = None
        clickecRect = self.itemAt(event.scenePos(), QtGui.QTransform())
        self._current_rect_item = QtWidgets.QGraphicsRectItem()
        if clickecRect is not None:
            rect = clickecRect.rect()
            print('RECT', rect.x(), rect.y())
        # x = event.scenePos().x()
        # y = event.scenePos().y()
        if self.opt == "Generate":
            if rect is not  None:
                self.addRect(rect.x(), rect.y(),
                        self.nWin.CELL_SIZE, self.nWin.CELL_SIZE, brush=QtCore.Qt.blue)
                self.nWin.grid[int(rect.x()//self.nWin.CELL_SIZE)][int(rect.y()//self.nWin.CELL_SIZE)] = 1
    #            print('rrrr',rect.x()//self.nWin.CELL_SIZE, rect.y()//self.nWin.CELL_SIZE)
        elif self.opt == "Select":
            print('Sek', clickecRect)

    def mouseMoveEvent(self, event):
        super(nGraphicsScene, self).mouseMoveEvent(event)
        rect = None
        self.nWin.tEv.stop()
        self.nWin.pBut_3.setEnabled(True)
        pX = event.scenePos().x()
        if pX < 0:
            pX = 0
        if pX > self.nWin.WIN_WIDTH:
            pX = self.nWin.WIN_WIDTH
        pY = event.scenePos().y()
        if pY < 0:
            pY = 0
        if pY > self.nWin.WIN_HEIGHT - self.nWin.CELL_SIZE:
            pY = self.nWin.WIN_HEIGHT - self.nWin.CELL_SIZE
        rect = self.itemAt(pX, pY, QtGui.QTransform()).rect()
        nX = rect.x()
        nY = rect.y()
        # if rect is not None:
        self.addRect(nX, nY, self.nWin.CELL_SIZE, self.nWin.CELL_SIZE, brush=QtCore.Qt.blue)
        self.nWin.grid[int(nX//self.nWin.CELL_SIZE)][int(nY//self.nWin.CELL_SIZE)] = 1
#        print('mov', nX//self.nWin.CELL_SIZE, nY//self.nWin.CELL_SIZE)

    def mouseReleaseEvent(self, event):
        super(nGraphicsScene, self).mouseReleaseEvent(event)
#        print('rel', event.scenePos().x(), event.scenePos().y())
#        self.nWin.tEv.start()

    def mouseDoubleClickEvent(self, event):
        super(nGraphicsScene, self).mouseDoubleClickEvent(event)
#        print('Dbl click', event.scenePos())
#         if self.nWin.nOpt == 'Start':
#             self.nWin.nOpt = 'Step'
#         else:
#             self.nWin.nOpt = 'Start'
#            self.nWin.nvResume()


class nWin(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(nWin, self).__init__()
        self.setapUI()

    def setapUI(self, parent=None):
        self.fp = ''
        self.nSec = 'Value'

        QtWidgets.QWidget.__init__(self, parent)
        self.setWindowTitle("Клеточный автомат")
        self.setGeometry(300, 300, 250, 150)
        self.stBar = QtWidgets.QStatusBar(self)
        self.stBar.showMessage("Press Q - stop; Press C - initialization")
        self.pBut_1 = QtWidgets.QPushButton(self)
        self.pBut_1.setObjectName("pBut_1")
        self.pBut_1.setText('Open')
        self.pBut_1.setStyleSheet("QPushButton {background-color: red; color: white;}")

        vBox = QtWidgets.QVBoxLayout()
        vBox.addWidget(self.pBut_1)
        vBox.addWidget(self.stBar)
        self.setLayout(vBox)

        self.pBut_1.clicked.connect(lambda x: fOpen(self, 'str(err)'))


def nMain():
    app = QtWidgets.QApplication(sys.argv)
    window = nWin()
    window.show()
    # window.nPn.end()
    sys.exit(app.exec_())


if __name__ == '__main__':
#    sys.excepthook = nSysHook
#    nMain()
    pass