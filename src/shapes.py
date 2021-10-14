
import abc
import dataclasses
import math

import numpy as np

import src.colors as colors

@dataclasses.dataclass
class Ray():
    origin: np.ndarray
    direction: np.ndarray


class Shape(abc.ABC):

    @abc.abstractclassmethod
    def intersection(self, ray: Ray) -> float:
        pass


@dataclasses.dataclass
class Sphere(Shape):
    """A sphere with center (x,y,z) and `radius`.
    """
    x: float
    y: float
    z: float
    radius: float
    color: colors.RGBLinear

    def intersection(self, ray: Ray) -> float or None:
        """"""
        """Will find an intersection or fail

        Args:
            ray (Ray): The ray that will potentially intersect the sphere

        Returns:
            float: distance to intersection point from origin
        """
        circle_center = np.array([self.x, self.y, self.z])
        assert np.shape(circle_center) == np.shape(ray.origin)
        is_inside: bool = (np.linalg.norm(circle_center - ray.origin) ** 2) < self.radius ** 2
        t_c = np.dot((circle_center - ray.origin), ray.direction)/np.linalg.norm(ray.direction)
        if not is_inside and t_c < 0:
            return
        d_sqr = np.linalg.norm(ray.origin + (t_c * ray.direction) - circle_center)**2
        if not is_inside and d_sqr > self.radius**2:
            return
        t_offset = math.sqrt(self.radius**2 - d_sqr)/np.linalg.norm(ray.direction)
        if is_inside:
            return t_c + t_offset
        else:
            return t_c - t_offset        



