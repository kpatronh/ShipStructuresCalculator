import math
import numpy as np
import pandas as pd

from structural_element import StructuralElement
from ship import Ship
from material import Material

class StructuralDesign:
    def __init__(self, vessel: Ship, mat: Material) -> None:
        self._vessel = vessel
        self._material = mat
        self._compute_NSR_minimal_structural_requirements()
    
    @staticmethod
    def allowable_stress_factors(structure_item_i: str) -> np.ndarray:
        """
            The first value is sigma_x/sigma_y
            The second value is tau_xy
            The third value is f_delta
            TODO: update limiting stress factors for the additional categories
        """
        limiting_stress_factor = dict([('Bottom', np.array([0.75, 0.0, 0.00125])),
                                       ('Keel', np.array([0.75, 0.0, 0.00125])),
                                       ('Side', np.array([0.75, 0.8, 0.00125])),
                                       ('Deck', np.array([0.75, 0.0, 0.001])),
                                       ('Strength deck', np.array([0.75, 0.0, 0.001])),
                                       ('Internal deck', np.array([0.75, 0.0, 0.001])),
                                       ('Inner bottom', np.array([0.75, 0.0, 0.001])),
                                       ('Exposed deck', np.array([0.75, 0.0, 0.001]))])
        
        return limiting_stress_factor[structure_item_i]

    def _select_limiting_stress_coefficient(self, structural_item: str) -> float:
        """
            factor_hts is 1.0 for local loads. 
            For global loads, custom values are to be computed and interpolated
        """
        f_factors = StructuralDesign.allowable_stress_factors(structural_item)
        factor_f1 = f_factors[0]
        factor_hts = 1.0
        factor_fs = factor_f1*factor_hts
        return factor_fs

    def _calculate_required_thickness(self, structural_item: StructuralElement) -> float:
        """
            Gamma is asummed as 1.0 because the plates are considered flat panels
            tp is in mm
        """
        gamma = 1.0
        unsupported_span = self._vessel.transverse_span
        spacing = structural_item.stiffener_spacing
        AR = np.max([unsupported_span, spacing])/np.min([unsupported_span, spacing])
        if AR <= 2.0:
            beta = AR*(1.0-0.25*AR)
        else:
            beta = 1.0
        f_sigma = self._select_limiting_stress_coefficient(structural_item.struct_type)
        design_pressure = structural_item.design_pressure
        sigma_o = structural_item.material.minimum_yield_stress
        tp = 22.4*spacing*gamma*beta*math.sqrt(design_pressure/(f_sigma*sigma_o))*1e-3

        return tp
    
    def _calculate_secondary_member_property_sections(self, structural_item: StructuralElement) -> np.ndarray:
        """
            Z is in cm3
            I is in cm4
            A is in cm2
        """
        le = self._vessel.transverse_span/1000.
        spacing = structural_item.stiffener_spacing
        design_pressure = structural_item.design_pressure
        sigma_o = structural_item.material.minimum_yield_stress
        E_young = structural_item.material.young_modulus/1e6
        tau_o = structural_item.material.shear_strength
        struct_type = structural_item.struct_type

        f_factors = StructuralDesign.allowable_stress_factors(struct_type)
        f_sigma = f_factors[0]
        f_tau = f_factors[1]
        f_delta = f_factors[2]

        # Secondary stiffening
        phi_z = 0.1
        phi_I = 1.0/288
        phi_A = 0.5

        Z = (phi_z*design_pressure*spacing*le**2)/(f_sigma*sigma_o)
        I = (100*phi_I*design_pressure*spacing*le**3)/(f_delta*E_young)
        if f_tau > 1e-5:
            Aw = (phi_A*design_pressure*spacing*le)/(100*f_tau*tau_o)
        else:
            Aw = 0.0

        required_section_properties = np.array([Z, I, Aw])
        return required_section_properties

    def _calculate_primary_member_property_sections(self, structural_item: StructuralElement) -> None:
        """
            Z is in cm3
            I is in cm4
            A is in cm2
        """
        unsupported_span = self._vessel.transverse_span
        spacing = structural_item.stiffener_spacing
        design_pressure = structural_item.design_pressure
        sigma_o = structural_item.material.minimum_yield_stress
        E_young = structural_item.material.young_modulus
        tau_o = structural_item.material.shear_strength
        struct_name = structural_item.name

        f_factors = StructuralDesign.allowable_stress_factors(struct_name)
        f_sigma = f_factors[0]
        f_tau = f_factors[1]
        f_delta = f_factors[2]

        # Primary stiffening
        phi_z = 1.0/12
        phi_I = 1.0/384
        phi_A = 0.5

        Z = (1000*phi_z*design_pressure*spacing*unsupported_span**2)/(f_sigma*sigma_o)
        I = (1e5*phi_I*design_pressure*spacing*unsupported_span**3)/(f_delta*E_young)
        Aw = (10*phi_A*design_pressure*spacing*unsupported_span)/(f_tau*tau_o)
    
    def calculate_structural_scantling(self, structure_list: list) -> None:
        plating_list = list()
        stiffeners_list = list()
        stiffened_plating_list = list()
        design_pressures_list = list()
        required_thickness_list = list()
        current_thickness_list =list()
        thickness_criteria_list = list()

        required_section_modulus_list = list()
        stiffener_section_modulus_list = list()
        required_second_moment_list = list()
        stiffener_second_moment_list = list()
        required_area_list = list()
        stiffener_area_list = list()
        
        section_modulus_criteria_list = list()
        second_moment_criteria_list = list()
        area_criteria_list = list()

        for struct_i in structure_list:
            struct_i.required_thickness = self._calculate_required_thickness(struct_i)

            if struct_i.struct_type in self._minimum_scantling:
                # print("Struct type: {}".format(struct_i.struct_type))
                # print("Required thickness: {:.2f} mm".format(self._minimum_scantling[struct_i.struct_type]))
                required_thickness = max(struct_i.required_thickness, self._minimum_scantling[struct_i.struct_type])
            else:
                required_thickness = struct_i.required_thickness

            if struct_i._num_secondary_stiffeners != 0:
                required_section_properties = self._calculate_secondary_member_property_sections(struct_i)

                stiffeners_list.append(struct_i._secondary_stiffener._name)
                stiffened_plating_list.append(struct_i.name)

                required_section_modulus_list.append(required_section_properties[0])
                stiffener_section_modulus_list.append(struct_i.stiffener_section_modulus)
                required_second_moment_list.append(required_section_properties[1])
                stiffener_second_moment_list.append(struct_i.stiffener_second_moment)
                required_area_list.append(required_section_properties[2])
                stiffener_area_list.append(struct_i.stiffener_area)

                section_modulus_criteria = self._assess_criteria(required_section_properties[0], struct_i.stiffener_section_modulus)
                second_moment_criteria = self._assess_criteria(required_section_properties[1], struct_i.stiffener_second_moment)
                area_criteria = self._assess_criteria(required_section_properties[2], struct_i.stiffener_area)

                section_modulus_criteria_list.append(section_modulus_criteria)
                second_moment_criteria_list.append(second_moment_criteria)
                area_criteria_list.append(area_criteria)
            # struct_i.print_structural_scantling_info()

            plating_list.append(struct_i.name)
            design_pressures_list.append(struct_i.design_pressure)
            required_thickness_list.append(required_thickness)
            current_thickness_list.append(struct_i.current_thickness)

            thickness_criteria = self._assess_criteria(required_thickness, struct_i.current_thickness)
            thickness_criteria_list.append(thickness_criteria)
        
        scantling_plating_info_dict = dict({'Design pressures [kN/m2]': design_pressures_list,
                                            'Required thickness [mm]': required_thickness_list,
                                            'Current thickness [mm]': current_thickness_list})
        
        criteria_plating_info_dict = dict({'Criteria': thickness_criteria_list})
        
        scantling_stiffener_info_dict = dict({'Stiffener name': stiffeners_list,
                                              'Required Z [cm3]': required_section_modulus_list,
                                              'Current Z [cm3]': stiffener_section_modulus_list,
                                              'Required I [cm4]': required_second_moment_list,
                                              'Current I [cm4]': stiffener_second_moment_list,
                                              'Required Aw [cm2]': required_area_list,
                                              'Current Aw [cm2]': stiffener_area_list})
        
        criteria_stiffener_info_dict = dict({'Stiffener name': stiffeners_list,
                                              'Z criteria': section_modulus_criteria_list,
                                              'I criteria': second_moment_criteria_list,
                                              'Aw criteria': area_criteria_list})
        
        self._scantling_plating_info_pd = pd.DataFrame(data=scantling_plating_info_dict, index=plating_list)
        self._scantling_stiffener_info_pd = pd.DataFrame(data=scantling_stiffener_info_dict, index=stiffened_plating_list)

        self._criteria_plating_info_pd = pd.DataFrame(data=criteria_plating_info_dict, index=plating_list)
        self._criteria_stiffener_info_pd = pd.DataFrame(data=criteria_stiffener_info_dict, index=stiffened_plating_list)

    def print_scantling_info(self) -> None:
        print(self._scantling_plating_info_pd)
        print(self._scantling_stiffener_info_pd)
    
    def print_criteria_info(self) -> None:
        print(self._criteria_plating_info_pd)
        print(self._criteria_stiffener_info_pd)

    def _assess_criteria(self, required_value: float, actual_value: float) -> str:
        if required_value < actual_value:
            return "Complied"
        else:
            return "Failed"
    
    def _compute_NSR_minimal_structural_requirements(self) -> None:
        LR = self._vessel.L
        B = self._vessel.B
        T = self._vessel.T

        if self._vessel.vessel_type == "NS1":
            omega = 1.1
        else:
            omega = 1.0
        
        L1 = min(LR, 190)

        sigma_o = self._material.minimum_yield_stress
        sigma_u = self._material.ultimate_tensile_stress
        kms = 635/(sigma_o + sigma_u)

        kms_root_square = math.sqrt(kms)
        LR_root_square = math.sqrt(LR)

        bottom_shell_plating = max(kms_root_square*(0.4*LR_root_square + 2.0), 5.0*omega)
        side_shell_plating = max(kms_root_square*(0.38*LR_root_square + 1.2), 4.0*omega)
        keel_plate_breadth = max(7*LR + 340, 750)
        keel_plate_thickness = omega*kms_root_square*1.35*L1**0.45

        inner_bottom_plating = max(kms_root_square*(0.4*LR_root_square + 1.5), 4.0*omega)
        centerline_girger_plating = max(kms_root_square*(0.9*LR_root_square + 1.0), 4.0*omega)
        side_girder_plating = max(kms_root_square*0.72*LR_root_square, 3.5*omega)
        double_bottom_depth = max(28*B + 205*math.sqrt(T), 630.)

        watertight_bulkhead_plating = omega*kms_root_square*(0.38*LR_root_square + 1.0)

        strength_deck_plating = omega*kms_root_square*(0.38*LR_root_square + 1.2)
        internal_lower_deck_plating = omega*kms_root_square*(0.18*LR_root_square + 1.7)
        exposed_deck_fwd_0_75LR = omega*kms_root_square*(0.015*LR_root_square + 5.5)
        exposed_Deck_afr_0_75LR = omega*kms_root_square*(0.38*LR_root_square + 1.2)

        self._minimum_scantling = dict()
        self._minimum_scantling['Bottom'] = bottom_shell_plating
        self._minimum_scantling['Keel'] = keel_plate_thickness
        self._minimum_scantling['Side'] = side_shell_plating
        self._minimum_scantling['Inner bottom'] = inner_bottom_plating
        self._minimum_scantling['Strength deck'] = strength_deck_plating
        self._minimum_scantling['Internal deck'] = internal_lower_deck_plating