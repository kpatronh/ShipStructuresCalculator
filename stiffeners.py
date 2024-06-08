import numpy as np
from geometry import Rectangle, RectanglesBasedGeometry
from materials import Steel

class FlatBar(Rectangle):
    def __init__(self, length, thickness, position, angle, material) -> None:
        super().__init__(length, thickness, position, angle)
        self.material = material
    
    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(material={self.material}, \n\length={self.width}, thickness={self.height}, position={self.position!r}, angle(deg)={round(self.angle*180/np.pi, 3)!r})"


class Angle(RectanglesBasedGeometry):
    def __init__(self, web_length, web_thickness, flange_length, flange_thickness, position, angle, material) -> None:
        web = FlatBar(length=web_length, thickness=web_thickness,
                      position=position, angle=angle, material=material)
        
        flange = FlatBar(length=flange_length, thickness=flange_thickness,
                         position=[0,web_length + 0.5*flange_thickness], angle=0, material=material)
        rectangles = [web, flange]
        super().__init__(rectangles)



class Bulb:
    def __init__(self) -> None:
        pass


class Tee:
    def __init__(self) -> None:
        pass

class DBStiffener:
    def __init__(self) -> None:
        pass


if __name__ == '__main__':

    def test1():
        material = Steel(name='steel_A131',properties=dict(yield_strength=235e6,
                                                            poisson_ratio=0.3,
                                                            young_modulus=2.1e11))
        stiffener = FlatBar(length=100, thickness=6.35, position=[0,0], angle=90, material=material)
        print(stiffener)
        print('Properties:\n',stiffener.section_properties)
    
    test1()