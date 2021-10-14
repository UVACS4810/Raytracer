import abc
import dataclasses
import numpy as np

import src.colors as colors
import src.shapes as shapes
import src.utils as utils
class Light(abc.ABC):
    pass

@dataclasses.dataclass
class Sun(Light):
    x: float
    y: float
    z: float
    color: colors.RGBLinear

    def lambert(self, ray: shapes.Ray, normal: np.ndarray, object_color: colors.RGBLinear):
        light_color_as_vector = np.array(utils.object_to_list(self.color))
        shape_color_as_vector = np.array(utils.object_to_list(object_color))
        
        new_color_as_vector: np.ndarray = shape_color_as_vector * light_color_as_vector * max(np.dot(ray.direction, normal), 0)
        return colors.RGBLinear(*(new_color_as_vector.tolist()))
