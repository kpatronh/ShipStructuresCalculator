import math
import numpy as np

from material import export_a131_material
from structural_element import StructuralElement
from ship import create_vessel
from ship import Ship


class DesignPressures:
    def __init__(self) -> None:
        """
            TODO: include the vessel object in the class constructor
        """
        pass

    def _calculate_design_wave_height(self, service_area: str) -> float:
        Hs = 0.0
        if service_area == "SA1":
            Hs = 5.5
        elif service_area == "SA2":
            Hs = 4.0
        elif service_area == "SA3":
            Hs = 3.6
        elif service_area == "SA4":
            Hs = 2.5
        else:
            Hs = 0.0

        H_dw = 1.67*Hs
        return H_dw

    def _calculate_wave_height_factor(self, service_area: str) -> float:
        if service_area == 'SA1':
            fHs = 1.0
        else:
            fHs = self._calculate_design_wave_height(service_area)/self._calculate_design_wave_height("SA1")

        return fHs

    def _calculate_nominal_wave_height(self, x: float, pressure_type: str,
                                       vessel: Ship) -> float:
        """
        TODO: Fix x_wl
        """
        x_wl = x
        # vessel = create_vessel()
        Cb = vessel.block_coefficient
        g = 9.81
        fHs = self._calculate_wave_height_factor(vessel.service_area)
        C_w = fHs*0.0771*vessel.L*(Cb + 0.2)**0.3*math.exp(-0.0044*vessel.L)
        Fn = 0.515*vessel.V/math.sqrt(g*vessel.L)
        xm = max((0.2, 0.45 - 0.6*Fn))

        if pressure_type == "shell":
            kr = 2.25
        else:
            kr = 4.5

        km = 1 + ((kr*(0.5 - xm)**2)/(Cb + 0.2))
        C_w_min = (C_w/km)*math.sqrt(2.25/kr)
        Hrm = C_w_min*(1 + (kr/(Cb + 0.2))*(x_wl/vessel.L - xm)**2)
        return Hrm

    def _calculate_hydrostatic_pressure(self, z: float, Tx: float, zk: float) -> float:
        Ph = 10.0*(Tx - (z - zk))
        return Ph
    
    def _calculate_hydrodynamic_pressure(self, x_wl: float, z: float,
                                         Lwl: float, draught: float,
                                         Hrm: float, fHs: float) -> float:
        """
        Hw: Nominal wave height
        Hrm: 
        Pw: Hydrostatic wave pressure
        """
        Tx = draught
        zk = 0.0

        u = (2.0*math.pi*Tx/Lwl)
        kz = math.exp(-u)
        fz = kz + (1.0 - kz)*(z - zk)/Tx
        
        Lp = Lwl
        Hpm_temp1 = 1.1*fHs*((2.0*x_wl/Lwl) - 1.0)*math.sqrt(Lp)
        Hpm_temp2 = 0.3*fHs*math.sqrt(Lwl)
        Hpm = max([Hpm_temp1, Hpm_temp2])
        Pm = 10.0*fz*Hrm
        Pp = 10.0*Hpm
        Pw = max([Pm, Pp])
        return Pw

    def _calculate_loads_shell_envelope(self, x_wl: float, struct_i: StructuralElement,
                                        vessel: Ship) -> float:
        """
        Hw: Nominal wave height
        Ps: Shell envelope pressure
        Ph: Hydrostatic pressure
        Pw: Hydrostatic wave pressure
        Pwd: Pressure on weather deck
        """
        # vessel = create_vessel()
        fHs = self._calculate_wave_height_factor(vessel.service_area)

        Tx = vessel.T
        Lwl = vessel.L
        zk = 0.0
        z = (0.5*(struct_i.start_point[1] + struct_i.end_point[1]))/1000.

        Hrm = self._calculate_nominal_wave_height(x_wl, "shell", vessel)
        Hw = 2.0*Hrm

        z_lim_1 = Tx + zk
        z_lim_2 = Tx + zk + Hw
        z_lim_3 = Tx + zk + 1.5*Hw

        fL = max(1.0 + 4.0*(x_wl/Lwl - 0.75), 1.0)
        Pd = 6.0 + 6.0*fL*fHs

        if struct_i.struct_type == "Exposed":
            if z <= (Tx + zk):
                Ph = self._calculate_hydrostatic_pressure(z, Tx, zk)
                Pw = self._calculate_hydrodynamic_pressure(x_wl, z, Lwl, Tx, Hrm, fHs)
                Pwd = Ph + Pw
            elif z <= (Tx + zk + 0.5*Hw):
                Pwd = Pd
            elif z <= (Tx + zk + 1.0*Hw):
                Pwd = Pd
            elif z <= (Tx + zk + 1.5*Hw):
                Pwd = 0.5*Pd
            else:
                Pwd = 0.5*Pd
            Ps = Pwd
        else:
            if z <= z_lim_1:
                # print('Tier 1')
                Ph = self._calculate_hydrostatic_pressure(z, Tx, zk)
                Pw = self._calculate_hydrodynamic_pressure(x_wl, z, Lwl, Tx, Hrm, fHs)
                Ps = Ph + Pw
            elif z > z_lim_1 and z <= z_lim_2:
                # print('Tier 2')
                Po = self._calculate_hydrodynamic_pressure(x_wl, z_lim_1, Lwl, Tx, Hrm, fHs)
                Pf = Pd
                Ps = Po - ((Po - Pf)/Hw)*(z - z_lim_1)
            elif z > z_lim_2 and z <= z_lim_3:
                # print('Tier 3')
                Po = Pd
                Pf = 0.5*Pd
                Ps = Po - ((Po - Pf)/(0.5*Hw))*(z - z_lim_2)
            else:
                # print('Tier 4')
                Ps = 0.5*Pd

        return Ps
    
    def _calculate_impact_loads_external_plating(self, x: float,
                                                 struct_i: StructuralElement,
                                                 vessel: Ship) -> float:
        """
        IPbi: Bottom impact pressure
        IPbf: Bow flare impact pressure

        Deadrise, buttock, effective deadrise, and waterline angles set randomly
        """
        impact_load = 0.0
        # vessel = create_vessel()

        Tx = vessel.T
        zk = 0.0
        z = (0.5*(struct_i.start_point[1] + struct_i.end_point[1]))/1000.
        Cb = vessel.block_coefficient

        g = 9.81

        deadrise_angle = 50
        buttock_angle = 13.0
        effective_deadrise_angle = 13.0
        waterline_angle = 0.0
        
        Vsp = (2.0/3.0)*vessel.V

        # psi = effective_deadrise_angle

        if Cb > 0.6:
            psi_deg = max((buttock_angle, deadrise_angle))
        else:
            psi_deg = max((buttock_angle, deadrise_angle - 10))

        psi = np.deg2rad(psi_deg)

        beta_p = np.deg2rad(deadrise_angle)
        gamma_p = np.deg2rad(waterline_angle)
        alpha_p = math.atan(math.tan(beta_p)*math.tan(gamma_p))
        
        alpha_p_deg = np.rad2deg(alpha_p)
        beta_p_deg = deadrise_angle
        gamma_p_deg = waterline_angle

        omega = math.sqrt((2.0*math.pi*g)/(0.8*vessel.L))
        omega_e = omega*(1.0 + (0.2*omega*Vsp)/g)
        Hrm = self._calculate_nominal_wave_height(x, "impact", vessel)
        Zwl = z - (Tx + zk)

        if struct_i.struct_type == "Bottom":
            if beta_p_deg >= 10.0:
                ksl = math.pi/math.tan(beta_p)
            else:
                ksl = 28.0*(1.0 - math.tan(2.0*beta_p))

            fsl = 1.0
            m1 = 0.25*(omega_e*fsl*Hrm)**2.0
            m0 = 0.25*(fsl*Hrm)**2.0
            Vth = math.sqrt(10.0)
            u = ((Zwl**2)/(2*m0)) + ((Vth**2)/(2*m1))
            PRsl = math.exp(-u)
            Nsl = 1720.0*PRsl*math.sqrt(m1/m0)

            if Nsl >= 1:
                Vbs = math.sqrt(Vth**2 + 2*m1*math.log(Nsl))
            else:
                Vbs = 0.0

            IPbi = 0.5*ksl*Vbs**2
            impact_load = IPbi
        elif struct_i.struct_type == "Side":

            if psi_deg >= 10.0:
                kbf = math.pi/math.tan(psi)
            else:
                kbf = 28.0*(1.0 - math.tan(psi))

            if vessel.block_coefficient <= 0.6:
                fsl_bf = 1.0
            else:
                fsl_bf = 1.2

            m1_bf = 0.25*(omega_e*fsl_bf*Hrm)**2.0
            m0_bf = 0.25*(fsl_bf*Hrm)**2.0

            Vthbf = math.sqrt(10.0)/math.cos(alpha_p)
            u_bf = ((Zwl**2)/(2*m0_bf)) + ((Vthbf**2)/(2*m1_bf))
            PRbf = math.exp(-u_bf)
            Nbf = 1720.0*PRbf*math.sqrt(m1_bf/m0_bf)

            if Nbf >= 1:
                Vbf = math.sqrt(Vthbf**2 + 2*m1_bf*math.log(Nbf))
            else:
                Vbf = 0.0

            # Second term
            if alpha_p_deg <= 80.0:
                krv = math.pi/math.tan(np.deg2rad(90 - alpha_p_deg))
            else:
                krv = 28.0*(1.0 - math.tan(2.0*np.deg2rad(90 - alpha_p_deg)))

            if gamma_p_deg >= 45.0:
                Hrv = 1.0
            elif gamma_p_deg < 0.0:
                Hrv = 0.0
            else:
                Hrv = math.cos(np.deg2rad(45 - gamma_p_deg))

            Vrv = 0.515*Vsp*math.sin(gamma_p)

            IPbf = 0.5*(kbf*Vbf**2.0 + krv*Hrv*Vrv**2)
            impact_load = IPbf
        else:
            impact_load = 0.0

        return impact_load

    def _compute_deck_pressures(self, struct_i: StructuralElement, inner_space: str):
        if inner_space == "Accomodation":
            P_in = 5.0
        elif inner_space == "Evacuation":
            P_in = 7.5
        elif inner_space == "Workshop":
            P_in = 10.0
        elif inner_space == "Store":
            P_in = 20.0
        else:
            P_in = 0.0
        
        return P_in
    
    def calculate_design_pressure(self, struct_i: StructuralElement, x_wl: float,
                                  vessel: Ship) -> float:
        """
        TODO: Correct the inner_space variables
        """
        # print(struct_i.struct_type)
        design_pressure = 0.0

        if struct_i.struct_type == "Deck":
            inner_space = "Accomodation"
            design_pressure = self._compute_deck_pressures(struct_i, inner_space)
        else:
            design_pressure_1 = self._calculate_loads_shell_envelope(x_wl, struct_i, vessel)
            design_pressure_2 = self._calculate_impact_loads_external_plating(x_wl, struct_i, vessel)
            design_pressure = max((design_pressure_1, design_pressure_2))

        return design_pressure
    

def test():
    mat_a131 = export_a131_material()
    long_pos = 60.
    vessel = create_vessel()

    name_i = 'Keel plating'
    struct_type_i = 'Bottom'
    start_pt_i = [0.0, 0.0]
    end_pt_i = [500.0, 0.0]
    thickness_i = 10.
    struct_0 = StructuralElement(name_i, struct_type_i, mat_a131, start_pt_i, end_pt_i,
                                 thickness_i)
    
    name_i = 'Bottom shell plating'
    struct_type_i = 'Bottom'
    start_pt_i = [500.0, 0.0]
    end_pt_i = [3000.0, 1500.0]
    thickness_i = 10.
    struct_1 = StructuralElement(name_i, struct_type_i, mat_a131, start_pt_i, end_pt_i,
                                 thickness_i)
    stiffener_type = 'FlatBar'
    stiffener_name = '120x5'
    spacing_i = 500
    struct_1.insert_stiffeners(stiffener_type, stiffener_name, spacing_i, offset=400.)

    name_i = 'Side shell plating'
    struct_type_i = 'Side'
    start_pt_i = [3000.0, 1500.0]
    end_pt_i = [6000.0, 9000.0]
    thickness_i = 10.
    struct_2 = StructuralElement(name_i, struct_type_i, mat_a131, start_pt_i, end_pt_i,
                                 thickness_i)
    stiffener_type = 'FlatBar'
    stiffener_name = '120x5'
    spacing_i = 500
    struct_2.insert_stiffeners(stiffener_type, stiffener_name, spacing_i, offset=400.)

    name_i = 'Upper deck'
    struct_type_i = 'Exposed'
    start_pt_i = [0.0, 9000.0]
    end_pt_i = [6000.0, 9000.0]
    thickness_i = 10.
    struct_3 = StructuralElement(name_i, struct_type_i, mat_a131, start_pt_i, end_pt_i,
                                 thickness_i)
    stiffener_type = 'FlatBar'
    stiffener_name = '120x5'
    spacing_i = 500
    struct_3.insert_stiffeners(stiffener_type, stiffener_name, spacing_i)

    name_i = 'Inner bottom plating'
    struct_type_i = 'Deck'
    start_pt_i = [0.0, 1000.0]
    end_pt_i = [1000.0, 1000.0]
    thickness_i = 10.
    struct_4 = StructuralElement(name_i, struct_type_i, mat_a131, start_pt_i, end_pt_i,
                                 thickness_i)
    stiffener_type = 'FlatBar'
    stiffener_name = '120x5'
    spacing_i = 500
    struct_4.insert_stiffeners(stiffener_type, stiffener_name, spacing_i, offset=200.)

    loads = DesignPressures()
    struct_0.design_pressure = loads.calculate_design_pressure(struct_0, long_pos, vessel)
    struct_1.design_pressure = loads.calculate_design_pressure(struct_1, long_pos, vessel)
    struct_2.design_pressure = loads.calculate_design_pressure(struct_2, long_pos, vessel)
    struct_3.design_pressure = loads.calculate_design_pressure(struct_3, long_pos, vessel)
    struct_4.design_pressure = loads.calculate_design_pressure(struct_4, long_pos, vessel)

    print(struct_0.design_pressure)
    print(struct_1.design_pressure)
    print(struct_2.design_pressure)
    print(struct_3.design_pressure)
    print(struct_4.design_pressure)
    

if __name__ == '__main__':
    test()