import os
import cv2
from pathlib import Path

# Configuration Variables
piece_name = "Queen" # Set this to the piece type you're labeling: "King", "Queen", "Empty", etc.
skip_existing = True  # Set to True to skip files already labeled
piece_exclude = ["Empty", "Pawn", "Knight", "Rook", "Bishop", "King"]
filename_exclude = ["-ZVbDR3sRRo", "3I_ESQVyxNc", "65VWIFlc4C4"]

# Key Bindings
YES_KEY = ord('y')  # Press 'y' for Yes
NO_KEY = ord('u')   # Press 'u' for No 
BACK_KEY = ord('b')  # Press 'b' to go back to the previous image
EXIT_KEY = ord('q')  # Press 'q' to quit the labeling session

# Paths
dataset_dir = "dataset"

def is_already_labeled(filename):
    """Check if the file is already labeled with the specified piece name."""
    return piece_name in filename or any((n in filename) for n in piece_exclude) or any((n in filename) for n in filename_exclude)

def label_images():
    """Display images one by one for labeling and rename them based on user input."""
    # Gather all file paths in a list for easy indexingq
    image_files = []
    for subdir, _, files in os.walk(dataset_dir):
        for file in files:
            filepath = os.path.join(subdir, file)
            if not (skip_existing and is_already_labeled(file)):
                image_files.append(filepath)

    # Start labeling
    index = 0
    while index < len(image_files):
        filepath = image_files[index]
        file = os.path.basename(filepath)

        # Load and display the image
        image = cv2.imread(filepath)
        if image is None:
            print(f"Unable to load image: {filepath}")
            index += 1
            continue

        cv2.destroyAllWindows()
        cv2.imshow("Labeling Tool", image)
        print(f"Labeling {file}. Is this a {piece_name}? (y/n), go back (b)")

        # Wait for a key press
        key = cv2.waitKey(0)

        # Handle key press
        if key == YES_KEY:
            # Rename the file with the specified piece name
            new_filename = f"{Path(file).stem}_Piece{piece_name}{Path(file).suffix}"
            new_filepath = os.path.join(Path(filepath).parent, new_filename)
            os.rename(filepath, new_filepath)
            print(f"Renamed to {new_filename}")
            # Move forward
            index += 1

        elif key == NO_KEY:
            print("Skipped.")
            # Move forward
            index += 1

        elif key == BACK_KEY:
            print("Going back...")
            # Move backward but ensure it doesn't go below zero
            index = max(0, index - 1)

        elif key == EXIT_KEY:
            print("Exiting...")
            cv2.destroyAllWindows()
            return

    print("Labeling completed.")
    cv2.destroyAllWindows()

if __name__ == "__main__":
    label_images()
