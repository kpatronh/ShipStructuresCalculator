import math
import numpy as np

from material import Material
from stiffeners import FlatBar

class StructuralElement:
    def __init__(self, name: str, struct_type: str, mat: Material,
                 start_pt: np.ndarray, end_pt: np.ndarray,
                 thickness: float) -> None:
        self._name = name
        self._struct_type = struct_type
        self._material = mat
        self._start_point = np.array(start_pt)
        self._end_point = np.array(end_pt)
        self._stiffener_span = 0.0
        self._design_pressure = 0.0
        self._required_thickness = 0.0
        self._current_thickness = thickness
        self._num_secondary_stiffeners = 0
        self._offset = 0.0
        self._length = math.sqrt((start_pt[0] - end_pt[0])**2 + (start_pt[1] - end_pt[1])**2)
        self._stiffening_spacing = self._length
        self._num_spacings = 1
        self._stiffener_area = 0.0
        self._stiffener_neutral_axis = 0.0
        self._stiffener_second_moment = 0.0
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def struct_type(self) -> str:
        return self._struct_type
    
    @property
    def material(self) -> Material:
        return self._material
    
    @property
    def start_point(self) -> np.ndarray:
        return self._start_point
    
    @property
    def end_point(self) -> np.ndarray:
        return self._end_point
    
    @property
    def length(self) -> float:
        return self._length
    
    @property
    def stiffener_spacing(self) -> float:
        return self._stiffening_spacing
    
    @property
    def stiffener_span(self) -> float:
        return self._stiffener_span

    @property
    def design_pressure(self) -> float:
        return self._design_pressure

    @design_pressure.setter
    def design_pressure(self, value: float):
        self._design_pressure = value

    @property
    def required_thickness(self) -> float:
        return self._required_thickness
    
    @required_thickness.setter
    def required_thickness(self, value: float):
        self._required_thickness = value

    @property
    def current_thickness(self) -> float:
        return self._current_thickness
    
    @current_thickness.setter
    def current_thickness(self, value: float):
        self._current_thickness = value
    
    @property
    def stiffener_second_moment(self) -> float:
        return self._stiffener_second_moment
    
    @property
    def stiffener_section_modulus(self) -> float:
        return self._stiffener_section_modulus
    
    @property
    def stiffener_area(self) -> float:
        return self._stiffener_area
    
    def insert_stiffeners(self, stiffener_type: str,
                          stiffener_name: str,
                          spacing: float,
                          offset: float = 0.0):
        if stiffener_type == 'FlatBar':
            self._secondary_stiffener = FlatBar(stiffener_name)
            plate_thickness = self.current_thickness
            self._stiffening_spacing = spacing
            self._secondary_stiffener.calculate_stiffener_section_properties(plate_thickness, spacing)
            num_stiffeners = math.ceil((self._length - offset)/spacing)
            num_spacings = num_stiffeners - 1
            self._num_secondary_stiffeners = num_stiffeners
            self._num_spacings = num_spacings
            self._offset = offset
            self._stiffener_area = self._secondary_stiffener._total_area
            self._stiffener_neutral_axis = self._secondary_stiffener._total_neutral_axis
            self._stiffener_second_moment = self._secondary_stiffener._total_second_area_moment
            self._stiffener_section_modulus = self._secondary_stiffener._total_section_modulus
            if (num_spacings*spacing + offset) > self._length:
                error_msg = "Panel too short, stiffeners too spread, or maximum number of stiffeners reached"
                raise Exception(error_msg)
    
    def compute_struct_section_properties(self) -> None:
        """
            Panel area is in m2
            Neutral axis of the panel is in m2

            Stiffener area is in m2
            Neutral axis of the stiffener is in m2

            TODO: compute the second moment of area in a more efficient way
        """
        length_m = self._length/1000.
        thickness_m = self.current_thickness/1000.
        # stiffener_area_m2 = self._stiffener_area/1e4
        stiffener_area_m2 = 0.0
        stiffener_neutral_axis_m = self._stiffener_neutral_axis/100.
        stiffener_second_moment_local_m4 = self._stiffener_second_moment/1e8
        panel_neutral_axis_m = 0.5*(self._start_point[1] + self._end_point[1])/1000.

        panel_area_m2 = thickness_m*length_m

        total_stiffener_area_m2 = self._num_secondary_stiffeners*stiffener_area_m2
        element_area = panel_area_m2 + total_stiffener_area_m2

        element_first_moment = (panel_area_m2*panel_neutral_axis_m) + (total_stiffener_area_m2*stiffener_neutral_axis_m)
        element_neutral_axis = element_first_moment/element_area

        panel_second_moment_local_m = (1./12)*length_m*thickness_m**3
        panel_steiner_moment = panel_area_m2*(panel_neutral_axis_m - element_neutral_axis)**2
        panel_second_moment_baseline = panel_second_moment_local_m + panel_steiner_moment

        stiffener_steiner_moment = total_stiffener_area_m2*(stiffener_neutral_axis_m - element_neutral_axis)**2
        stiffener_second_moment_baseline = stiffener_second_moment_local_m4 + stiffener_steiner_moment

        element_second_moment_baseline = panel_second_moment_baseline + stiffener_second_moment_baseline

        self._element_area = element_area
        self._element_neutral_axis = element_neutral_axis
        self._element_second_moment = element_second_moment_baseline

        # self.print_element_section_properties()
    
    def print_structural_scantling_info(self):
        print("Structure: {}".format(self._name))
        print("Type: {}".format(self._struct_type))
        print("Design pressure: {} kN/m2".format(self._design_pressure))
        print("Required thickness: {:.2f} mm".format(self._required_thickness))
    
    def print_element_section_properties(self) -> None:
        print(self.name)
        print('Neutral axis: {:.3f} m'.format(self._element_neutral_axis))
        print('Area: {:.3f} m2'.format(self._element_area))
        print('Inertia moment: {:.3e} m4'.format(self._element_second_moment))