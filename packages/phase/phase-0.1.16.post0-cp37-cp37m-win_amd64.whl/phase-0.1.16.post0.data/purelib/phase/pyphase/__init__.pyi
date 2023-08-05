"""
        pyPhase is a python wrapper package over I3DR's Phase C++ library.
    """
from __future__ import annotations
import phase.pyphase
import typing
import numpy
_Shape = typing.Tuple[int, ...]

__all__ = [
    "RGBDVideoStream",
    "RGBDVideoWriter",
    "StereoVision",
    "bgr2bgra",
    "bgr2rgba",
    "bgra2rgba",
    "calib",
    "cvMatIsEqual",
    "depth2xyz",
    "disparity2depth",
    "disparity2xyz",
    "flip",
    "getVersionMajor",
    "getVersionMinor",
    "getVersionPatch",
    "getVersionString",
    "normaliseDisparity",
    "processStereo",
    "processStereoFiles",
    "readImage",
    "savePLY",
    "scaleImage",
    "showImage",
    "stereocamera",
    "stereomatcher",
    "types",
    "xyz2depth"
]


class RGBDVideoStream():
    """
    Stream RGB and Depth video

    Parameters
    ----------
    rgb_video_filepath : str
    depth_video_filepath : str
    """
    def __init__(self, arg0: str, arg1: str) -> None: 
        """
        Class to load RGBD video stream
        """
    def close(self) -> None: 
        """
        Close RGBD video stream
        """
    def getDownsampleFactor(self) -> float: 
        """
        Get the value of Downsample Factor

        Returns
        -------
        value : float
            Downsampled factor
        """
    def getHFOV(self) -> float: 
        """
        Get horitonzal Field Of View of camera from Q matrix

        Returns
        -------
        fov_x : float
            Horitonzal Field Of View of camera from Q matrix
        """
    def getHeight(self) -> int: 
        """
        Get the height of image

        Returns
        -------
        value : int
            Height of image
        """
    def getLoadThreadResult(self) -> bool: 
        """
        Check if thread is loaded with result

        Returns
        -------
        bool
            True if thread is loaded with result
        """
    @staticmethod
    def getReadThreadResult(*args, **kwargs) -> typing.Any: 
        """
        Get read thread

        Returns
        -------
        bool
            True if opened
        numpy.ndarray
            Image
        numpy.ndarray
            Image
        """
    def getWidth(self) -> int: 
        """
        Get the width of image

        Returns
        -------
        value : int
            Width of image
        """
    def isFinished(self) -> bool: 
        """
        Check if RGBD video stream is finished

        Returns
        -------
        bool
            True if finished
        """
    def isLoadThreadRunning(self) -> bool: 
        """
        Check if thread load is running

        Returns
        -------
        bool
            True if thread load is running
        """
    def isLoaded(self) -> bool: 
        """
        Check if RGBD video stream is loaded

        Returns
        -------
        bool
            True if loaded
        """
    def isOpened(self) -> bool: 
        """
        Check if RGBD video stream is opened

        Returns
        -------
        bool
            True if opened
        """
    def isReadThreadRunning(self) -> bool: 
        """
        Check if thread read is running

        Returns
        -------
        bool
            True if thread read is running
        """
    def load(self) -> bool: 
        """
        Load camera

        Returns
        -------
        bool
            True if camera loaded
        """
    def loadThreaded(self) -> None: 
        """
        Load thread
        """
    @staticmethod
    def read(*args, **kwargs) -> typing.Any: 
        """
        Read camera data

        Returns
        -------
        bool
            True if opened
        numpy.ndarray
            Image
        numpy.ndarray
            Image
        """
    def readThreaded(self) -> None: 
        """
        Read thread
        """
    def restart(self) -> None: 
        """
        Restart camera
        """
    def setDownsampleFactor(self, arg0: float) -> None: 
        """
        Set downsample factor

        Parameters
        ----------
        value : float
            Desired value of downsample factor
        """
    pass
class RGBDVideoWriter():
    """
    RGBD Video Writer


    Write RGB and Depth video
    """
    def __init__(self, arg0: str, arg1: str, arg2: int, arg3: int) -> None: 
        """
        Class to write RGBD video
        """
    def add(self, arg0: numpy.ndarray, arg1: numpy.ndarray) -> None: 
        """
        Add colour channel RGB and the depth to form 4 channels

        Parameters
        ----------
        rgb : numpy.ndarray
        depth : numpy.ndarray
        """
    def close(self) -> None: 
        """
        Close RGBD video writer
        """
    def getSaveThreadResult(self) -> bool: 
        """
        Get save thread

        Returns
        -------
        bool
            True if equal
        """
    def isOpened(self) -> bool: 
        """
        Check if RGBD writer is opened

        Returns
        -------
        bool
            True if RGBD writer is opened
        """
    def isSaveThreadRunning(self) -> bool: 
        """
        Check if save thread is running

        Returns
        -------
        bool
            True if save thread is running
        """
    def save(self) -> bool: 
        """
        Save RGBD video

        Returns
        -------
        bool
            True if RGBD video is saved
        """
    def saveThreaded(self) -> None: 
        """
        Save threaded
        """
    pass
class StereoVision():
    """
    Stereo Vision class


    Capture images from stereo camera and process with stereo matcher
    to generate depth. Brings together Stereo Camera and Stereo Matcher classes into
    single class for easy use.
    """
    @staticmethod
    def __init__(*args, **kwargs) -> typing.Any: 
        """
        Load stereo matcher

        Parameters
        ----------
        left_yaml : str
        right_yaml : str
        """
    def connect(self) -> bool: 
        """
        Connect camera from reading CameraDeviceInfo
        """
    def disconnect(self) -> None: 
        """
        Disconnect camera from reading CameraDeviceInfo
        """
    @staticmethod
    def getCalibration(*args, **kwargs) -> typing.Any: 
        """
        Load stereo calibration
        """
    @staticmethod
    def getCamera(*args, **kwargs) -> typing.Any: 
        """
        Load camera
        """
    def getDownsampleFactor(self) -> float: 
        """
        Get the value of Downsample Factor

        Returns
        -------
        value : float
            Downsampled factor
        """
    def getHFOV(self) -> float: 
        """
        Get horitonzal Field Of View of camera from Q matrix

        Returns
        -------
        fov_x : float
            Horitonzal Field Of View of camera from Q matrix
        """
    def getHeight(self) -> int: 
        """
        Get the height of image

        Returns
        -------
        value : int
            Height of image
        """
    @staticmethod
    def getMatcher(*args, **kwargs) -> typing.Any: 
        """
        Load stereo matcher
        """
    @staticmethod
    def getReadThreadResult(*args, **kwargs) -> typing.Any: 
        """
        Get the result of thread read
        """
    def getWidth(self) -> int: 
        """
        Get the width of image

        Returns
        -------
        value : int
            Width of image
        """
    def isCapturing(self) -> bool: 
        """
        Check if camera is capturing
        """
    def isConnected(self) -> bool: 
        """
        Check if camera is connected
        """
    def isReadThreadRunning(self) -> bool: 
        """
        Check if camera thread is reading

        Returns
        -------
        bool
            True if thread is reading
        """
    def isValidCalibration(self) -> bool: 
        """
        Check if the calibration file pair is valid 

        Returns
        -------
        bool
            True is calibration is valid
        """
    @staticmethod
    def read(*args, **kwargs) -> typing.Any: 
        """
        Read image from camera

        Parameters
        ----------
        timeout : int
            timeout in millisecond, default timeout is 1000(1s)
        Returns
        -------
        left : numpy.ndarray, right : numpy.ndarray
            Return stereo images left, right
        """
    def setDownsampleFactor(self, arg0: float) -> None: 
        """
        Set downsample factor

        Parameters
        ----------
        value : float
            Desired value of downsample factor
        """
    def setTestImagePaths(self, arg0: str, arg1: str) -> None: 
        """
        Set the path for test images, input both left and right image path

        Parameters
        ----------
        left_test_image_path    : str
        right_test_image_path   : str
        """
    def startCapture(self) -> bool: 
        """
        To start camera communication
        """
    def startReadThread(self, timeout: int = 1000, rectify: bool = True) -> None: 
        """
        Read camera thread

        Parameters
        ----------
        timeout : int
            timeout in millisecond, default timeout is 1000(1s)

        Returns
        -------
        bool
            True if thread is reading
        """
    def stopCapture(self) -> None: 
        """
        To stop camera communication
        """
    pass
def bgr2bgra(arg0: numpy.ndarray) -> numpy.ndarray:
    """
    Convert BGR image to BGRA.

    Parameters
    ----------
    bgr : numpy.ndarray
        BGR image to convert

    Returns
    -------
    numpy.ndarray
        BGRA image
    """
def bgr2rgba(arg0: numpy.ndarray) -> numpy.ndarray:
    """
    Convert BGR image to RGBA.

    Parameters
    ----------
    bgr : numpy.ndarray
        BGR image to convert

    Returns
    -------
    numpy.ndarray
        RGBA image
    """
def bgra2rgba(arg0: numpy.ndarray) -> numpy.ndarray:
    """
    Convert BGRA image to RGBA.

    Parameters
    ----------
    bgra : numpy.ndarray
        BGRA image to convert

    Returns
    -------
    numpy.ndarray
        RGBA image
    """
def cvMatIsEqual(arg0: numpy.ndarray, arg1: numpy.ndarray) -> bool:
    """
    Check if two numpy.ndarray objects are equal.

    Parameters
    ----------
    mat1 : numpy.ndarray
        First numpy.ndarray object
    mat2 : numpy.ndarray
        Second numpy.ndarray object

    Returns
    -------
    bool
        True if equal
    """
def depth2xyz(arg0: numpy.ndarray, arg1: float) -> numpy.ndarray:
    """
    Calculate Point cloud (xyz) from depth image.

    Parameters
    ----------
    xyz : numpy.ndarray
        Point cloud (xyz)
    hfov : float
        Horizontal field of view (degrees)

    Returns
    -------
    numpy.ndarray
        Point cloud (xyz)
    """
def disparity2depth(arg0: numpy.ndarray, arg1: numpy.ndarray) -> numpy.ndarray:
    """
    Calculate depth image from disparity image.

    Parameters
    ----------
    disparity : numpy.ndarray
        Disparity image
    Q: numpy.ndarray
        Q Matrix from calibration (e.g. 'calibration.getQ()')

    Returns
    -------
    numpy.ndarray
        Depth image
    """
def disparity2xyz(arg0: numpy.ndarray, arg1: numpy.ndarray) -> numpy.ndarray:
    """
    Calculate point cloud (xyz) from disparity image.

    Parameters
    ----------
    disparity : numpy.ndarray
        Disparity image
    Q: numpy.ndarray
        Q Matrix from calibration (e.g. 'calibration.getQ()')

    Returns
    -------
    numpy.ndarray
        Point clouds (xyz)
    """
def flip(arg0: numpy.ndarray, arg1: int) -> numpy.ndarray:
    """
    Flip image horizontally or vertically based on flip code.

    Parameters
    ----------
    image : numpy.ndarray
        Image to flip
    flip_code : int
        Flip code (0 = horizontal, 1 = vertical)

    Returns
    -------
    numpy.ndarray
        Flipped image
    """
def getVersionMajor() -> int:
    """
    Get major of pyphase

    Returns
    -------
    value : int
    """
def getVersionMinor() -> int:
    """
    Get minor of pyphase

    Returns
    -------
    value : int
    """
def getVersionPatch() -> int:
    """
    Get version patch of pyphase

    Returns
    -------
    value : int
    """
def getVersionString() -> str:
    """
    Get version of pyphase

    Returns
    -------
    string : str
    """
def normaliseDisparity(arg0: numpy.ndarray) -> numpy.ndarray:
    """
    Normalise disparity image.

    Parameters
    ----------
    disparity : numpy.ndarray
        Dispairty image to normalise

    Returns
    -------
    numpy.ndarray
        Normalised disparity image
    """
def processStereo(*args, **kwargs) -> typing.Any:
    """
    Load in calibration files and process stereo images, returns error if failed
    """
def processStereoFiles(*args, **kwargs) -> typing.Any:
    """
    Process stereo calibration files, returns error if failed
    """
def readImage(arg0: str) -> numpy.ndarray:
    """
    Read image from file.

    Parameters
    ----------
    image_filepath : str
        Filepath of image

    Returns
    -------
    numpy.ndarray
        Image
    """
def savePLY(arg0: str, arg1: numpy.ndarray, arg2: numpy.ndarray) -> bool:
    """
    Save point cloud to PLY file.

    Parameters
    ----------
    ply_filepath : str
        Filepath of PLY file
    xyz : numpy.ndarray
        Point cloud (xyz)
    rgb : numpy.ndarray
        RGB image for point cloud colours

    Returns
    -------
    bool
        True if successful
    """
def scaleImage(arg0: numpy.ndarray, arg1: float) -> numpy.ndarray:
    """
    Scale image to a new size.

    Parameters
    ----------
    image : numpy.ndarray
        Image to scale
    scale_factor : float
        Scale factor to apply to image

    Returns
    -------
    numpy.ndarray
        Scaled image
    """
def showImage(arg0: str, arg1: numpy.ndarray) -> int:
    """
    Display image in GUI window.

    Parameters
    ----------
    window_name : str
        Name of window
    image : numpy.ndarray
        Point cloud (xyz)
    """
def xyz2depth(arg0: numpy.ndarray) -> numpy.ndarray:
    """
    Calculate depth image from point cloud (xyz).

    Parameters
    ----------
    xyz : numpy.ndarray
        Point cloud (xyz)

    Returns
    -------
    numpy.ndarray
        Depth image
    """
