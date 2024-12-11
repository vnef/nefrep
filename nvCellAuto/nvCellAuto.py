from PyQt5 import QtTest, uic
from PyQt5.QtCore import Qt
# from PyQt5.Qt import QSizePolicy
# from PyQt5.QtWidgets import QTableWidgetItem
import random
from PyQt5.uic.Compiler.qtproxies import QtCore
from nvCFun import *

class nCaApp(QtWidgets.QMainWindow, QtWidgets.QGraphicsItem):
    cellSignal = QtCore.pyqtSignal(object)
    stopSignal = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super(nCaApp, self).__init__()
        self.setapUI()

    def setapUI(self, parent=None):
        self.turn = 0
        self.grid = []
        self.nThr = 'Start'
        self.nB = 'ng == 1'
        self.nS = 'ng == 1'
        self.fp = ''
        self.nSec = ''
        self.nOpt = 'Start'

        cfg = nParser(self, nFName='nvInit.ini', nSec='DEFAULT')
        cfg.read_file(self.fp)
        self.pathProject = cfg.get('File', 'pathProject')
        self.CELL_SIZE = int(cfg.get(self.nSec, 'CELL_SIZE'))
        self.nRPoint = int(cfg.get(self.nSec, 'nRPoint'))
        print(self.nSec, self.CELL_SIZE)

        QtWidgets.QWidget.__init__(self, parent)
        uic.loadUi('nvCArb.ui', self)
        self.setWindowTitle("Клеточный автомат")
        self.statusBar().showMessage('Key press: Q - Stop, C - Clear, S - Step '
                                     'Move mouse - Initialization; Check: A - Auto, S - Step')

        self.WIN_WIDTH = self.gr_1.width()
        self.WIN_HEIGHT = self.gr_1.height()
        self.GRID_WIDTH = self.WIN_WIDTH//self.CELL_SIZE
        self.GRID_HEIGHT = self.WIN_HEIGHT//self.CELL_SIZE

        self.tEv = QtCore.QTimer()

        self.cBoxB_3.setChecked(True)
        self.cBoxS_2.setChecked(True)
        self.cBoxS_3.setChecked(True)

        self.pBut_1.setStyleSheet("QPushButton""{""background-color : lightblue;""}""QPushButton::pressed"
                             "{""background-color : red;""}")
        self.pBut_2.setStyleSheet("QPushButton""{""background-color : lightblue;""}""QPushButton::pressed"
                             "{""background-color : red;""}")
        self.pBut_3.setStyleSheet("QPushButton""{""background-color : lightblue;""}""QPushButton::pressed"
                             "{""background-color : red;""}")
        self.lcdNum_1.setStyleSheet("QLCDNumber {background-color: black;  color: white; font: bold}")

        self.nScen = nGraphicsScene(nWin=self)
        self.gr_1.setScene(self.nScen)
        self.gr_1.showMaximized()

        self.grid = self.fCellInitZero()
        self.fDrawGrid(self.grid)
        self.lEd_2.setText(str(self.GRID_WIDTH))
        self.lEd_3.setText(str(self.GRID_HEIGHT))

        self.tEv.timeout.connect(self.nvLife)
        self.rBut_1.toggled.connect(self.fClickRb1)
        self.rBut_2.toggled.connect(self.fClickRb2)
        self.pBut_1.clicked.connect(self.nvStart)
        self.pBut_2.clicked.connect(self.nvStop)
        self.pBut_3.clicked.connect(self.nvResume)
    #    self.pBut_3.clicked.connect(self.nTest)

    def nvStart(self):
        self.turn = 0
        self.nvRules()
        self.nScen.clear()
        self.pBut_1.setEnabled(False)
        self.pBut_3.setEnabled(False)
        self.grid = self.fInitCell()
        self.fDrawGrid(self.grid)
        self.tEv.setInterval(50)
        self.tEv.start()

    def nvStop(self):
        self.pBut_1.setEnabled(True)
        self.pBut_3.setEnabled(True)
        self.tEv.stop()
        self.stopSignal.emit('Stop')
#        self.nScen.addEllipse(10, 20, 90, 120, self.nPen)

    def nvResume(self):
        self.lEd_2.setText(str(self.GRID_WIDTH))
        self.lEd_3.setText(str(self.GRID_HEIGHT))
        self.nvRules()
        self.pBut_1.setEnabled(False)
        self.pBut_3.setEnabled(False)
        self.tEv.setInterval(100)
        self.tEv.start()

    def nvLife(self):
        # Отображение игрового поля
        self.fDrawGrid(self.grid)
        # Обновление игрового поля
        self.grid = self.fNextGen(self.grid)
        # Увеличение счетчика ходов
        self.turn += 1
        self.lcdNum_1.display(self.turn)
        if self.turn % 10 == 0:
            QtTest.QTest.qWait(20)
        # Добавление случайных точек один раз за каждые 10 ходов
        if self.turn % self.nRPoint == 0:
#            nDat = QtCore.QDateTime.currentDateTime().toString('hh:mm:ss.zzz')
            for _ in range(5):
                x = random.randint(0, self.GRID_HEIGHT - 1)
                y = random.randint(0, self.GRID_WIDTH - 1)
                self.grid[y][x] = 1

    def fInitCell(self):
#        self.nScen.clear()
        self.WIN_WIDTH = self.gr_1.width()
        self.WIN_HEIGHT = self.gr_1.height()
        self.GRID_WIDTH = self.WIN_WIDTH//self.CELL_SIZE
        self.GRID_HEIGHT = self.WIN_HEIGHT//self.CELL_SIZE
        self.lEd_2.setText(str(self.GRID_WIDTH))
        self.lEd_3.setText(str(self.GRID_HEIGHT))
        grid = []
        for _ in range(self.GRID_WIDTH):
            row = [random.randint(0, 1) for _ in range(self.GRID_HEIGHT)]
            grid.append(row)
        return grid

    def fCellInitZero(self):
        grid = []
        self.WIN_WIDTH = self.gr_1.width()
        self.WIN_HEIGHT = self.gr_1.height()
        self.GRID_WIDTH = self.WIN_WIDTH//self.CELL_SIZE
        self.GRID_HEIGHT = self.WIN_HEIGHT//self.CELL_SIZE
        for _ in range(self.GRID_WIDTH):
            row = [0] * int(self.GRID_HEIGHT)
            grid.append(row)
        return grid

    def fDrawGrid(self, grid):
        self.nScen.clear()
        for row in range(self.GRID_WIDTH):
            for col in range(self.GRID_HEIGHT):
                if grid[row][col] == 1:
                    self.nScen.addRect(row*self.CELL_SIZE, col*self.CELL_SIZE,
                                  self.CELL_SIZE, self.CELL_SIZE, brush=QtCore.Qt.red)
                else:
                    self.nScen.addRect(row*self.CELL_SIZE, col*self.CELL_SIZE,
                                    self.CELL_SIZE, self.CELL_SIZE, brush=QtCore.Qt.green)

    def fNextGen(self, grid):
        new_grid = [[0] * self.GRID_HEIGHT for _ in range(self.GRID_WIDTH)]
        W = self.GRID_WIDTH
        H = self.GRID_HEIGHT
        for x in range(self.GRID_WIDTH):
            for y in range(self.GRID_HEIGHT):
                ng = (grid[x][(y - 1) % H] + grid[x][(y + 1) % H] +
                         grid[(x - 1) % W][y] + grid[(x + 1) % H][y] +
                         grid[(x - 1) % W][(y - 1) % H] + grid[(x - 1) % W][(y + 1) % H] +
                         grid[(x + 1) % W][(y - 1) % H] + grid[(x+ 1) % W][(y + 1) % H])
                if grid[x][y] == 1:
                    if eval(self.nS):                # S
                        new_grid[x][y] = 1
                else:
                    if eval(self.nB):                 # B
                        new_grid[x][y] = 1
        #        print('============', ng, x, y, new_grid[x][y])
            if self.nOpt == 'Step':
                self.tEv.stop()
        return new_grid

    def fClickRb1(self):
        if self.rBut_1.isChecked():
            self.nOpt = 'Start'
            self.nvResume()

    def fClickRb2(self):
        if self.rBut_2.isChecked():
            self.nOpt = 'Step'

    def nvRules(self):
        lsb = ''
        lss = ''
        # self.nSender = self.sender()
        # self.nSender.isChecked()
        if (self.cBoxB_0.checkState() == 2):
            lsb = lsb + 'ng == 0 ' + 'or '
        if (self.cBoxB_1.checkState() == 2):
            lsb = lsb + 'ng == 1 ' + 'or '
        if (self.cBoxB_2.checkState() == 2):
            lsb = lsb + 'ng == 2 ' + 'or '
        if (self.cBoxB_3.checkState() == 2):
            lsb = lsb + 'ng == 3 ' + 'or '
        if (self.cBoxB_4.checkState() == 2):
            lsb = lsb + 'ng == 4 ' + 'or '
        if (self.cBoxB_5.checkState() == 2):
            lsb = lsb + 'ng == 5 ' + 'or '
        if (self.cBoxB_6.checkState() == 2):
            lsb = lsb + 'ng == 6 ' + 'or '
        if (self.cBoxB_7.checkState() == 2):
            lsb = lsb + 'ng == 7 ' + 'or '
        if (self.cBoxB_8.checkState() == 2):
            lsb = lsb + 'ng == 8 ' + 'or '
        if lsb == '':
            lsb = 'ng == 100 or '

        if (self.cBoxS_0.checkState() == 2):
            lss = lss + 'ng == 0 ' + 'or '
        if (self.cBoxS_1.checkState() == 2):
            lss = lss + 'ng == 1 ' + 'or '
        if (self.cBoxS_2.checkState() == 2):
            lss = lss + 'ng == 2 ' + 'or '
        if (self.cBoxS_3.checkState() == 2):
            lss = lss + 'ng == 3 ' + 'or '
        if (self.cBoxS_4.checkState() == 2):
            lss = lss + 'ng == 4 ' + 'or '
        if (self.cBoxS_5.checkState() == 2):
            lss = lss + 'ng == 5 ' + 'or '
        if (self.cBoxS_6.checkState() == 2):
            lss = lss + 'ng == 6 ' + 'or '
        if (self.cBoxS_7.checkState() == 2):
            lss = lss + 'ng == 7 ' + 'or '
        if (self.cBoxS_8.checkState() == 2):
            lss = lss + 'ng == 8 ' + 'or '
        if lss == '':
            lss = 'ng == 100 or '

        self.nB = lsb[:len(lsb) - 3]
        self.nS = lss[:len(lss) - 3]
        return lsb, lss

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Q:
            self.tEv.stop()
            self.pBut_1.setEnabled(True)
            self.pBut_3.setEnabled(True)
        if e.key() == Qt.Key_C:
            self.turn = 0
            self.lcdNum_1.display(self.turn)
            self.grid = self.fCellInitZero()
            self.fDrawGrid(self.grid)
            self.lEd_2.setText(str(self.GRID_WIDTH))
            self.lEd_3.setText(str(self.GRID_HEIGHT))
        if e.key() == Qt.Key_S:
            if self.nOpt == 'Step':
                self.tEv.start()
        # nDat = QtCore.QDateTime.currentDateTime().toString('hh:mm:ss.zzz')
        # print(nDat)
        # QtWidgets.QApplication.sendEvent(self.nvRules(),  QtGui.QKeyEvent(QtCore.QEvent.KeyPress))

    def nTest(self):
        self.nScen.itemAt()

def nvMain():
    app = QtWidgets.QApplication(sys.argv)
    window = nCaApp()
    window.show()
    # window.nPn.end()
    sys.exit(app.exec_())

if __name__ == '__main__':
#    sys.excepthook = nSysHook
    nvMain()