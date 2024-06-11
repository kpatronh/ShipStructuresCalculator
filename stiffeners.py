import numpy as np
from geometry import Rectangle, RectanglesBasedGeometry
from materials import Steel

class FlatBar(Rectangle):
    def __init__(self, length, thickness, position, angle, material) -> None:
        super().__init__(length, thickness, position, angle)
        self.material = material
    
    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(length={self.width}, thickness={self.height}, position={self.position}, angle={round(self.angle*180/np.pi, 3)!r}, material={self.material})"

    def __str__(self):
        return f"FB {self.width}x{self.height}, {self.material.name}, at {self.position} with orientation {round(self.angle*180/np.pi, 3)} degrees"

class Angle(RectanglesBasedGeometry):
    def __init__(self, web_length, web_thickness, flange_length, flange_thickness, position, angle, material) -> None:

        self.web_length = web_length
        self.web_thickness = web_thickness
        self.flange_length = flange_length
        self.flange_thickness = flange_thickness
        self.position = position
        self.angle = angle
        self.material = material
        self._components = self._create_components()
        super().__init__(self._components)
        self._k = 1

    def _create_components(self):
        web = FlatBar(length=self.web_length, thickness=self.web_thickness, position=self.position, angle=self.angle, material=self.material)
        flange_position = self.position + 0.5*self.web_thickness*web.unit_normal + (0.5*self.flange_thickness + self.web_length)*web.unit_direction
        flange_angle = self.angle - 90
        flange = FlatBar(length=self.flange_length, thickness=self.flange_thickness, position=flange_position, angle=flange_angle, material=self.material)
        return [web, flange]

    def flip_flange(self):
        web = self._components[0]
        self._k = self._k * -1.0
        flange_position = self.position + self._k *0.5*self.web_thickness*web.unit_normal + (0.5*self.flange_thickness + self.web_length)*web.unit_direction
        flange_angle = self.angle - self._k*90
        flange = FlatBar(length=self.flange_length, thickness=self.flange_thickness, position=flange_position, angle=flange_angle, material=self.material)
        self._components = [web, flange]
        super().__init__(self._components)

    def __str__(self):
        return f"L{self.web_length}x{self.web_thickness}+{self.flange_length}x{self.flange_thickness}, {self.material.name}, at {self.position} with orientation {round(self.angle*180/np.pi, 3)} degrees"

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(web_length={self.web_length}, web_thickness={self.web_thickness}, flange_length={self.flange_length}, flange_thickness={self.flange_thickness}, position={self.position}, angle={round(self.angle*180/np.pi, 3)!r}, material={self.material})"

    

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
        print(repr(stiffener))
        stiffener.plot()

    def test2():
        material = Steel(name='steel_A131',properties=dict(yield_strength=235e6,
                                                            poisson_ratio=0.3,
                                                            young_modulus=2.1e11))
        stiffener = Angle(web_length=100, web_thickness=6.35, flange_length=50, flange_thickness=6.35,
                          position=0.0, angle=90, material=material)
        print(stiffener)
        print(repr(stiffener))
        """
        print('Properties:\n',stiffener.section_properties)
        stiffener.plot()
        stiffener.flip_flange()
        stiffener.plot()
        stiffener.flip_flange()
        stiffener.plot()
        """

    test2()