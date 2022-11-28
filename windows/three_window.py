from PySide2.Qt3DCore import Qt3DCore
from PySide2.Qt3DExtras import Qt3DExtras
from PySide2.QtGui import QVector3D, QQuaternion, QColor

from models import BoxModel
from windows.box_entity import BoxEntity


class ThreeWindow(Qt3DExtras.Qt3DWindow):
    def __init__(self):
        super(ThreeWindow, self).__init__()

        # Camera
        # self.camera().lens().setPerspectiveProjection(45, 16 / 9, 0.1, 1000)
        self.camera().setPosition(QVector3D(0, 40, 30))
        self.camera().setViewCenter(QVector3D(0, 0, 0))

        # For camera controls
        self.createScene()
        self.camController = Qt3DExtras.QOrbitCameraController(self.rootEntity)
        self.camController.setLinearSpeed(50)
        self.camController.setLookSpeed(180)
        self.camController.setCamera(self.camera())

        self.setRootEntity(self.rootEntity)

    def createScene(self):
        # Root entity
        self.rootEntity = Qt3DCore.QEntity()

        # Material
        self.material = Qt3DExtras.QPhongMaterial(self.rootEntity)

        self.groundEntity = Qt3DCore.QEntity(self.rootEntity)
        self.groundMesh = Qt3DExtras.QCuboidMesh()
        self.groundEntity.addComponent(self.groundMesh)
        self.groundTransform = Qt3DCore.QTransform()
        self.groundTransform.setScale3D(QVector3D(100, 0.1, 100))
        self.groundTransform.setTranslation(QVector3D(0, -40, 0))
        self.groundEntity.addComponent(self.groundTransform)
        self.groundEntity.addComponent(self.material)
