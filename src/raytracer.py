
import math
from typing import Tuple

import numpy as np
from PIL import Image

import src.colors as colors
import src.scene as scene
import src.shapes as shapes


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

            ray_from_eye = make_eye_ray(x, y, meta)
            closest_shape = None
            current_closest = math.inf
            for shape in objects.shapes:
                distance_to_shape = shape.intersection(ray_from_eye)
                if distance_to_shape:
                    if distance_to_shape < current_closest:
                        current_closest = distance_to_shape
                        closest_shape = shape
            
            if closest_shape:
                # calculate the point of intersection
                point_of_intersection = meta.eye + (current_closest*ray_from_eye.direction)
                # find the normal of the shape at the point of intersection
                pixel_color = colors.RGBLinear(0.0, 0.0, 0.0)
                normal = closest_shape.normal_at_point(point_of_intersection)
                for light in objects.lights:
                    # make a ray to the light source 
                    ray_to_light_direction = light.point - point_of_intersection
                    ray_to_light = shapes.Ray(point_of_intersection, ray_to_light_direction)
                    color_from_light = light.lambert(
                        ray=ray_to_light,
                        normal=normal,
                        object_color=closest_shape.color,
                    )
                    # add the color from the light to the current pixel color
                    if color_from_light:
                        pixel_color += color_from_light
                # Apply the exposure function to the linear color
                pixel_color.apply_exposure(meta.exposure_function)
                # convert to color to sRGB
                converted_color = pixel_color.as_rgb(rounded=True)
                image.im.putpixel((x, y), (converted_color.r, converted_color.g, converted_color.b, converted_color.a))

