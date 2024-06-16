from geometry import RectanglesBasedGeometry, RectanglesBasedGeometries
from stiffeners import FlatBar, Angle, Bulb, Tee
from materials import Steel
from platings import FlatPlate

class GeneralFlatPanel(RectanglesBasedGeometries):
    def __init__(self, plating, stiffeners):
        self.plating = plating
        self.stiffeners = stiffeners
        self._geometries = []
        self._create_geometries()
        super().__init__(self._geometries)

    def _create_flatbar(self, input_params, position, angle):
        return FlatBar(web_length=input_params['web_length'], 
                       thickness=input_params['thickness'],
                       position=position,
                       angle=angle,
                       material=input_params['material'])

    def _create_angle(self, input_params, position, angle):
        return Angle(web_length=input_params['web_length'],
                     web_thickness=input_params['web_thickness'],
                     flange_length=input_params['flange_length'],
                     flange_thickness=input_params['flange_thickness'],
                     position=position,
                     angle=angle,
                     material=input_params['material'])

    def _create_bulb(self, input_params, position, angle ):
        return Bulb(length=input_params['length'],
                    thickness=input_params['thickness'],
                    position=position,
                    angle=angle,
                    material=input_params['material'])

    def _create_tee(self, input_params, position, angle):
        return Tee(web_length=input_params['web_length'],
                   web_thickness=input_params['web_thickness'],
                   flange_length=input_params['flange_length'],
                   flange_thickness=input_params['flange_thickness'],
                   position=position,
                   angle=angle,
                   material=input_params['material'])

    def _create_geometries(self):
        self._geometries.append(self.plating)
        
        for stiffener in self.stiffeners:
            stiffener_type = stiffener['type']
            dist = stiffener['dist']
            rel_angle = stiffener['angle']
            input_params = stiffener['params']

            position = dist*self.plating.unit_direction + 0.5*self.plating.thickness*self.plating.unit_normal
            angle = self.plating.angle + rel_angle

            if stiffener_type == 'FlatBar':
                new_stiffener = self._create_flatbar(input_params, position, angle)
                
            elif stiffener_type == 'Angle':
                new_stiffener = self._create_angle(input_params, position, angle)
                
            elif stiffener_type == 'Bulb':
                new_stiffener = self._create_bulb(input_params, position, angle)
                
            elif stiffener_type == 'Tee':
                new_stiffener = self._create_tee(input_params, position, angle)
            else:
                raise ValueError(f"Unknown stiffener type: {stiffener_type}")
            
            self._geometries.append(new_stiffener)



if __name__ == '__main__':
    def test0():
        material = Steel(name='steel_A131',properties=dict(yield_strength=235e6, poisson_ratio=0.3, young_modulus=2.1e11))
       
        plating = FlatPlate(length=1, thickness=10/1000, position=[0,0], angle=0, material=material)
       
        stiffener = dict(type='FlatBar', dist=0.1, angle=90, params=dict(web_length=100/1000,
                                                                        thickness=10/1000,
                                                                        material=material))
        stiffener2 = dict(type='Angle', dist=0.3, angle=90,
                          params=dict(web_length=100/1000, web_thickness=10/1000,
                                      flange_length=50/1000, flange_thickness=10/1000,
                                      material=material))
        
        stiffener3 = dict(type='Bulb', dist=0.5, angle=90,
                          params=dict(length=100/1000, thickness=10/1000, material=material))
        
        stiffener4 = dict(type='Tee', dist=0.7, angle=90,
                          params=dict(web_length=100/1000, web_thickness=10/1000,
                                      flange_length=50/1000, flange_thickness=10/1000,
                                      material=material))
        
        panel = GeneralFlatPanel(plating=plating,
                                 stiffeners=[stiffener, stiffener2, stiffener3, stiffener4])
        
        panel.plot()

    
    test0()