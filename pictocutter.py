import os
from PIL import Image

def PictoCutter(MapName, CoachCount, ResizeAgain=True):
    input_folder = os.path.join(os.path.dirname(__file__), "input")
    css_file_path = os.path.join(input_folder, "pictos-sprite.css")
    png_file_path = os.path.join(input_folder, "pictos-sprite.png")

    output_dir = os.path.join("output", MapName)
    os.makedirs(output_dir, exist_ok=True)

    # Read the CSS file
    with open(css_file_path, "r", encoding="utf-8") as css_file:
        css = css_file.readlines()

    # Load the atlas image
    atlas = Image.open(png_file_path)
    atlas_width, atlas_height = atlas.size
    
    # Frame dimensions for each pictogram
    frame_width = frame_height = 256  # Each pictogram is 256x256
    
    # Starting coordinates
    x = 0
    y = 0
    
    for line in css:
        if '-' in line and '{' in line:  # Filter CSS picto entries
            PictoName = line.split("-")[1].split("{")[0].strip()
            # Ensure we don't exceed image boundaries
            if x + frame_width > atlas_width:
                x = 0
                y += frame_height

            # Crop and resize each frame
            picto = atlas.crop((x, y, x + frame_width, y + frame_height))
            if ResizeAgain:
                picto = picto.resize((256, 256))  # Ensure output is 256x256
            picto.save(os.path.join(output_dir, f"{PictoName}.png"))

            x += frame_width  # Move to the next frame horizontally
    
    print("Done: Pictos saved to", output_dir)

# Prompt the user for Codename and Picto Count
if __name__ == "__main__":
    MapName = input("Song codename: ").strip()
    CoachCount = input("Picto Count: ").strip()
    PictoCutter(MapName, int(CoachCount))
