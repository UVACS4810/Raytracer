
import math
from typing import Optional, Tuple

import numpy as np
from PIL import Image
from src import utils

import src.colors as colors
import src.scene as scene
import src.shapes as shapes


def make_eye_ray(x: float, y: float, meta: scene.SceneMata) -> Optional[shapes.Ray]:
    """Makes a ray starting at the eye

    Args:
        x (float): the pixel value for the column
        y (float): the pixel value for the row
        meta (scene.SceneMata): Metadata about the scene

    Returns:
        shapes.Ray: A ray with normalized direction
    """
    s_x, s_y = make_flat_projection(x, y, meta)
    if meta.lense == scene.Lense.normal:
        ray_direction = meta.forward + s_x * meta.right + s_y * meta.up
    elif meta.lense == scene.Lense.fisheye:
        # 1) divide s_x and s_y​ by the length of forward, and thereafter use a 
        # normalized forward vector for this computation.
        len_of_forward = np.linalg.norm(meta.forward)
        s_x = s_x / len_of_forward
        s_y = s_y / len_of_forward
        # 2) let r^2 = s_x^2 + s_y^2
        r_sqr = s_x**2 + s_y**2
        # 3) if r> 1 then don't shoot any rays
        if math.sqrt(r_sqr) > 1:
            return None
        # 4) otherwise, use s_x * right, s_y * up, and sqrt(1-r^2)*forward
        ray_direction = math.sqrt(1-r_sqr) * meta.forward + s_x * meta.right + s_y * meta.up
    elif meta.lense == scene.Lense.panorama:
        raise NotImplementedError
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

def lerp(p1: np.ndarray, p2: np.ndarray, t: float) -> np.ndarray:
    """performs linear interpolation between two np.ndarrays
    Args:
        p1 (np.ndarray): point containing some collection of values
        p2 (np.ndarray): point containing some collection of values
        t (float): goes from 0.0 to 1.0
    Returns:
        np.ndarray: [description]
    """
    return p1 + ((p2 - p1) * t)

def make_reflection_ray(incident: shapes.Ray, normal: shapes.Ray, origin: np.ndarray) -> shapes.Ray:
    direction = incident.direction - 2 * np.dot(incident.direction, normal.direction) * normal.direction
    return shapes.Ray(origin, direction)

def trace_ray(ray: shapes.Ray, objects: scene.SceneObjects, meta: scene.SceneMata, depth = 0) -> colors.RGBLinear:
    closest_shape = None
    distance_to_closest_shape = math.inf
    for shape in objects.shapes:
        distance_to_shape = shape.intersection(ray)
        if distance_to_shape:
            if distance_to_shape < distance_to_closest_shape:
                distance_to_closest_shape = distance_to_shape
                closest_shape = shape
    pixel_color = colors.RGBLinear(0.0, 0.0, 0.0)
    if closest_shape:
        # calculate the point of intersection
        point_of_intersection = meta.eye + (distance_to_closest_shape*ray.direction)
        # find the normal of the shape at the point of intersection
        normal = closest_shape.normal_at_point(point_of_intersection)
        for light in objects.lights:
            # make a ray to the light source 
            ray_to_light_direction = light.point - point_of_intersection
            distance_to_light = np.linalg.norm(ray_to_light_direction)
            ray_to_light = shapes.Ray(point_of_intersection, ray_to_light_direction)
            # check for shadows
            has_shadow = False
            for shape in objects.shapes:
                shape_distance = shape.intersection(ray_to_light)
                if shape_distance:
                    if shape_distance < distance_to_light:
                        has_shadow == True

            if not has_shadow:
                color_from_light = light.lambert(
                    ray=ray_to_light,
                    normal=normal,
                    object_color=closest_shape.color,
                )
            else:
                color_from_light = colors.RGBLinear()
            # add the color from the light to the current pixel color
            if color_from_light:
                pixel_color += color_from_light
            # Check for reflection
            if closest_shape.shininess != 0.0 and depth < meta.reflection_depth:
                reflection_ray = make_reflection_ray(ray, normal, point_of_intersection)
                color_from_reflection = trace_ray(reflection_ray, objects, meta, depth + 1)
                # Calculate the mix of the color from the standard light and the color from reflection
                pixel_color = lerp(pixel_color.as_ndarray(), color_from_reflection.as_ndarray(), closest_shape.shininess)

    return pixel_color
    

def raytrace_scene(objects: scene.SceneObjects, meta: scene.SceneMata, image: Image) -> None:
    for x in range(meta.width):
        for y in range(meta.height):
            # Make the ray

            ray_from_eye = make_eye_ray(x, y, meta)
            if not ray_from_eye:
                continue
            pixel_color = trace_ray(ray_from_eye, objects, meta)
            # Apply the exposure function to the linear color
            pixel_color.apply_exposure(meta.exposure_function)
            # convert to color to sRGB
            converted_color = pixel_color.as_rgb(rounded=True)
            image.im.putpixel((x, y), (converted_color.r, converted_color.g, converted_color.b, converted_color.a))

