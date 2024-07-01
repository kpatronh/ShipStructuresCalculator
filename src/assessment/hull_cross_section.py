import math
import numpy as np
import matplotlib.pyplot as plt

from design_pressures import DesignPressures
from hull_girder_loads import HullGirderLoads
from material import Material
from ship import Ship
from structural_design import StructuralDesign

class HullCrossSection:
    def __init__(self, structure_list: list, x: float, mat: Material,
                 vessel: Ship) -> None:
        self._longitudinal_position = x
        self._structure_list = structure_list
        self._num_structures = len(structure_list)
        self._vessel = vessel

        loads = DesignPressures()

        for struct_i in self._structure_list:
            struct_i.design_pressure = loads.calculate_design_pressure(struct_i, x, vessel)
            struct_i.compute_struct_section_properties()
        
        self._material = mat
    
    @property
    def vessel(self) -> Ship:
        return self._vessel

    def _draw_secondary_stiffeners(self, start_pt: np.ndarray, end_pt: np.ndarray,
                                   num_spacings: int, offset: float,
                                   length: float, spacing: float):
        """
        t_vector is a num_stiffenersx2 size vector
        Given two points in R2 (x1, y1) and (x2, y2),
        the components of the t vector are dx = x2 - x1 and dy = y2 - y1.
        The normal vector is <-dy, dx> or <dy, -dx>
        https://stackoverflow.com/questions/1243614/how-do-i-calculate-the-normal-vector-of-a-line-segment
        """
        direction_vector = end_pt - start_pt
        perpendicular_vector = np.array([-direction_vector[1], direction_vector[0]])
        length_perp_vector = math.sqrt((perpendicular_vector[0])**2 + (perpendicular_vector[1])**2)
        normal_vector = perpendicular_vector/length_perp_vector

        start_with_offset = start_pt + (offset/length)*direction_vector
        last_stiffener = start_pt + ((offset + (num_spacings*spacing))/length)*direction_vector

        to_point = np.linspace(start_with_offset, last_stiffener, num_spacings+1)
        tf_point = np.zeros_like(to_point)
        for j in range(to_point.shape[0]):
            # print(to_point[j,:])
            # print(normal_vector)
            tf_point[j, :] = to_point[j, :] + 100*normal_vector
        return to_point, tf_point

    def visualize_cross_section(self) -> None:
        points = np.zeros((self._num_structures, 2))
        fig, ax = plt.subplots()
        for struct_i in self._structure_list:
            line_i_x = np.array([struct_i._start_point[0], struct_i._end_point[0]])
            line_i_y = np.array([struct_i._start_point[1], struct_i._end_point[1]])
            ax.plot(line_i_x, line_i_y, 'b')
            if struct_i._num_secondary_stiffeners != 0:
                stiffener_pos, final_pt = self._draw_secondary_stiffeners(struct_i._start_point,
                                                                          struct_i._end_point,
                                                                          struct_i._num_spacings,
                                                                          struct_i._offset,
                                                                          struct_i._length,
                                                                          struct_i.stiffener_spacing)
                # ax.plot(stiffener_pos[:,0], stiffener_pos[:,1], 'ko')
                for to, tf in zip(stiffener_pos, final_pt):
                    ax.plot(np.array([to[0], tf[0]]), np.array([to[1], tf[1]]),'k')
        plt.tight_layout()
        plt.show()
    
    def compute_cross_section_properties_1(self):
        print('FIRST METHOD')
        A_net = 0.0
        Sy_net = 0.0
        Iyo_net = 0.0
        max_height = -9999999
        for struct_i in self._structure_list:
            length_m = struct_i.length/1000.
            zi = struct_i.start_point[1]/1000.
            zk = struct_i.end_point[1]/1000.
            z_max = max(zi, zk)
            if z_max > max_height:
                max_height = z_max
            t_net = struct_i.current_thickness
            a_net = length_m*t_net*1e-3
            
            sy_net = 0.5*a_net*(zk + zi)
            iyo_net = (a_net/3.)*(zk**2 + zk*zi + zi**2)

            A_net += (2*a_net)
            Sy_net += (2*sy_net)
            Iyo_net += (2*iyo_net)
        
        zn = Sy_net/A_net

        Iy_net = Iyo_net - A_net*zn**2

        z_k = zn
        z_d = max_height - z_k

        Z_keel = Iy_net/z_k
        Z_deck = Iy_net/z_d

        self._cross_section_area = A_net
        self._cross_section_neutral_axis = zn
        self._cross_section_second_moment = Iy_net
        self._cross_section_section_modulus = min(Z_deck, Z_keel)
        self._deck_section_modulus = Z_deck
        self._keel_section_modulus = Z_keel
    
    def compute_cross_section_properties_2(self) -> None:
        print('SECOND METHOD')
        A_net = 0.0
        Qy_net = 0.0
        Iy_net = 0.0
        Iy_baseline = 0.0
        max_height = -9999999
        for struct_i in self._structure_list:
            zi = struct_i.start_point[1]/1000.
            zk = struct_i.end_point[1]/1000.
            z_max = max(zi, zk)
            if z_max > max_height:
                max_height = z_max
            
            a_net_i = struct_i._element_area
            z_net_i = struct_i._element_neutral_axis
            I_net_i = struct_i._element_second_moment

            A_net += a_net_i
            Qy_net += (a_net_i*z_net_i)
            Iy_baseline += (I_net_i + (a_net_i*z_net_i**2))
        
        zn = Qy_net/A_net

        Iy_net = Iy_baseline - A_net*(zn**2)

        z_k = zn
        z_d = max_height - z_k

        Z_keel = Iy_net/z_k
        Z_deck = Iy_net/z_d

        self._cross_section_area = A_net
        self._cross_section_neutral_axis = zn
        self._cross_section_second_moment = Iy_net
        self._cross_section_section_modulus = min(Z_deck, Z_keel)
        self._deck_section_modulus = Z_deck
        self._keel_section_modulus = Z_keel
    
    def print_cross_section_properties(self):
        print("=================================")
        print('Neutral axis: {:.3f} m'.format(self._cross_section_neutral_axis))
        print('Area: {:.3f} m2'.format(self._cross_section_area))
        print('Section modulus: {:.3f} m3'.format(self._cross_section_section_modulus))
        print('Inertia moment: {:.3f} m4'.format(self._cross_section_second_moment))
        print("=================================")

    def compute_longitudinal_strength(self):
        x = self._longitudinal_position

        global_loads = HullGirderLoads(self._vessel)
        hull_girder_bending_moment = global_loads.calculate_hull_girder_loads(x)

        deck_bending_stress = hull_girder_bending_moment/(1000*self._deck_section_modulus)
        keel_bending_stress = hull_girder_bending_moment/(1000*self._keel_section_modulus)

        sigma_o = self._material.minimum_yield_stress
        f_hts = self._material._hts_correction_factor("Global")
        
        LR = self._vessel.L

        if x > 0.3*LR and x < 0.7*LR:
            f_hg = 0.75
        else:
            f_hg = 0.319 + 2.311*(x/LR) - 2.974*(x/LR)**2

        hull_girder_permisible_stress = f_hg*f_hts*sigma_o

        self._assess_strength_criteria(deck_bending_stress, keel_bending_stress,
                                       hull_girder_permisible_stress)
        
        self._print_longitudinal_strength_information(deck_bending_stress,
                                                      keel_bending_stress,
                                                      hull_girder_permisible_stress)
    
    def _assess_strength_criteria(self, sigma_D: float, sigma_B: float, sigma_P: float) -> None:
        """
            sigma_D: hull girder bending stress at strength deck, in N/mm2
            sigma_B: hull girder bending stress at keel, in N/mm2
            sigma_P: maximum permissible hull vertical bending stress, in N/mm2
        """
        print("=================================")
        if sigma_D < sigma_P:
            print("Deck bending stress criteria complied")
        else:
            print("Deck bending stress criteria failed")
        
        if sigma_B < sigma_P:
            print("Keel bending stress criteria complied")
        else:
            print("Keel bending stress criteria failed")
        print("=================================")
    
    def _print_longitudinal_strength_information(self, sigma_D: float, sigma_B: float, sigma_P: float) -> None:
        """
            sigma_D: hull girder bending stress at strength deck, in N/mm2
            sigma_B: hull girder bending stress at keel, in N/mm2
            sigma_P: maximum permissible hull vertical bending stress, in N/mm2
        """
        print("=================================")
        print('Hull girder bending stress at strength deck: {:.3f} MPa'.format(sigma_D))
        print('Hull girder bending stress at keel: {:.3f} MPa'.format(sigma_B))
        print('Maximum permissible hull vertical bending stress: {:.3f} MPa'.format(sigma_P))
        print("=================================")
    
    def calculate_local_scantlings(self):
        local_scantling = StructuralDesign(self.vessel, self._material)
        local_scantling.calculate_structural_scantling(self._structure_list)
        local_scantling.print_scantling_info()
        local_scantling.print_criteria_info()
