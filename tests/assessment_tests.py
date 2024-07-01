import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from copy import deepcopy

from src.assessment.design_pressures import DesignPressures
from src.assessment.material import Material

from src.definition.platings import FlatPlate
from src.definition.stiffeners import FlatBar, Bulb, Angle, Tee
from src.definition.panels import StiffenedPanel

def test0():
    
    # Material
    steel_A131 = Material(name='A131', young=201e9, yield_stress=235, ultimate_stress=400)

    # Stiffeners
    hp80x6 = Bulb(length=80, thickness=6, material=steel_A131)
    L450x80x8 = Angle(web_length=450, web_thickness=8, flange_length=80, flange_thickness=8, material=steel_A131)
    T450x8_150x12 = Tee(web_length=450, web_thickness=8, flange_length=150, flange_thickness=12, material=steel_A131)
    
    # Stiffened panel
    panel = StiffenedPanel(name='deck1', type='Deck')
    panel.set_plating(FlatPlate.from_endpoints(initial_point=[0, 8750],
                                               final_point=[-6470, 8750],
                                               thickness=10,
                                               material=steel_A131))
    panel.add_stiffener(relative_position=500, relative_angle=90, stiffener=deepcopy(L450x80x8))
    panel.add_stiffener(relative_position=2000, relative_angle=90, stiffener=deepcopy(T450x8_150x12))
    panel.add_stiffeners_group(relative_position=1000, relative_angle=90, spacing=500, stiffener=deepcopy(hp80x6), count=2)
    panel.add_stiffeners_group(relative_position=2500, relative_angle=90, spacing=500, stiffener=deepcopy(hp80x6), count=8)
    panel.plot()
    

test0()