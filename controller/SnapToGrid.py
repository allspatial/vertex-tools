__author__ = 'mwagner'

from PyQt4.Qt import QThread, pyqtSignal, QMutex, QMutexLocker


class SnapToGrid(QThread):

    finished = pyqtSignal(str, bool)
    progressed = pyqtSignal(str, int)

    def __init__(self, layer_id, parent=None):

        super(SnapToGrid, self).__init__(parent)
        self.layer_id = layer_id
        self.stopped = False
        self.mutex = QMutex()
        self.completed = False

    def run(self):

        self.snap()
        self.stop()
        self.finished.emit(self.layer_id, self.completed)

    def stop(self):

        with QMutexLocker(self.mutex):
            self.stopped = True

    def snap(self):

        limit = 5000000
        for x in range(0, limit):
            with QMutexLocker(self.mutex):
                if self.stopped:
                    return

            if x % 500 == 0:
                self.progressed.emit(self.layer_id, x)

        self.completed = True
