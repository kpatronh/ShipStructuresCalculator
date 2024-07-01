import numpy as np

from hull_cross_section import HullCrossSection
from material import export_a131_material
from ship import create_vessel
from structural_element import StructuralElement

def test() -> None:
    mat_a131 = export_a131_material()

    name_i = 'Keel plating'
    struct_type_i = 'Keel'
    start_pt_i = [0.0, 0.0]
    end_pt_i = [500.0, 0.0]
    thickness_i = 13.
    struct_0 = StructuralElement(name_i, struct_type_i, mat_a131, start_pt_i, end_pt_i,
                                 thickness_i)
    
    name_i = 'Bottom shell plating'
    struct_type_i = 'Bottom'
    start_pt_i = [500.0, 0.0]
    end_pt_i = [3000.0, 1500.0]
    thickness_i = 8.
    struct_1 = StructuralElement(name_i, struct_type_i, mat_a131, start_pt_i, end_pt_i,
                                 thickness_i)
    stiffener_type = 'FlatBar'
    stiffener_name = '160x7'
    spacing_i = 500
    struct_1.insert_stiffeners(stiffener_type, stiffener_name, spacing_i, offset=400.)

    name_i = 'Side shell plating'
    struct_type_i = 'Side'
    start_pt_i = [3000.0, 1500.0]
    end_pt_i = [10000.0, 8000.0]
    thickness_i = 6.
    struct_2 = StructuralElement(name_i, struct_type_i, mat_a131, start_pt_i, end_pt_i,
                                 thickness_i)
    stiffener_type = 'FlatBar'
    stiffener_name = '140x6'
    spacing_i = 500
    struct_2.insert_stiffeners(stiffener_type, stiffener_name, spacing_i, offset=400.)

    name_i = 'Upper deck'
    struct_type_i = 'Strength deck'
    start_pt_i = [0.0, 8000.0]
    end_pt_i = [10000.0, 8000.0]
    thickness_i = 7.
    struct_3 = StructuralElement(name_i, struct_type_i, mat_a131, start_pt_i, end_pt_i,
                                 thickness_i)
    stiffener_type = 'FlatBar'
    stiffener_name = '120x5'
    spacing_i = 500
    struct_3.insert_stiffeners(stiffener_type, stiffener_name, spacing_i)

    name_i = 'Inner bottom plating'
    struct_type_i = 'Inner bottom'
    start_pt_i = [0.0, 1000.0]
    end_pt_i = [1000.0, 1000.0]
    thickness_i = 10.
    struct_4 = StructuralElement(name_i, struct_type_i, mat_a131, start_pt_i, end_pt_i,
                                 thickness_i)
    stiffener_type = 'FlatBar'
    stiffener_name = '160x7'
    spacing_i = 500
    struct_4.insert_stiffeners(stiffener_type, stiffener_name, spacing_i, offset=200.)

    name_i = 'Deck 3'
    struct_type_i = 'Internal deck'
    start_pt_i = [0.0, 3200.0]
    end_pt_i = [4700.0, 3200.0]
    thickness_i = 7.
    struct_5 = StructuralElement(name_i, struct_type_i, mat_a131, start_pt_i, end_pt_i,
                                 thickness_i)
    stiffener_type = 'FlatBar'
    stiffener_name = '140x6'
    spacing_i = 500
    struct_5.insert_stiffeners(stiffener_type, stiffener_name, spacing_i)
    
    name_i = 'Deck 2'
    struct_type_i = 'Internal deck'
    start_pt_i = [0.0, 5400.0]
    end_pt_i = [7200.0, 5400.0]
    thickness_i = 7.
    struct_6 = StructuralElement(name_i, struct_type_i, mat_a131, start_pt_i, end_pt_i,
                                 thickness_i)
    stiffener_type = 'FlatBar'
    stiffener_name = '140x5'
    spacing_i = 500
    struct_6.insert_stiffeners(stiffener_type, stiffener_name, spacing_i)

    structure_list = [struct_0, struct_1, struct_2, struct_3, struct_4, struct_5, struct_6]

    vessel = create_vessel()

    long_pos = 60.
    hull_cs = HullCrossSection(structure_list, long_pos, mat_a131, vessel)

    do_visualize = 0
    do_scantling = 1

    if do_visualize:
        hull_cs.visualize_cross_section()

    if do_scantling:
        hull_cs.calculate_local_scantlings()

        hull_cs.compute_cross_section_properties_1()
        # hull_cs.compute_cross_section_properties_2()
        hull_cs.print_cross_section_properties()
        hull_cs.compute_longitudinal_strength()
        

if __name__ == '__main__':
    test()