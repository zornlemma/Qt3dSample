from PySide2.Qt3DCore import Qt3DCore
from PySide2.Qt3DExtras import Qt3DExtras
from PySide2.QtGui import QVector3D, QQuaternion

from models import SphereModel


class SphereEntity(Qt3DCore.QEntity):
    def __init__(self, model: SphereModel = None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if model is None:
            model = SphereModel.get_random()
        self.id = model.id

        self.mesh = Qt3DExtras.QSphereMesh(self)

        self.transform = Qt3DCore.QTransform(self)

        self.material = Qt3DExtras.QPhongMaterial(self)

        self.addComponent(self.mesh)
        self.addComponent(self.transform)
        self.addComponent(self.material)
        self.reduce(model)

    def reduce(self, model: SphereModel):
        self.transform.setTranslation(model.translation.to_qt())
        self.transform.setScale(model.radius)
        self.material.setAmbient(model.color.to_qt())
