import numpy as np
from geometry import Rectangle
from materials import Steel

class FlatPlate(Rectangle):
    def __init__(self, length, thickness, position, angle, material) -> None:
        super().__init__(length, thickness, position, angle)
        self.thickness = thickness
        self.material = material
    
    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(length={self.width}, thickness={self.height}, position={self.position}, angle={self.angle}, material={self.material})"

    def __str__(self):
        return f"PL {self.height}, {self.material.name}, at {self.position} with orientation {self.angle} degrees"
    
    @classmethod
    def from_endpoints(cls, initial_point, final_point, thickness, material):
        position = initial_point
        dif = final_point - initial_point
        length = np.linalg.norm(dif)
        unit_dir = dif/length
        angle = np.degrees(np.arccos(unit_dir[0]))
        return cls(length, thickness, position, angle, material)

if __name__ == '__main__':

    def test1():
        material = Steel(name='steel_A131',properties=dict(yield_strength=235e6,
                                                            poisson_ratio=0.3,
                                                            young_modulus=2.1e11))
        plate = FlatPlate(length=1000, thickness=6.35, position=[0,0], angle=0.0, material=material)
        print(plate)
        print(repr(plate))
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

    test2()