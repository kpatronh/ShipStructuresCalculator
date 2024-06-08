import numpy as np

class Rectangle:
    def __init__(self, width, height, position, angle) -> None: 
        """This class represents a rectangle with given dimension, position and orientation

        Args:
            width (float): width
            height (float): height
            position (array-like): position with respect to the universal axis
            angle (float): angle in degrees, with respect to the horizontal, positive counterclockwise
        """
        self.width = width
        self.height = height
        self.position = np.array(position)
        self.angle = angle * (np.pi/180.0) # in radians
    
    @property 
    def unit_direction(self):
        return np.array([np.cos(self.angle), np.sin(self.angle)])

    @property
    def unit_normal(self):
        return  np.array([-np.sin(self.angle), np.cos(self.angle)])

    @property
    def area(self):
        return self.width * self.height
    
    @property
    def centroid(self):
        return self.position + self.unit_direction * self.width/2.0
    
    @property
    def inertia(self):
        # moment of inertia with respect to rotated centroidal axes
        Iy = ((self.width)*(self.height**3))/12
        Iz = ((self.height)*(self.width**3))/12

        # centroidal polar moment of inertia 
        Ix = Iy + Iz

        # centroidal product moment of inertia
        Iyz = 0.0

        # moment of inertia with respect to axes paralell to the cartesian axes, centered on the centroid
        Iyp = 0.5*(Iy + Iz) + 0.5*(Iy - Iz)*np.cos(-2*self.angle)  
        Izp = 0.5*(Iy + Iz) - 0.5*(Iy - Iz)*np.cos(-2*self.angle)
        Iyzp = 0.5*(Iy - Iz)*np.sin(-2*self.angle) 
        return dict(Iy=Iy, Iz=Iz, Ix=Ix,  Iyz=Iyz,  Iyp=Iyp, Izp=Izp, Iyzp=Iyzp)
    
    def compute_inertia_wrt_parallel_axes(self, axes_center):
        # computation of moment of inertia with respect to axes parallel to the (cartesian) centroidal axes
        I = self.inertia
        area = self.area
        d = axes_center - self.centroid
        dy, dz = d[0], d[1]
        d2z, d2y, dyz = dz*dz, dy*dy, dy*dz
        Iya = I['Iyp'] + d2z*area
        Iza = I['Izp'] + d2y*area
        Ixa = I['Ix'] + (d2z + d2y)*area
        Iyza = I['Iyzp'] + dyz*area
        return dict(Iya=Iya, Iza=Iza, Ixa=Ixa, Iyza=Iyza)

    @property
    def section_properties(self):
        return f"unit_direction = {self.unit_direction}\
              \nunit_normal = {self.unit_normal}\
              \narea = {self.area}\
              \ncentroid = {self.centroid}\
              \ninertia = {self.inertia}"

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(width={self.width!r}, height={self.height!r}, position={self.position!r}, angle(deg)={round(self.angle*180/np.pi, 3)!r})"

class RectanglesBasedGeometry:
    def __init__(self, rectangles) -> None:
        self.rectangles = rectangles

    @property
    def area(self):
        a = 0.0
        for rect in self.rectangles:
            a += rect.area
        return a

    @property
    def centroid(self):
        a = 0.0
        c = np.array([0.0, 0.0])
        for rect in self.rectangles:
            a += rect.area
            c += rect.centroid * rect.area
        return c / a

    @property
    def inertia(self):
    # area inertia with respect to centroid axes of the compound geometry
        centroid = self.centroid
        Iy, Iz, Ix, Iyz = 0.0, 0.0, 0.0, 0.0
        for rect in self.rectangles:
            Irect = rect.compute_inertia_wrt_parallel_axes(centroid)
            Iy += Irect['Iya']
            Iz += Irect['Iza']
            Ix += Irect['Ixa']
            Iyz += Irect['Iyza']
        return dict(Iy=Iy, Iz=Iz, Ix=Ix, Iyz=Iyz)

    @property
    def section_properties(self):
        return f"area = {self.area}\
               \ncentroid = {self.centroid}\
               \ninertia = {self.inertia}"

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(rectangles={self.rectangles!r})"
    


if __name__ == "__main__":
    
    def test1():
        thickness = 25.4
        height = 100
        keel = Rectangle(width=thickness, height=height, position=[0,0], angle=90)
        print(keel)
        print(keel.section_properties)

    def test2():
        "Sample problem A/12 from Meriam(2018) Engineering Mechanics Statics"
        rect1 = Rectangle(width=40, height=10, position=[0, 5], angle=0)
        rect2 = Rectangle(width=40, height=10, position=[5, 10], angle=90)
        angle_section = RectanglesBasedGeometry([rect1, rect2])

        print('Rect 1:')
        print(rect1.section_properties)
        print(rect1.compute_inertia_wrt_parallel_axes(axes_center=angle_section.centroid))
        
        print('\nRect 2:')
        print(rect2.section_properties)
        print(rect2.compute_inertia_wrt_parallel_axes(axes_center=angle_section.centroid))

        print('\nAngle section:')
        print(angle_section)
        print(angle_section.section_properties)

    test2()
        




    
    