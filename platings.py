import numpy as np
from geometry import Rectangle, RectanglesBasedGeometry
from materials import Steel

class FlatPlate(RectanglesBasedGeometry):
    def __init__(self, length, thickness, position, angle, material):
        self._length = length
        self._thickness = thickness
        self._position = position
        self._angle = angle 
        self._material = material
        self._plate = None
        self._create()

    def _create(self):
        self._plate = Rectangle(width=self._length, height=self._thickness, position=self._position, angle=self._angle)
        super().__init__([self._plate])

    @property
    def length(self):
        return self._length
    
    @length.setter
    def length(self, new_length):
        self._length = new_length
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
    def plate(self):
        return self._plate

    def move(self, displacement):
        super().move(displacement)
        self._position = self._plate.position
        
    def rotate(self, rotation_point, angle):
        super().rotate(rotation_point, angle)
        self._angle = self._plate.angle
        self._position = self._plate.position

    def __str__(self):
        return f"PL{self.thickness} with {self.length} length, {self.material.name}, at {self.position} with orientation {self.angle} degrees"
    
    @classmethod
    def from_endpoints(cls, initial_point, final_point, thickness, material):
        position = np.array(initial_point)
        dif = np.array(final_point) - np.array(initial_point)
        length = np.linalg.norm(dif)
        unit_dir = dif/length
        
        x, y = unit_dir[0], unit_dir[1]
        if x > 0 and y >= 0:    # vector in first quadrant
            angle = np.degrees(np.arctan(y/x))
        elif x < 0 and y >= 0:  # vector in second quandrant
            angle = 180 - np.degrees(np.arctan(y/x))
        elif x < 0 and y <= 0:  # vector in third quandrant
            angle = 180 + np.degrees(np.arctan(y/x))
        else: # vector in fourth quadrant
            angle = 360 - np.degrees(np.arctan(y/x))
        if angle >= 360:
            angle = angle - 360
        
        return cls(length, thickness, position, angle, material)

    @property
    def unit_direction(self):
        return self._plate.unit_direction
    
    @property
    def unit_normal(self):
        return self._plate.unit_normal

if __name__ == '__main__':

    def test1():
        material = Steel(name='steel_A131',properties=dict(yield_strength=235e6,
                                                            poisson_ratio=0.3,
                                                            young_modulus=2.1e11))
        plate = FlatPlate(length=1000, thickness=6.35, position=[0,0], angle=0.0, material=material)
        print(plate)
        plate.plot()
    
    def test2():
        material = Steel(name='steel_A131',properties=dict(yield_strength=235e6,
                                                           poisson_ratio=0.3,
                                                           young_modulus=2.1e11))
        initial_point = np.array([0,0])
        final_point = np.array([1000,0])
        plate = FlatPlate.from_endpoints(initial_point, final_point, 6.35, material)
        print(plate)
        plate.plot()

        plate.rotate(rotation_point=[0,0], angle=45)
        print(plate)
        plate.plot()    

    def test3():
        material = Steel(name='steel_A131',properties=dict(yield_strength=235e6,
                                                           poisson_ratio=0.3,
                                                           young_modulus=2.1e11))
        initial_point = np.array([0,0])
        final_point = np.array([1000,0])
        plate = FlatPlate.from_endpoints(initial_point, final_point, 6.35, material)
        print(plate)
        plate.plot()

        plate.rotate(rotation_point=[0,0], angle=45)
        print(plate)
        plate.plot()  

        plate.length = 2000
        plate.thickness = 10
        plate.angle = 0
        print(plate)
        plate.plot()

    def test4():
        material = Steel(name='steel_A131',properties=dict(yield_strength=235e6,
                                                           poisson_ratio=0.3,
                                                           young_modulus=2.1e11))
        initial_point = np.array([-6470, 8750])
        final_point = np.array([-7000, 6000])
        plate = FlatPlate.from_endpoints(initial_point, final_point, 6.35, material)
        print(plate)
        plate.plot()
    test4()




