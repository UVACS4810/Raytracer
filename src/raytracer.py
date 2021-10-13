
import dataclasses
from src.shapes import Shape

@dataclasses.dataclass
class SceneInfo():
    """Will store information about things that need to be rendered in the scene
    """
    shapes: "list[Shape]" = []

def raytrace_scene()
