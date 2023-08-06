import Part as PartModule


# AppPartPy.cpp
def sameParameter(shape: PartModule.Shape, enforce: bool, prec: float = 0.0, /) -> bool:
    """
    sameParameter(shape, enforce, prec=0.0)
    Possible exceptions: (Exception).
    """


def encodeRegularity(shape: PartModule.Shape, tolerance: float = 1e-10, /) -> None:
    """
    encodeRegularity(shape, tolerance = 1e-10)

    Possible exceptions: (Exception).
    """


def removeSmallEdges(arg1: PartModule.Shape, arg2: float, /) -> PartModule.Shape:
    """
    removeSmallEdges(shape, tolerance, ReShapeContext)
    Removes edges which are less than given tolerance from shape
    Possible exceptions: (Exception).
    """


def fixVertexPosition(arg1: PartModule.Shape, arg2: float, /) -> bool:
    """
    fixVertexPosition(shape, tolerance, ReShapeContext)
    Fix position of the vertices having tolerance more tnan specified one
    Possible exceptions: (Exception).
    """


def leastEdgeSize(shape: PartModule.Shape, /) -> float:
    """
    leastEdgeSize(shape)
    Calculate size of least edge
    Possible exceptions: (Exception).
    """
