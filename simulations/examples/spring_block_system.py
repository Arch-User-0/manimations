
from manim import *
import numpy as np
import math
from math import asin,sin
class Spring_Block(VMobject):
    def __init__(self,radius=1,spring_const=1,mass_of_object=1,Length=2,amplitude=1,dens=5,block = Rectangle(height=2,width=2),**kwargs):
        #dens isnt the 'mass' density, its the measure of how coiled the spring is
        super().__init__(**kwargs)
        self.radius=radius
        self.spring_const=spring_const
        self.mass_of_object=mass_of_object
        self.amplitude=amplitude
        self.Length=Length
        self.tracker=ValueTracker(0)
        self.dens = dens
        
        k=spring_const
        m=mass_of_object
        self.natural_freq= math.sqrt(k/m)

        self.spring = ParametricFunction(lambda t: (t,self.radius * math.asin(math.sin(dens * t / Length)),0), t_range=[0,Length])
        def oscillate(mob,dt):
            total_Length = self.Length + self.amplitude*math.sin(self.natural_freq * self.tracker.get_value())
            initial_left = mob.get_left()
            temp_func=ParametricFunction(lambda t: (t,
                self.radius*math.asin(math.sin(self.dens*t/(total_Length))),  
                0),
            t_range=(0,total_Length),color=mob.get_color())
            new_left=temp_func.get_left()

            SHIFT = initial_left-new_left

            temp_func.shift(SHIFT)
            # print("T: ",self.tracker.get_value(), "Displacement: ", self.get_displacement(), "Time period: ", self.get_time_period())
            mob.become(temp_func)


        self.add(self.spring)
        self.spring.add_updater(oscillate)

        self.block = always_redraw(lambda:block.next_to(self.spring.get_right(),buff=0))
        self.add(self.block)
    def get_time_period(self):
        return 2*PI/math.sqrt(self.spring_const/self.mass_of_object)
    def get_block_displacement(self):
        return (round(self.amplitude*math.sin(self.natural_freq*self.tracker.get_value()),2)) 
    def get_block_acceleration(self):
        return (-1*self.spring_const/self.mass_of_object)*self.get_block_displacement() # a = -(k/m)*displacement






class test(Scene):
    def construct(self):
        
        spr = Spring_Block(Length=6,mass_of_object=12,spring_const=PI*PI,amplitude=3,dens=10*PI,radius=0.3)
        txt = always_redraw(lambda:Text("Displacement: {spr.get_displacement()} A").scale(0.5).to_corner(UL))

        self.wait()
        T = spr.get_time_period()

        
        self.play(Create(spr.spring),Create(spr.block))
        self.play(spr.animate.to_edge(LEFT))

        block_info = always_redraw(lambda: Text("Mass: 144kg").move_to(spr.block.get_center()).scale(0.3))

        self.play(spr.spring.animate.set_color(RED), spr.block.animate.set_color(BLUE))
        # self.play(Write(txt),Write(block_info))


        self.play(spr.tracker.animate.set_value(100),run_time=5,rate_func=linear)
        self.wait()
    
    

