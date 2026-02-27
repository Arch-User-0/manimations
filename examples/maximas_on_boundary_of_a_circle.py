from manim import *
from Waves import *
import numpy as np
class scene(ThreeDScene):
    def construct(self):
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
        )#.add_coordinates()

        self.set_camera_orientation(phi = 55*DEGREES,theta = 20*DEGREES)
        r=2
        cylinder = Cylinder(radius=r,height=4,color=RED)
        self.add(axes)
        src_1=np.array([1.0,0,0])
        p1= Dot().move_to(src_1)
        src_2= np.array([-1.0,0,0])
        p2=Dot().move_to(src_2)
        src_3= np.array([0,1.0,0])
        p3=Dot().move_to(src_3)

        self.add(p1)
        self.add(p2)
        self.add(p3)
        
        source = (src_1,src_2,src_3)
        wave = RadialWave(src_1,src_2,src_3, radial_distance=2,amplitude=0.1,wavelength=0.75,color=TEAL,propagation_center=(0,0,0))
        boundary = always_redraw(lambda: ParametricFunction(lambda t: (r*np.cos(t),r*np.sin(t),wave._radial_wave(r*np.cos(t),r*np.sin(t),sources=source)),t_range=[0,2*np.pi]))
        
        self.add(cylinder)
        self.add(wave)
        self.add(boundary)
        wave.start_updating_wave_radially((0,0,0))
        self.begin_ambient_camera_rotation(rate=0.09)
        self.wait(2*np.pi)
        # self.set_camera_orientation(phi = 85*DEGREES,theta = 20*DEGREES)
        # self.wait(5)
        # self.interactive_embed()