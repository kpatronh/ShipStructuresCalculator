import numpy as np

from ship_particulars import create_vessel
from ship_particulars import Ship

class HullGirderLoads:
    def __init__(self, vessel: Ship) -> None:
        self._ship = vessel

    def _calculate_distribution_factor(self, x: float, Ls: float) -> float:
        x_vector = np.array([0.0, 0.1*Ls, 0.3*Ls, 0.7*Ls, 0.9*Ls, Ls])
        f_sw_vector = np.array([0.0, 0.15, 1.0, 1.0, 0.15, 0.0])
        f_sw = np.interp(x, x_vector, f_sw_vector)
        return f_sw
    
    def _calculate_distribution_factor_VWBM(self, x: float, Ls: float) -> float:
        x_vector = np.array([0.0, 0.4*Ls, 0.65*Ls, Ls])
        f_m_vector = np.array([0.0, 1.0, 1.0, 0.0])
        f_m = np.interp(x, x_vector, f_m_vector)
        return f_m
    
    def _calculate_vertical_wave_bending_moment(self, x: float, Cw: float,
                                                Ls: float, B: float,
                                                Cb: float) -> tuple[float, float]:
        """
            Assuming a RA value of 1.0, the sagging correction factor is -1.10
            MwH: Vertical wave bending moment in hogging condition
            MWH: Vertical wave bending moment in sagging condition
        """

        if Ls <= 90:
            Lf = 0.0412*Ls + 4.0
        elif Ls > 90 and Ls <= 300:
            Lf = 10.75 - ((300-Ls)/100)**1.5
        elif Ls > 300 and Ls <= 350:
            Lf = 10.75
        elif Ls > 350 and Ls < 500:
            Lf = 10.75 - ((Ls - 350)/150)**1.5

        Cb1 = max(Cb, 0.6)
        fs = 1.0
        Mo = 0.1*Lf*fs*(Ls**2)*B*(Cb1 + 0.7)

        FfH = (1.9*Cb1)/(Cb1+0.7)
        FfS = -1.1
        Df = self._calculate_distribution_factor_VWBM(x, Ls)

        MwH = FfH*Df*Mo
        MwS = FfS*Df*Mo

        print('Hogging vertical wave bending moment: {:.3f} kN.m'.format(MwH))
        print('Sagging vertical wave bending moment: {:.3f} kN.m'.format(MwS))

        # MwH = 0.19*f_nl_vh*fm*fp*Cw*Ls**2*B*Cb
        # MwS = -0.19*f_nl_vs*fm*fp*Cw*Ls**2*B*Cb

        return MwH, MwS
    
    def _calculate_minimum_still_water_bending_moment(self, x: float, Cw: float,
                                                      Ls: float, B: float,
                                                      Cb: float) -> tuple[float, float]:
        """
        Confirm with another formulas
        M_sw_h: Still water bending moment in hogging condition
        M_sw_s: Still water bending moment in sagging condition
        """
        f_sw = self._calculate_distribution_factor(x, Ls)

        M_sw_h_min = f_sw*(171*Cw*Ls**2*B*(Cb+0.7)*1e-3)
        M_sw_s_min = -0.85*f_sw*(171*Cw*Ls**2*B*(Cb+0.7)*1e-3)

        # M_wv_h, M_wv_s = self._calculate_vertical_wave_bending_moment(x, Cw, Ls, B, Cb)
        # M_sw_h_min = f_sw*(171*Cw*Ls**2*B*(Cb+0.7)*1e-3 - M_wv_h)
        # M_sw_s_min = -0.85*f_sw*(171*Cw*Ls**2*B*(Cb+0.7)*1e-3 + M_wv_s)

        return M_sw_h_min, M_sw_s_min
    
    def calculate_hull_girder_loads(self, x: float) -> float:
        """
        Cw: wave coefficient
        Ls: Rule length
        x: longitudinal position
        M_wv_h: Vertical wave bending moment in hogging condition
        M_wv_s: Vertical wave bending moment in sagging condition
        """
        L = self._ship.L
        Ls = 0.96*L
        B = self._ship.B
        T = self._ship.T
        delta = self._ship.disp

        Cb = delta/(1.025*L*B*T)

        if Ls >= 90 and Ls < 300:
            Cw = 10.75 - ((300-Ls)/100)**1.5
        elif Ls >= 300 and Ls < 350:
            Cw = 10.75
        elif Ls >= 350 and Ls < 500:
            Cw = 10.75 - ((Ls - 350)/150)**1.5
        
        # M_sw_h, M_sw_s = self._calculate_minimum_still_water_bending_moment(x, Cw, Ls, B, Cb)
        M_sw_h = 25000.
        M_sw_s = 10000.
        M_wv_h, M_wv_s = self._calculate_vertical_wave_bending_moment(x, Cw, Ls, B, Cb)

        M_hogging = M_sw_h + M_wv_h
        M_sagging = M_sw_s + M_wv_s

        print("=================================")
        print('Hogging bending moment: {:.3f} kN.m'.format(M_hogging))
        print('Sagging bending moment: {:.3f} kN.m'.format(M_sagging))
        print("=================================")

        hull_girder_bending_moment = max(M_hogging, M_sagging)

        return hull_girder_bending_moment
    