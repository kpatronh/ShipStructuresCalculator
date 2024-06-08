import numpy as np
from geometry import Rectangle
from materials import Steel

class FlatPlate(Rectangle):
    def __init__(self, length, thickness, position, angle, material) -> None:
        super().__init__(length, thickness, position, angle)
        self.material = material
    
    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(material={self.material}, \n\tlength={self.width}, thickness={self.height}, position={self.position!r}, angle(deg)={round(self.angle*180/np.pi, 3)!r})"

if __name__ == '__main__':

    def test1():
        material = Steel(name='steel_A131',properties=dict(yield_strength=235e6,
                                                            poisson_ratio=0.3,
                                                            young_modulus=2.1e11))
        plate = FlatPlate(length=1000, thickness=6.35, position=[0,0], angle=0.0, material=material)
        print(plate)
        print('Properties:\n',plate.section_properties)
    
    test1()