from manim import *
import numpy as np
from Charge import Charge, ElectricField
class interaction(ThreeDScene):
    
    def construct(self):
        self.set_camera_orientation(phi = 85*DEGREES,theta = 195*DEGREES)
        # print(self.camera.get_center())
        self.camera.move_to([0.5,-3,0])
        axes = ThreeDAxes(
            x_range=[-5,5,1,],
            y_range=[-5,5,1],
            z_range=[-3,3,1],
            x_axis_config={
                "color":"RED"
            },
            y_axis_config={
                "color":GREEN
            },
            z_axis_config={
                "color":BLUE
            },z_index=1
        )
        horizontal_bounds=[-2.5,2.5]
        charge_1 = Charge(Id="",pos=[0.1,0,0.3], radius = 0.05)
        # trace_2 = TracedPath(lambda:charge_2.get_center(),dissipating_time=4)
        # trace_3 = TracedPath(lambda:charge_3.get_center(),dissipating_time=4)
        self.charges=[charge_1]
        Field = ElectricField(x_range=horizontal_bounds,y_range=horizontal_bounds,z_range=[-0.5,0.5],stroke_width=DEFAULT_STROKE_WIDTH/5,three_dimensions=True,field_func= lambda pos: (
            OUT*pos[2]/2
        ))
        # self.add(trace_2)
        # self.add(trace_3.set_color(PINK))
        self.add(Field)
        for charge in self.charges:
            self.add(charge)
        

        self.add(axes)
        Charge.charge_updater(self.charges,Field)
        # self.wait(30)
        self.interactive_embed()