import numpy as np
import matplotlib.pyplot as plt
import matplotlib


class Rectangle:
    def __init__(self, width, height, position, angle): 
        """This class represents a rectangle, which is defined based upon its dimensions, position and orientation

        Args:
            width (float): width
            height (float): height
            position (array-like): position with respect to the universal axis
            angle (float): angle in degrees, with respect to the horizontal, positive counterclockwise
        """
        self.width = width
        self.height = height
        self.position = np.array(position)
        self.angle = angle 
    
    @property 
    def unit_direction(self):
        """Unit direction vector of the rectangle"""
        return np.array([np.cos(np.radians(self.angle)), np.sin(np.radians(self.angle))])
        
    @property
    def unit_normal(self):
        """Unit normal vector of the rectangle"""
        return np.array([-np.sin(np.radians(self.angle)), np.cos(np.radians(self.angle))])

    @property
    def area(self):
        """Area of the rectangle"""
        return self.width * self.height
    
    @property
    def centroid(self):
        """Centroid of the rectangle"""
        return self.position + self.unit_direction * self.width/2.0
    
    @property
    def inertia(self):
        """Moments of inertia of the rectangle"""

        # moment of inertia with respect to rotated centroidal axes
        Iy = ((self.width)*(self.height**3))/12
        Iz = ((self.height)*(self.width**3))/12

        # centroidal polar moment of inertia 
        Ix = Iy + Iz

        # centroidal product moment of inertia
        Iyz = 0.0

        # moment of inertia with respect to axes paralell to the cartesian axes, centered on the centroid
        Iyp = 0.5*(Iy + Iz) + 0.5*(Iy - Iz)*np.cos(-2*np.radians(self.angle))  
        Izp = 0.5*(Iy + Iz) - 0.5*(Iy - Iz)*np.cos(-2*np.radians(self.angle))
        Iyzp = 0.5*(Iy - Iz)*np.sin(-2*np.radians(self.angle)) 
        return dict(Iy=Iy, Iz=Iz, Ix=Ix,  Iyz=Iyz,  Iyp=Iyp, Izp=Izp, Iyzp=Iyzp)
    
    def compute_inertia_wrt_parallel_axes(self, axes_center):
        # computation of the moments of inertia with respect to axes parallel to the (cartesian) centroidal axes
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
        """Corner points of the rectangle"""
        upper_left = self.position + 0.5*self.height * self.unit_normal
        lower_left = self.position - 0.5*self.height * self.unit_normal
        lower_right = lower_left + self.width * self.unit_direction
        upper_right = upper_left + self.width * self.unit_direction
        points=dict(upper_left=upper_left, lower_left=lower_left, lower_right=lower_right, upper_right=upper_right)
        return points

    @property
    def bounding_box(self):
        """bounding box of the rectangle"""
        corner_points = self.corner_points
        xs = corner_points['upper_left'][0], corner_points['lower_left'][0], corner_points['lower_right'][0], corner_points['upper_right'][0]
        ys = corner_points['upper_left'][1], corner_points['lower_left'][1], corner_points['lower_right'][1], corner_points['upper_right'][1]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        return min_x, max_x, min_y, max_y
    
    def patch(self, edgecolor='gray', facecolor='silver', fill=True, line_width=1.5):
        pos = self.position - 0.5*self.height*self.unit_normal
        return plt.Rectangle(xy=(pos[0],pos[1]),
                                   width=self.width,
                                   height=self.height,
                                   angle=self.angle,
                                   edgecolor = edgecolor,
                                   facecolor = facecolor,
                                   fill=fill,
                                   lw=line_width)

    def plot(self, edgecolor='gray', facecolor='silver', fill=True, line_width=1.5, zoom_factor=10):
        fig = plt.gcf()
        ax = fig.gca()
        ax.add_patch(self.patch(edgecolor, facecolor, fill, line_width))
        
        min_x, max_x, min_y, max_y = self.bounding_box
        dx, dy = abs(max_x - min_x), abs(max_y - min_y)
        kx, ky = dy/zoom_factor, dx/zoom_factor
        
        plt.xlim([min_x - kx*dx, max_x + kx*dx])
        plt.ylim([min_y - ky*dy, max_y + ky*dy])
        plt.grid()
        plt.tight_layout()
        ax.set_aspect('equal', adjustable='box')
        plt.show()
        
    def __repr__(self):
        class_name = type(self).__name__
        if self.angle >= 360:
            self.angle = self.angle - 360
        return f"{class_name}(width={self.width}, height={self.height}, position={self.position}, angle(deg)={self.angle})"

    def __str__(self) -> str:
        if self.angle >= 360:
            self.angle = self.angle - 360
        return f"Rectangle of width {self.width} and height {self.height}, placed at {self.position} and oriented {self.angle} degrees"

    def move(self, displacement):
        """move the rectangle"""
        self.position += np.array(displacement)

    def rotate(self, rotation_point, angle):
        """rotate the rectangle"""
        self.angle += angle

        rotation_point = np.array(rotation_point)
        rotation_angle = np.radians(angle)
        
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
        #return self.position, self.angle

        
class RectanglesBasedGeometry:
    """This class is used to represent a single geometry compound of rectangles
    """
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

    def compute_inertia_wrt_paralell_axes(self, axes_center):
        # area inertia with respect to parallel axes of the compound geometry
        Iy, Iz, Ix, Iyz = 0.0, 0.0, 0.0, 0.0
        for rect in self.components:
            Irect = rect.compute_inertia_wrt_parallel_axes(axes_center)
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
                    
    def plot(self, edgecolor='gray', facecolor='silver', fill=True, line_width=1.5, zoom_factor=10):    
        fig = plt.gcf()
        ax = fig.gca()
        
        for rect in self.components:
            ax.add_patch(rect.patch(edgecolor, facecolor, fill, line_width))
        
        min_x, max_x, min_y, max_y = self.bounding_box
        dx, dy = abs(max_x - min_x), abs(max_y - min_y)
        kx, ky = dy/zoom_factor, dx/zoom_factor
        
        plt.xlim([min_x - kx*dx, max_x + kx*dx])
        plt.ylim([min_y - ky*dy, max_y + ky*dy])
        plt.grid()
        plt.tight_layout()
        ax.set_aspect('equal', adjustable='box')
        plt.show()

    def move(self, displacement):
        for rect in self.components:
            rect.move(displacement)

    def rotate(self, rotation_point, angle):
        for rect in self.components:
            rect.rotate(rotation_point, angle)


class RectanglesBasedGeometries:
    def __init__(self, geometries) -> None:
        self.geometries = geometries

    @property
    def area(self):
        a = 0.0
        for geometry in self.geometries:
            for rect in geometry.components:
                a += rect.area
        return a

    @property
    def centroid(self):
        a = 0.0
        c = np.array([0.0, 0.0])
        for geometry in self.geometries:
            for rect in geometry.components:
                a += rect.area
                c += rect.centroid * rect.area
        return c/a

    @property
    def inertia(self):
    # area inertia with respect to centroid axes of the set of geometries
        centroid = self.centroid
        Iy, Iz, Ix, Iyz = 0.0, 0.0, 0.0, 0.0
        for geometry in self.geometries:
            for rect in geometry.components:
                Irect = rect.compute_inertia_wrt_parallel_axes(centroid)
                Iy += Irect['Iya']
                Iz += Irect['Iza']
                Ix += Irect['Ixa']
                Iyz += Irect['Iyza']
        return dict(Iy=Iy, Iz=Iz, Ix=Ix, Iyz=Iyz)    
    
    def compute_inertia_wrt_parallel_axes(self, axes_center):
        Iy, Iz, Ix, Iyz = 0.0, 0.0, 0.0, 0.0
        for geometry in self.geometries:
            for rect in geometry.components:
                Irect = rect.compute_inertia_wrt_parallel_axes(axes_center)
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

    @property
    def bounding_box(self):
        xs, ys = [], []
        for geometry in self.geometries:
            for rect in geometry.components:
                min_x, max_x, min_y, max_y = rect.bounding_box
                xs.append(min_x)
                xs.append(max_x)
                ys.append(min_y)
                ys.append(max_y)   
        min_x, max_x, min_y, max_y = min(xs), max(xs), min(ys), max(ys)
        return min_x, max_x, min_y, max_y
                    
    def plot(self, edgecolor='gray', facecolor='silver', fill=True, line_width=1.5, zoom_factor=10):    
        fig = plt.gcf()
        ax = fig.gca()
        
        for geometry in self.geometries:
            for rect in geometry.components:
                ax.add_patch(rect.patch(edgecolor, facecolor, fill, line_width))
                
        min_x, max_x, min_y, max_y = self.bounding_box
        dx, dy = abs(max_x - min_x), abs(max_y - min_y)
        kx, ky = dy/zoom_factor, dx/zoom_factor
        
        plt.xlim([min_x - kx*dx, max_x + kx*dx])
        plt.ylim([min_y - ky*dy, max_y + ky*dy])
        plt.grid()
        plt.tight_layout()
        ax.set_aspect('equal', adjustable='box')
        plt.show()

    def __str__(self) -> str:
        msg = ''
        for i, geometry in enumerate(self.geometries):
            msg += f"Geometry {i+1}:\n"
            for rect in geometry.components:
                msg += f"{rect}\n"
        return msg


if __name__ == "__main__":
    
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
        print(angle_section.compute_inertia_wrt_paralell_axes(axes_center=angle_section.centroid))

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
        keel.rotate(rotation_point=[0,0], angle=-45)
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
        angle_section.rotate(rotation_point=[0,0], angle=45)
        angle_section.plot()

    def test8():
        thickness = 25.4
        height = 300
        keel = Rectangle(width=height, height=thickness, position=[0,0], angle=90)
        print(keel)
        print(keel.section_properties)
        print(repr(keel))
        keel.plot()
        keel.width = 500
        print(keel)
        print(keel.section_properties)
        print(repr(keel))
        keel.plot()

    def test9():
        rect1 = Rectangle(width=40, height=10, position=[0, 5], angle=0)
        rect2 = Rectangle(width=40, height=10, position=[5, 10], angle=90)
        angle_section1 = RectanglesBasedGeometry([rect1, rect2])

        rect3 = Rectangle(width=40, height=10, position=[50, 5], angle=0)
        rect4 = Rectangle(width=40, height=10, position=[55, 10], angle=90)
        angle_section2 = RectanglesBasedGeometry([rect3, rect4])

        geometry = RectanglesBasedGeometries([angle_section1, angle_section2])
        print(geometry)
        print(geometry.section_properties)
        geometry.plot()
        

        angle_section1.rotate(rotation_point=[0,0], angle=180)
        print(geometry)
        print(geometry.section_properties)
        geometry.plot()


        

    test9()




    
    