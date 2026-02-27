from manim import *
from manim.opengl import *
import math
import cmath
import numpy as np
import sympy
import matplotlib.cm as cm
from matplotlib.colors import hsv_to_rgb
from PIL import Image, ImageChops
config.background_color = BLACK
class scene(ThreeDScene):
    
    def Laplace_Transform(self):
        t,s = sympy.symbols('t s')
        f=sympy.sin(2*t)*sympy.exp(-t)
        L = sympy.laplace_transform(f,t,s)[0]
        in_S = sympy.lambdify(s,L,modules=['numpy'])
        return (in_S)
    
    def generate_texture(self):
        pixel_density = 200
        bounds = [-5,5]
        length = int((bounds[1]-bounds[0]) * pixel_density)
        u = np.linspace(bounds[0],bounds[1],length)
        v = np.linspace(bounds[0],bounds[1],length)
        U,V = np.meshgrid(u,v)
        Z = self.Laplace_Transform()(U+1j*V)
        arg = np.angle(Z)

        mod_Z = np.abs(Z)
        hue = (arg+np.pi ) / (2 * np.pi)
        # hue = (-hue) % 1.0
        value =  np.exp(-0.1 * mod_Z)
        saturation = np.ones_like(value)
        HSV = np.stack((hue, saturation, value), axis=-1)
        RGB = hsv_to_rgb(HSV)


        img = Image.fromarray((RGB * 255).astype(np.uint8))
        #some shit is wrong so i have to invert the image, then flip it about real axis to get the correct one. NEEDS VERIFICATION
        img = ImageChops.invert(img)#inverting color
        img = img.transpose(Image.FLIP_TOP_BOTTOM)#flipping it
        img.save('images/laplace_transform_texture.png')
        



    def construct(self):
        self.generate_texture()

        splane = ComplexPlane(
            x_range=[-5,5,1],
            y_range=[-5,5,1],
            x_axis_config={
                "color":"RED"
            },
            y_axis_config={
                "color":GREEN
            }).move_to((0,0,0)).add_coordinates()

        x_length=splane.x_axis.get_length()
        y_length=splane.y_axis.get_length()
        axes = ThreeDAxes(
            x_range=[-5,5,1,],
            x_length=x_length,
            y_length=y_length,
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

        self.set_camera_orientation(phi = 65*DEGREES,theta = 20*DEGREES)
        
        

        self.play(Create(axes),Create(splane),run_time=2)
        def func(u,v):
            try:
                z = np.abs(transformed_f(u+v*1j))
                return np.array([u,v,z]) 
            except ZeroDivisionError:
                print("POLE")
            
        transformed_f = self.Laplace_Transform()

        temp_surface = OpenGLSurface(lambda u,v: axes.c2p(*func(u,v)),u_range=[-5,5.0],v_range=[-5,5.0],opacity=0.69,color = GRAY,shadow=0.8)
        self.u=ValueTracker(6)
        self.v=ValueTracker(6)
        mesh =  OpenGLSurfaceMesh(temp_surface,resolution=[10,10])
        bigger_mesh = OpenGLSurfaceMesh(temp_surface,resolution=[20,20])

        file = "images/laplace_transform_texture.png"
        transformed_surface = OpenGLTexturedSurface(temp_surface,file)
        
        
        # self.play(Create(self.temp_surface),Create(mesh))

        # self.play(ReplacementTransform(self.temp_surface,transformed_surface),self.u.animate.set_value(21),self.v.animate.set_value(21), run_time=4)
        self.play(Create(temp_surface),Create(mesh), lag_ratio=1.25,run_time=3)
        
        self.play(Uncreate(temp_surface))
        self.play(Create(transformed_surface),Transform(mesh,bigger_mesh),lag_ratio=0.69,run_time=3)
        self.begin_ambient_camera_rotation(rate=0.35)
        self.wait(10)
        self.interactive_embed()
        