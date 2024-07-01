class Ship:
    def __init__(self, L: float, B: float, T: float, disp: float,
                 speed: float, service_area: str, vessel_type: str,
                 frame_length: float, transverse_span: float) -> None:
        """
        Variables
        ----------

        * L: length, in meters
        * B: moulded breadth, in meters
        * T: design draught, in metres
        * disp: moulded displacement, in tons, at draught T
        * V: design speed in kn
        * service_area_notation: LR service area notation.
            (See the LR's Naval Ships rules, page 574 of .pdf)
        * vessel_type: NS1, NS2, or NS3 vessel
        * frame_length: in mm
        * transverse_span: length between two transverse primary structure in mm
        """
        self._L = L
        self._B = B
        self._T = T
        self._disp = disp
        self._V = speed
        self._service_area = service_area
        self._vessel_type = vessel_type
        self._frame_length = frame_length
        self._transverse_span = transverse_span

    @property
    def L(self):
        return self._L

    @L.setter
    def L(self, value):
        self._L = value

    @property
    def B(self):
        return self._B

    @B.setter
    def B(self, value):
        self._B = value

    @property
    def T(self):
        return self._T

    @T.setter
    def T(self, value):
        self._T = value

    @property
    def disp(self):
        return self._disp

    @disp.setter
    def disp(self, value):
        self._disp = value

    @property
    def V(self):
        return self._V

    @V.setter
    def V(self, value):
        self._V = value

    @property
    def service_area(self):
        return self._service_area

    @service_area.setter
    def service_area(self, value_str):
        self._service_area = value_str

    @property
    def block_coefficient(self):
        disp_m3 = self.disp/1.025
        self._block_coefficient = disp_m3/(self.L*self.B*self.T)
        return self._block_coefficient

    @property
    def vessel_type(self) -> str:
        return self._vessel_type
    
    @property
    def frame_length(self) -> float:
        return self._frame_length
    
    @property
    def transverse_span(self) -> float:
        return self._transverse_span

    def print_ship_info(self):
        print("=================================")
        print('Length: {:.1f} m'.format(self._L))
        print('Draught: {:.1f} m'.format(self._T))
        print('Displacement: {:d} ton'.format(self._disp))
        print('Speed: {:.1f} kn'.format(self._V))
        print('Service areas: {}'.format(self._service_area))
        print('Vessel type: {}'.format(self._vessel_type))
        print('Frame length: {:.1f} m'.format(self._frame_length))
        print('Transverse span: {:.1f} m'.format(self._transverse_span))
        print("=================================")


def create_vessel() -> Ship:
    """
    FREMM frigate
    """
    L = 142
    B = 18
    T = 6.4
    disp = 9000
    V = 27

    service_area = 'SA1'
    vessel_type = 'NS2'
    frame_length = 500.
    transverse_span = 1500.

    vessel = Ship(L, B, T, disp, V, service_area, vessel_type, frame_length, transverse_span)
    vessel.print_ship_info()

    return vessel


if __name__ == '__main__':
    create_vessel()
