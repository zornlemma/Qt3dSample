from PySide2 import QtWidgets


class CtlWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.createHorizontalGroupBox()

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addWidget(self.horizontalGroupBox)

        self.setLayout(self.mainLayout)

        self.setWindowTitle("Basic Layouts")


    def createHorizontalGroupBox(self):
        self.horizontalGroupBox = QtWidgets.QGroupBox("Add Objects", self)
        layout = QtWidgets.QHBoxLayout()

        self.buttonAddBox = QtWidgets.QPushButton("Add Box")
        layout.addWidget(self.buttonAddBox)
        self.buttonAddSphere = QtWidgets.QPushButton("Add Sphere")
        layout.addWidget(self.buttonAddSphere)
        self.horizontalGroupBox.setFixedHeight(100)

        self.horizontalGroupBox.setLayout(layout)


if __name__ == '__main__':

    import sys

    app = QtWidgets.QApplication(sys.argv)
    dialog = CtlWidget()
    sys.exit(dialog.exec_())
