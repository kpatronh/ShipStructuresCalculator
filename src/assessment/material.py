import math

import numpy as np

class Material:
    def __init__(self, name: str, young: float, yield_stress: float, ultimate_stress: float) -> None:
        self._name = name
        self._young_modulus = young
        self._minimum_yield_stress = yield_stress
        self._ultimate_tensile_stress = ultimate_stress
        self._shear_strength = yield_stress/math.sqrt(3.0)
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def young_modulus(self) -> float:
        return self._young_modulus
    
    @property
    def minimum_yield_stress(self) -> float:
        return self._minimum_yield_stress
    
    @property
    def ultimate_tensile_stress(self) -> float:
        return self._ultimate_tensile_stress
    
    @property
    def shear_strength(self) -> float:
        return self._shear_strength
    
    def _hts_correction_factor(self, load_type: str) -> float:
        so_vector = np.array([235., 265., 315., 355., 390])
        f_hts_vector_global = np.array([1.0, 0.964, 0.956, 0.919, 0.886*(390/self.minimum_yield_stress)])
        f_hts_vector_local = np.array([1.0, 1.0, 1.0, 1.0, 0.91*(390/self.minimum_yield_stress)])

        if load_type == "Global":
            f_hts = np.interp(self.minimum_yield_stress, so_vector, f_hts_vector_global)
        else:
            f_hts = np.interp(self.minimum_yield_stress, so_vector, f_hts_vector_local)
        
        return f_hts

def export_a131_material() -> Material:
    mat_name = 'a131'
    mat_yield = 235.
    mat_ultimate = 400.
    young = 201e9

    mat_a131 = Material(mat_name, young, mat_yield, mat_ultimate)

    return mat_a131

def test():
    mat_name = 'a131'
    mat_yield = 235.
    mat_ultimate = 400.
    young = 210e9

    mat_a131 = Material(mat_name, young, mat_yield, mat_ultimate)
