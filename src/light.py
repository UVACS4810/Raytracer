import abc
import dataclasses

import numpy as np

import src.colors as colors
import src.shapes as shapes
import src.utils as utils

@dataclasses.dataclass
class Light(abc.ABC):
    point: np.ndarray
    color: colors.RGBLinear

    @abc.abstractmethod
    def lambert(self, ray: shapes.Ray, normal: np.ndarray, object_color: colors.RGBLinear) -> colors.RGBLinear:
        raise NotImplementedError

@dataclasses.dataclass
class Sun(Light):
    def lambert(self, ray: shapes.Ray, normal: np.ndarray, object_color: colors.RGBLinear) -> colors.RGBLinear:
        real_ray = shapes.Ray(ray.origin, self.point)
        light_color_as_vector = np.array(utils.object_to_list(self.color))
        shape_color_as_vector = np.array(utils.object_to_list(object_color))
        
        new_color_as_vector: np.ndarray = shape_color_as_vector * light_color_as_vector * max(np.dot(real_ray.direction, normal), 0)
        return colors.RGBLinear(*(new_color_as_vector.tolist()))

@dataclasses.dataclass
class Bulb(Light):
    def lambert(self, ray: shapes.Ray, normal: np.ndarray, object_color: colors.RGBLinear) -> colors.RGBLinear:
        light_color_as_vector = np.array(utils.object_to_list(self.color))
        shape_color_as_vector = np.array(utils.object_to_list(object_color))
        
        new_color_as_vector: np.ndarray = shape_color_as_vector * light_color_as_vector * max(np.dot(ray.direction, normal), 0)
        distance_to_bulb = np.linalg.norm(self.point - ray.origin)
        new_color_as_vector *= 1/(distance_to_bulb**2)
        return colors.RGBLinear(*(new_color_as_vector.tolist()))