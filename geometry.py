import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from scipy.linalg import norm

class Rectangle:
    def __init__(self, width, height, position, angle): 
        """This class represents a rectangle, based on its dimensions, position and orientation

        Args:
            width (float): width
            height (float): height
            position (array-like): position with respect to the universal axis
            angle (float): angle in degrees, with respect to the horizontal, positive counterclockwise
        """
        self.width = width
        self.height = height
        self.position = np.array(position)
        self.angle = from_deg_to_rad(angle) # in radians 
    
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

    @property
    def corner_points(self):
        upper_left = self.position + 0.5*self.height * self.unit_normal
        lower_left = self.position - 0.5*self.height * self.unit_normal
        lower_right = lower_left + self.width * self.unit_direction
        upper_right = upper_left + self.width * self.unit_direction
        points=dict(upper_left=upper_left, lower_left=lower_left, lower_right=lower_right, upper_right=upper_right)
        return points

    @property
    def bounding_box(self):
        corner_points = self.corner_points
        xs = corner_points['upper_left'][0], corner_points['lower_left'][0], corner_points['lower_right'][0], corner_points['upper_right'][0]
        ys = corner_points['upper_left'][1], corner_points['lower_left'][1], corner_points['lower_right'][1], corner_points['upper_right'][1]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        return min_x, max_x, min_y, max_y
        
    def plot(self, edgecolor='gray', facecolor='silver', fill=True, line_width=1.5):
        plt.figure()
        fig = plt.gcf()
        ax = fig.gca()
        pos = self.position - 0.5*self.height*self.unit_normal
        ax.add_patch(plt.Rectangle(xy=(pos[0],pos[1]),
                                   width=self.width,
                                   height=self.height,
                                   angle=from_rad_to_deg(self.angle),
                                   edgecolor = edgecolor,
                                   facecolor = facecolor,
                                   fill=fill,
                                   lw=line_width))
        min_x, max_x, min_y, max_y = self.bounding_box
        dx = abs(max_x - min_x)
        dy = abs(max_y - min_y)
        kx = dy/10
        ky = dx/10
        plt.xlim([min_x - kx*dx, max_x + kx*dx])
        plt.ylim([min_y - ky*dy, max_y + ky*dy])
        plt.grid()
        ax.set_aspect('equal', adjustable='box')
        plt.show()

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(width={self.width}, height={self.height}, position={self.position}, angle(deg)={from_rad_to_deg(self.angle)})"

    def __str__(self) -> str:
        return f"Rectangle of width {self.width} and height {self.height}, placed at {self.position} and oriented {from_rad_to_deg(self.angle)} degrees"

    def move(self, displacement):
        self.position += np.array(displacement)

    def rotate(self, rotation_point, angle):
        rotation_angle = from_deg_to_rad(angle)
        self.angle += rotation_angle

        rotation_point = np.array(rotation_point)

        # Calculate the rotation matrix
        rotation_matrix = np.array([
            [np.cos(rotation_angle), -np.sin(rotation_angle)],
            [np.sin(rotation_angle), np.cos(rotation_angle)]
        ])

        # Translate the reference point to the origin relative to the rotation point
        translated_ref_point = self.position - rotation_point
        
        # Apply the rotation
        rotated_point = rotation_matrix.dot(translated_ref_point)
        
        # Translate back to the original coordinate system
        self.position = rotated_point + rotation_point
        
        
        


class RectanglesBasedGeometry:
    def __init__(self, rectangles):
        self.components = rectangles

    @property
    def area(self):
        a = 0.0
        for rect in self.components:
            a += rect.area
        return a

    @property
    def centroid(self):
        a = 0.0
        c = np.array([0.0, 0.0])
        for rect in self.components:
            a += rect.area
            c += rect.centroid * rect.area
        return c / a

    @property
    def inertia(self):
    # area inertia with respect to centroid axes of the compound geometry
        centroid = self.centroid
        Iy, Iz, Ix, Iyz = 0.0, 0.0, 0.0, 0.0
        for rect in self.components:
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
        return f"{class_name}(rectangles={self.components})"
    
    def __str__(self) -> str:
        msg = ''
        for i, rect in enumerate(self.components):
            msg += f"Rectangle {i+1}: {rect}\n"
        return msg

    @property
    def bounding_box(self):
        xs, ys = [], []
        for rect in self.components:
            min_x, max_x, min_y, max_y = rect.bounding_box
            xs.append(min_x)
            xs.append(max_x)
            ys.append(min_y)
            ys.append(max_y)
        min_x, max_x, min_y, max_y = min(xs), max(xs), min(ys), max(ys)
        return min_x, max_x, min_y, max_y
                    
    def plot(self, edgecolor='gray', facecolor='silver', fill=True, line_width=1.5):    
        plt.figure()
        fig = plt.gcf()
        ax = fig.gca()
        for rect in self.components:
            pos = rect.position - 0.5*rect.height*rect.unit_normal
            patch_rect = matplotlib.patches.Rectangle(xy=(pos[0],pos[1]),
                                                            width=rect.width,
                                                            height=rect.height,
                                                            angle= from_rad_to_deg(rect.angle),
                                                            edgecolor = edgecolor,
                                                            facecolor = facecolor,
                                                            fill=fill,
                                                            lw=line_width)
            ax.add_patch(patch_rect)
        min_x, max_x, min_y, max_y = self.bounding_box
        dx = abs(max_x - min_x)
        dy = abs(max_y - min_y)
        kx = dy/10
        ky = dx/10
        plt.xlim([min_x - kx*dx, max_x + kx*dx])
        plt.ylim([min_y - ky*dy, max_y + ky*dy])
        plt.grid()
        ax.set_aspect('equal', adjustable='box')
        plt.show()

    def move(self, displacement):
        for rect in self.components:
            rect.move(displacement)

    def rotate(self, center, angle):
        for rect in self.components:
            rect.rotate(center, angle)


def from_rad_to_deg(rad):
    return round(rad * (180.0/np.pi), 6)

def from_deg_to_rad(deg):
    return round(deg * (np.pi/180.0), 6)

if __name__ == "__main__":
    
    def test0():
        deg = 180
        print(f"{deg} degrees in radians is {from_deg_to_rad(deg)}")

        rad = np.pi/2
        print(f"{rad} rad in degrees is {from_rad_to_deg(rad)}")

    def test1():
        thickness = 25.4
        height = 300
        keel = Rectangle(width=height, height=thickness, position=[0,0], angle=90)
        print(keel)
        print(keel.section_properties)
        print(repr(keel))
        keel.plot()
        
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
        angle_section.plot()
    
    def test3():
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
        
        print(rect2.corner_points)
        print(rect2.bounding_box)
        print(angle_section)
        angle_section.plot()

    def test4():
        thickness = 25.4
        height = 300
        keel = Rectangle(width=height, height=thickness, position=[0,0], angle=90)
        print(keel)
        print(keel.section_properties)
        print(repr(keel))
        keel.plot()
        keel.move([500, 0])
        print(keel)
        keel.plot()

    def test5():
        thickness = 25.4
        height = 300
        keel = Rectangle(width=height, height=thickness, position=[0,0], angle=90)
        keel.plot()
        keel.rotate(center=[0,150], angle=-45)
        keel.plot()

    def test6():
        rect1 = Rectangle(width=40, height=10, position=[0, 5], angle=0)
        rect2 = Rectangle(width=40, height=10, position=[5, 10], angle=90)
        angle_section = RectanglesBasedGeometry([rect1, rect2])
        angle_section.plot()
        angle_section.move([100, 100])
        angle_section.plot()

    def test7():
        rect1 = Rectangle(width=80, height=10, position=[0, 5], angle=0)
        rect2 = Rectangle(width=40, height=10, position=[5, 10], angle=90)
        angle_section = RectanglesBasedGeometry([rect1, rect2])
        angle_section.plot()
        angle_section.rotate(center=[0,0], angle=45)
        angle_section.plot()

    test7()
        




    
    