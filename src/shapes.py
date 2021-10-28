
import abc
import dataclasses
import math
from typing import Optional

import numpy as np

import src.colors as colors

@dataclasses.dataclass(unsafe_hash=True)
class Ray():
    origin: np.ndarray
    direction: np.ndarray

    def __post_init__(self):
        normal_of_direction = np.linalg.norm(self.direction)
        self.direction = self.direction / normal_of_direction
    def __str__(self) -> str:
        return str(self.origin) + str(self.direction)

@dataclasses.dataclass
class _ShapeBase:
    color: colors.RGBLinear
    shininess: float
    transparency: float
    roughness: float

@dataclasses.dataclass
class Shape(abc.ABC, _ShapeBase):
    @abc.abstractmethod
    def intersection(self, ray: Ray) -> Optional[float]:
        pass
    
    @abc.abstractmethod
    def normal_at_point(self, point: np.ndarray) -> np.ndarray:
        pass

@dataclasses.dataclass
class _SphereFields:
    center: np.ndarray
    radius: float

@dataclasses.dataclass
class Sphere(Shape, _SphereFields):
    """A sphere with center (x,y,z) and `radius`.
    """

    def intersection(self, ray: Ray) -> Optional[float]:
        """"""
        """Will find an intersection or fail

        Args:
            ray (Ray): The ray that will potentially intersect the sphere

        Returns:
            float: distance to intersection point from origin
        """
        assert np.shape(self.center) == np.shape(ray.origin)
        is_inside: bool = (np.linalg.norm(self.center - ray.origin) ** 2) < self.radius ** 2
        t_c = np.dot((self.center - ray.origin), ray.direction)/np.linalg.norm(ray.direction)
        if not is_inside and t_c < 0:
            return
        d_sqr = np.linalg.norm(ray.origin + (t_c * ray.direction) - self.center)**2
        if not is_inside and d_sqr > self.radius**2:
            return
        t_offset = math.sqrt(self.radius**2 - d_sqr)/np.linalg.norm(ray.direction)
        if is_inside:
            return t_c + t_offset
        else:
            return t_c - t_offset

    def normal_at_point(self, point: np.ndarray) -> np.ndarray:
        # TODO: Figure out a better way to ensure point shape
        assert point.shape == (3,)
        normal = point - self.center
        normalized_normal = normal / np.linalg.norm(normal)
        # apply gausian roughness
        gausian_normal = np.random.normal(normalized_normal, self.roughness)
        # Renormalize
        return gausian_normal / np.linalg.norm(gausian_normal)