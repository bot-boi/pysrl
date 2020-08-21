class InterfaceNode:
    # bounds is related to client dimensions
    def __init__(self, bounds: Box, modifier: float):
        self.bounds = bounds
        self.modifier = modifier


class Interface:
    def __init__(self):

