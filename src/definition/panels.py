from geometry import RectanglesBasedGeometries
from stiffeners import FlatBar, Angle, Bulb, Tee
from materials import Steel
from platings import FlatPlate
import copy

class StiffenedPanel(RectanglesBasedGeometries):
    def __init__(self, name=None) -> None:
        self.name = name
        self._plating = None
        self._stiffeners = dict()
        self._stiffeners_counter = 0

    @property
    def plating(self):
        return self._plating

    @property
    def stiffeners(self):
        return self._stiffeners
    
    @property
    def num_stiffeners(self):
        return len(self._stiffeners)

    def _create(self):
        components = []
        components.append(self._plating)
        for _,stiffener in self._stiffeners.items():
            components.append(stiffener)
        super().__init__(components)

    def set_plating(self, plate):
        self._plating = plate
        self._create()

    def add_stiffener(self, relative_position, relative_angle, stiffener, id=None):
        stiffener.position = self._plating.position + relative_position*self._plating.unit_direction + 0.5*self._plating.thickness*self._plating.unit_normal
        stiffener.angle = self._plating.angle + relative_angle
        if id is not None:
            self._stiffeners[id] = stiffener
        else:
            self._stiffeners_counter += 1
            self._stiffeners[self._stiffeners_counter] = stiffener            
        self._create()

    def remove_stiffener(self, id):
        del self._stiffeners[id]
        self._create()

    def get_stiffener(self, id):
        return self._stiffeners[id]

    def add_stiffeners_group(self, relative_position, relative_angle, spacing, stiffener, count):
        for i in range(count):
            stiffener_i = copy.deepcopy(stiffener)
            relative_pos_i = relative_position + spacing*i
            self.add_stiffener(relative_pos_i, relative_angle, stiffener_i)
            
    def reverse_stiffeners_orientation(self):
        for _,stiffener in self._stiffeners.items():
            disp = -1*stiffener.web.unit_direction*self._plating.thickness
            stiffener.move(disp)
            stiffener.angle += 180
        self._create()
        
    def __str__(self) -> str:
        msg = f'Stiffened panel "{self.name}":\n'
        msg += f' Plate: {self._plating}\n'
        for i, stiffener in self._stiffeners.items():
            msg += f' Stiffener {i}: {stiffener}\n'
        return msg
    
    def set_stiffeners_angle(self, new_angle):
        for _, stiffener in self._stiffeners.items():
            stiffener.angle = new_angle
        self._create()

    def update(self):
        self._create()

if __name__ == '__main__':
    def test0():
        panel = StiffenedPanel()
        
        steel = Steel(name='steel_A131',properties=dict(yield_strength=235e6,
                                                            poisson_ratio=0.3,
                                                            young_modulus=2.1e11))
        
        plate = FlatPlate.from_endpoints(initial_point=[0,0], final_point=[100, 0], thickness=10, material=steel)
        panel.set_plating(plate=plate)

        stiffener1 = FlatBar(web_length=100, thickness=10, material=steel)
        panel.add_stiffener(relative_position=0, relative_angle=90, stiffener=stiffener1)

        print(panel)
        print(panel.section_properties)
        panel.plot()

    def test1():
        panel = StiffenedPanel()
        
        steel = Steel(name='steel_A131',properties=dict(yield_strength=235e6,
                                                            poisson_ratio=0.3,
                                                            young_modulus=2.1e11))
        
        plate = FlatPlate.from_endpoints(initial_point=[0,0], final_point=[2000, 0], thickness=10, material=steel)
        panel.set_plating(plate=plate)

        stiffener1 = FlatBar(web_length=300, thickness=10, material=steel)
        stiffener2 = Bulb(length=100, thickness=6.35, material=steel)
        stiffener3 = Tee(web_length=150, web_thickness=8, flange_length=75, flange_thickness=7, material=steel)
        
        panel.add_stiffener(relative_position=0, relative_angle=90, stiffener=stiffener1)
        panel.add_stiffeners_group(relative_position=150, relative_angle=90, spacing=300, stiffener=stiffener2, count=5)
        panel.add_stiffener(relative_position=1500, relative_angle=90, stiffener=stiffener3)
        
        print(panel)
        print(panel.section_properties)
        panel.plot()

    def test2():
        panel = StiffenedPanel(name='bottom_panel')
        
        steel = Steel(name='steel_A131',properties=dict(yield_strength=235e6,
                                                            poisson_ratio=0.3,
                                                            young_modulus=2.1e11))
        
        plate = FlatPlate.from_endpoints(initial_point=[0,0], final_point=[2000, 0], thickness=10, material=steel)
        panel.set_plating(plate=plate)

        stiffener1 = FlatBar(web_length=300, thickness=10, material=steel)
        stiffener2 = Bulb(length=100, thickness=6.35, material=steel)
        stiffener3 = Tee(web_length=150, web_thickness=8, flange_length=75, flange_thickness=7, material=steel)
        
        panel.add_stiffener(relative_position=0, relative_angle=90, stiffener=stiffener1)
        panel.add_stiffeners_group(relative_position=150, relative_angle=90, spacing=300, stiffener=stiffener2, count=5)
        panel.add_stiffener(relative_position=1500, relative_angle=90, stiffener=stiffener3)
        
        print(panel)
        print(panel.section_properties)
        panel.plot()
        panel.remove_stiffener(id=7)
        print(panel)
        print(panel.section_properties)
        panel.plot()

        panel.reverse_stiffeners_orientation()
        print(panel)
        print(panel.section_properties)
        panel.plot()

        panel.get_stiffener(id=3).flip_flange()
        print(panel)
        print(panel.section_properties)
        panel.plot()


        
    test2()
        

        


    







