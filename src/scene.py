import dataclasses
import math
from typing import Callable
from src.shapes import Shape
import numpy as np
import src.colors as colors
import src.light as light

@dataclasses.dataclass
class SceneMata():
    """contains information that will need to last for the lifecycle of the image
    \b eye: A point, and thus not normalized.
    \b forward: . A vector, but not normalized: longer forward vectors make for a narrow field of view.
    \b right: A normalized vector.
    \b up: A normalized vector.
    """
    height: int
    width: int
    color: colors.RGBLinear = colors.RGBLinear(1.0, 1.0, 1.0)
    eye: np.ndarray = np.array([0, 0, 0])
    forward: np.ndarray = np.array([0,0,-1])
    right: np.ndarray = np.array([1,0,0])
    up: np.ndarray = np.array([0,1,0])
    exposure_function: Callable[[float], float] = lambda x: x 
    def clear(self):
        """Used to wipe info that will not cary over to the next image in the animation
        """
        self.color = colors.RGBLinear(1.0, 1.0, 1.0)

@dataclasses.dataclass
class SceneObjects():
    """Will store information about things that need to be rendered in the scene
    """
    shapes: "list[Shape]" = dataclasses.field(default_factory=list)
    lights: "list[light.Light]" = dataclasses.field(default_factory=list)