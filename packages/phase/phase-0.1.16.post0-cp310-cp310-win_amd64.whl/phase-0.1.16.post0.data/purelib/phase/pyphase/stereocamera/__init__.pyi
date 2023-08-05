"""stereo camera"""
from __future__ import annotations
import phase.pyphase.stereocamera
import typing
import phase.pyphase.types

__all__ = [
    "AbstractStereoCamera",
    "DeimosStereoCamera",
    "PhobosStereoCamera",
    "PylonStereoCamera",
    "TitaniaStereoCamera",
    "UVCStereoCamera",
    "createStereoCamera"
]


class AbstractStereoCamera():
    """
    Variables contain camera data
    """
    def connect(self) -> bool: 
        """
        Connect camera from reading CameraDeviceInfo
        """
    def disconnect(self) -> None: 
        """
        Disconnect camera from reading CameraDeviceInfo
        """
    def enableDataCapture(self, arg0: bool) -> None: 
        """
        Enable data capture

        Parameters
        ----------
        enable : bool
            Set "True" to enable data capture
        """
    def enableHardwareTrigger(self, arg0: bool) -> None: 
        """
        To enable camera trigger

        Parameters
        ----------

        enable : bool
            Set "True" to enable trigger
        """
    def getCaptureCount(self) -> int: 
        """
        Get the capture count

        Returns
        -------
        value : int
            Value of capture count
        """
    def getDownsampleFactor(self) -> float: 
        """
        Get the value of Downsample Factor
                    
                    Returns
                    -------
                    value : float
                        Downsampled factor
                    
        """
    def getFrameRate(self) -> float: 
        """
        Get the value of frame rate
        """
    def getHeight(self) -> int: 
        """
        Get the height of image

        Returns
        -------
        value : int
            Height of image
        """
    def getReadThreadResult(self) -> phase.pyphase.types.CameraReadResult: 
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
    def isContinousReadThreadRunning(self) -> bool: 
        """
        Check if thread is continuously reading

        Returns
        -------
        bool
            True if thread is reading
        """
    def isReadThreadRunning(self) -> bool: 
        """
        Check if camera thread is reading

        Returns
        -------
        bool
            True if thread is reading
        """
    def read(self, timeout: int = 1000) -> phase.pyphase.types.CameraReadResult: 
        """
        Read image from createStereoCamera

        Parameters
        ----------
        timeout : int
            timeout in millisecond, default timeout is 1000(1s)

        Returns
        -------
        left : numpy.ndarray, right : numpy.ndarray
            Return stereo images left, right
        """
    def resetCaptureCount(self) -> None: 
        """
        Reset the capture count
        """
    def setDataCapturePath(self, arg0: str) -> None: 
        """
        Set path of saved directory for capture data

        path : str
            directory of desired capture data storage
        """
    def setDownsampleFactor(self, arg0: float) -> None: 
        """
        To overwrite the downsample factor

        Parameters
        ----------
        float : value
            Set desired downsample factor
        """
    def setExposure(self, arg0: int) -> None: 
        """
        To overwrite the exposure value

        Parameters
        ----------

        value : int
            Input desired value of exposure
        """
    def setFrameRate(self, arg0: float) -> None: 
        """
        To overwrite the frame rate

        Parameters
        ----------
        value : float
            Input desired value of frame rate
        """
    def setLeftAOI(self, arg0: int, arg1: int, arg2: int, arg3: int) -> None: 
        """
        To set a new area of interest for LEFT image

        Parameters
        ----------
        x_min : int
            x value of top left corner of targeted AOI
        y_min : int
            y value of top left corner of targeted AOI
        x_max : int
            x value of bottom right corner of targeted AOI
        y_max : int
            y value of bottom right corner of targeted AOI
        """
    def setLeftFlipX(self, arg0: bool) -> None: 
        """
        Flip left image in x axis

        Parameters
        ----------
        enable : bool
            Set "True" to flip image
        """
    def setLeftFlipY(self, arg0: bool) -> None: 
        """
        Flip left image in y axis

        Parameters
        ----------
        enable : bool
            Set "True" to flip image
        """
    def setReadThreadCallback(self, arg0: typing.Callable[[phase.pyphase.types.CameraReadResult], None]) -> None: 
        """
        Set read thread callback from function read
        """
    def setRightAOI(self, arg0: int, arg1: int, arg2: int, arg3: int) -> None: 
        """
        To set a new area of interest for RIGHT image

        Parameters
        ----------
        x_min : int
            x value of top left corner of targeted AOI
        y_min : int
            y value of top left corner of targeted AOI
        x_max : int
            x value of bottom right corner of targeted AOI
        y_max : int
            y value of bottom right corner of targeted AOI
        """
    def setRightFlipX(self, arg0: bool) -> None: 
        """
        Flip right image in x axis

        Parameters
        ----------
        enable : bool
            Set "True" to flip image
        """
    def setRightFlipY(self, arg0: bool) -> None: 
        """
        Flip right image in y axis

        Parameters
        ----------
        enable : bool
            Set "True" to flip image
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
    def startContinousReadThread(self, timeout: int = 1000) -> bool: 
        """
        Start read thread continuously

        Parameters
        ----------
        timeout : int
            timeout in millisecond, default timeout is 1000(1s)

        Returns
        -------
        bool
            True if thread is reading
        """
    def startReadThread(self, timeout: int = 1000) -> bool: 
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
    def stopContinousReadThread(self) -> None: 
        """
        Stop read thread continuously after startContinousReadThread
        """
    pass
class DeimosStereoCamera():
    """
    Variables contain Deimos camera data
    """
    def __init__(self, arg0: phase.pyphase.types.CameraDeviceInfo) -> None: 
        """
        Variable stored unique camera information

        Parameters
        ----------

        left_serial     : str
            Camera left serial ID
        right_serial    : str
            Camera right serial ID
        unique_serial   : str
            Camera unique serial ID
        device_type     : enum
            enum of device type, according to the type of camera
        interface_type  : enum
            enum of interface type, according to the type of camera connection
        """
    def connect(self) -> bool: 
        """
        Connect camera from reading CameraDeviceInfo
        """
    def disconnect(self) -> None: 
        """
        Disconnect camera from reading CameraDeviceInfo
        """
    def enableDataCapture(self, arg0: bool) -> None: 
        """
        Enable data capture

        Parameters
        ----------
        enable : bool
            Set "True" to enable data capture
        """
    def enableHardwareTrigger(self, arg0: bool) -> None: 
        """
        To enable camera trigger

        Parameters
        ----------

        enable : bool
            Set "True" to enable trigger
        """
    def getCaptureCount(self) -> int: 
        """
        Get the capture count

        Returns
        -------
        value : int
            Value of capture count
        """
    def getDownsampleFactor(self) -> float: 
        """
        Get the value of Downsample Factor

        Returns
        -------
        value : float
            Downsampled factor
        """
    def getFrameRate(self) -> float: 
        """
        Get the value of frame rate
        """
    def getHeight(self) -> int: 
        """
        Get the height of Deimos image

        Returns
        -------
        value : int
            Height of Deimos image
        """
    def getReadThreadResult(self) -> phase.pyphase.types.CameraReadResult: 
        """
        Get the result of thread read
        """
    def getWidth(self) -> int: 
        """
        Get the width of Deimos image

        Returns
        -------
        value : int
            Width of Deimos image
        """
    def isCapturing(self) -> bool: 
        """
        Check if camera is capturing
        """
    def isConnected(self) -> bool: 
        """
        Check if camera is connected
        """
    def isContinousReadThreadRunning(self) -> bool: 
        """
        Check if thread is continuously reading

        Returns
        -------
        bool
            True if thread is reading
        """
    def isReadThreadRunning(self) -> bool: 
        """
        Check if camera thread is reading

        Returns
        -------
        bool
            True if thread is reading
        """
    def read(self, timeout: int = 1000) -> phase.pyphase.types.CameraReadResult: 
        """
        Read image from createStereoCamera

        Parameters
        ----------
        timeout : int
            timeout in millisecond, default timeout is 1000(1s)

        Returns
        -------
        left : numpy.ndarray, right : numpy.ndarray
            Return stereo images left, right
        """
    def resetCaptureCount(self) -> None: 
        """
        Reset the capture count
        """
    def setDataCapturePath(self, arg0: str) -> None: 
        """
        Set path of saved directory for capture data

        path : str
            directory of desired capture data storage
        """
    def setDownsampleFactor(self, arg0: float) -> None: 
        """
        To overwrite the downsample factor

        Parameters
        ----------
        float : value
            Set desired downsample factor
        """
    def setExposure(self, arg0: int) -> None: 
        """
        To overwrite the exposure value

        Parameters
        ----------

        value : int
            Input desired value of exposure
        """
    def setFrameRate(self, arg0: float) -> None: 
        """
        To overwrite the frame rate

        Parameters
        ----------
        value : float
            Input desired value of frame rate
        """
    def setLeftAOI(self, arg0: int, arg1: int, arg2: int, arg3: int) -> None: 
        """
        To set a new area of interest for LEFT image

        Parameters
        ----------
        x_min : int
            x value of top left corner of targeted AOI
        y_min : int
            y value of top left corner of targeted AOI
        x_max : int
            x value of bottom right corner of targeted AOI
        y_max : int
            y value of bottom right corner of targeted AOI
        """
    def setLeftFlipX(self, arg0: bool) -> None: 
        """
        Flip left image in x axis

        Parameters
        ----------
        enable : bool
            Set "True" to flip image
        """
    def setLeftFlipY(self, arg0: bool) -> None: 
        """
        Flip left image in y axis

        Parameters
        ----------
        enable : bool
            Set "True" to flip image
        """
    def setReadThreadCallback(self, arg0: typing.Callable[[phase.pyphase.types.CameraReadResult], None]) -> None: 
        """
        Set read thread callback from function read
        """
    def setRightAOI(self, arg0: int, arg1: int, arg2: int, arg3: int) -> None: 
        """
        To set a new area of interest for RIGHT image

        Parameters
        ----------
        x_min : int
            x value of top left corner of targeted AOI
        y_min : int
            y value of top left corner of targeted AOI
        x_max : int
            x value of bottom right corner of targeted AOI
        y_max : int
            y value of bottom right corner of targeted AOI
        """
    def setRightFlipX(self, arg0: bool) -> None: 
        """
        Flip right image in x axis

        Parameters
        ----------
        enable : bool
            Set "True" to flip image
        """
    def setRightFlipY(self, arg0: bool) -> None: 
        """
        Flip right image in y axis

        Parameters
        ----------
        enable : bool
            Set "True" to flip image
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
    def startContinousReadThread(self, timeout: int = 1000) -> bool: 
        """
        Start read thread continuously

        Parameters
        ----------
        timeout : int
            timeout in millisecond, default timeout is 1000(1s)

        Returns
        -------
        bool
            True if thread is reading
        """
    def startReadThread(self, timeout: int = 1000) -> bool: 
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
    def stopContinousReadThread(self) -> None: 
        """
        Stop read thread continuously after startContinousReadThread
        """
    pass
class PhobosStereoCamera():
    """
    Variables contain Phobos camera data
    """
    def __init__(self, arg0: phase.pyphase.types.CameraDeviceInfo) -> None: 
        """
        Variable stored unique camera information

        Parameters
        ----------

        left_serial     : str
            Camera left serial ID
        right_serial    : str
            Camera right serial ID
        unique_serial   : str
            Camera unique serial ID
        device_type     : enum
            enum of device type, according to the type of camera
        interface_type  : enum
            enum of interface type, according to the type of camera connection
        """
    def connect(self) -> bool: 
        """
        Connect camera from reading CameraDeviceInfo
        """
    def disconnect(self) -> None: 
        """
        Disconnect camera from reading CameraDeviceInfo
        """
    def enableDataCapture(self, arg0: bool) -> None: 
        """
        Enable data capture

        Parameters
        ----------
        enable : bool
            Set "True" to enable data capture
        """
    def enableHardwareTrigger(self, arg0: bool) -> None: 
        """
        To enable camera trigger

        Parameters
        ----------

        enable : bool
            Set "True" to enable trigger
        """
    def getCaptureCount(self) -> int: 
        """
        Get the capture count

        Returns
        -------
        value : int
            Value of capture count
        """
    def getDownsampleFactor(self) -> float: 
        """
        Get the value of Downsample Factor

        Returns
        -------
        value : float
            Downsampled factor
        """
    def getFrameRate(self) -> float: 
        """
        Get the value of frame rate
        """
    def getHeight(self) -> int: 
        """
        Get the height of Phobos image

        Returns
        -------
        value : int
            Height of Phobos image
        """
    def getReadThreadResult(self) -> phase.pyphase.types.CameraReadResult: 
        """
        Get the result of thread read
        """
    def getWidth(self) -> int: 
        """
        Get the width of Phobos image

        Returns
        -------
        value : int
            Width of Phobos image
        """
    def isCapturing(self) -> bool: 
        """
        Check if camera is capturing
        """
    def isConnected(self) -> bool: 
        """
        Check if camera is connected
        """
    def isContinousReadThreadRunning(self) -> bool: 
        """
        Check if thread is continuously reading

        Returns
        -------
        bool
            True if thread is reading
        """
    def isReadThreadRunning(self) -> bool: 
        """
        Check if camera thread is reading

        Returns
        -------
        bool
            True if thread is reading
        """
    def read(self, timeout: int = 1000) -> phase.pyphase.types.CameraReadResult: 
        """
        Read image from createStereoCamera

        Parameters
        ----------
        timeout : int
            timeout in millisecond, default timeout is 1000(1s)
        Returns
        -------
        left : numpy.ndarray, right : numpy.ndarray
            Return stereo images left, right
        """
    def resetCaptureCount(self) -> None: 
        """
        Reset the capture count
        """
    def setDataCapturePath(self, arg0: str) -> None: 
        """
        Set path of saved directory for capture data

        path : str
            directory of desired capture data storage
        """
    def setDownsampleFactor(self, arg0: float) -> None: 
        """
        To overwrite the downsample factor

        Parameters
        ----------
        float : value
            Set desired downsample factor
        """
    def setExposure(self, arg0: int) -> None: 
        """
        To overwrite the exposure value

        Parameters
        ----------

        value : int
            Input desired value of exposure
        """
    def setFrameRate(self, arg0: float) -> None: 
        """
        To overwrite the frame rate

        Parameters
        ----------
        value : float
            Input desired value of frame rate
        """
    def setLeftAOI(self, arg0: int, arg1: int, arg2: int, arg3: int) -> None: 
        """
        To set a new area of interest for LEFT image

        Parameters
        ----------
        x_min : int
            x value of top left corner of targeted AOI
        y_min : int
            y value of top left corner of targeted AOI
        x_max : int
            x value of bottom right corner of targeted AOI
        y_max : int
            y value of bottom right corner of targeted AOI
        """
    def setLeftFlipX(self, arg0: bool) -> None: 
        """
        Flip left image in x axis

        Parameters
        ----------
        enable : bool
            Set "True" to flip image
        """
    def setLeftFlipY(self, arg0: bool) -> None: 
        """
        Flip left image in y axis

        Parameters
        ----------
        enable : bool
            Set "True" to flip image
        """
    def setReadThreadCallback(self, arg0: typing.Callable[[phase.pyphase.types.CameraReadResult], None]) -> None: 
        """
        Set read thread callback from function read
        """
    def setRightAOI(self, arg0: int, arg1: int, arg2: int, arg3: int) -> None: 
        """
        To set a new area of interest for RIGHT image

        Parameters
        ----------
        x_min : int
            x value of top left corner of targeted AOI
        y_min : int
            y value of top left corner of targeted AOI
        x_max : int
            x value of bottom right corner of targeted AOI
        y_max : int
            y value of bottom right corner of targeted AOI
        """
    def setRightFlipX(self, arg0: bool) -> None: 
        """
        Flip right image in x axis

        Parameters
        ----------
        enable : bool
            Set "True" to flip image
        """
    def setRightFlipY(self, arg0: bool) -> None: 
        """
        Flip right image in y axis

        Parameters
        ----------
        enable : bool
            Set "True" to flip image
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
    def startContinousReadThread(self, timeout: int = 1000) -> bool: 
        """
        Start read thread continuously

        Parameters
        ----------
        timeout : int
            timeout in millisecond, default timeout is 1000(1s)

        Returns
        -------
        bool
            True if thread is reading
        """
    def startReadThread(self, timeout: int = 1000) -> bool: 
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
    def stopContinousReadThread(self) -> None: 
        """
        Stop read thread continuously after startContinousReadThread
        """
    pass
class PylonStereoCamera():
    """
    Variables contain Pylon camera data
    """
    def __init__(self, arg0: phase.pyphase.types.CameraDeviceInfo) -> None: 
        """
        Variable stored unique camera information

        Parameters
        ----------

        left_serial     : str
            Camera left serial ID
        right_serial    : str
            Camera right serial ID
        unique_serial   : str
            Camera unique serial ID
        device_type     : enum
            enum of device type, according to the type of camera
        interface_type  : enum
            enum of interface type, according to the type of camera connection
        """
    def connect(self) -> bool: 
        """
        Connect camera from reading CameraDeviceInfo
        """
    def disconnect(self) -> None: 
        """
        Disconnect camera from reading CameraDeviceInfo
        """
    def enableDataCapture(self, arg0: bool) -> None: 
        """
        Enable data capture

        Parameters
        ----------
        enable : bool
            Set "True" to enable data capture
        """
    def enableHardwareTrigger(self, arg0: bool) -> None: 
        """
        To enable camera trigger

        Parameters
        ----------

        enable : bool
            Set "True" to enable trigger
        """
    def getCaptureCount(self) -> int: 
        """
        Get the capture count

        Returns
        -------
        value : int
            Value of capture count 
        """
    def getDownsampleFactor(self) -> float: 
        """
        Get the value of Downsample Factor

        Returns
        -------
        value : float
            Downsampled factor
        """
    def getFrameRate(self) -> float: 
        """
        Get the value of frame rate
        """
    def getHeight(self) -> int: 
        """
        Get the height of Pylon image

        Returns
        -------
        value : int
            Height of Pylon image
        """
    def getReadThreadResult(self) -> phase.pyphase.types.CameraReadResult: 
        """
        Get the result of thread read
        """
    def getWidth(self) -> int: 
        """
        Get the width of Pylon image

        Returns
        -------
        value : int
            Width of Pylon image
        """
    def isCapturing(self) -> bool: 
        """
        Check if camera is capturing
        """
    def isConnected(self) -> bool: 
        """
        Check if camera is connected
        """
    def isContinousReadThreadRunning(self) -> bool: 
        """
        Check if thread is continuously reading

        Returns
        -------
        bool
            True if thread is reading
        """
    def isReadThreadRunning(self) -> bool: 
        """
        Check if camera thread is reading

        Returns
        -------
        bool
            True if thread is reading
        """
    def read(self, timeout: int = 1000) -> phase.pyphase.types.CameraReadResult: 
        """
        Read image from createStereoCamera

        Parameters
        ----------
        timeout : int
            timeout in millisecond, default timeout is 1000(1s)
        Returns
        -------
        left : numpy.ndarray, right : numpy.ndarray
            Return stereo images left, right
        """
    def resetCaptureCount(self) -> None: 
        """
        Reset the capture count
        """
    def setDataCapturePath(self, arg0: str) -> None: 
        """
        Set path of saved directory for capture data

        path : str
            directory of desired capture data storage
        """
    def setDownsampleFactor(self, arg0: float) -> None: 
        """
        To overwrite the downsample factor

        Parameters
        ----------
        float : value
            Set desired downsample factor
        """
    def setExposure(self, arg0: int) -> None: 
        """
        To overwrite the exposure value

        Parameters
        ----------

        value : int
            Input desired value of exposure
        """
    def setFrameRate(self, arg0: float) -> None: 
        """
        To overwrite the frame rate

        Parameters
        ----------
        value : float
            Input desired value of frame rate
        """
    def setLeftAOI(self, arg0: int, arg1: int, arg2: int, arg3: int) -> None: 
        """
        To set a new area of interest for LEFT image

        Parameters
        ----------
        x_min : int
            x value of top left corner of targeted AOI
        y_min : int
            y value of top left corner of targeted AOI
        x_max : int
            x value of bottom right corner of targeted AOI
        y_max : int
            y value of bottom right corner of targeted AOI
        """
    def setLeftFlipX(self, arg0: bool) -> None: 
        """
        Flip left image in x axis

        Parameters
        ----------
        enable : bool
            Set "True" to flip image
        """
    def setLeftFlipY(self, arg0: bool) -> None: 
        """
        Flip left image in y axis

        Parameters
        ----------
        enable : bool
            Set "True" to flip image
        """
    def setReadThreadCallback(self, arg0: typing.Callable[[phase.pyphase.types.CameraReadResult], None]) -> None: 
        """
        Set read thread callback from function read
        """
    def setRightAOI(self, arg0: int, arg1: int, arg2: int, arg3: int) -> None: 
        """
        To set a new area of interest for RIGHT image

        Parameters
        ----------
        x_min : int
            x value of top left corner of targeted AOI
        y_min : int
            y value of top left corner of targeted AOI
        x_max : int
            x value of bottom right corner of targeted AOI
        y_max : int
            y value of bottom right corner of targeted AOI
        """
    def setRightFlipX(self, arg0: bool) -> None: 
        """
        Flip right image in x axis

        Parameters
        ----------
        enable : bool
            Set "True" to flip image
        """
    def setRightFlipY(self, arg0: bool) -> None: 
        """
        Flip right image in y axis

        Parameters
        ----------
        enable : bool
            Set "True" to flip image
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
    def startContinousReadThread(self, timeout: int = 1000) -> bool: 
        """
        Start read thread continuously

        Parameters
        ----------
        timeout : int
            timeout in millisecond, default timeout is 1000(1s)

        Returns
        -------
        bool
            True if thread is reading
        """
    def startReadThread(self, timeout: int = 1000) -> bool: 
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
    def stopContinousReadThread(self) -> None: 
        """
        Stop read thread continuously after startContinousReadThread
        """
    pass
class TitaniaStereoCamera():
    """
    Variables contain Titania camera data
    """
    def __init__(self, arg0: phase.pyphase.types.CameraDeviceInfo) -> None: 
        """
        Variable stored unique camera information

        Parameters
        ----------

        left_serial     : str
            Camera left serial ID
        right_serial    : str
            Camera right serial ID
        unique_serial   : str
            Camera unique serial ID
        device_type     : enum
            enum of device type, according to the type of camera
        interface_type  : enum
            enum of interface type, according to the type of camera connection
        """
    def connect(self) -> bool: 
        """
        Connect camera from reading CameraDeviceInfo
        """
    def disconnect(self) -> None: 
        """
        Disconnect camera from reading CameraDeviceInfo
        """
    def enableDataCapture(self, arg0: bool) -> None: 
        """
        Enable data capture

        Parameters
        ----------
        enable : bool
            Set "True" to enable data capture
        """
    def enableHardwareTrigger(self, arg0: bool) -> None: 
        """
        To enable camera trigger

        Parameters
        ----------

        enable : bool
            Set "True" to enable trigger
        """
    def getCaptureCount(self) -> int: 
        """
        Get the capture count

        Returns
        -------
        value : int
            Value of capture count
        """
    def getDownsampleFactor(self) -> float: 
        """
         Get the value of Downsample Factor

        Returns
        -------
        value : float
            Downsampled factor
        """
    def getFrameRate(self) -> float: 
        """
        Get the value of frame rate
        """
    def getHeight(self) -> int: 
        """
        Get the height of Titania image

        Returns
        -------
        value : int
            Height of Titania image
        """
    def getReadThreadResult(self) -> phase.pyphase.types.CameraReadResult: 
        """
        Get the result of thread read
        """
    def getWidth(self) -> int: 
        """
        Get the width of Titania image

        Returns
        -------
        value : int
            Width of Titania image
        """
    def isCapturing(self) -> bool: 
        """
        Check if camera is capturing
        """
    def isConnected(self) -> bool: 
        """
        Check if camera is connected
        """
    def isContinousReadThreadRunning(self) -> bool: 
        """
        Check if thread is continuously reading

        Returns
        -------
        bool
            True if thread is reading
        """
    def isReadThreadRunning(self) -> bool: 
        """
        Check if camera thread is reading

        Returns
        -------
        bool
            True if thread is reading
        """
    def read(self, timeout: int = 1000) -> phase.pyphase.types.CameraReadResult: 
        """
        Read image from TitaniaStereoCamera

        Parameters
        ----------
        timeout : int
            timeout in millisecond, default timeout is 1000(1s)
        Returns
        -------
        left : numpy.ndarray, right : numpy.ndarray
            Return stereo images left, right
        """
    def resetCaptureCount(self) -> None: 
        """
        Reset the capture count
        """
    def setDataCapturePath(self, arg0: str) -> None: 
        """
        Set path of saved directory for capture data

        path : str
            directory of desired capture data storage
        """
    def setDownsampleFactor(self, arg0: float) -> None: 
        """
        To overwrite the downsample factor

        Parameters
        ----------
        float : value
            Set desired downsample factor
        """
    def setExposure(self, arg0: int) -> None: 
        """
        To overwrite the exposure value

        Parameters
        ----------

        value : int
            Input desired value of exposure
        """
    def setFrameRate(self, arg0: float) -> None: 
        """
        To overwrite the frame rate

        Parameters
        ----------
        value : float
            Input desired value of frame rate
        """
    def setLeftAOI(self, arg0: int, arg1: int, arg2: int, arg3: int) -> None: 
        """
        To set a new area of interest for LEFT image

        Parameters
        ----------
        x_min : int
            x value of top left corner of targeted AOI
        y_min : int
            y value of top left corner of targeted AOI
        x_max : int
            x value of bottom right corner of targeted AOI
        y_max : int
            y value of bottom right corner of targeted AOI
        """
    def setLeftFlipX(self, arg0: bool) -> None: 
        """
        Flip left image in x axis

        Parameters
        ----------
        enable : bool
            Set "True" to flip image
        """
    def setLeftFlipY(self, arg0: bool) -> None: 
        """
        Flip left image in y axis

        Parameters
        ----------
        enable : bool
            Set "True" to flip image
        """
    def setReadThreadCallback(self, arg0: typing.Callable[[phase.pyphase.types.CameraReadResult], None]) -> None: 
        """
        Set read thread callback from function read
        """
    def setRightAOI(self, arg0: int, arg1: int, arg2: int, arg3: int) -> None: 
        """
        To set a new area of interest for RIGHT image

        Parameters
        ----------
        x_min : int
            x value of top left corner of targeted AOI
        y_min : int
            y value of top left corner of targeted AOI
        x_max : int
            x value of bottom right corner of targeted AOI
        y_max : int
            y value of bottom right corner of targeted AOI
        """
    def setRightFlipX(self, arg0: bool) -> None: 
        """
        Flip right image in x axis

        Parameters
        ----------
        enable : bool
            Set "True" to flip image
        """
    def setRightFlipY(self, arg0: bool) -> None: 
        """
        Flip right image in y axis

        Parameters
        ----------
        enable : bool
            Set "True" to flip image
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
    def startContinousReadThread(self, timeout: int = 1000) -> bool: 
        """
        Start read thread continuously

        Parameters
        ----------
        timeout : int
            timeout in millisecond, default timeout is 1000(1s)

        Returns
        -------
        bool
            True if thread is reading
        """
    def startReadThread(self, timeout: int = 1000) -> bool: 
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
    def stopContinousReadThread(self) -> None: 
        """
        Stop read thread continuously after startContinousReadThread
        """
    pass
class UVCStereoCamera():
    """
    Variables contain Phobos camera data
    """
    def __init__(self, arg0: phase.pyphase.types.CameraDeviceInfo) -> None: 
        """
        Variable stored unique camera information

        Parameters
        ----------

        left_serial     : str
            Camera left serial ID
        right_serial    : str
            Camera right serial ID
        unique_serial   : str
            Camera unique serial ID
        device_type     : enum
            enum of device type, according to the type of camera
        interface_type  : enum
            enum of interface type, according to the type of camera connection
        """
    def connect(self) -> bool: 
        """
        Connect camera from reading CameraDeviceInfo
        """
    def disconnect(self) -> None: 
        """
        Disconnect camera from reading CameraDeviceInfo
        """
    def enableDataCapture(self, arg0: bool) -> None: 
        """
        Enable data capture

        Parameters
        ----------
        enable : bool
            Set "True" to enable data capture
        """
    def enableHardwareTrigger(self, arg0: bool) -> None: 
        """
        To enable camera trigger

        Parameters
        ----------

        enable : bool
            Set "True" to enable trigger
        """
    def getCaptureCount(self) -> int: 
        """
        Get the capture count

        Returns
        -------
        value : int
            Value of capture count
        """
    def getDownsampleFactor(self) -> float: 
        """
        Get the value of Downsample Factor

        Returns
        -------
        value : float
            Downsampled factor
        """
    def getFrameRate(self) -> float: 
        """
        Get the value of frame rate
        """
    def getHeight(self) -> int: 
        """
        Get the height of UVC image

        Returns
        -------
        value : int
            Height of UVC image)
        """
    def getReadThreadResult(self) -> phase.pyphase.types.CameraReadResult: 
        """
        Get the result of thread read
        """
    def getWidth(self) -> int: 
        """
        Get the width of UVC image

        Returns
        -------
        value : int
            Width of UVC image
        """
    def isCapturing(self) -> bool: 
        """
        Check if camera is capturing
        """
    def isConnected(self) -> bool: 
        """
        Check if camera is connected
        """
    def isContinousReadThreadRunning(self) -> bool: 
        """
        Check if thread is continuously reading

        Returns
        -------
        bool
            True if thread is reading
        """
    def isReadThreadRunning(self) -> bool: 
        """
        Check if camera thread is reading

        Returns
        -------
        bool
            True if thread is reading
        """
    def read(self, timeout: int = 1000) -> phase.pyphase.types.CameraReadResult: 
        """
        Read image from createStereoCamera

        Parameters
        ----------
        timeout : int
            timeout in millisecond, default timeout is 1000(1s)
        Returns
        -------
        left : numpy.ndarray, right : numpy.ndarray
            Return stereo images left, right
        """
    def resetCaptureCount(self) -> None: 
        """
        Reset the capture count
        """
    def setDataCapturePath(self, arg0: str) -> None: 
        """
        Set path of saved directory for capture data

        path : str
            directory of desired capture data storage
        """
    def setDownsampleFactor(self, arg0: float) -> None: 
        """
        To overwrite the downsample factor

        Parameters
        ----------
        float : value
            Set desired downsample factor
        """
    def setExposure(self, arg0: int) -> None: 
        """
        To overwrite the exposure value

        Parameters
        ----------

        value : int
            Input desired value of exposure
        """
    def setFrameRate(self, arg0: float) -> None: 
        """
        To overwrite the frame rate

        Parameters
        ----------
        value : float
            Input desired value of frame rate
        """
    def setLeftAOI(self, arg0: int, arg1: int, arg2: int, arg3: int) -> None: 
        """
        To set a new area of interest for LEFT image

        Parameters
        ----------
        x_min : int
            x value of top left corner of targeted AOI
        y_min : int
            y value of top left corner of targeted AOI
        x_max : int
            x value of bottom right corner of targeted AOI
        y_max : int
            y value of bottom right corner of targeted AOI
        """
    def setLeftFlipX(self, arg0: bool) -> None: 
        """
        Flip left image in x axis

        Parameters
        ----------
        enable : bool
            Set "True" to flip image
        """
    def setLeftFlipY(self, arg0: bool) -> None: 
        """
        Flip left image in y axis

        Parameters
        ----------
        enable : bool
            Set "True" to flip image
        """
    def setReadThreadCallback(self, arg0: typing.Callable[[phase.pyphase.types.CameraReadResult], None]) -> None: 
        """
        Set read thread callback from function read
        """
    def setRightAOI(self, arg0: int, arg1: int, arg2: int, arg3: int) -> None: 
        """
        To set a new area of interest for RIGHT image

        Parameters
        ----------
        x_min : int
            x value of top left corner of targeted AOI
        y_min : int
            y value of top left corner of targeted AOI
        x_max : int
            x value of bottom right corner of targeted AOI
        y_max : int
            y value of bottom right corner of targeted AOI
        """
    def setRightFlipX(self, arg0: bool) -> None: 
        """
        Flip right image in x axis

        Parameters
        ----------
        enable : bool
            Set "True" to flip image
        """
    def setRightFlipY(self, arg0: bool) -> None: 
        """
        Flip right image in y axis

        Parameters
        ----------
        enable : bool
            Set "True" to flip image
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
    def startContinousReadThread(self, timeout: int = 1000) -> bool: 
        """
        Start read thread continuously

        Parameters
        ----------
        timeout : int
            timeout in millisecond, default timeout is 1000(1s)

        Returns
        -------
        bool
            True if thread is reading
        """
    def startReadThread(self, timeout: int = 1000) -> bool: 
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
    def stopContinousReadThread(self) -> None: 
        """
        Stop read thread continuously after startContinousReadThread
        """
    pass
def createStereoCamera(arg0: phase.pyphase.types.CameraDeviceInfo) -> AbstractStereoCamera:
    """
    Read device type and return in related camera variable
    """
