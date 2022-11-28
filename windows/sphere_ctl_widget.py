from typing import Callable

from PySide2 import QtWidgets
from PySide2.QtGui import QPalette

from models import *


class SphereCtlWidget(QtWidgets.QGroupBox):
    def __init__(self, dispatch: Callable, model: SphereModel = None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if model is None:
            model = SphereModel.get_random()
        self.dispatch = dispatch
        self.model_action = lambda: dispatch(self, self.to_model())

        self.setTitle("sphere")
        self.id = model.id

        self.setFixedHeight(200)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(QtWidgets.QLabel("name"), 1, 0)
        self.w_name = QtWidgets.QLineEdit()
        layout.addWidget(self.w_name, 1, 1, 1, 5)
        layout.addWidget(QtWidgets.QLabel("pos x"), 2, 0)
        self.w_pos_x = QtWidgets.QDoubleSpinBox()
        self.w_pos_x.setMinimum(-100)
        self.w_pos_x.setMaximum(100)
        layout.addWidget(self.w_pos_x, 2, 1)
        layout.addWidget(QtWidgets.QLabel("pos y"), 2, 2)
        self.w_pos_y = QtWidgets.QDoubleSpinBox()
        self.w_pos_y.setMinimum(-100)
        self.w_pos_y.setMaximum(100)
        layout.addWidget(self.w_pos_y, 2, 3)
        layout.addWidget(QtWidgets.QLabel("pos z"), 2, 4)
        self.w_pos_z = QtWidgets.QDoubleSpinBox()
        self.w_pos_z.setMinimum(-100)
        self.w_pos_z.setMaximum(100)
        layout.addWidget(self.w_pos_z, 2, 5)

        layout.addWidget(QtWidgets.QLabel("radius"), 3, 0)
        self.w_radius = QtWidgets.QDoubleSpinBox()
        layout.addWidget(self.w_radius, 3, 1)

        self.w_color_label = QtWidgets.QLabel("Color")
        self.w_color_label.setAutoFillBackground(True)
        self.w_pal = QPalette()
        self.w_color_label.setPalette(self.w_pal)
        layout.addWidget(self.w_color_label, 3, 4)
        self.w_color_picker = QtWidgets.QPushButton("Pick a color")
        self.w_color_picker.clicked.connect(self.pick_color)
        layout.addWidget(self.w_color_picker, 3, 5)

        self.w_deleter = QtWidgets.QPushButton("Delete")
        layout.addWidget(self.w_deleter, 4, 0, 1, 2)

        self.reduce(model)
        self.store_connect()

        self.setLayout(layout)

    def pick_color(self):
        my_color = QtWidgets.QColorDialog.getColor()
        if my_color.isValid():
            self.w_pal.setColor(QPalette.Window, my_color)
            self.w_color_label.setPalette(self.w_pal)
            self.model_action()

    def store_connect(self):
        self.w_name.textChanged.connect(self.model_action)
        self.w_pos_x.valueChanged.connect(self.model_action)
        self.w_pos_y.valueChanged.connect(self.model_action)
        self.w_pos_z.valueChanged.connect(self.model_action)
        self.w_radius.valueChanged.connect(self.model_action)
        self.w_deleter.clicked.connect(lambda: self.dispatch(self, None))

    def to_model(self) -> SphereModel:
        color = self.w_pal.color(QPalette.Window)
        return SphereModel(id=self.id,
                           name=self.w_name.text(),
                           translation=Vector3Model(x=self.w_pos_x.value(), y=self.w_pos_y.value(),
                                                    z=self.w_pos_z.value()),
                           color=RgbaModel(r=color.redF(), g=color.greenF(), b=color.blueF(), a=color.alphaF()),
                           radius=self.w_radius.value(),
                           )

    def reduce(self, model: SphereModel):
        self.w_name.setText(model.name)

        self.w_pos_x.setValue(model.translation.x)
        self.w_pos_y.setValue(model.translation.y)
        self.w_pos_z.setValue(model.translation.z)

        self.w_radius.setValue(model.radius)

        self.w_pal.setColor(QPalette.Window, model.color.to_qt())
        self.w_color_label.setPalette(self.w_pal)

        self.id = model.id
        # if want to use name here, may need parent redraw
        self.setTitle('sphere-' + str(model.id))
