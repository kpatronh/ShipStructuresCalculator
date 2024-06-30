import numpy as np
from geometry import Rectangle, RectanglesBasedGeometry
from materials import Steel


class FlatBar(RectanglesBasedGeometry):
    def __init__(self, web_length, thickness, material, position=[0,0], angle=90):
        self._web_length = web_length
        self._thickness = thickness
        self._material = material
        self._position = position
        self._angle = angle 
        self._web = None
        self._create()

    def _create(self):
        self._web = Rectangle(width=self._web_length, height=self._thickness, position=self._position, angle=self._angle)
        super().__init__([self._web])

    @property
    def web_length(self):
        return self._web_length
    
    @web_length.setter
    def web_length(self, new_web_length):
        self._web_length = new_web_length
        self._create()

    @property
    def thickness(self):
        return self._thickness
    
    @thickness.setter
    def thickness(self, new_thickness):
        self._thickness = new_thickness
        self._create()

    @property
    def material(self):
        return self._material
    
    @material.setter
    def material(self, new_material):
        self._material = new_material
        self._create()
        
    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self, new_position):
        self._position = new_position
        self._create()

    @property
    def angle(self):
        return self._angle
    
    @angle.setter
    def angle(self, new_angle):
        self._angle = new_angle
        self._create()

    @property
    def web(self):
        return self._web

    def move(self, displacement):
        super().move(displacement)
        self._position = self._web.position
        
    def rotate(self, rotation_point, angle):
        super().rotate(rotation_point, angle)
        self._angle = self._web.angle
        self._position = self._web.position

    def __str__(self):
        if self._angle >= 360:
            self._angle = self._angle - 360
        return f"FB {self.web_length}x{self.thickness}, {self.material.name}, at {self.position} with orientation {self.angle} degrees"


class Angle(RectanglesBasedGeometry):
    def __init__(self, web_length, web_thickness, flange_length, flange_thickness, material, position=[0,0], angle=90):
        self._web_length = web_length
        self._web_thickness = web_thickness
        self._flange_length = flange_length
        self._flange_thickness = flange_thickness
        self._position = position
        self._angle = angle
        self._material = material

        self._web = None
        self._flange = None
        self._create()

    def _create(self):
        self._web = Rectangle(width=self._web_length, height=self._web_thickness, position=self._position, angle=self._angle)
        flange_position = self._position + 0.5*self._web.height*self._web.unit_normal + (self._web.width + 0.5*self._flange_thickness)*self._web.unit_direction
        flange_angle = self._web.angle - 90
        self._flange = Rectangle(width=self._flange_length, height=self._flange_thickness, position=flange_position, angle=flange_angle)
        super().__init__([self._web, self._flange])
    
    @property
    def web_length(self):
        return self._web_length

    @web_length.setter
    def web_length(self, new_web_length):
        self._web_length = new_web_length
        self._create()

    @property
    def web_thickness(self):
        return self._web_thickness

    @web_thickness.setter
    def web_thickness(self, web_thickness):
        self._web_thickness = web_thickness
        self._create()

    @property
    def flange_length(self):
        return self._flange_length

    @flange_length.setter
    def flange_length(self, new_flange_length):
        self._flange_length = new_flange_length
        self._create()

    @property
    def flange_thickness(self):
        return self._flange_thickness

    @flange_thickness.setter
    def flange_thickness(self, flange_thickness):
        self._flange_thickness = flange_thickness
        self._create()

    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self, new_position):
        self._position = new_position
        self._create()

    @property
    def angle(self):
        return self._angle
    
    @angle.setter
    def angle(self, new_angle):
        self._angle = new_angle
        self._create()

    @property
    def material(self):
        return self._material
    
    @material.setter
    def material(self, new_material):
        self._material = new_material
        self._create()

    @property
    def web(self):
        return self._web
    
    @property
    def flange(self):
        return self._flange

    def move(self, displacement):
        super().move(displacement)
        self._position = self._web.position
        
    def rotate(self, rotation_point, angle):
        super().rotate(rotation_point, angle)
        self._angle = self._web.angle
        self._position = self._web.position
        
    def flip_flange(self):
        rotation_point = self._web.position + (0.5*self._flange.height + self._web.width)*self._web.unit_direction
        self._flange.rotate(rotation_point=rotation_point, angle=180)

    def reverse_orientation(self):
        super().rotate(self._position, 180)
        self._angle = self._web.angle
        
    def __str__(self):
        num_digits = 2
        web_length = round(self._web_length, num_digits)
        web_thickness = round(self._web_thickness, num_digits)
        flange_length = round(self._flange_length, num_digits)
        flange_thickness = round(self._flange_thickness, num_digits)
        if self._angle >= 360:
            self._angle = self._angle - 360
        return f"L{web_length}x{web_thickness}+{flange_length}x{flange_thickness}, {self.material.name}, at {self.position} with orientation {self.angle} degrees"


class Bulb(Angle):
    """
    Class used to represent bulb profiles
    Idealisation of bulb profiles as per: DNVGL(2015) Rules for classification of ships, Part 3 Hull, Ch.3 Structural Design Principles,
                                          Sect. 7, 1.4.1 Stiffener profile with a bulb section 
    Reference: https://amarineblog.com/wp-content/uploads/2017/07/dnvgl-structure-detail-guide.pdf
    """
    def __init__(self, length, thickness, material, position=[0,0], angle=90) -> None:
        # dimensions to be entered in mm
        self._length = length
        self._thickness = thickness
        self._position = position
        self._angle = angle
        self._material = material
        self._create_equivalent_angle()

    def _create_equivalent_angle(self):
        web_length, web_thickness, flange_length, flange_thickness = self._get_equivalent_angle_dimensions()
        super().__init__(web_length, web_thickness, flange_length, flange_thickness, self._material, self._position, self._angle)

    def _get_equivalent_angle_dimensions(self):
        if self._length <= 120:
            alpha = 1.1 + ((120 - self._length)**2)/3000
        else:
            alpha = 1.0
        web_length = self._length - (self._length/9.2) + 2
        web_thickness = self._thickness
        flange_length = alpha * (self._thickness + (self._length/6.7) - 2)
        flange_thickness = (self._length/9.2) - 2
        return web_length, web_thickness, flange_length, flange_thickness

    @property
    def length(self):
        return self._length
    
    @length.setter
    def length(self, new_length):
        self._length = new_length
        self._create_equivalent_angle()

    @property
    def thickness(self):
        return self._thickness
    
    @thickness.setter
    def thickness(self, new_thickness):
        self._thickness = new_thickness
        self._create_equivalent_angle()

    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self, new_position):
        self._position = new_position
        self._create_equivalent_angle()

    @property
    def angle(self):
        return self._angle
    
    @angle.setter
    def angle(self, new_angle):
        self._angle = new_angle
        self._create_equivalent_angle()

    @property
    def material(self):
        return self._material
    
    @material.setter
    def material(self, new_material):
        self._material = new_material
        self._create_equivalent_angle()

    def __str__(self):
        if self._angle >= 360:
            self._angle = self._angle - 360
        return f"HP{self._length}x{self._thickness}, {self.material.name}, at {self.position} with orientation {self.angle} degrees"
        

class Tee(RectanglesBasedGeometry):
    def __init__(self, web_length, web_thickness, flange_length, flange_thickness, material, position=[0,0], angle=90):
        self._web_length = web_length
        self._web_thickness = web_thickness
        self._flange_length = flange_length
        self._flange_thickness = flange_thickness
        self._position = position
        self._angle = angle
        self._material = material

        self._web = None
        self._flange = None
        self._create()

    def _create(self):
        self._web = Rectangle(width=self._web_length, height=self._web_thickness, position=self._position, angle=self._angle)
        flange_position = self._position + 0.5*self._flange_length*self._web.unit_normal + (self._web.width + 0.5*self._flange_thickness)*self._web.unit_direction
        flange_angle = self._web.angle - 90
        self._flange = Rectangle(width=self._flange_length, height=self._flange_thickness, position=flange_position, angle=flange_angle)
        super().__init__([self._web, self._flange])
    
    @property
    def web_length(self):
        return self._web_length

    @web_length.setter
    def web_length(self, new_web_length):
        self._web_length = new_web_length
        self._create()

    @property
    def web_thickness(self):
        return self._web_thickness

    @web_thickness.setter
    def web_thickness(self, web_thickness):
        self._web_thickness = web_thickness
        self._create()

    @property
    def flange_length(self):
        return self._flange_length

    @flange_length.setter
    def flange_length(self, new_flange_length):
        self._flange_length = new_flange_length
        self._create()

    @property
    def flange_thickness(self):
        return self._flange_thickness

    @flange_thickness.setter
    def flange_thickness(self, flange_thickness):
        self._flange_thickness = flange_thickness
        self._create()

    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self, new_position):
        self._position = new_position
        self._create()

    @property
    def angle(self):
        return self._angle
    
    @angle.setter
    def angle(self, new_angle):
        self._angle = new_angle
        self._create()

    @property
    def material(self):
        return self._material
    
    @material.setter
    def material(self, new_material):
        self._material = new_material
        self._create()

    @property
    def web(self):
        return self._web
    
    @property
    def flange(self):
        return self._flange

    def move(self, displacement):
        super().move(displacement)
        self._position = self._web.position
        
    def rotate(self, rotation_point, angle):
        super().rotate(rotation_point, angle)
        self._angle = self._web.angle
        self._position = self._web.position
        

    def reverse_orientation(self):
        super().rotate(self._position, 180)
        self._angle = self._web.angle
        
    def __str__(self):
        num_digits = 2
        web_length = round(self._web_length, num_digits)
        web_thickness = round(self._web_thickness, num_digits)
        flange_length = round(self._flange_length, num_digits)
        flange_thickness = round(self._flange_thickness, num_digits)
        if self._angle >= 360:
            self._angle = self._angle - 360
        return f"T{web_length}x{web_thickness}+{flange_length}x{flange_thickness}, {self.material.name}, at {self.position} with orientation {self.angle} degrees"


if __name__ == '__main__':

    def test1():
        material = Steel(name='steel_A131',properties=dict(yield_strength=235e6, poisson_ratio=0.3, young_modulus=2.1e11))
        stiffener = FlatBar(web_length=100, thickness=6.35, material=material)
        print(stiffener)
        print(stiffener.section_properties)
        stiffener.plot()
        
        stiffener.angle += 45
        stiffener.web_length = 200
        stiffener.move(displacement=[100,100])
        print(stiffener)
        print(stiffener.section_properties)
        stiffener.plot()      

        stiffener.move([-100,-100])
        stiffener.rotate(rotation_point=[0,0], angle=-45)
        stiffener.web_length = 100
        print(stiffener)
        print(stiffener.section_properties)  
        stiffener.plot()

        stiffener.rotate(rotation_point=[0,0], angle=180)
        print(stiffener)
        print(stiffener.section_properties)  
        stiffener.plot()
        
    def test2():
        material = Steel(name='steel_A131',properties=dict(yield_strength=235e6, poisson_ratio=0.3, young_modulus=2.1e11))
        stiffener = Angle(web_length=100, web_thickness=6.35, flange_length=50, flange_thickness=6.35,
                          position=[0., 0.], angle=90, material=material)
        print(stiffener)
        print(stiffener.section_properties)
        stiffener.plot()

        stiffener.web_length = 200
        stiffener.flange_length = 70
        print(stiffener)
        print(stiffener.section_properties)
        stiffener.plot()

        stiffener.flip_flange()
        print(stiffener)
        print(stiffener.section_properties)
        stiffener.plot()
    
        stiffener.reverse_orientation()
        print(stiffener)
        print(stiffener.section_properties)
        stiffener.plot()

        stiffener.rotate(rotation_point=[0,0], angle=45)
        print(stiffener)
        print(stiffener.section_properties)
        stiffener.plot()

        stiffener.move(displacement=[100,100])
        print(stiffener)
        print(stiffener.section_properties)
        stiffener.plot()

    def test3():
        material = Steel(name='steel_A131',properties=dict(yield_strength=235e6, poisson_ratio=0.3, young_modulus=2.1e11))
        stiffener = Bulb(length=100, thickness=6.0, position=[0,0], angle=90, material=material)
        print(stiffener)
        print(stiffener.section_properties)
        stiffener.plot()

        stiffener.length = 200
        stiffener.thickness = 8
        print(stiffener)
        print(stiffener.section_properties)
        stiffener.plot()

        stiffener.flip_flange()
        print(stiffener)
        print(stiffener.section_properties)
        stiffener.plot()
    
        stiffener.reverse_orientation()
        print(stiffener)
        print(stiffener.section_properties)
        stiffener.plot()

        stiffener.rotate(rotation_point=[0,0], angle=45)
        print(stiffener)
        print(stiffener.section_properties)
        stiffener.plot()

        stiffener.move(displacement=[100,100])
        print(stiffener)
        print(stiffener.section_properties)
        stiffener.plot()

    def test4():
        material = Steel(name='steel_A131',properties=dict(yield_strength=235e6, poisson_ratio=0.3, young_modulus=2.1e11))
        stiffener = Tee(web_length=100, web_thickness=6.35, flange_length=100, flange_thickness=6.35,
                          position=[0., 0.], angle=90, material=material)
        print(stiffener)
        print(stiffener.section_properties)
        stiffener.plot()

        stiffener.web_length = 200
        stiffener.flange_length = 70
        print(stiffener)
        print(stiffener.section_properties)
        stiffener.plot()
   
        stiffener.reverse_orientation()
        print(stiffener)
        print(stiffener.section_properties)
        stiffener.plot()

        stiffener.rotate(rotation_point=[0,0], angle=45)
        print(stiffener)
        print(stiffener.section_properties)
        stiffener.plot()

        stiffener.move(displacement=[100,100])
        print(stiffener)
        print(stiffener.section_properties)
        stiffener.plot()

    test1()