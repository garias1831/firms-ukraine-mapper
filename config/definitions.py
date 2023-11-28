import os
#Used for loading assets using relative paths, such that assets such as images can be loaded without hardcoding
#An absolute path, which would def crash on other computers
#Thank you https://towardsdatascience.com/simple-trick-to-work-with-relative-paths-in-python-c072cdc9acb9
#Also, anywhere where you see a os.path.join can also be attributed to this source
ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__) , '..'))