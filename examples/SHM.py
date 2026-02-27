
from spring_block_system import *
from manim import *
import numpy as np
import math

class scene(Scene):
    def construct(self):
        block = Rectangle(width=1,height=1)
        system = Spring_Block(radius=0.15,mass_of_object=4,Length=4,dens=6*PI,amplitude=2, block = block)
        system.to_edge(LEFT)
        wall = Line( start=(0,-5,0), end = (0,5,0))
        wall.to_edge(LEFT)
        
        floor = Line(start=(-8,-1/2,0),end=(5,-1/2,0),stroke_width=1)

        disp_label = always_redraw(lambda: Text(str(system.get_block_displacement())).scale(0.5).to_corner(UL))
        acc_label = always_redraw(lambda: Text(str(system.get_block_acceleration())).scale(0.5).next_to(disp_label))

        self.add(floor)
        self.add(wall)

        #mentioning forces
        # F_restoring = always_redraw(lambda: Arrow(start=(0,0,0),end=((system.get_block_acceleration()*2),0,0)))
        test_tracker= ValueTracker(0)
        F_restoring = always_redraw(lambda: Arrow(start=(1,0,0),end=((1+test_tracker.get_value()*2),0,0)))
        

        self.play(Create(system),Write(acc_label),Write(disp_label))
        self.play(Create(F_restoring))
        T = system.get_time_period()
        self.play(system.tracker.animate.set_value(2*T),test_tracker.animate.set_value(PI),run_time=T,rate_func=linear)
