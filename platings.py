import numpy as np
from geometry import Rectangle, from_rad_to_deg, from_deg_to_rad
from materials import Steel

class FlatPlate(Rectangle):
    def __init__(self, length, thickness, position, angle, material) -> None:
        super().__init__(length, thickness, position, angle)
        self.material = material
    
    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(length={self.width}, thickness={self.height}, position={self.position}, angle={from_rad_to_deg(self.angle)}, material={self.material})"

    def __str__(self):
        return f"PL {self.height}, {self.material.name}, at {self.position} with orientation {from_rad_to_deg(self.angle)} degrees"
    

if __name__ == '__main__':

    def test1():
        material = Steel(name='steel_A131',properties=dict(yield_strength=235e6,
                                                            poisson_ratio=0.3,
                                                            young_modulus=2.1e11))
        plate = FlatPlate(length=1000, thickness=6.35, position=[0,0], angle=0.0, material=material)
        print(plate)
        print(repr(plate))
        plate.plot()
    
    test1()