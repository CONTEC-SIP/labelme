from PIL.ImageQt import ImageQt
from qtpy import QtGui
from qtpy import QtWidgets

from .. import utils


class PreviewDialog(QtWidgets.QDialog):
    def __init__(self, img, polygons, parent=None):
        super(PreviewDialog, self).__init__(parent)
        self.setWindowTitle("Preview")

        self.imageLabel = QtWidgets.QLabel()
        self.imageLabel.setBackgroundRole(QtGui.QPalette.Base)
        self.imageLabel.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)

        name_to_id = {'none': 0,
                      'building': 1,
                      'road': 2,
                      'street': 3,
                      'plastic_house': 4,
                      'farmland': 5,
                      'forest': 6,
                      'waterside': 7}

        mask, _ = utils.shapes_to_label(img.shape, polygons, name_to_id)
        qim = ImageQt(utils.lblreturn(mask))
        self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(qim))

        boxlayout = QtWidgets.QVBoxLayout()
        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        self.scrollArea.setWidget(self.imageLabel)
        self.scrollArea.adjustSize()
        boxlayout.addWidget(self.scrollArea)

        self.setLayout(boxlayout)

