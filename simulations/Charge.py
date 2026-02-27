from manim.opengl import *
from manim import *
from manim.constants import ORIGIN
from manim.utils.color import RED,BLUE
# from manim import *
import numpy as np
from External_Fields import *

class Charge(OpenGLMobject):
    def __init__(self,Id=None, q: float = 1,pos: np.ndarray = ORIGIN,radius = 0.1,mass=1,initial_velocity:float=np.zeros(3),stationary:bool = False,freeze=False,unfreeze_after_freezing=False,**kwargs,):
        # self.external_electric_field = external_electric_field
        self.stationary = stationary #Do you want the charged to be fixed?
        self.freeze = freeze #Minor difference from stationary:This preserves the velocity of charge after calling unfreeze()
        self.unfreeze_after_freezing = unfreeze_after_freezing #Use only if you want to unfreeze/move the charge after freezing it first. No need to pass unfreeze=true if you just initialised the charge
        self.id = Id #Optional; used for debugging
        self.radius = radius
        self.mass = mass
        self.q = q
        self.initial_velocity = initial_velocity if (not stationary) else [0,0,0]
        self.velocity = self.initial_velocity
        self.pos = pos
        OpenGLMobject.__init__(self,**kwargs)
        self.acceleration = np.zeros(3)
        self.displacement=0
        self.temp_vel=np.zeros(3)
        #checking if its positive or negative so to assign a proper color to it. positive = red, negative = blue
        if q>0:
            color = RED
        else : 
            color = BLUE
        #Using openglsurface for the 'body' of the charge
        self.add(OpenGLSurface(lambda u,v: (self.radius*np.sin(v)*np.cos(u), self.radius*np.sin(v)*np.sin(u), self.radius*np.cos(v)), u_range=[0,np.pi],v_range=[0,2*np.pi], color = color).move_to(self.pos))
        
    #Kinematics implementation using Euler integration
    def charge_updater(charges,external_electric_field:ElectricField = ElectricField(x_range=[0,0],y_range=[0,0],field_func = lambda pos: 0*pos[0]*RIGHT),external_magnetic_field:MagneticField = MagneticField(x_range=[0,0],y_range=[0,0],field_func = lambda pos: np.zeros(3))):

        def update_charges(a_charge,dt):


            charge_array_length = len(charges)#ignore
            i=1#ignore

            pos_vec = np.zeros(3) #Initialising the position vector; the position vector is from the charge being updated to nth charge where n loops through arrays of all the charges passed in the updater
            a_charge.acceleration = np.zeros(3) #initialising acceleration of the charge being updated currently

            for other_charge in charges:
                
                #ALL these conditional statements are added to have more control in interactive mode. 
                if(other_charge is not a_charge):#the condition ensures 'other_charge' is the charge in the array of charges passed that is affecting the charge thats supposed to be updated. This is because a charge cannot interact with itself 
                    if(a_charge.stationary):#if charge is stationary, dont update it. This can also be used in interactive mode to stop a charge thats in motion. The same charge can be unfrozen when required
                        a_charge.acceleration=np.zeros(3)
                        a_charge.velocity = np.zeros(3)
                        a_charge.initial_velocity = np.zeros(3)
                        print("Stat")
                    else:
                        i+=1#ignore
                        pos_vec = (other_charge.get_center()-a_charge.get_center())
                        dist = np.linalg.norm(pos_vec)
                        a_charge.acceleration += (-pos_vec*a_charge.q * other_charge.q/(a_charge.mass * dist**3)) + (external_electric_field.get_value_at(a_charge.get_center())*a_charge.q)/a_charge.mass + np.cross(a_charge.velocity,external_magnetic_field.get_value_at(a_charge.get_center()))*a_charge.q/a_charge.mass

                        # if(i == charge_array_length ): #for debugging; ignore
                            # print("for", a_charge.id, other_charge.id,"pos_vec=",pos_vec)
                            # print("a_net",a_charge.acceleration)
            
            if(charge_array_length==1):
                if(a_charge.stationary):#if charge is stationary, dont update it. This can also be used in interactive mode to stop a charge thats in motion. The same charge can be unfrozen when required
                        a_charge.acceleration=np.zeros(3)
                        a_charge.velocity = np.zeros(3)
                        a_charge.initial_velocity = np.zeros(3)
                else:
                        a_charge.acceleration += (external_electric_field.get_value_at(a_charge.get_center())*a_charge.q)/a_charge.mass + np.cross(a_charge.velocity,external_magnetic_field.get_value_at(a_charge.get_center()))*a_charge.q/a_charge.mass
            

            if(a_charge.freeze):
                print("Frozen")
                pass #no kinematics applied and its acceleration,velocity is preserved 
            if(not a_charge.freeze or a_charge.unfreeze_after_freezing):

                a_charge.freeze = False 
                a_charge.unfreeze_after_freezing = False

                a_charge.velocity = a_charge.initial_velocity+a_charge.acceleration*dt
                a_charge.initial_velocity = a_charge.velocity
                a_charge.displacement = a_charge.velocity*dt
                a_charge.shift(a_charge.displacement)
        
        for charge in charges:#adding the updater function to each charge
            charge.add_updater(update_charges) 

