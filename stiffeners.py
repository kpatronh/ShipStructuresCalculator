import numpy as np
from geometry import Rectangle, RectanglesBasedGeometry
from materials import Steel

"""
#opciones al usuario:
- cambiar parametros de entrada
- rotar refuerzo
- mover refuerzo
- cambiar orientacion de ala


utilizar parámetros privador
crear setter
métodos de transformación modifican
"""

class FlatBar(RectanglesBasedGeometry):
    def __init__(self, web_length, thickness, position, angle, material):
        self._web_length = web_length
        self._thickness = thickness
        self._position = position
        self._angle = angle 
        self._material = material
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

    def move(self, displacement):
        super().move(displacement)
        self._position = self._web.position
        
    def rotate(self, rotation_point, angle):
        super().rotate(rotation_point, angle)
        self._angle = self._web.angle
        self._position = self._web.position

    def __str__(self):
        return f"FB {self.web_length}x{self.thickness}, {self.material.name}, at {self.position} with orientation {self.angle} degrees"


class Angle(RectanglesBasedGeometry):
    def __init__(self, web_length, web_thickness, flange_length, flange_thickness, position, angle, material):
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
        






class FlatBar4(RectanglesBasedGeometry):
    def __init__(self, web_length, thickness, position, angle, material):
        self.web_length = web_length
        self.thickness = thickness
        self.position = position
        self.angle = angle
        self.material = material
    
    @property
    def web(self):
        return Rectangle(width=self.web_length, height=self.thickness, position=self.position, angle=self.angle)
    
        
        self._web = None
        self._build()
        
    def _build(self):
        self._web = Rectangle(width=self.web_length, height=self.thickness, position=self.position, angle=self.angle)
        super().__init__([self._web])
    
    def update(self):
        self._build()

    def reverse_orientation(self):
        self.rotate(rotation_point=self.position, angle=180)

class FlatBar3:
    def __init__(self, web_length, thickness, position, angle, material) -> None:
        self.web_length = web_length
        self.thickness = thickness
        self.position = position
        self.angle = angle
        self.material = material

        self._web = None
        self._build()

    def _build(self):
        self._web = Rectangle(width=self.web_length, height=self.thickness, position=self.position, angle=self.angle)
    
    def update(self):
        self._build()

    def rotate(self, rotation_point, angle):
        self.geometry.rotate(rotation_point, angle)

    def reverse_orientation(self):
        self.geometry.rotate(rotation_point=self.position, angle=180)

    @property
    def web(self):
        return self._web

    @property
    def geometry(self):
        return RectanglesBasedGeometry([self.web])
    
    def plot(self):
        return self.geometry.plot()
    
    @property
    def section_properties(self):
        return self.geometry.section_properties



    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(web_length={self.web_length}, thickness={self.thickness}, position={self.position}, angle={self.angle}, material={self.material})"

    def __str__(self):
        return f"FB {self.web_length}x{self.thickness}, {self.material.name}, at {self.position} with orientation {self.angle} degrees"

class Angle3:
    def __init__(self, web_length, web_thickness, flange_length, flange_thickness, position, angle, material) -> None:
        self.web_length = web_length
        self.web_thickness = web_thickness
        self.flange_length = flange_length
        self.flange_thickness = flange_thickness

        self.position = position
        self.angle = angle
        self.material = material

        self._flange = None
        self._web = None
        self._build()

    def _build(self):
        self._web = FlatBar(web_length=self.web_length, thickness=self.web_thickness, position=self.position, angle=self.angle, material=self.material)
        flange_position = self.position + 0.5*self.web_thickness*self.web.geometry.unit_normal + (0.5*self.flange_thickness + self.web_length)*self.web.geometry.unit_direction
        flange_angle = self.angle - 90
        self._flange = FlatBar(web_length=self.web_length, thickness=self.web_thickness, position=flange_position, angle=flange_angle, material=self.material)

    def update(self):
        self._build()
    
    def flip_flange(self):
        rotation_point = self.position + (0.5*self.flange_thickness + self.web_length)*self.web.geometry.unit_direction
        self._flange.geometry.rotate(rotation_point, 180)
    
    def reverse_orientation(self):
        self.geometry.rotate(rotation_point=self.position, angle=180)

    @property
    def web(self):
        return self._web
    
    @property
    def flange(self):
        return self._flange

    @property
    def geometry(self):
        return RectanglesBasedGeometry([self.web, self.flange])

class Bulb3(Angle):
    """
    Class used to represent bulb profiles
    Idealisation of bulb profiles as per: DNVGL(2015) Rules for classification of ships, Part 3 Hull, Ch.3 Structural Design Principles,
                                          Sect. 7, 1.4.1 Stiffener profile with a bulb section 
    Reference: https://amarineblog.com/wp-content/uploads/2017/07/dnvgl-structure-detail-guide.pdf
    """
    def __init__(self, length, thickness, position, angle, material) -> None:
        self.length = length
        self.thickness = thickness
        web_length, web_thickness, flange_length, flange_thickness = self._get_equivalent_angle_dimensions()
        super().__init__(web_length, web_thickness, flange_length, flange_thickness, position, angle, material)

    def _get_equivalent_angle_dimensions(self):
        if self.length <= 120:
            alpha = 1.1 + ((120 - self.length)**2)/3000
        else:
            alpha = 1.0
        web_length = self.length - (self.length/9.2) + 2
        web_thickness = self.thickness
        flange_length = alpha * (self.thickness + (self.length/6.7) - 2)
        flange_thickness = (self.length/9.2) - 2
        return web_length, web_thickness, flange_length, flange_thickness

    """
    def flange(self, right=True):
        if right:
            position = self.position + 0.5*self.web_thickness*self.web.geometry.unit_normal + (0.5*self.flange_thickness + self.web_length)*self.web.geometry.unit_direction
            angle = self.angle - 90
        else:
            position = self.position -0.5*self.web_thickness*self.web.geometry.unit_normal + (0.5*self.flange_thickness + self.web_length)*self.web.geometry.unit_direction
            angle = self.angle + 90
        return FlatBar(web_length=self.flange_length, thickness=self.flange_thickness, position=position, angle=angle, material=self.material)
    
    def geometry(self, flange_right=True):
        return RectanglesBasedGeometry([self.web, self.flange(flange_right)])
    
    """

class FlatBar2(Rectangle):
    def __init__(self, web_length, thickness, position, angle, material) -> None:
        self.web_length = web_length
        self.height = thickness
        self.thickness = thickness
        self.material = material
        super().__init__(web_length, thickness, position, angle)
        
    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(web_length={self.web_length}, thickness={self.thickness}, position={self.position}, angle={self.angle}, material={self.material})"

    def __str__(self):
        return f"FB {self.width}x{self.height}, {self.material.name}, at {self.position} with orientation {self.angle} degrees"

class Angle2(RectanglesBasedGeometry):
    """Class used to represent stiffeners with angle cross section
    """
    def __init__(self, web_length, web_thickness, flange_length, flange_thickness, position, angle, material) -> None:
        self.web_length = web_length
        self.web_thickness = web_thickness
        self.flange_length = flange_length
        self.flange_thickness = flange_thickness

        self.position = position
        self.angle = angle
        self.material = material

        self._web = FlatBar(web_length=self.web_length, thickness=self.web_thickness, position=position, angle=angle, material=self.material)
        flange_position = self.position + 0.5*self.web_thickness*self._web.unit_normal + (0.5*self.flange_thickness + self.web_length)*self._web.unit_direction
        flange_angle = angle - 90
        self._flange = FlatBar(web_length=self.flange_length, thickness=self.flange_thickness, position=flange_position, angle=flange_angle, material=self.material)
        self._components = [self._web, self._flange]
        super().__init__(self._components)
        self._flange_orientation = 1

    def flip_flange(self):
        self._flange_orientation = self._flange_orientation * -1.0
        flange_position = self.position + self._flange_orientation*0.5*self.web_thickness*self._web.unit_normal + (0.5*self.flange_thickness + self.web_length)*self._web.unit_direction
        flange_angle = self.angle - self._flange_orientation*90
        self._flange = FlatBar(web_length=self.flange_length, thickness=self.flange_thickness, position=flange_position, angle=flange_angle, material=self.material)
        self._components[1] = self._flange
        super().__init__(self._components)

    def reverse_orientation(self):
        self.flip_flange()
        self.rotate(rotation_point=self._web.position, angle=180)
        self.angle += 180

    def __str__(self):
        return f"L{self.web_length}x{self.web_thickness}+{self.flange_length}x{self.flange_thickness}, {self.material.name}, at {self.position} with orientation {self.angle} degrees"

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(web_length={self.web_length}, web_thickness={self.web_thickness}, flange_length={self.flange_length}, flange_thickness={self.flange_thickness}, position={self.position}, angle={self.angle}, material={self.material})"

class Bulb2(Angle):
    """
    Class used to represent bulb profiles
    Idealisation of bulb profiles as per: DNVGL(2015) Rules for classification of ships, Part 3 Hull, Ch.3 Structural Design Principles,
                                          Sect. 7, 1.4.1 Stiffener profile with a bulb section 
    Reference: https://amarineblog.com/wp-content/uploads/2017/07/dnvgl-structure-detail-guide.pdf
    """
    def __init__(self, length, thickness, position, angle, material) -> None:
        self.length = length
        self.thickness = thickness
        web_length, web_thickness, flange_length, flange_thickness = self._get_equivalent_angle_dimensions()
        super().__init__(web_length, web_thickness, flange_length, flange_thickness, position, angle, material)

    def _get_equivalent_angle_dimensions(self):
        if self.length <= 120:
            alpha = 1.1 + ((120 - self.length)**2)/3000
        else:
            alpha = 1.0
        web_length = self.length - (self.length/9.2) + 2
        web_thickness = self.thickness
        flange_length = alpha * (self.thickness + (self.length/6.7) - 2)
        flange_thickness = (self.length/9.2) - 2
        return web_length, web_thickness, flange_length, flange_thickness
 
class Tee2(RectanglesBasedGeometry):
    """
    Class used to represent stiffeners with tee cross section
    """
    def __init__(self, web_length, web_thickness, flange_length, flange_thickness, position, angle, material) -> None:
        self.web_length = web_length
        self.web_thickness = web_thickness
        self.flange_length = flange_length
        self.flange_thickness = flange_thickness

        self.position = position
        self.angle = angle
        self.material = material

        self._web = FlatBar(web_length=self.web_length, thickness=self.web_thickness, position=position, angle=angle, material=self.material)
        flange_position = self.position + 0.5*self.web_length*self._web.unit_normal + (0.5*self.flange_thickness + self.web_length)*self._web.unit_direction
        flange_angle = angle - 90
        self._flange = FlatBar(web_length=self.flange_length, thickness=self.flange_thickness, position=flange_position, angle=flange_angle, material=self.material)
        self._components = [self._web, self._flange]
        super().__init__(self._components)

    def reverse_orientation(self):
        self.rotate(rotation_point=self._web.position, angle=180)
        self.angle += 180


if __name__ == '__main__':

    def test1():
        material = Steel(name='steel_A131',properties=dict(yield_strength=235e6, poisson_ratio=0.3, young_modulus=2.1e11))
        stiffener = FlatBar(web_length=100, thickness=6.35, position=[0., 0.], angle=90, material=material)
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
        stiffener = Bulb(length=100, thickness=8.0, position=[0,0], angle=90, material=material)
        stiffener.plot()
        stiffener.reverse_orientation()
        stiffener.plot()

    def test4():
        material = Steel(name='steel_A131',properties=dict(yield_strength=235e6, poisson_ratio=0.3, young_modulus=2.1e11))
        stiffener = Tee(web_length=100, web_thickness=6.35, flange_length=100, flange_thickness=6.35,
                          position=[0., 0.], angle=90, material=material)
        stiffener.plot()
        stiffener.reverse_orientation()
        stiffener.plot()

    def test21():
        material = Steel(name='steel_A131',properties=dict(yield_strength=235e6, poisson_ratio=0.3, young_modulus=2.1e11))
        stiffener = Angle(web_length=100, web_thickness=6.35, flange_length=50, flange_thickness=6.35,
                          position=[0., 0.], angle=90, material=material)
        print(stiffener)
        print(stiffener.geometry.section_properties)
        stiffener.geometry.plot()

        stiffener.flip_flange()
        print(stiffener)
        print(stiffener.geometry.section_properties)
        stiffener.geometry.plot()
        
        # stiffener.reverse_orientation()
        # print(stiffener)
        # print(stiffener.section_properties)
        # stiffener.plot()
    
    test2()