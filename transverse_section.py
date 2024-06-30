from geometry import RectanglesBasedGeometries
from panels import StiffenedPanel
from platings import FlatPlate
from materials import Steel
from stiffeners import Bulb, Angle, Tee
from copy import deepcopy

class TransverseSection(RectanglesBasedGeometries):
    def __init__(self, name=None) -> None:
        self.name = name
        self._stiffened_panels = dict()
        self._stiffened_panels_counter = 0
    
    @property
    def stiffened_panels(self):
        return self._stiffened_panels

    @property
    def num_stiffened_panels(self):
        return len(self._stiffened_panels)

    def _create(self):
        components = []
        for _, panel in self._stiffened_panels.items():
            components.append(panel.plating)
            for _, stiffener in panel.stiffeners.items():
                components.append(stiffener)
        super().__init__(components)
    
    def update(self):
        self._create()

    def add_stiffened_panel(self, panel, id=None):
        if id is not None:
            self._stiffened_panels[id] = panel
        else:
            self._stiffened_panels_counter += 1
            self._stiffened_panels[self._stiffened_panels_counter] = panel
        self._create()

    def remove_stiffened_panel(self, id):
        del self._stiffened_panels[id]
        self._create()

    def get_stiffened_panel(self, id):
        return self._stiffened_panels[id]

    def __str__(self) -> str:
        msg = f'Transverse section "{self.name}":\n'
        for panel in self._stiffened_panels:
            msg += panel._str__()
    
    def print_stiffened_panels(self):
        for _, panel in self._stiffened_panels.items():
            print(panel)
        
if __name__ == '__main__':
    def test0():
        
        # geometry
        points = dict()
        points['a'] = [0, 8750]
        points['b'] = [-6470, 8750]
        points['c'] = [0, 6000]
        points['d'] = [-7000, 6000]
        points['e'] = [-3284, 3250]
        points['f'] = [-6648, 3250]  
        points['g'] = [-6144.19, 2382.54]
        points['h'] = [-5697.53, 1769.34]
        points['i'] = [-4876.26, 1211.99]
        points['j'] = [-3000, 1250]
        points['k'] = [-2000, 1250]
        points['l'] = [-2000, 1005.28]
        points['m'] = [-1000, 1005.28]
        points['n'] = [-1000, 1250]
        points['o'] = [0, 1250]
        points['p'] = [-400, 0]
        points['q'] = [0, 0]
        points['r'] = [-3000, 704.5]
        points['s'] = [-2000, 434.2]
        points['t'] = [-1000, 162.6]

        # platings
        steel = Steel(name='A131', properties=None)
        plates = dict()    
        plates[0] = FlatPlate.from_endpoints(initial_point=points['a'], final_point=points['b'], thickness=10, material=steel)
        plates[1] = FlatPlate.from_endpoints(initial_point=points['c'], final_point=points['d'], thickness=10, material=steel)
        plates[2] = FlatPlate.from_endpoints(initial_point=points['e'], final_point=points['f'], thickness=8, material=steel)
        plates[3] = FlatPlate.from_endpoints(initial_point=points['b'], final_point=points['d'], thickness=10, material=steel)
        plates[4] = FlatPlate.from_endpoints(initial_point=points['d'], final_point=points['f'], thickness=8, material=steel)
        plates[5] = FlatPlate.from_endpoints(initial_point=points['f'], final_point=points['g'], thickness=9, material=steel)
        plates[6] = FlatPlate.from_endpoints(initial_point=points['g'], final_point=points['h'], thickness=9, material=steel)
        plates[7] = FlatPlate.from_endpoints(initial_point=points['h'], final_point=points['i'], thickness=9, material=steel)
        plates[8] = FlatPlate.from_endpoints(initial_point=points['i'], final_point=points['p'], thickness=10, material=steel)
        plates[9] = FlatPlate.from_endpoints(initial_point=points['p'], final_point=points['q'], thickness=25, material=steel)
        plates[10] = FlatPlate.from_endpoints(initial_point=points['j'], final_point=points['k'], thickness=20, material=steel)
        plates[11] = FlatPlate.from_endpoints(initial_point=points['l'], final_point=points['m'], thickness=20, material=steel)
        plates[12] = FlatPlate.from_endpoints(initial_point=points['n'], final_point=points['o'], thickness=20, material=steel)
        plates[13] = FlatPlate.from_endpoints(initial_point=points['j'], final_point=points['r'], thickness=20, material=steel)
        plates[14] = FlatPlate.from_endpoints(initial_point=points['k'], final_point=points['s'], thickness=20, material=steel)
        plates[15] = FlatPlate.from_endpoints(initial_point=points['n'], final_point=points['t'], thickness=20, material=steel)
        plates[16] = FlatPlate.from_endpoints(initial_point=points['o'], final_point=points['q'], thickness=13, material=steel)

        panels = dict()
        transverse_section = TransverseSection()
        for k in range(len(plates)):
            panels[k] = StiffenedPanel()
            panels[k].set_plating(plates[k])
            transverse_section.add_stiffened_panel(panels[k], id=k)

        # stiffeners 
        hp80x6 = Bulb(length=80, thickness=6, material=steel)
        hp100x6 = Bulb(length=100, thickness=6, material=steel)
        hp120x7 = Bulb(length=120, thickness=7, material=steel)
        hp140x7 = Bulb(length=140, thickness=7, material=steel)
        hp160x7 = Bulb(length=160, thickness=7, material=steel)
        L450x80x8 = Angle(web_length=450, web_thickness=8, flange_length=80, flange_thickness=8, material=steel)
        T450x8_150x12 = Tee(web_length=450, web_thickness=8, flange_length=150, flange_thickness=12, material=steel)
        T350x10_150x15 = Tee(web_length=350, web_thickness=10, flange_length=150, flange_thickness=15, material=steel)

        # attaching stiffeners to the platings
        panels[0].name = 'deck1'
        panels[0].add_stiffener(relative_position=500, relative_angle=90, stiffener=deepcopy(L450x80x8))
        panels[0].add_stiffener(relative_position=2000, relative_angle=90, stiffener=deepcopy(T450x8_150x12))
        panels[0].add_stiffeners_group(relative_position=1000, relative_angle=90, spacing=500, stiffener=deepcopy(hp80x6), count=2)
        panels[0].add_stiffeners_group(relative_position=2500, relative_angle=90, spacing=500, stiffener=deepcopy(hp80x6), count=8)

        panels[1].name = 'deck2'
        panels[1].add_stiffener(relative_position=2000, relative_angle=90, stiffener=deepcopy(T450x8_150x12))
        panels[1].add_stiffeners_group(relative_position=500, relative_angle=90, spacing=500, stiffener=deepcopy(hp80x6), count=3)
        panels[1].add_stiffeners_group(relative_position=2500, relative_angle=90, spacing=500, stiffener=deepcopy(hp80x6), count=9)

        panels[2].name = 'deck3'
        panels[2].add_stiffener(relative_position=1000, relative_angle=90, stiffener=deepcopy(T350x10_150x15))
        panels[2].add_stiffeners_group(relative_position=0, relative_angle=90, spacing=250, stiffener=deepcopy(hp80x6), count=2)
        panels[2].add_stiffeners_group(relative_position=1500, relative_angle=90, spacing=500, stiffener=deepcopy(hp80x6), count=4)

        panels[3].name = 'upper side shell'
        panels[3].add_stiffeners_group(relative_position=500, relative_angle=90, spacing=500, stiffener=deepcopy(hp80x6), count=5)

        panels[4].name = 'mid side shell'
        panels[4].add_stiffeners_group(relative_position=500, relative_angle=90, spacing=500, stiffener=deepcopy(hp120x7), count=5)

        panels[5].name = 'upper bilge'
        panels[5].add_stiffeners_group(relative_position=500, relative_angle=90, spacing=500, stiffener=deepcopy(hp140x7), count=2)

        panels[6].name = 'mid bilge'
        panels[6].add_stiffeners_group(relative_position=760/3.0, relative_angle=90, spacing=500, stiffener=deepcopy(hp140x7), count=2)

        panels[7].name = 'lower bilge'
        panels[7].add_stiffeners_group(relative_position=500, relative_angle=90, spacing=500, stiffener=deepcopy(hp140x7), count=2)

        panels[8].name = 'bottom'
        panels[8].add_stiffeners_group(relative_position=500, relative_angle=90, spacing=500, stiffener=deepcopy(hp160x7), count=3)
        panels[8].set_stiffeners_angle(new_angle=90)
        panels[8].add_stiffeners_group(relative_position=2500, relative_angle=90, spacing=1000, stiffener=deepcopy(hp100x6), count=3)
        panels[8].set_stiffeners_angle(new_angle=90)

        panels[10].name = 'engine seating'
        panels[10].add_stiffeners_group(relative_position=500, relative_angle=270, spacing=500, stiffener=deepcopy(hp120x7), count=1)

        panels[11].name = 'lower engine seating'
        panels[11].add_stiffeners_group(relative_position=500, relative_angle=270, spacing=500, stiffener=deepcopy(hp120x7), count=1)

        panels[12].name = 'engine seating'
        panels[12].add_stiffeners_group(relative_position=500, relative_angle=270, spacing=500, stiffener=deepcopy(hp120x7), count=1)


        transverse_section.update()
        transverse_section.print_stiffened_panels()
        transverse_section.plot()
        print(transverse_section.section_properties)

        return transverse_section

    def test1():
        transverse_section = test0()
        transverse_section.get_stiffened_panel(id=0).get_stiffener(id=1).web_length = 900
        transverse_section.get_stiffened_panel(id=0).update()
        transverse_section.update()
        transverse_section.print_stiffened_panels()
        transverse_section.plot()
        print(transverse_section.section_properties)

    def test2():
        transverse_section = test0()
        transverse_section.get_stiffened_panel(id=0).get_stiffener(id=2).web_length = 500
        transverse_section.get_stiffened_panel(id=0).update()
        transverse_section.update()
        transverse_section.print_stiffened_panels()
        transverse_section.plot()
        print(transverse_section.section_properties)

    test0()
