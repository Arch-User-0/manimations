
from manim import *
from Charge import *
import numpy as np
from manim.opengl import *
class Show(ThreeDScene):
    def construct(self):
        
        self.set_camera_orientation(phi = 85*DEGREES,theta = 195*DEGREES)
        
        # self.camera.move_to([0.5,-3,0])
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
        charge_1 = Charge(Id="",pos=[0,0,0],stationary=True, q =1,radius = 0.05)
        charge_2 = Charge(Id="",pos=[1,0,0],initial_velocity=[0.5,0.45,-0.25], q =-1,radius = 0.05)
        charge_3 = Charge(Id="",pos=[-2,0,0],initial_velocity=[0.65,-0.45,0.5], q =-1,radius = 0.05)
        trace_2 = TracedPath(lambda: charge_2.get_center(),dissipating_time=4,color=PINK)
        trace_3 = TracedPath(lambda: charge_3.get_center(),dissipating_time=4,color=GREEN)
        trace_2.set_color(PINK)
        trace_3.set_color(GREEN)
        V_field = PotentialField(charge=charge_1)
        Field = ElectricField(field_func= lambda pos:(pos[2]*OUT/10),z_range=[-0.5,0.5],x_range=[-3,3],y_range=[-3,3],opacity=0.5)

        self.charges=[charge_1,charge_2,charge_3]
        self.add(axes,trace_2.set_color(PINK),trace_3.set_color(GREEN),*self.charges,Field)
        Charge.charge_updater(self.charges,external_electric_field=Field)
        # self.wait(3)
        self.interactive_embed()
