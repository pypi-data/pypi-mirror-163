import typing

import FreeCAD
import Part as PartModule
import Part.ShapeFix


# ShapeFix_WireVertexPy.xml
class WireVertex(FreeCAD.PyObjectBase):
    """Fixing disconnected edges in the wire"""

    def __init__(self):
        """Fixing disconnected edges in the wire"""

    def fix(self) -> int:
        """
        Fixes all statuses except Disjoined, i.e. the cases in which a
        common value has been set, with or without changing parameters
        Returns the count of fixed vertices, 0 if none
        """

    def fixSame(self) -> int:
        """Returns the count of fixed vertices, 0 if none"""

    def init(self, arg1: PartModule.Wire, arg2: float, /):
        """Loads the wire, ininializes internal analyzer with the given precision"""

    def wire(self) -> PartModule.Shape:
        """Returns resulting wire"""


# ShapeFix_FaceConnectPy.xml
class FaceConnect(FreeCAD.PyObjectBase):
    """Rebuilds connectivity between faces in shell"""

    def __init__(self):
        """Rebuilds connectivity between faces in shell"""

    def add(self, face: PartModule.Face, face2: PartModule.Face, /):
        """add(face, face)"""

    def build(self, shell: PartModule.Shell, sewtolerance: float, fixtolerance: float, /) -> PartModule.Shape:
        """build(shell, sewtolerance, fixtolerance)"""

    def clear(self):
        """Clears internal data structure"""


# ShapeFix_ShapePy.xml
class Shape(Part.ShapeFix.Root):
    """Class for fixing operations on shapes"""

    def __init__(self, arg1: PartModule.Shape = None, /):
        """Class for fixing operations on shapes"""

    @property
    def FixFreeFaceMode(self) -> bool:
        """Mode for applying fixes of ShapeFix_Face"""

    @FixFreeFaceMode.setter
    def FixFreeFaceMode(self, value: bool): ...

    @property
    def FixFreeShellMode(self) -> bool:
        """Mode for applying fixes of ShapeFix_Shell"""

    @FixFreeShellMode.setter
    def FixFreeShellMode(self, value: bool): ...

    @property
    def FixFreeWireMode(self) -> bool:
        """Mode for applying fixes of ShapeFix_Wire"""

    @FixFreeWireMode.setter
    def FixFreeWireMode(self, value: bool): ...

    @property
    def FixSameParameterMode(self) -> bool:
        """Mode for applying ShapeFix::SameParameter after all fixes"""

    @FixSameParameterMode.setter
    def FixSameParameterMode(self, value: bool): ...

    @property
    def FixSolidMode(self) -> bool:
        """Mode for applying fixes of ShapeFix_Solid"""

    @FixSolidMode.setter
    def FixSolidMode(self, value: bool): ...

    @property
    def FixVertexPositionMode(self) -> bool:
        """Mode for applying ShapeFix::FixVertexPosition before all fixes"""

    @FixVertexPositionMode.setter
    def FixVertexPositionMode(self, value: bool): ...

    @property
    def FixVertexTolMode(self) -> bool:
        """Mode for fixing tolerances of vertices on whole shape"""

    @FixVertexTolMode.setter
    def FixVertexTolMode(self, value: bool): ...

    def fixEdgeTool(self) -> Part.ShapeFix.Edge:
        """Returns tool for fixing edges"""

    def fixFaceTool(self) -> Part.ShapeFix.Face:
        """Returns tool for fixing faces"""

    def fixShellTool(self) -> Part.ShapeFix.Shell:
        """Returns tool for fixing shells"""

    def fixSolidTool(self) -> Part.ShapeFix.Solid:
        """Returns tool for fixing solids"""

    def fixWireTool(self) -> Part.ShapeFix.Wire:
        """Returns tool for fixing wires"""

    def init(self, arg1: PartModule.Shape, /):
        """Initializes by shape"""

    def perform(self) -> bool:
        """Iterates on sub- shape and performs fixes"""

    def shape(self) -> Part.ShapeFix.Shape:
        """Returns resulting shape"""


# ShapeFix_EdgeConnectPy.xml
class EdgeConnect(FreeCAD.PyObjectBase):
    """Root class for fixing operations"""

    def __init__(self):
        """Root class for fixing operations"""

    @typing.overload
    def add(self, edge: PartModule.Edge, edge2: PartModule.Edge, /): ...

    @typing.overload
    def add(self, shape: PartModule.Shape, /):
        """
        add(edge, edge)
        Adds information on connectivity between start vertex
        of second edge and end vertex of first edge taking
        edges orientation into account

        add(shape)
        Adds connectivity information for the whole shape.
        
        Possible exceptions: (TypeError).
        """

    def build(self):
        """Builds shared vertices, updates their positions and tolerances"""

    def clear(self):
        """Clears internal data structure"""


# ShapeFix_FixSmallSolidPy.xml
class FixSmallSolid(Part.ShapeFix.Root):
    """Fixing solids with small size"""

    def __init__(self):
        """Fixing solids with small size"""

    def merge(self, arg1: PartModule.Shape, /) -> PartModule.Shape:
        """Merge small solids in the given shape to adjacent non-small ones"""

    def remove(self, arg1: PartModule.Shape, /) -> PartModule.Shape:
        """Remove small solids from the given shape"""

    def setFixMode(self, arg1: int, /):
        """
        Set working mode for operator:
        - theMode = 0 use both WidthFactorThreshold and VolumeThreshold parameters
        - theMode = 1 use only WidthFactorThreshold parameter
        - theMode = 2 use only VolumeThreshold parameter
        """

    def setVolumeThreshold(self, arg1: float = None, /):
        """Set or clear volume threshold for small solids"""

    def setWidthFactorThreshold(self, arg1: float = None, /):
        """Set or clear width factor threshold for small solids"""


# ShapeFix_EdgePy.xml
class Edge(FreeCAD.PyObjectBase):
    """Fixing invalid edge"""

    def __init__(self):
        """Fixing invalid edge"""

    def fixAddCurve3d(self, arg1: PartModule.Edge, /) -> bool: ...

    @typing.overload
    def fixAddPCurve(self, arg1: PartModule.Edge, arg2: PartModule.Face, arg3: bool, arg4: float = None, /) -> bool: ...

    @typing.overload
    def fixAddPCurve(self, arg1: PartModule.Edge, arg2: PartModule.GeometrySurface, arg3: FreeCAD.Placement, arg4: bool, arg5: float = None, /) -> bool:
        """Possible exceptions: (TypeError)."""

    def fixRemoveCurve3d(self, arg1: PartModule.Edge, /) -> bool: ...

    @typing.overload
    def fixRemovePCurve(self, arg1: PartModule.Edge, arg2: PartModule.Face, /) -> bool: ...

    @typing.overload
    def fixRemovePCurve(self, arg1: PartModule.Edge, arg2: PartModule.GeometrySurface, arg3: FreeCAD.Placement, /) -> bool:
        """Possible exceptions: (TypeError)."""

    @typing.overload
    def fixReversed2d(self, arg1: PartModule.Edge, arg2: PartModule.Face, /) -> bool: ...

    @typing.overload
    def fixReversed2d(self, arg1: PartModule.Edge, arg2: PartModule.GeometrySurface, arg3: FreeCAD.Placement, /) -> bool:
        """Possible exceptions: (TypeError)."""

    @typing.overload
    def fixSameParameter(self, arg1: PartModule.Edge, arg2: float = None, /) -> bool: ...

    @typing.overload
    def fixSameParameter(self, arg1: PartModule.Edge, arg2: PartModule.Face, arg3: float = None, /) -> bool:
        """Possible exceptions: (TypeError)."""

    def fixVertexTolerance(self, arg1: PartModule.Edge, arg2: PartModule.Face = None, /) -> bool: ...


# ShapeFix_FreeBoundsPy.xml
class FreeBounds(FreeCAD.PyObjectBase):
    """This class is intended to output free bounds of the shape"""

    @typing.overload
    def __init__(self): ...

    @typing.overload
    def __init__(self, arg1: PartModule.Shape, arg2: float, arg3: float, arg4: bool, arg5: bool, /): ...

    @typing.overload
    def __init__(self, arg1: PartModule.Shape, arg2: float, arg3: bool, arg4: bool, /):
        """
        This class is intended to output free bounds of the shape
        Possible exceptions: (TypeError).
        """

    def closedWires(self) -> PartModule.Shape:
        """Returns compound of closed wires out of free edges"""

    def openWires(self) -> PartModule.Shape:
        """Returns compound of open wires out of free edges"""

    def shape(self) -> PartModule.Shape:
        """Returns modified source shape"""


# ShapeFix_SplitCommonVertexPy.xml
class SplitCommonVertex(Part.ShapeFix.Root):
    """Class for fixing operations on shapes"""

    def __init__(self, arg1: PartModule.Shape = None, /):
        """Class for fixing operations on shapes"""

    def init(self, arg1: PartModule.Shape, /):
        """Initializes by shape"""

    def perform(self):
        """Iterates on sub- shape and performs fixes"""

    def shape(self) -> PartModule.Shape:
        """Returns resulting shape"""


# ShapeFix_SolidPy.xml
class Solid(Part.ShapeFix.Root):
    """Root class for fixing operations"""

    def __init__(self, arg1: PartModule.Solid = None, /):
        """Root class for fixing operations"""

    @property
    def CreateOpenSolidMode(self) -> bool:
        """Mode for creation of solids"""

    @CreateOpenSolidMode.setter
    def CreateOpenSolidMode(self, value: bool): ...

    @property
    def FixShellMode(self) -> bool:
        """Mode for applying fixes of ShapeFix_Shell"""

    @FixShellMode.setter
    def FixShellMode(self, value: bool): ...

    @property
    def FixShellOrientationMode(self) -> bool:
        """
        Mode for applying analysis and fixes of
        orientation of shells in the solid
        """

    @FixShellOrientationMode.setter
    def FixShellOrientationMode(self, value: bool): ...

    def fixShellTool(self) -> Part.ShapeFix.Shell:
        """Returns tool for fixing shells"""

    def init(self, arg1: PartModule.Solid, /):
        """Initializes by solid"""

    def perform(self) -> bool:
        """Iterates on subshapes and performs fixes"""

    def shape(self) -> PartModule.Shape:
        """
        In case of multiconnexity returns compound of fixed solids
        else returns one solid
        """

    def solid(self) -> PartModule.Shape:
        """Returns resulting solid"""

    def solidFromShell(self, arg1: PartModule.Shell, /) -> PartModule.Shape:
        """Calls MakeSolid and orients the solid to be not infinite"""


# ShapeFix_WirePy.xml
class Wire(Part.ShapeFix.Root):
    """Class for fixing operations on wires"""

    @typing.overload
    def __init__(self): ...

    @typing.overload
    def __init__(self, arg1: PartModule.Wire, arg2: PartModule.Face, arg3: float, /):
        """
        Class for fixing operations on wires
        Possible exceptions: (TypeError).
        """

    @property
    def ClosedWireMode(self) -> bool:
        """
        Mode which defines whether the wire
        is to be closed (by calling methods like fixDegenerated()
        and fixConnected() for last and first edges)
        """

    @ClosedWireMode.setter
    def ClosedWireMode(self, value: bool): ...

    @property
    def FixAddCurve3dMode(self) -> bool: ...

    @FixAddCurve3dMode.setter
    def FixAddCurve3dMode(self, value: bool): ...

    @property
    def FixAddPCurveMode(self) -> bool: ...

    @FixAddPCurveMode.setter
    def FixAddPCurveMode(self, value: bool): ...

    @property
    def FixConnectedMode(self) -> bool: ...

    @FixConnectedMode.setter
    def FixConnectedMode(self, value: bool): ...

    @property
    def FixDegeneratedMode(self) -> bool: ...

    @FixDegeneratedMode.setter
    def FixDegeneratedMode(self, value: bool): ...

    @property
    def FixEdgeCurvesMode(self) -> bool: ...

    @FixEdgeCurvesMode.setter
    def FixEdgeCurvesMode(self, value: bool): ...

    @property
    def FixGaps2dMode(self) -> bool: ...

    @FixGaps2dMode.setter
    def FixGaps2dMode(self, value: bool): ...

    @property
    def FixGaps3dMode(self) -> bool: ...

    @FixGaps3dMode.setter
    def FixGaps3dMode(self, value: bool): ...

    @property
    def FixGapsByRangesMode(self) -> bool:
        """
        Mode which defines whether tool
        tries to fix gaps first by changing curves ranges (i.e.
        using intersection, extrema, projections) or not
        """

    @FixGapsByRangesMode.setter
    def FixGapsByRangesMode(self, value: bool): ...

    @property
    def FixIntersectingEdgesMode(self) -> bool: ...

    @FixIntersectingEdgesMode.setter
    def FixIntersectingEdgesMode(self, value: bool): ...

    @property
    def FixLackingMode(self) -> bool: ...

    @FixLackingMode.setter
    def FixLackingMode(self, value: bool): ...

    @property
    def FixNonAdjacentIntersectingEdgesMode(self) -> bool: ...

    @FixNonAdjacentIntersectingEdgesMode.setter
    def FixNonAdjacentIntersectingEdgesMode(self, value: bool): ...

    @property
    def FixNotchedEdgesMode(self) -> bool: ...

    @FixNotchedEdgesMode.setter
    def FixNotchedEdgesMode(self, value: bool): ...

    @property
    def FixRemoveCurve3dMode(self) -> bool: ...

    @FixRemoveCurve3dMode.setter
    def FixRemoveCurve3dMode(self, value: bool): ...

    @property
    def FixRemovePCurveMode(self) -> bool: ...

    @FixRemovePCurveMode.setter
    def FixRemovePCurveMode(self, value: bool): ...

    @property
    def FixReorderMode(self) -> bool: ...

    @FixReorderMode.setter
    def FixReorderMode(self, value: bool): ...

    @property
    def FixReversed2dMode(self) -> bool: ...

    @FixReversed2dMode.setter
    def FixReversed2dMode(self, value: bool): ...

    @property
    def FixSameParameterMode(self) -> bool: ...

    @FixSameParameterMode.setter
    def FixSameParameterMode(self, value: bool): ...

    @property
    def FixSeamMode(self) -> bool: ...

    @FixSeamMode.setter
    def FixSeamMode(self, value: bool): ...

    @property
    def FixSelfIntersectingEdgeMode(self) -> bool: ...

    @FixSelfIntersectingEdgeMode.setter
    def FixSelfIntersectingEdgeMode(self, value: bool): ...

    @property
    def FixSelfIntersectionMode(self) -> bool: ...

    @FixSelfIntersectionMode.setter
    def FixSelfIntersectionMode(self, value: bool): ...

    @property
    def FixShiftedMode(self) -> bool: ...

    @FixShiftedMode.setter
    def FixShiftedMode(self, value: bool): ...

    @property
    def FixSmallMode(self) -> bool: ...

    @FixSmallMode.setter
    def FixSmallMode(self, value: bool): ...

    @property
    def FixTailMode(self) -> bool: ...

    @FixTailMode.setter
    def FixTailMode(self, value: bool): ...

    @property
    def FixVertexToleranceMode(self) -> bool: ...

    @FixVertexToleranceMode.setter
    def FixVertexToleranceMode(self, value: bool): ...

    @property
    def ModifyGeometryMode(self) -> bool:
        """Mode for modifying geometry of vertexes and edges"""

    @ModifyGeometryMode.setter
    def ModifyGeometryMode(self, value: bool): ...

    @property
    def ModifyRemoveLoopMode(self) -> bool:
        """Mode for modifying edges"""

    @ModifyRemoveLoopMode.setter
    def ModifyRemoveLoopMode(self, value: bool): ...

    @property
    def ModifyTopologyMode(self) -> bool:
        """Mode for modifying topology of the wire"""

    @ModifyTopologyMode.setter
    def ModifyTopologyMode(self, value: bool): ...

    @property
    def PreferencePCurveMode(self) -> bool:
        """
        Mode which defines whether the 2d (True)
        representation of the wire is preferable over 3d one (in the
        case of ambiguity in FixEdgeCurves)
        """

    @PreferencePCurveMode.setter
    def PreferencePCurveMode(self, value: bool): ...

    def clearModes(self):
        """Sets all modes to default"""

    def clearStatuses(self):
        """Clears all statuses"""

    def face(self, arg1: PartModule.GeometrySurface, arg2: FreeCAD.Placement = None, /):
        """Returns working face"""

    def fixClosed(self, arg1: float = None, /) -> bool:
        """Fixes a wire to be well closed"""

    def fixConnected(self, num: float = None, /) -> bool:
        """
        Applies fixConnected(num) to all edges in the wire
        Connection between first and last edges is treated only if
        flag ClosedMode is True
        If prec is -1 then maxTolerance() is taken.
        Possible exceptions: (Part.OCCError, TypeError).
        """

    def fixDegenerated(self, arg1: int = None, /) -> bool:
        """
        Applies fixDegenerated(...) to all edges in the wire
        Possible exceptions: (Part.OCCError).
        """

    def fixEdgeCurves(self) -> bool:
        """Groups the fixes dealing with 3d and pcurves of the edges"""

    def fixEdgeTool(self) -> Part.ShapeFix.Edge:
        """Returns tool for fixing wires"""

    def fixGap2d(self, arg1: int, arg2: bool, /) -> bool:
        """
        Fixes gap between ends of pcurves on num-1 and num-th edges
        Possible exceptions: (Part.OCCError).
        """

    def fixGap3d(self, arg1: int, arg2: bool, /) -> bool:
        """
        Fixes gap between ends of 3d curves on num-1 and num-th edges
        Possible exceptions: (Part.OCCError).
        """

    def fixGaps2d(self) -> bool:
        """Fixes gaps between ends of pcurves on adjacent edges"""

    def fixGaps3d(self) -> bool:
        """Fixes gaps between ends of 3d curves on adjacent edges"""

    @typing.overload
    def fixLacking(self, arg1: bool = None, /) -> bool: ...

    @typing.overload
    def fixLacking(self, arg1: int, arg2: bool = None, /) -> bool:
        """Possible exceptions: (Part.OCCError, TypeError)."""

    def fixNotchedEdges(self) -> bool: ...

    def fixReorder(self) -> bool:
        """Performs an analysis and reorders edges in the wire"""

    def fixSeam(self, arg1: int, /) -> bool:
        """
        Fixes seam edges
        Possible exceptions: (Part.OCCError).
        """

    def fixSelfIntersection(self) -> bool: ...

    def fixShifted(self) -> bool:
        """
        Fixes edges which have pcurves shifted by whole parameter
        range on the closed surface
        """

    @typing.overload
    def fixSmall(self, arg1: bool, arg2: float = None, /) -> int | bool: ...

    @typing.overload
    def fixSmall(self, arg1: int, arg2: bool, arg3: float, /) -> int | bool:
        """
        Applies fixSmall(...) to all edges in the wire
        Possible exceptions: (Part.OCCError, TypeError).
        """

    def fixTails(self) -> bool: ...

    def init(self, arg1: PartModule.Wire, arg2: PartModule.Face, arg3: float, /):
        """Initializes by wire, face, precision"""

    def isLoaded(self) -> bool:
        """Tells if the wire is loaded"""

    def isReady(self) -> bool:
        """Tells if the wire and face are loaded"""

    def load(self, arg1: PartModule.Wire, /):
        """Load data for the wire, and drops all fixing statuses"""

    def numberOfEdges(self) -> int:
        """Returns number of edges in the working wire"""

    def perform(self) -> bool:
        """Iterates on subshapes and performs fixes"""

    def setFace(self, arg1: PartModule.Face, /):
        """Set working face for the wire"""

    def setMaxTailAngle(self, arg1: float, /):
        """Sets the maximal allowed angle of the tails in radians"""

    def setMaxTailWidth(self, arg1: float, /):
        """Sets the maximal allowed width of the tails"""

    def setSurface(self, surface: PartModule.GeometrySurface, Placement: FreeCAD.Placement = None, /):
        """
        setSurface(surface, [Placement])
        Set surface for the wire
        """

    def wire(self) -> PartModule.Shape:
        """Makes the resulting Wire (by basic Brep_Builder)"""

    def wireAPIMake(self) -> PartModule.Shape:
        """Makes the resulting Wire (by BRepAPI_MakeWire)"""


# ShapeFix_FacePy.xml
class Face(Part.ShapeFix.Root):
    """Class for fixing operations on faces"""

    @typing.overload
    def __init__(self, arg1: PartModule.Face = None, /): ...

    @typing.overload
    def __init__(self, arg1: PartModule.GeometrySurface, arg2: float, arg3: bool = None, /):
        """Class for fixing operations on faces"""

    @property
    def AutoCorrectPrecisionMode(self) -> bool:
        """Mode for applying auto-corrected precision"""

    @AutoCorrectPrecisionMode.setter
    def AutoCorrectPrecisionMode(self, value: bool): ...

    @property
    def FixAddNaturalBoundMode(self) -> bool:
        """
        If true, natural boundary is added on faces that miss them.
        Default is False for faces with single wire (they are
        handled by FixOrientation in that case) and True for others.
        """

    @FixAddNaturalBoundMode.setter
    def FixAddNaturalBoundMode(self, value: bool): ...

    @property
    def FixIntersectingWiresMode(self) -> bool:
        """Mode for applying fixes of intersecting wires"""

    @FixIntersectingWiresMode.setter
    def FixIntersectingWiresMode(self, value: bool): ...

    @property
    def FixLoopWiresMode(self) -> bool:
        """Mode for applying fixes of loop wires"""

    @FixLoopWiresMode.setter
    def FixLoopWiresMode(self, value: bool): ...

    @property
    def FixMissingSeamMode(self) -> bool:
        """If True, tries to insert seam if missing"""

    @FixMissingSeamMode.setter
    def FixMissingSeamMode(self, value: bool): ...

    @property
    def FixOrientationMode(self) -> bool:
        """
        Mode for applying fixes of orientation
        If True, wires oriented to border limited square
        """

    @FixOrientationMode.setter
    def FixOrientationMode(self, value: bool): ...

    @property
    def FixPeriodicDegeneratedMode(self) -> bool:
        """Mode for applying periodic degeneration"""

    @FixPeriodicDegeneratedMode.setter
    def FixPeriodicDegeneratedMode(self, value: bool): ...

    @property
    def FixSmallAreaWireMode(self) -> bool:
        """If True, drops small wires"""

    @FixSmallAreaWireMode.setter
    def FixSmallAreaWireMode(self, value: bool): ...

    @property
    def FixSplitFaceMode(self) -> bool:
        """Mode for applying fixes of split face"""

    @FixSplitFaceMode.setter
    def FixSplitFaceMode(self, value: bool): ...

    @property
    def FixWireMode(self) -> bool:
        """Mode for applying fixes of ShapeFix_Wire"""

    @FixWireMode.setter
    def FixWireMode(self, value: bool): ...

    @property
    def RemoveSmallAreaFaceMode(self) -> bool:
        """If True, drops small wires"""

    @RemoveSmallAreaFaceMode.setter
    def RemoveSmallAreaFaceMode(self, value: bool): ...

    def add(self, arg1: PartModule.Wire, /):
        """
        Add a wire to current face using BRep_Builder.
        Wire is added without taking into account orientation of face
        (as if face were FORWARD)
        """

    def clearModes(self):
        """Sets all modes to default"""

    def face(self) -> PartModule.Shape:
        """Returns a face which corresponds to the current state"""

    def fixAddNaturalBound(self) -> bool:
        """
        Adds natural boundary on face if it is missing.
        Two cases are supported:
         - face has no wires
         - face lies on geometrically double-closed surface
        (sphere or torus) and none of wires is left-oriented
        Returns True if natural boundary was added
        """

    def fixIntersectingWires(self) -> bool:
        """
        Detects and fixes the special case when face has more than one wire
        and this wires have intersection point
        """

    def fixLoopWire(self) -> tuple[bool, list[PartModule.Shape]]:
        """Detects if wire has a loop and fixes this situation by splitting on the few parts."""

    def fixMissingSeam(self) -> bool:
        """
        Detects and fixes the special case when face on a closed
        surface is given by two wires closed in 3d but with gap in 2d.
        In that case it creates a new wire from the two, and adds a
        missing seam edge
        Returns True if missing seam was added
        """

    def fixOrientation(self) -> bool:
        """
        Fixes orientation of wires on the face
        It tries to make all wires lie outside all others (according
        to orientation) by reversing orientation of some of them.
        If face lying on sphere or torus has single wire and
        AddNaturalBoundMode is True, that wire is not reversed in
        any case (supposing that natural bound will be added).
        Returns True if wires were reversed
        """

    def fixPeriodicDegenerated(self) -> bool:
        """
        Fixes topology for a specific case when face is composed
        by a single wire belting a periodic surface. In that case
        a degenerated edge is reconstructed in the degenerated pole
        of the surface. Initial wire gets consistent orientation.
        Must be used in couple and before FixMissingSeam routine
        """

    def fixSmallAreaWire(self, arg1: bool, /) -> bool:
        """
        Detects wires with small area (that is less than
        100*Precision.PConfusion(). Removes these wires if they are internal.
        Returns True if at least one small wire removed, False nothing is done.
        """

    def fixWireTool(self) -> Part.ShapeFix.Wire:
        """Returns tool for fixing wires"""

    def fixWiresTwoCoincidentEdges(self) -> bool:
        """If wire contains two coincidence edges it must be removed"""

    @typing.overload
    def init(self, arg1: PartModule.Face, /): ...

    @typing.overload
    def init(self, arg1: PartModule.GeometrySurface, arg2: float, arg3: bool = None, /):
        """Initializes by face"""

    def perform(self) -> bool:
        """Iterates on subshapes and performs fixes"""

    def result(self) -> PartModule.Shape:
        """
        Returns resulting shape (Face or Shell if split)
        To be used instead of face() if FixMissingSeam involved
        """


# ShapeFix_FixSmallFacePy.xml
class FixSmallFace(Part.ShapeFix.Root):
    """Class for fixing operations on faces"""

    def __init__(self):
        """Class for fixing operations on faces"""

    def fixFace(self, arg1: PartModule.Face, /) -> PartModule.Shape: ...

    def fixShape(self) -> PartModule.Shape: ...

    def fixSplitFace(self, arg1: PartModule.Shape, /) -> PartModule.Shape: ...

    def fixSpotFace(self) -> PartModule.Shape:
        """Fixing case of spot face, if tol = -1 used local tolerance"""

    def fixStripFace(self, arg1: bool = None, /) -> PartModule.Shape:
        """Fixing case of strip face, if tol = -1 used local tolerance"""

    def init(self, arg1: PartModule.Shape, /):
        """Initializes by shape"""

    def perform(self):
        """Fixing case of spot face"""

    def removeFacesInCaseOfSpot(self, arg1: PartModule.Face, /) -> bool:
        """Remove spot face from compound"""

    def removeFacesInCaseOfStrip(self, arg1: PartModule.Face, /) -> bool:
        """Remove strip face from compound"""

    def replaceVerticesInCaseOfSpot(self, arg1: PartModule.Face, /):
        """Compute average vertex and replacing vertices by new one"""

    def shape(self) -> PartModule.Shape: ...


# ShapeFix_SplitToolPy.xml
class SplitTool(FreeCAD.PyObjectBase):
    """Tool for splitting and cutting edges"""

    def __init__(self):
        """Tool for splitting and cutting edges"""

    def cutEdge(self, arg1: PartModule.Edge, arg2: float, arg3: float, arg4: PartModule.Face, /) -> bool:
        """Cut edge by parameters pend and cut"""

    @typing.overload
    def splitEdge(self, arg1: PartModule.Edge, arg2: float, arg3: PartModule.Vertex, arg4: PartModule.Face, arg5: float, arg6: float, /) -> tuple[typing.Any, typing.Any]: ...

    @typing.overload
    def splitEdge(self, arg1: PartModule.Edge, arg2: float, arg3: float, arg4: PartModule.Vertex, arg5: PartModule.Face, arg6: float, arg7: float, /) -> tuple[typing.Any, typing.Any]:
        """
        Split edge on two new edges using new vertex
        Possible exceptions: (TypeError).
        """


# ShapeFix_ShapeTolerancePy.xml
class ShapeTolerance(FreeCAD.PyObjectBase):
    """Modifies tolerances of sub-shapes (vertices, edges, faces)"""

    def __init__(self):
        """Modifies tolerances of sub-shapes (vertices, edges, faces)"""

    def limitTolerance(self, shape: PartModule.Shape, tmin: float, tmax: float = 0, ShapeEnum: int = None, /) -> bool:
        """limitTolerance(shape, tmin, [tmax=0, ShapeEnum=SHAPE])"""

    def setTolerance(self, shape: PartModule.Shape, precision: float, ShapeEnum: int = None, /):
        """setTolerance(shape, precision, [ShapeEnum=SHAPE])"""


# ShapeFix_WireframePy.xml
class Wireframe(Part.ShapeFix.Root):
    """Provides methods for fixing wireframe of shape"""

    def __init__(self, arg1: PartModule.Shape = None, /):
        """Provides methods for fixing wireframe of shape"""

    @property
    def LimitAngle(self) -> float:
        """Limit angle for merging edges"""

    @LimitAngle.setter
    def LimitAngle(self, value: float): ...

    @property
    def ModeDropSmallEdges(self) -> bool:
        """Returns mode managing removing small edges"""

    @ModeDropSmallEdges.setter
    def ModeDropSmallEdges(self, value: bool): ...

    def clearStatuses(self):
        """Clears all statuses"""

    def fixSmallEdges(self) -> bool:
        """Fixes small edges in shape by merging adjacent edges"""

    def fixWireGaps(self) -> bool:
        """Fixes gaps between ends of curves of adjacent edges"""

    def load(self, arg1: PartModule.Shape, /):
        """Loads a shape, resets statuses"""

    def shape(self) -> PartModule.Shape: ...


# ShapeFix_RootPy.xml
class Root(FreeCAD.PyObjectBase):
    """Root class for fixing operations"""

    def __init__(self):
        """Root class for fixing operations"""

    @property
    def MaxTolerance(self) -> float:
        """Maximal allowed tolerance"""

    @MaxTolerance.setter
    def MaxTolerance(self, value: float): ...

    @property
    def MinTolerance(self) -> float:
        """Minimal allowed tolerance"""

    @MinTolerance.setter
    def MinTolerance(self, value: float): ...

    @property
    def Precision(self) -> float:
        """Basic precision value"""

    @Precision.setter
    def Precision(self, value: float): ...

    def limitTolerance(self, arg1: float, /) -> float:
        """Returns tolerance limited by [MinTolerance,MaxTolerance]"""


# ShapeFix_ShellPy.xml
class Shell(Part.ShapeFix.Root):
    """Root class for fixing operations"""

    def __init__(self, arg1: PartModule.Shell = None, /):
        """Root class for fixing operations"""

    @property
    def FixFaceMode(self) -> bool:
        """Mode for applying fixes using ShapeFix_Face"""

    @FixFaceMode.setter
    def FixFaceMode(self, value: bool): ...

    @property
    def FixOrientationMode(self) -> bool:
        """Mode for applying fixes of orientation of faces"""

    @FixOrientationMode.setter
    def FixOrientationMode(self, value: bool): ...

    def errorFaces(self) -> PartModule.Shape:
        """Returns not oriented subset of faces"""

    def fixFaceOrientation(self, arg1: PartModule.Shell, arg2: bool = None, arg3: bool = None, /) -> bool:
        """
        Fixes orientation of faces in shell.
        Changes orientation of face in the shell, if it is oriented opposite
        to neighbouring faces. If it is not possible to orient all faces in the
        shell (like in case of mebious band), this method orients only subset
        of faces. Other faces are stored in Error compound.
        Modes :
        isAccountMultiConex - mode for account cases of multiconnexity.
        If this mode is equal to Standard_True, separate shells will be created
        in the cases of multiconnexity. If this mode is equal to Standard_False,
        one shell will be created without account of multiconnexity. By default - Standard_True;
        NonManifold - mode for creation of non-manifold shells.
        If this mode is equal to Standard_True one non-manifold will be created from shell
        contains multishared edges. Else if this mode is equal to Standard_False only
        manifold shells will be created. By default - Standard_False.
        """

    def fixFaceTool(self) -> Part.ShapeFix.Face:
        """Returns tool for fixing faces"""

    def init(self, arg1: PartModule.Shell, /):
        """Initializes by shell"""

    def numberOfShells(self) -> int:
        """Returns the number of obtained shells"""

    def perform(self) -> bool:
        """Iterates on subshapes and performs fixes"""

    def setNonManifoldFlag(self, arg1: bool, /):
        """Sets NonManifold flag"""

    def shape(self) -> PartModule.Shape:
        """In case of multiconnexity returns compound of fixed shells and one shell otherwise"""

    def shell(self) -> PartModule.Shape:
        """Returns fixed shell (or subset of oriented faces)"""
