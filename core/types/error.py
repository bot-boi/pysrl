class NumpyShapeError(Exception):
    def __init__(self, xpshape: str, shape: tuple,
                 message='''Expected numpy ndarray with shape {},
                         got {] instead'''):
        super().__init__(message.format(xpshape, shape))
