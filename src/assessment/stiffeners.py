import numpy as np


class Stiffener:
    def __init__(self, name: str) -> None:
        self._name = name

class FlatBar(Stiffener):
    def __init__(self, name: str) -> None:
        super().__init__('FB'+name)
        split_name = name.split('x')
        self._height = float(split_name[0])
        self._web_thickness = float(split_name[1])
    
    def _compute_local_section_properties(self) -> np.ndarray:
        """
            height is in mm
            thickness is in mm

            section_properties is a numpy array comprised by four values
            First value is the stiffener neutral axis
            Second value is the stiffener area
            Third value is the stiffener section modulus
            Fourth value is the stiffener second moment of area (inertia moment)
        """
        height = self._height
        thickness = self._web_thickness

        area_mm2 = height*thickness
        area_cm2 = area_mm2/100.
    
        neutral_axis_mm = 0.5*height
        neutral_axis_cm = neutral_axis_mm/10

        second_area_moment_mm4 = (1.0/12)*thickness*height**3
        second_area_moment_cm4 = second_area_moment_mm4/1e4

        total_height_cm = height/10.
        section_modulus_cm3 = second_area_moment_cm4/max(neutral_axis_cm, total_height_cm - neutral_axis_cm)

        section_properties = np.array([neutral_axis_cm, area_cm2,
                                       section_modulus_cm3, second_area_moment_cm4])
        
        return section_properties
    
    def _compute_effective_section_properties(self,
                                              plate_thickness: float,
                                              spacing: float) -> np.ndarray:
        """
            height is in mm
            web_thickness is in mm
            plate_thickness is in mm

            section_properties is a numpy array comprised by four values
            First value is the total neutral axis
            Second value is the total area
            Third value is the total section modulus
            Fourth value is the total second moment of area (inertia moment)
        """
        height = self._height
        web_thickness = self._web_thickness

        effective_width = min([max([40.0*plate_thickness, 600.]), spacing])
        effective_area = effective_width*plate_thickness

        stiffener_area = height*web_thickness

        total_area_mm2 = effective_area + stiffener_area
        total_area_cm2 = total_area_mm2/100.

        plate_first_moment = 0.5*plate_thickness*effective_area
        stiffener_first_moment = (plate_thickness + (0.5*height))*stiffener_area
        first_area_moment = plate_first_moment + stiffener_first_moment
        neutral_axis_mm = first_area_moment/total_area_mm2
        neutral_axis_cm = neutral_axis_mm/10.

        # plate_second_moment = (1.0/12)*effective_width*effective_area**3 + effective_area*(neutral_axis_mm - (0.5*plate_thickness))**2
        # stiffener_second_moment = (1.0/12)*web_thickness*height**3 + stiffener_area*(neutral_axis_mm - (plate_thickness + 0.5*height))**2
        # second_area_moment_1 = plate_second_moment + stiffener_second_moment

        plate_second_moment_2 = (1.0/12)*effective_width*plate_thickness**3 + effective_area*((0.5*plate_thickness))**2
        stiffener_second_moment_2 = (1.0/12)*web_thickness*height**3 + stiffener_area*((plate_thickness + 0.5*height))**2
        second_area_moment_baseline = plate_second_moment_2 + stiffener_second_moment_2
        total_second_area_moment_mm4 = second_area_moment_baseline - total_area_mm2*neutral_axis_mm**2

        total_second_area_moment_cm4 = total_second_area_moment_mm4/1e4

        total_height_cm = (plate_thickness + height)/10.
        total_section_modulus_cm3 = total_second_area_moment_cm4/max(neutral_axis_cm, total_height_cm - neutral_axis_cm)

        section_properties = np.array([neutral_axis_cm, total_area_cm2,
                                       total_section_modulus_cm3,
                                       total_second_area_moment_cm4])
        
        return section_properties
    
    def calculate_stiffener_section_properties(self,
                                               plate_thickness: float,
                                               spacing: float):
        section_properties = self._compute_effective_section_properties(plate_thickness, spacing)
        
        self._total_neutral_axis = section_properties[0]
        self._total_area = section_properties[1]
        self._total_section_modulus = section_properties[2]
        self._total_second_area_moment = section_properties[3]
    
    def print_stiffener_section_properties(self):
        print(self._name)
        print('Neutral axis: {:.3f} cm'.format(self._total_neutral_axis))
        print('Area: {:.3f} cm2'.format(self._total_area))
        print('Section modulus: {:.3f} cm3'.format(self._total_section_modulus))
        print('Inertia moment: {:.3f} cm4'.format(self._total_second_area_moment))

def test():
    fb_1 = FlatBar('120x5')
    t_plate = 10.
    spacing = 500.
    fb_1.calculate_stiffener_section_properties(t_plate, spacing)
    fb_1.print_stiffener_section_properties()

if __name__ == '__main__':
    test()