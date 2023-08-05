"""stereo matcher"""
import phase.pyphase.stereomatcher
import typing
import numpy
import phase.pyphase.types
_Shape = typing.Tuple[int, ...]

__all__ = [
    "AbstractStereoMatcher",
    "StereoBM",
    "StereoHOBM",
    "StereoI3DRSGM",
    "StereoParams",
    "StereoSGBM",
    "createStereoMatcher"
]


class AbstractStereoMatcher():
    """
    Class to set the parameters for stereo matcher
    """
    def compute(self, arg0: numpy.ndarray, arg1: numpy.ndarray) -> phase.pyphase.types.StereoMatcherComputeResult: 
        """
        Compute stereo matching

        Parameters
        ----------
        left_image : numpy.ndarray
            Left image of stereo pair
        right_image : numpy.ndarray
            Right image of stereo pair
        """
    def getComputeThreadResult(self) -> phase.pyphase.types.StereoMatcherComputeResult: 
        """
        Get compute thread result 
        """
    def isComputeThreadRunning(self) -> bool: 
        """
        Check if compute thread is running

        Returns
        -------
        bool
            True is compute thread is running
        """
    @staticmethod
    def setComputeThreadCallback(*args, **kwargs) -> typing.Any: 
        """
        Set to compute thread callback

        Parameters
        ----------
        computeThread_callback : std::function<void __cdecl(void)>
        """
    def startComputeThread(self, arg0: numpy.ndarray, arg1: numpy.ndarray) -> None: 
        """
        Start compute thread

        Parameters
        ----------
        left_image : numpy.ndarray
            Left image of stereo pair
        right_image : numpy.ndarray
            Right image of stereo pair
        """
    pass
class StereoBM():
    """
    Class to set the parameters for stereoBM matcher
    """
    @typing.overload
    def __init__(self) -> None: 
        """
        Stereo parameters contain matcherType, windowSize, minDisparity, numDisparities, interpolation
        """
    @typing.overload
    def __init__(self, arg0: StereoParams) -> None: ...
    def compute(self, arg0: numpy.ndarray, arg1: numpy.ndarray) -> phase.pyphase.types.StereoMatcherComputeResult: 
        """
        Compute stereo matching

        Parameters
        ----------
        left_image : numpy.ndarray
            Left image of stereo pair
        right_image : numpy.ndarray
            Right image of stereo pair
        """
    def getComputeThreadResult(self) -> phase.pyphase.types.StereoMatcherComputeResult: 
        """
        Get compute thread result 
        """
    def isComputeThreadRunning(self) -> bool: 
        """
        Check if compute thread is running

        Returns
        -------
        bool
            True is compute thread is running
        """
    def setComputeThreadCallback(self, arg0: typing.Callable[[], None]) -> None: 
        """
        Set to compute thread callback

        Parameters
        ----------
        computeThread_callback : std::function<void __cdecl(void)>
        """
    def setMinDisparity(self, arg0: int) -> None: 
        """
        Set minimum disparity value

        Parameters
        ----------
        value : int
            Desired value of minimum disparity value
        """
    def setNumDisparities(self, arg0: int) -> None: 
        """
        Set number of disparities

        Parameters
        ----------
        value : int
            Desired value of number of disparities
        """
    def setWindowSize(self, arg0: int) -> None: 
        """
        Set window size value

        Parameters
        ----------
        value : int
            Desired value of window size value
        """
    def startComputeThread(self, arg0: numpy.ndarray, arg1: numpy.ndarray) -> None: 
        """
        Start compute thread

        Parameters
        ----------
        left_image : numpy.ndarray
            Left image of stereo pair
        right_image : numpy.ndarray
            Right image of stereo pair
        """
    pass
class StereoHOBM():
    """
    Class to set the parameters for stereoHOBM matcher
    """
    @typing.overload
    def __init__(self) -> None: 
        """
        TODOC


                    Stereo parameters contain matcherType, windowSize, minDisparity, numDisparities, interpolation
                    
                    
        """
    @typing.overload
    def __init__(self, arg0: StereoParams) -> None: ...
    def compute(self, arg0: numpy.ndarray, arg1: numpy.ndarray) -> phase.pyphase.types.StereoMatcherComputeResult: 
        """
        Compute stereo matching

        Parameters
        ----------
        left_image : numpy.ndarray
            Left image of stereo pair
        right_image : numpy.ndarray
            Right image of stereo pair
        """
    def getComputeThreadResult(self) -> phase.pyphase.types.StereoMatcherComputeResult: 
        """
        Get compute thread result 
        """
    def isComputeThreadRunning(self) -> bool: 
        """
        Check if compute thread is running

        Returns
        -------
        bool
            True is compute thread is running
        """
    def setComputeThreadCallback(self, arg0: typing.Callable[[], None]) -> None: 
        """
        Set to compute thread callback

        Parameters
        ----------
        computeThread_callback : std::function<void __cdecl(void)>
        """
    def setMinDisparity(self, arg0: int) -> None: 
        """
        Set minimum disparity value

        Parameters
        ----------
        value : int
            Desired value of minimum disparity value
        """
    def setNumDisparities(self, arg0: int) -> None: 
        """
        Set number of disparities

        Parameters
        ----------
        value : int
            Desired value of number of disparities
        """
    def setWindowSize(self, arg0: int) -> None: 
        """
        Set window size value

        Parameters
        ----------
        value : int
            Desired value of window size value
        """
    def startComputeThread(self, arg0: numpy.ndarray, arg1: numpy.ndarray) -> None: 
        """
        Start compute thread

        Parameters
        ----------
        left_image : numpy.ndarray
            Left image of stereo pair
        right_image : numpy.ndarray
            Right image of stereo pair
        """
    pass
class StereoI3DRSGM():
    """
    Class to set the parameters for stereoI3DRSGM matcher
    """
    @typing.overload
    def __init__(self) -> None: 
        """
        TODOC


                    Stereo parameters contain matcherType, windowSize, minDisparity, numDisparities, interpolation
                    
                    
        """
    @typing.overload
    def __init__(self, arg0: StereoParams) -> None: ...
    def compute(self, arg0: numpy.ndarray, arg1: numpy.ndarray) -> phase.pyphase.types.StereoMatcherComputeResult: 
        """
        Compute stereo matching

        Parameters
        ----------
        left_image : numpy.ndarray
            Left image of stereo pair
        right_image : numpy.ndarray
            Right image of stereo pair
        """
    def enableInterpolation(self, arg0: bool) -> None: 
        """
        To enable interpolation

        Parameters
        ----------
        enable : bool
            Set True to enable interpolation
        """
    def enableSubpixel(self, arg0: bool) -> None: 
        """
        To enable subpixel

        Parameters
        ----------
        enable : bool
            Set True to enable subpixel
        """
    def getComputeThreadResult(self) -> phase.pyphase.types.StereoMatcherComputeResult: 
        """
        Get compute thread result
        """
    def isComputeThreadRunning(self) -> bool: 
        """
        Check if compute thread is running

        Returns
        -------
        bool
            True is compute thread is running
        """
    @staticmethod
    def isLicenseValid() -> bool: 
        """
        Check if the I3DRSGM license is valid

        Returns
        -------
        bool
            True if license is valid
        """
    def setComputeThreadCallback(self, arg0: typing.Callable[[], None]) -> None: 
        """
        Set to compute thread callback

        Parameters
        ----------
        computeThread_callback : std::function<void __cdecl(void)>
        """
    def setMinDisparity(self, arg0: int) -> None: 
        """
        Set minimum disparity value

        Parameters
        ----------
        value : int
            Desired value of minimum disparity value
        """
    def setNumDisparities(self, arg0: int) -> None: 
        """
        Set number of disparities

        Parameters
        ----------
        value : int
            Desired value of number of disparities
        """
    def setSpeckleMaxDiff(self, arg0: float) -> None: 
        """
        To enable speckle maximum difference

        Parameters
        ----------
        enable : bool
            Set True to enable speckle maximum difference
        """
    def setSpeckleMaxSize(self, arg0: int) -> None: 
        """
        To enable speckle maximum size

        Parameters
        ----------
        enable : bool
            Set True to enable speckle maximum size
        """
    def setWindowSize(self, arg0: int) -> None: 
        """
        Set window size value

        Parameters
        ----------
        value : int
            Desired value of window size value
        """
    def startComputeThread(self, arg0: numpy.ndarray, arg1: numpy.ndarray) -> None: 
        """
        Start compute thread

        Parameters
        ----------
        left_image : numpy.ndarray
            Left image of stereo pair
        right_image : numpy.ndarray
            Right image of stereo pair
        """
    pass
class StereoParams():
    """
    Class of stereo matcher parameters
    """
    def __init__(self, arg0: phase.pyphase.types.StereoMatcherType, arg1: int, arg2: int, arg3: int, arg4: bool) -> None: 
        """
        Stereo parameters contain matcherType, windowSize, minDisparity, numDisparities, interpolation
        """
    @property
    def interpolation(self) -> bool:
        """
        :type: bool
        """
    @interpolation.setter
    def interpolation(self, arg0: bool) -> None:
        pass
    @property
    def matcherType(self) -> phase.pyphase.types.StereoMatcherType:
        """
        :type: phase.pyphase.types.StereoMatcherType
        """
    @matcherType.setter
    def matcherType(self, arg0: phase.pyphase.types.StereoMatcherType) -> None:
        pass
    @property
    def minDisparity(self) -> int:
        """
        :type: int
        """
    @minDisparity.setter
    def minDisparity(self, arg0: int) -> None:
        pass
    @property
    def numDisparities(self) -> int:
        """
        :type: int
        """
    @numDisparities.setter
    def numDisparities(self, arg0: int) -> None:
        pass
    @property
    def windowSize(self) -> int:
        """
        :type: int
        """
    @windowSize.setter
    def windowSize(self, arg0: int) -> None:
        pass
    pass
class StereoSGBM():
    """
    Class to set the parameters for stereoSGBM matcher
    """
    @typing.overload
    def __init__(self) -> None: 
        """
        Stereo parameters contain matcherType, windowSize, minDisparity, numDisparities, interpolation
        """
    @typing.overload
    def __init__(self, arg0: StereoParams) -> None: ...
    def compute(self, arg0: numpy.ndarray, arg1: numpy.ndarray) -> phase.pyphase.types.StereoMatcherComputeResult: 
        """
        Compute stereo matching

        Parameters
        ----------
        left_image : numpy.ndarray
            Left image of stereo pair
        right_image : numpy.ndarray
            Right image of stereo pair
        """
    def getComputeThreadResult(self) -> phase.pyphase.types.StereoMatcherComputeResult: 
        """
        Get compute thread result
        """
    def isComputeThreadRunning(self) -> bool: 
        """
        Check if compute thread is running

        Returns
        -------
        bool
            True is compute thread is running
        """
    def setComputeThreadCallback(self, arg0: typing.Callable[[], None]) -> None: 
        """
        Set to compute thread callback

        Parameters
        ----------
        computeThread_callback : std::function<void __cdecl(void)>
        """
    def setMinDisparity(self, arg0: int) -> None: 
        """
        Set minimum disparity value

        Parameters
        ----------
        value : int
            Desired value of minimum disparity value
        """
    def setNumDisparities(self, arg0: int) -> None: 
        """
        Set number of disparities

        Parameters
        ----------
        value : int
            Desired value of number of disparities
        """
    def setWindowSize(self, arg0: int) -> None: 
        """
        Set window size value

        Parameters
        ----------
        value : int
            Desired value of window size value
        """
    def startComputeThread(self, arg0: numpy.ndarray, arg1: numpy.ndarray) -> None: 
        """
        Start compute thread

        Parameters
        ----------
        left_image : numpy.ndarray
            Left image of stereo pair
        right_image : numpy.ndarray
            Right image of stereo pair
        """
    pass
@typing.overload
def createStereoMatcher(arg0: StereoParams) -> AbstractStereoMatcher:
    """
    Stereo matcher type ROS, OpenCV etc.




    Stereo parameters contain matcherType, windowSize, minDisparity, numDisparities, interpolation
    """
@typing.overload
def createStereoMatcher(arg0: phase.pyphase.types.StereoMatcherType) -> AbstractStereoMatcher:
    pass
