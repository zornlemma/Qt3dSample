from typing import List, Dict
from uuid import UUID, uuid4

from PySide2.QtGui import QVector3D, QColor
from pydantic import BaseModel, Field
import random

DEFAULT_SCALE = 10


class Vector3Model(BaseModel):
    x: float
    y: float
    z: float

    def to_qt(self) -> QVector3D:
        return QVector3D(self.x, self.y, self.z)

    @classmethod
    def get_random(cls, scale: int) -> 'Vector3Model':
        return Vector3Model(x=random.randint(-scale, scale),
                            y=random.randint(-scale, scale),
                            z=random.randint(-scale, scale), )


class RgbaModel(BaseModel):
    r: float
    g: float
    b: float
    a: float

    def to_qt(self) -> QColor:
        return QColor.fromRgbF(self.r, self.g, self.b, self.a)

    @classmethod
    def get_random(cls) -> 'RgbaModel':
        return RgbaModel(r=random.random(),
                         g=random.random(),
                         b=random.random(),
                         a=random.random(), )


class BoxModel(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str = Field(default_factory=lambda: str(uuid4()))
    translation: Vector3Model
    rotate: int
    color: RgbaModel
    size: Vector3Model

    @classmethod
    def get_random(cls) -> 'BoxModel':
        return BoxModel(
            translation=Vector3Model.get_random(DEFAULT_SCALE),
            rotate=random.randrange(0, 360),
            color=RgbaModel.get_random(),
            size=Vector3Model(x=1, y=1, z=1),
        )


class SphereModel(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str = Field(default_factory=lambda: str(uuid4()))
    translation: Vector3Model
    color: RgbaModel
    radius: float

    @classmethod
    def get_random(cls) -> 'SphereModel':
        return SphereModel(
            translation=Vector3Model.get_random(DEFAULT_SCALE),
            color=RgbaModel.get_random(),
            radius=random.uniform(0.5, 4),
        )


class SceneModel(BaseModel):
    boxes: Dict[str, BoxModel] = {}
    spheres: Dict[str, SphereModel] = {}
