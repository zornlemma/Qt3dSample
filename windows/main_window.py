import collections
from typing import Union

from PySide2 import QtWidgets
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QMainWindow, QPushButton, QScrollArea

from models import BoxModel, SceneModel, SphereModel
from windows.box_ctl_widget import BoxCtlWidget
from windows.box_entity import BoxEntity
from windows.ctl_widget import CtlWidget
from windows.sphere_ctl_widget import SphereCtlWidget
from windows.sphere_entity import SphereEntity
from windows.three_window import ThreeWindow

PERSIST_FILE_NAME = 'entities.json'

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.controlWidget = CtlWidget(parent=self)

        self.w = ThreeWindow()
        self.w.show()

        self.scrollArea = QScrollArea()
        self.scrollArea.setFixedHeight(800)
        self.scrollArea.setFixedWidth(500)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(Qt.AlignTop)
        self.scrollArea.setWidget(self.controlWidget)
        self.setCentralWidget(self.scrollArea)

        self.models = SceneModel()
        self.id2Widgets = collections.defaultdict(list)
        self.controlWidget.buttonAddBox.clicked.connect(lambda: self.createBox())
        self.controlWidget.buttonAddSphere.clicked.connect(lambda: self.createSphere())
        self.load()

    def createBox(self, old_model: BoxModel = None):
        model = BoxModel.get_random() if old_model is None else old_model
        boxEntity = BoxEntity(model=model, parent=self.w.rootEntity)
        boxCtlWidget = BoxCtlWidget(model=model, dispatch=self.dispatch)
        self.controlWidget.mainLayout.addWidget(boxCtlWidget)
        self.controlWidget.repaint()

        self.id2Widgets[model.id].append(boxEntity)
        self.id2Widgets[model.id].append(boxCtlWidget)
        self.models.boxes[str(model.id)] = model
        self.persist()

    def createSphere(self, old_model: SphereModel = None):
        model = SphereModel.get_random() if old_model is None else old_model
        sphereEntity = SphereEntity(model=model, parent=self.w.rootEntity)
        sphereCtlWidget = SphereCtlWidget(model=model, dispatch=self.dispatch)
        self.controlWidget.mainLayout.addWidget(sphereCtlWidget)
        self.controlWidget.repaint()

        self.id2Widgets[model.id].append(sphereEntity)
        self.id2Widgets[model.id].append(sphereCtlWidget)
        self.models.spheres[str(model.id)] = model
        self.persist()

    def dispatch(self, source: QtWidgets.QWidget, model: Union[BoxModel, SphereModel]):
        if model is None:
            for w in self.id2Widgets[source.id]:
                w.setParent(None)
                w.deleteLater()
            self.controlWidget.setLayout(self.controlWidget.mainLayout)
            self.controlWidget.repaint()
            del self.id2Widgets[source.id]
            self.models.boxes.pop(str(source.id), None)
            self.models.spheres.pop(str(source.id), None)

        else:
            for w in self.id2Widgets[model.id]:
                if w is not source:
                    # TODO: block signal
                    #   https://stackoverflow.com/questions/34990596/how-to-set-value-of-a-widget-without-triggering-valuechanged-callback-in-pyside
                    w.reduce(model)

            if isinstance(model, BoxModel):
                self.models.boxes[str(model.id)] = model
            elif isinstance(model, SphereModel):
                self.models.spheres[str(model.id)] = model

        self.persist()


    def persist(self):
        with open(PERSIST_FILE_NAME, 'w') as fout:
            fout.write(self.models.json())

    def load(self):
        from os.path import exists
        if exists(PERSIST_FILE_NAME):
            self.models = SceneModel.parse_file(PERSIST_FILE_NAME)
            for _, m in self.models.boxes.items():
                self.createBox(m)
            for _, m in self.models.spheres.items():
                self.createSphere(m)
