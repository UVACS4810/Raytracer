
import src.utils as utils
import src.vertex as vertex
import src.colors as colors
import src.scene as scene
import src.shapes as shapes

def get_image_info(line: str) -> utils.ImageInfo:
    """parses the first line of the file to get the metadata

    Args:
        line (str): the first line of a file

    Returns:
        ImageInfo: the input file metadata
    """
    line_as_list = utils.line_to_list(line)
    # Set the Image info
    image_info = utils.ImageInfo(
        width=int(line_as_list[1]),
        height=int(line_as_list[2]),
        filename=line_as_list[3],
    )
    # Set the values for the case in which we are making multiple png files
    if line_as_list[0] == "pngs":
        image_info.number_of_images = int(line_as_list[-1])

    return image_info

def get_vertex_by_index(verts, index: str) -> vertex.Vertex:
    if (index.strip("-")).isnumeric():
        index = int(index)
    else:
        raise Exception("The index of a vertex must be a number", index)
    # if its a negative index just use that idex
    if index < 0:
        return verts[index]
    return verts[index - 1]

def parse_line(line: "list[str]", scene_objects: scene.SceneObjects, scene_meta: scene.SceneMata) -> None:
    """
    parse keywords:
    \b color r g b:
    """
    keyword: str = line[0]
    ### DRAW DATA UPDATES ###
    if keyword == "color":
        r = float(line[1])
        g = float(line[2])
        b = float(line[3])
        scene_meta.color = colors.RGBLinear(r, g, b)
    
    elif keyword == "sphere":
        x = float(line[1])
        y = float(line[2])
        z = float(line[3])
        r = float(line[4])
        new_sphere = shapes.Sphere(x, y, z, r, scene_meta.color)
        scene_objects.shapes.append(new_sphere)
   
