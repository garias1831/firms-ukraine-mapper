from cmu_graphics import *

class VisualConfig:
    '''Global configuration for app visual state. Includes data such as primary/secondary colors.
    Attributes:
        bgcolor: tuple<int>. defines the background color for the UI.
    '''
    def __init__(self, _bgcolor):
        self.bgcolor = _bgcolor

