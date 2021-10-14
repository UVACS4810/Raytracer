
import dataclasses

from PIL import Image
import math
import src.scene as scene
import src.shapes as shapes
import src.colors as colors
def make_ray(x: float, y: float, meta: scene.SceneMata) -> shapes.Ray:
    h_w_max = max(meta.height, meta.width)
    s_x = (2*x - meta.width)/h_w_max
    s_y = (meta.height- 2*y) / h_w_max
    ray_direction = meta.forward + s_x * meta.right + s_y * meta.up
    return shapes.Ray(meta.eye, ray_direction)


def raytrace_scene(objects: scene.SceneObjects, meta: scene.SceneMata, image: Image) -> None:
    for x in range(meta.width):
        for y in range(meta.height):
            # Make the ray
            ray = make_ray(x, y, meta)
            closest_shape = None
            current_closest = math.inf
            for shape in objects.shapes:
                distance_to_shape = shape.intersection(ray)
                if distance_to_shape:
                    if shape.x == 1:
                        print("hello")
                    if distance_to_shape < current_closest:
                        current_closest = distance_to_shape
                        closest_shape = shape
            
            if closest_shape:
                pixel_color = colors.RGBLinear(0.0, 0.0, 0.0)
                for light in objects.lights:
                    pass
                # convert to color to sRGB
                converted_color = pixel_color.as_rgb()
                image.im.putpixel((x, y), (converted_color.r, converted_color.g, converted_color.b, converted_color.a))

