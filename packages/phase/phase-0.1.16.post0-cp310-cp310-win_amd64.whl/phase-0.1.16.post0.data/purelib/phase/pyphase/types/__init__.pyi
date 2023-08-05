"""custom Phase types"""
from __future__ import annotations
import phase.pyphase.types
import typing
import numpy
_Shape = typing.Tuple[int, ...]

__all__ = [
    "CameraDeviceInfo",
    "CameraDeviceType",
    "CameraInterfaceType",
    "CameraReadResult",
    "DEVICE_TYPE_DEIMOS",
    "DEVICE_TYPE_GENERIC_PYLON",
    "DEVICE_TYPE_GENERIC_UVC",
    "DEVICE_TYPE_INVALID",
    "DEVICE_TYPE_PHOBOS",
    "DEVICE_TYPE_TITANIA",
    "INTERFACE_TYPE_GIGE",
    "INTERFACE_TYPE_USB",
    "INTERFACE_TYPE_VIRTUAL",
    "LEFT",
    "LeftOrRight",
    "MatrixFloat",
    "MatrixUInt8",
    "Point2d",
    "Point2f",
    "Point2i",
    "RGBDVideoFrame",
    "RIGHT",
    "STEREO_MATCHER_BM",
    "STEREO_MATCHER_HOBM",
    "STEREO_MATCHER_I3DRSGM",
    "STEREO_MATCHER_SGBM",
    "StereoImagePair",
    "StereoMatcherComputeResult",
    "StereoMatcherType",
    "StereoVisionReadResult"
]


class CameraDeviceInfo():
    """
    Camera info class contains camera serials, camera type and connection type
    """
    def __init__(self, arg0: str, arg1: str, arg2: str, arg3: CameraDeviceType, arg4: CameraInterfaceType) -> None: 
        """
        TODOC
        """
    def getLeftCameraSerial(self) -> str: 
        """
        Get the left camera serial

        Returns
        -------
        left_camera_serial : str
        """
    def getRightCameraSerial(self) -> str: 
        """
        Get the right camera serial

        Returns
        -------
        right_camera_serial : str
        """
    def getUniqueSerial(self) -> str: 
        """
        Get the camera unique serial

        Returns
        -------
        unique_serial : str
        """
    def setLeftCameraSerial(self, arg0: str) -> None: 
        """
        Set the left camera serial

        Parameters
        ----------
        left_camera_serial : str
        """
    def setRightCameraSerial(self, arg0: str) -> None: 
        """
        Set the right camera serial

        Parameters
        ----------
        right_camera_serial : str
        """
    def setUniqueSerial(self, arg0: str) -> None: 
        """
        Set the camera unique serial

        Parameters
        ----------
        unique_serial : str
        """
    @property
    def device_type(self) -> CameraDeviceType:
        """
                    Device type in enum
                    
                    

        :type: CameraDeviceType
        """
    @device_type.setter
    def device_type(self, arg0: CameraDeviceType) -> None:
        """
        Device type in enum
        """
    @property
    def interface_type(self) -> CameraInterfaceType:
        """
                    Interface type in enum

                    

        :type: CameraInterfaceType
        """
    @interface_type.setter
    def interface_type(self, arg0: CameraInterfaceType) -> None:
        """
        Interface type in enum
        """
    pass
class CameraDeviceType():
    """
            Structure of CameraDeviceType

            

    Members:

      DEVICE_TYPE_GENERIC_PYLON

      DEVICE_TYPE_GENERIC_UVC

      DEVICE_TYPE_DEIMOS

      DEVICE_TYPE_PHOBOS

      DEVICE_TYPE_TITANIA

      DEVICE_TYPE_INVALID
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    DEVICE_TYPE_DEIMOS: phase.pyphase.types.CameraDeviceType # value = <CameraDeviceType.DEVICE_TYPE_DEIMOS: 2>
    DEVICE_TYPE_GENERIC_PYLON: phase.pyphase.types.CameraDeviceType # value = <CameraDeviceType.DEVICE_TYPE_GENERIC_PYLON: 0>
    DEVICE_TYPE_GENERIC_UVC: phase.pyphase.types.CameraDeviceType # value = <CameraDeviceType.DEVICE_TYPE_GENERIC_UVC: 1>
    DEVICE_TYPE_INVALID: phase.pyphase.types.CameraDeviceType # value = <CameraDeviceType.DEVICE_TYPE_INVALID: 5>
    DEVICE_TYPE_PHOBOS: phase.pyphase.types.CameraDeviceType # value = <CameraDeviceType.DEVICE_TYPE_PHOBOS: 3>
    DEVICE_TYPE_TITANIA: phase.pyphase.types.CameraDeviceType # value = <CameraDeviceType.DEVICE_TYPE_TITANIA: 4>
    __members__: dict # value = {'DEVICE_TYPE_GENERIC_PYLON': <CameraDeviceType.DEVICE_TYPE_GENERIC_PYLON: 0>, 'DEVICE_TYPE_GENERIC_UVC': <CameraDeviceType.DEVICE_TYPE_GENERIC_UVC: 1>, 'DEVICE_TYPE_DEIMOS': <CameraDeviceType.DEVICE_TYPE_DEIMOS: 2>, 'DEVICE_TYPE_PHOBOS': <CameraDeviceType.DEVICE_TYPE_PHOBOS: 3>, 'DEVICE_TYPE_TITANIA': <CameraDeviceType.DEVICE_TYPE_TITANIA: 4>, 'DEVICE_TYPE_INVALID': <CameraDeviceType.DEVICE_TYPE_INVALID: 5>}
    pass
class CameraInterfaceType():
    """
            Structure of CameraInterfaceType

            

    Members:

      INTERFACE_TYPE_USB

      INTERFACE_TYPE_GIGE

      INTERFACE_TYPE_VIRTUAL
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    INTERFACE_TYPE_GIGE: phase.pyphase.types.CameraInterfaceType # value = <CameraInterfaceType.INTERFACE_TYPE_GIGE: 1>
    INTERFACE_TYPE_USB: phase.pyphase.types.CameraInterfaceType # value = <CameraInterfaceType.INTERFACE_TYPE_USB: 0>
    INTERFACE_TYPE_VIRTUAL: phase.pyphase.types.CameraInterfaceType # value = <CameraInterfaceType.INTERFACE_TYPE_VIRTUAL: 2>
    __members__: dict # value = {'INTERFACE_TYPE_USB': <CameraInterfaceType.INTERFACE_TYPE_USB: 0>, 'INTERFACE_TYPE_GIGE': <CameraInterfaceType.INTERFACE_TYPE_GIGE: 1>, 'INTERFACE_TYPE_VIRTUAL': <CameraInterfaceType.INTERFACE_TYPE_VIRTUAL: 2>}
    pass
class CameraReadResult():
    """
    Structure of CameraReadResult
    """
    def __init__(self, arg0: bool, arg1: numpy.ndarray, arg2: numpy.ndarray) -> None: ...
    @property
    def left(self) -> numpy.ndarray:
        """
        :type: numpy.ndarray
        """
    @left.setter
    def left(self, arg0: numpy.ndarray) -> None:
        pass
    @property
    def right(self) -> numpy.ndarray:
        """
        :type: numpy.ndarray
        """
    @right.setter
    def right(self, arg0: numpy.ndarray) -> None:
        pass
    @property
    def valid(self) -> bool:
        """
        :type: bool
        """
    @valid.setter
    def valid(self, arg0: bool) -> None:
        pass
    pass
class LeftOrRight():
    """
            Structure of LeftOrRight

            

    Members:

      LEFT

      RIGHT
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    LEFT: phase.pyphase.types.LeftOrRight # value = <LeftOrRight.LEFT: 0>
    RIGHT: phase.pyphase.types.LeftOrRight # value = <LeftOrRight.RIGHT: 1>
    __members__: dict # value = {'LEFT': <LeftOrRight.LEFT: 0>, 'RIGHT': <LeftOrRight.RIGHT: 1>}
    pass
class MatrixFloat():
    """
    Class to access data float type matrix
    """
    @typing.overload
    def __init__(self, arg0: MatrixFloat) -> None: 
        """
                Access float type matrix data

                Parameters
                ----------
                rows : int
                cols : int
                channels : int

                


                Access float type matrix data

                

        Access float type matrix data
        """
    @typing.overload
    def __init__(self, arg0: int, arg1: int, arg2: int) -> None: ...
    @typing.overload
    def __init__(self, arg0: numpy.ndarray[numpy.float32]) -> None: ...
    def getAt(self, arg0: int, arg1: int, arg2: int) -> float: 
        """
        Get the data of the desired index of matrix

        Parameters
        ----------
        row : int
        column : int
        layer : int

        Returns
        -------
        data : float
            The value of data in float
        """
    def getColumns(self) -> int: 
        """
        Get columns of the float type matrix

        Returns
        -------
        columns : int
            Column of the matrix
        """
    def getLayers(self) -> int: 
        """
        Get layers of the float type matrix

        Returns
        -------
        layers : int
            Layer of the matrix
        """
    def getLength(self) -> int: 
        """
        Get length of the float type matrix, defines as rows X columns X layer

        Returns
        -------
        value : int
            Length of the matrix
        """
    def getRows(self) -> int: 
        """
        Get rows of the float type matrix

        Returns
        -------
        rows : int
            Row of the matrix
        """
    def getSize(self) -> int: 
        """
        Get size of the float type matrix

        Returns
        -------
        value : int
            Size of the matrix
        """
    def isEmpty(self) -> bool: 
        """
        Check if the matrix is empty

        Returns
        -------
        bool
            True if empty
        """
    def setAt(self, arg0: int, arg1: int, arg2: int, arg3: float) -> None: 
        """
        Set the data value to the desired index of matrix

        Parameters
        ----------
        row : int
        column : int
        layer : int
        value : float
        """
    pass
class MatrixUInt8():
    """
    Class to access data UInt8 type matrix
    """
    @typing.overload
    def __init__(self, arg0: MatrixUInt8) -> None: 
        """
                Access UInt8 type matrix data

                Parameters
                ----------
                rows : int
                cols : int
                channels : int
                


                Access UInt8 type matrix data

                

        Access UInt8 type matrix data
        """
    @typing.overload
    def __init__(self, arg0: int, arg1: int, arg2: int) -> None: ...
    @typing.overload
    def __init__(self, arg0: numpy.ndarray[numpy.uint8]) -> None: ...
    def getAt(self, arg0: int, arg1: int, arg2: int) -> int: 
        """
        Get the data of the desired index of matrix

        Parameters
        ----------
        row : int
        column : int
        layer : int

        Returns
        -------
        data : int
            The value of data in float
        """
    def getColumns(self) -> int: 
        """
        Get columns of the UInt8 type matrix

        Returns
        -------
        columns : int
            Column of the matrix
        """
    def getLayers(self) -> int: 
        """
        Get layers of the UInt8 type matrix

        Returns
        -------
        layers : int
            Layer of the matrix
        """
    def getLength(self) -> int: 
        """
        Get length of the UInt8 type matrix, defines as rows X columns X layer

        Returns
        -------
        value : int
            Length of the matrix
        """
    def getRows(self) -> int: 
        """
        Get rows of the UInt8 type matrix

        Returns
        -------
        rows : int
            Row of the matrix
        """
    def getSize(self) -> int: 
        """
        Get size of the UInt8 type matrix

        Returns
        -------
        value : int
            Size of the matrix
        """
    def isEmpty(self) -> bool: 
        """
        Check if the matrix is empty

        Returns
        -------
        bool
            True if empty
        """
    def setAt(self, arg0: int, arg1: int, arg2: int, arg3: int) -> None: 
        """
        Set the data value to the desired index of matrix

        Parameters
        ----------
        row : int
        column : int
        layer : int
        value : int
        """
    pass
class Point2d():
    """
    Structure of Point2d
    """
    def __init__(self, arg0: float, arg1: float) -> None: ...
    @property
    def x(self) -> float:
        """
        :type: float
        """
    @x.setter
    def x(self, arg0: float) -> None:
        pass
    @property
    def y(self) -> float:
        """
        :type: float
        """
    @y.setter
    def y(self, arg0: float) -> None:
        pass
    pass
class Point2f():
    """
    Structure of Point2f
    """
    def __init__(self, arg0: float, arg1: float) -> None: ...
    @property
    def x(self) -> float:
        """
        :type: float
        """
    @x.setter
    def x(self, arg0: float) -> None:
        pass
    @property
    def y(self) -> float:
        """
        :type: float
        """
    @y.setter
    def y(self, arg0: float) -> None:
        pass
    pass
class Point2i():
    """
    Structure of Point2i
    """
    def __init__(self, arg0: int, arg1: int) -> None: ...
    @property
    def x(self) -> int:
        """
        :type: int
        """
    @x.setter
    def x(self, arg0: int) -> None:
        pass
    @property
    def y(self) -> int:
        """
        :type: int
        """
    @y.setter
    def y(self, arg0: int) -> None:
        pass
    pass
class RGBDVideoFrame():
    """
    Structure of RGBDVideoFrame
    """
    def __init__(self, arg0: bool, arg1: numpy.ndarray, arg2: numpy.ndarray) -> None: ...
    @property
    def depth(self) -> numpy.ndarray:
        """
        :type: numpy.ndarray
        """
    @depth.setter
    def depth(self, arg0: numpy.ndarray) -> None:
        pass
    @property
    def image(self) -> numpy.ndarray:
        """
        :type: numpy.ndarray
        """
    @image.setter
    def image(self, arg0: numpy.ndarray) -> None:
        pass
    @property
    def valid(self) -> bool:
        """
        :type: bool
        """
    @valid.setter
    def valid(self, arg0: bool) -> None:
        pass
    pass
class StereoImagePair():
    """
    Structure of StereoImagePair
    """
    def __init__(self, arg0: numpy.ndarray, arg1: numpy.ndarray) -> None: ...
    @property
    def left(self) -> numpy.ndarray:
        """
        :type: numpy.ndarray
        """
    @left.setter
    def left(self, arg0: numpy.ndarray) -> None:
        pass
    @property
    def right(self) -> numpy.ndarray:
        """
        :type: numpy.ndarray
        """
    @right.setter
    def right(self, arg0: numpy.ndarray) -> None:
        pass
    pass
class StereoMatcherComputeResult():
    """
    Structure of StereoMatcherComputeResult
    """
    def __init__(self, arg0: bool, arg1: numpy.ndarray) -> None: ...
    @property
    def disparity(self) -> numpy.ndarray:
        """
        :type: numpy.ndarray
        """
    @disparity.setter
    def disparity(self, arg0: numpy.ndarray) -> None:
        pass
    @property
    def valid(self) -> bool:
        """
        :type: bool
        """
    @valid.setter
    def valid(self, arg0: bool) -> None:
        pass
    pass
class StereoMatcherType():
    """
            Structure of StereoMatcherType

            

    Members:

      STEREO_MATCHER_BM

      STEREO_MATCHER_SGBM

      STEREO_MATCHER_I3DRSGM

      STEREO_MATCHER_HOBM
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    STEREO_MATCHER_BM: phase.pyphase.types.StereoMatcherType # value = <StereoMatcherType.STEREO_MATCHER_BM: 0>
    STEREO_MATCHER_HOBM: phase.pyphase.types.StereoMatcherType # value = <StereoMatcherType.STEREO_MATCHER_HOBM: 3>
    STEREO_MATCHER_I3DRSGM: phase.pyphase.types.StereoMatcherType # value = <StereoMatcherType.STEREO_MATCHER_I3DRSGM: 2>
    STEREO_MATCHER_SGBM: phase.pyphase.types.StereoMatcherType # value = <StereoMatcherType.STEREO_MATCHER_SGBM: 1>
    __members__: dict # value = {'STEREO_MATCHER_BM': <StereoMatcherType.STEREO_MATCHER_BM: 0>, 'STEREO_MATCHER_SGBM': <StereoMatcherType.STEREO_MATCHER_SGBM: 1>, 'STEREO_MATCHER_I3DRSGM': <StereoMatcherType.STEREO_MATCHER_I3DRSGM: 2>, 'STEREO_MATCHER_HOBM': <StereoMatcherType.STEREO_MATCHER_HOBM: 3>}
    pass
class StereoVisionReadResult():
    """
    Structure of StereoVisionReadResult
    """
    def __init__(self, arg0: bool, arg1: numpy.ndarray, arg2: numpy.ndarray, arg3: numpy.ndarray) -> None: ...
    @property
    def disparity(self) -> numpy.ndarray:
        """
        :type: numpy.ndarray
        """
    @disparity.setter
    def disparity(self, arg0: numpy.ndarray) -> None:
        pass
    @property
    def left(self) -> numpy.ndarray:
        """
        :type: numpy.ndarray
        """
    @left.setter
    def left(self, arg0: numpy.ndarray) -> None:
        pass
    @property
    def right(self) -> numpy.ndarray:
        """
        :type: numpy.ndarray
        """
    @right.setter
    def right(self, arg0: numpy.ndarray) -> None:
        pass
    @property
    def valid(self) -> bool:
        """
        :type: bool
        """
    @valid.setter
    def valid(self, arg0: bool) -> None:
        pass
    pass
DEVICE_TYPE_DEIMOS: phase.pyphase.types.CameraDeviceType # value = <CameraDeviceType.DEVICE_TYPE_DEIMOS: 2>
DEVICE_TYPE_GENERIC_PYLON: phase.pyphase.types.CameraDeviceType # value = <CameraDeviceType.DEVICE_TYPE_GENERIC_PYLON: 0>
DEVICE_TYPE_GENERIC_UVC: phase.pyphase.types.CameraDeviceType # value = <CameraDeviceType.DEVICE_TYPE_GENERIC_UVC: 1>
DEVICE_TYPE_INVALID: phase.pyphase.types.CameraDeviceType # value = <CameraDeviceType.DEVICE_TYPE_INVALID: 5>
DEVICE_TYPE_PHOBOS: phase.pyphase.types.CameraDeviceType # value = <CameraDeviceType.DEVICE_TYPE_PHOBOS: 3>
DEVICE_TYPE_TITANIA: phase.pyphase.types.CameraDeviceType # value = <CameraDeviceType.DEVICE_TYPE_TITANIA: 4>
INTERFACE_TYPE_GIGE: phase.pyphase.types.CameraInterfaceType # value = <CameraInterfaceType.INTERFACE_TYPE_GIGE: 1>
INTERFACE_TYPE_USB: phase.pyphase.types.CameraInterfaceType # value = <CameraInterfaceType.INTERFACE_TYPE_USB: 0>
INTERFACE_TYPE_VIRTUAL: phase.pyphase.types.CameraInterfaceType # value = <CameraInterfaceType.INTERFACE_TYPE_VIRTUAL: 2>
LEFT: phase.pyphase.types.LeftOrRight # value = <LeftOrRight.LEFT: 0>
RIGHT: phase.pyphase.types.LeftOrRight # value = <LeftOrRight.RIGHT: 1>
STEREO_MATCHER_BM: phase.pyphase.types.StereoMatcherType # value = <StereoMatcherType.STEREO_MATCHER_BM: 0>
STEREO_MATCHER_HOBM: phase.pyphase.types.StereoMatcherType # value = <StereoMatcherType.STEREO_MATCHER_HOBM: 3>
STEREO_MATCHER_I3DRSGM: phase.pyphase.types.StereoMatcherType # value = <StereoMatcherType.STEREO_MATCHER_I3DRSGM: 2>
STEREO_MATCHER_SGBM: phase.pyphase.types.StereoMatcherType # value = <StereoMatcherType.STEREO_MATCHER_SGBM: 1>
