import numpy as np
from geometry import Rectangle, RectanglesBasedGeometry
from materials import Steel

class FlatBar():
    def __init__(self, web_length, thickness, position, angle, material) -> None:
        self.web_length = web_length
        self.thickness = thickness
        self.position = np.array(position)
        self.angle = angle
        self.material = material

    @property
    def geometry(self):
        return Rectangle(width=self.web_length, height=self.thickness, position=self.position, angle=self.angle)
       
    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(web_length={self.web_length}, thickness={self.thickness}, position={self.position}, angle={self.angle}, material={self.material})"

    def __str__(self):
        return f"FB {self.web_length}x{self.thickness}, {self.material.name}, at {self.position} with orientation {self.angle} degrees"
    
    def move(self, displacement):
        new_position = self.geometry.move(displacement)
        self.position = new_position
    
    def rotate(self, rotation_point, angle):
        new_position, new_angle = self.geometry.rotate(rotation_point, angle)
        self.position = new_position
        self.angle = new_angle

    def plot(self):
        self.geometry.plot()
        


class Angle():
    """Class used to represent stiffeners with angle cross section
    """
    def __init__(self, web_length, web_thickness, flange_length, flange_thickness, position, angle, material) -> None:
        
        self.web_length = web_length
        self.web_thickness = web_thickness
        self.flange_length = flange_length
        self.flange_thickness = flange_thickness

        self.position = np.array(position)
        self.angle = angle
        self.material = material

        self._web = None
        self._flange = None
    
    @property
    def web(self):
        return FlatBar(web_length=self.web_length, thickness=self.web_thickness, position=self.position, angle=self.angle, material=self.material)

    def _set_flange_particulars(self, flip=False):
        if not flip:
            flange_position = self.position + 0.5*self.web_thickness*self.web.geometry.unit_normal + (0.5*self.flange_thickness + self.web_length)*self.web.geometry.unit_direction
            flange_angle = self.angle - 90
        else:
            flange_position = self.position - 0.5*self.web_thickness*self.web.geometry.unit_normal + (0.5*self.flange_thickness + self.web_length)*self.web.geometry.unit_direction
            flange_angle = self.angle + 180
        return flange_position, flange_angle

    def flange(self, flip=False):
        flange_position, flange_angle = self._set_flange_particulars(flip)
        return FlatBar(web_length=self.flange_length, thickness=self.flange_thickness, position=flange_position, angle=flange_angle, material=self.material)

    def geometry(self, flipped_flange=False):
        flange = self.flange(flipped_flange)
        return RectanglesBasedGeometry([self.web.geometry, flange.geometry])
    

    """




    def _set_flange_particulars(self, flip=False):
        if not flip:
            flange_position = self.position + 0.5*self.web_thickness*self.web.geometry.unit_normal + (0.5*self.flange_thickness + self.web_length)*self.web.geometry.unit_direction
            flange_angle = self._angle - 90
        else:
            flange_position = self.position - 0.5*self.web_thickness*self.web.geometry.unit_normal + (0.5*self.flange_thickness + self.web_length)*self.web.geometry.unit_direction
            flange_angle = self._angle + 180
        return flange_position, flange_angle

    def flange(self, flip=False):
        flange_position, flange_angle = self._set_flange_particulars(flip)
        return FlatBar(web_length=self.flange_length, thickness=self.flange_thickness, position=flange_position, angle=flange_angle, material=self.material)

    def geometry(self, flipped_flange=False):
        return RectanglesBasedGeometry([self.web, self.flange(flipped_flange)])
    """
        
    def reverse_orientation(self):
        self.flip_flange()
        self.rotate(rotation_point=self._web.position, angle=180)
        self.angle += 180

    def __str__(self):
        return f"L{self.web_length}x{self.web_thickness}+{self.flange_length}x{self.flange_thickness}, {self.material.name}, at {self.position} with orientation {self.angle} degrees"

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(web_length={self.web_length}, web_thickness={self.web_thickness}, flange_length={self.flange_length}, flange_thickness={self.flange_thickness}, position={self.position}, angle={self.angle}, material={self.material})"

class Bulb(Angle):
    """
    Class used to represent bulb profiles
    Idealisation of bulb profiles as per: DNVGL(2015) Rules for classification of ships, Part 3 Hull, Ch.3 Structural Design Principles,
                                          Sect. 7, 1.4.1 Stiffener profile with a bulb section 
    Reference: https://amarineblog.com/wp-content/uploads/2017/07/dnvgl-structure-detail-guide.pdf
    """
    def __init__(self, length, thickness, position, angle, material) -> None:
        # dimensions of stiffeners are to be in mm
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
 
class Tee(RectanglesBasedGeometry):
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
        print(repr(stiffener))
        print(stiffener.geometry.section_properties)
        stiffener.geometry.plot()
        
        stiffener.web_length = 200
        stiffener.geometry.plot()

        stiffener.position = [100, 100]
        stiffener.geometry.plot()

        stiffener.angle = 45
        stiffener.geometry.plot()

        stiffener.angle += -45
        stiffener.geometry.plot()

        stiffener.move(displacement=[-100,-100])
        stiffener.rotate(rotation_point=[0,0], angle=90)
        print(stiffener)
        print(stiffener.geometry.section_properties)
        stiffener.geometry.plot()
        
        
    def test2():
        material = Steel(name='steel_A131',properties=dict(yield_strength=235e6, poisson_ratio=0.3, young_modulus=2.1e11))
        stiffener = Angle(web_length=100, web_thickness=6.35, flange_length=50, flange_thickness=6.35,
                          position=[0., 0.], angle=90, material=material)
        print(stiffener)
        print(stiffener.geometry().section_properties)
        stiffener.geometry().plot()

        stiffener.flange(flip=True)
        print(stiffener)
        print(stiffener.geometry().section_properties)
        stiffener.geometry().plot()
        
        """
        stiffener.reverse_orientation()
        print(stiffener)
        print(stiffener.section_properties)
        stiffener.plot()

        stiffener.web.length = 500
        print(stiffener)
        print(stiffener.section_properties)
        stiffener.plot()
        """
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

    test2()