from manim.opengl import *#remove later
from manim import ArrowVectorField 
from manim.constants import DEGREES
from manim.constants import RIGHT,UP,OUT
import numpy as np
from manim import * #remove it later 
from manim.opengl import OpenGLSurface
from typing import cast
class ElectricField(ArrowVectorField):
    def __init__(self, field_func, **kwargs):    
        self.field_func = field_func
        super().__init__( field_func , **kwargs)

    def get_value_at(self,at):
        return self.field_func(at)
class MagneticField(ArrowVectorField):
    def __init__(self, field_func, **kwargs):    
        self.field_func = field_func
        super().__init__( field_func , **kwargs)

    def get_value_at(self,at):
        return self.field_func(at)

class dL_wire(Line):
    def __init__(self,dl = Line(start=(0,0,0),end=(1,0,0)),current=1,**kwargs):
        self.dl=dl
        self.current=current
        self.dl_vec = dl.end-dl.start

class MagneticFieldFromCurrentElement(ArrowVectorField):#let mu/4pi = 1
    def __init__(self, dL_wire , **kwargs):
        
        field_func =   (lambda pos: dL_wire.current*(np.cross(dL_wire.dl_vec,pos)/(np.linalg.norm(dL_wire.dl_vec)**3)))

        # field_func =   (lambda pos: current*(np.cross(dl_vec-dl.get_center(),pos)/(np.linalg.norm(dl_vec-dl.get_center())**3)))
        
        super().__init__(field_func, **kwargs)


# class MagneticFieldDueToSegments(VGroup):
#     def __init__(self, wires, **kwargs):
#         self.wires=wires
#         super().__init__()

#     def return_field(self):
#         field = MagneticFieldFromCurrentElement(dL_wire(current=0))
#         for wire in wires:
#             field+=MagneticFieldFromCurrentElement(dL_wire=wire)
#         return field

    
class PotentialField(OpenGLSurface): #assumes charges to be on xy plane. if thats not the case, then the z coordinates will be ignored
    def __init__(self,charge,**kwargs):
        from Charge import Charge
        charge=Charge()
        print(charge.q)
        func=np.zeros(3)
        super().__init__(func,**kwargs)

