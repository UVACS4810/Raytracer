import sys

import src.file_parse as file_parse
import src.utils as utils
import src.scene as scene

# Main method
if __name__ == "__main__":
    # get the file name
    args = sys.argv
    cmnd_line_args = utils.parse_args(args)

    # open the file
    with open(cmnd_line_args.file, "r") as file:
        lines = file.readlines()
        # Read the first line to determine meta info about the file
        first_line: str
        if lines:
            first_line = lines[0]
        else:
            raise Exception("Not Enough Lines")
        
        # Get the image info from the first line
        image_info = file_parse.get_image_info(first_line)
        draw_data = scene.SceneMata(
            height=image_info.height,
            width=image_info.width
        )
        if len(lines) > 1:
            for i in range(1, len(lines)):
                line = utils.line_to_list(lines[i])
                # If the line is empty, do nothing
                if not line:
                    pass
                else:
                    file_parse.parse_line(line, draw_data)

        # Save each of the files
        image = utils.make_images(image_info)[0]
        # Do the actual raytracing with the image and the 
        image.save(image_info.filename)
