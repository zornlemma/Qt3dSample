from PySide2.Qt3DCore import Qt3DCore
from PySide2.Qt3DExtras import Qt3DExtras
from PySide2.QtGui import QVector3D, QQuaternion

from models import BoxModel


class BoxEntity(Qt3DCore.QEntity):
    def __init__(self, model: BoxModel = None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if model is None:
            model = BoxModel.get_random()
        self.id = model.id

        self.boxMesh = Qt3DExtras.QCuboidMesh(self)

        self.boxTransform = Qt3DCore.QTransform(self)

        self.material = Qt3DExtras.QPhongMaterial(self)

        self.addComponent(self.boxMesh)
        self.addComponent(self.boxTransform)
        self.addComponent(self.material)
        self.reduce(model)

    def reduce(self, model: BoxModel):
        self.boxTransform.setTranslation(model.translation.to_qt())
        self.boxTransform.setScale3D(model.size.to_qt())
        self.boxTransform.setRotation(QQuaternion.fromAxisAndAngle(QVector3D(0, 1, 0), model.rotate))
        self.material.setAmbient(model.color.to_qt())
