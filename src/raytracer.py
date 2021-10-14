
import dataclasses
from typing import Tuple
import numpy as np
from PIL import Image
import math
import src.scene as scene
import src.shapes as shapes
import src.colors as colors
def make_eye_ray(x: float, y: float, meta: scene.SceneMata) -> shapes.Ray:
    """Makes a ray starting at the eye

    Args:
        x (float): the pixel value for the column
        y (float): the pixel value for the row
        meta (scene.SceneMata): Metadata about the scene

    Returns:
        shapes.Ray: A ray with normalized direction
    """
    s_x, s_y = make_flat_projection(x, y, meta)
    ray_direction = meta.forward + s_x * meta.right + s_y * meta.up
    return shapes.Ray(meta.eye, ray_direction)

def make_flat_projection(x: float, y: float, meta: scene.SceneMata) -> Tuple[float, float]:
    """Converts pixel coordinates into the flat projection needed for absolute positioning

    Args:
        x (float): column pixel value
        y (float): row pixel value
        meta (scene.SceneMata): Metadata about the scene

    Returns:
        Tuple[float, float]: the flat projection for x, y
    """
    h_w_max = max(meta.height, meta.width)
    s_x = (2*x - meta.width)/h_w_max
    s_y = (meta.height- 2*y) / h_w_max
    return s_x, s_y

def raytrace_scene(objects: scene.SceneObjects, meta: scene.SceneMata, image: Image) -> None:
    for x in range(meta.width):
        for y in range(meta.height):
            # Make the ray

            ray = make_eye_ray(x, y, meta)
            closest_shape = None
            current_closest = math.inf
            for shape in objects.shapes:
                distance_to_shape = shape.intersection(ray)
                if distance_to_shape:
                    if distance_to_shape < current_closest:
                        current_closest = distance_to_shape
                        closest_shape = shape
            
            if closest_shape:
                pixel_color = colors.RGBLinear(0.0, 0.0, 0.0)
                for light in objects.lights:
                    # find the normal of the 
                    
                # convert to color to sRGB
                converted_color = pixel_color.as_rgb()
                image.im.putpixel((x, y), (converted_color.r, converted_color.g, converted_color.b, converted_color.a))

