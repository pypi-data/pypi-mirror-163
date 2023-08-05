"""camera calibration"""
import phase.pyphase.calib
import typing
import numpy
import phase.pyphase.types
_Shape = typing.Tuple[int, ...]

__all__ = [
    "CalibrationFileType",
    "CameraCalibration",
    "INVALID",
    "OPENCV_YAML",
    "ROS_YAML",
    "StereoCameraCalibration"
]


class CalibrationFileType():
    """
                Check the format of calibration files
                

    Members:

      ROS_YAML : 
                Format of ROS stereo calibration yaml

                

      OPENCV_YAML : 
                Format of OpenCV stereo calibration yaml
                
                

      INVALID : 
                   Invalid stereo calibration format 
                
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
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
    INVALID: phase.pyphase.calib.CalibrationFileType # value = <CalibrationFileType.INVALID: 2>
    OPENCV_YAML: phase.pyphase.calib.CalibrationFileType # value = <CalibrationFileType.OPENCV_YAML: 1>
    ROS_YAML: phase.pyphase.calib.CalibrationFileType # value = <CalibrationFileType.ROS_YAML: 0>
    __members__: dict # value = {'ROS_YAML': <CalibrationFileType.ROS_YAML: 0>, 'OPENCV_YAML': <CalibrationFileType.OPENCV_YAML: 1>, 'INVALID': <CalibrationFileType.INVALID: 2>}
    pass
class CameraCalibration():
    """
    Variables of stereo camera calibration file
    """
    @typing.overload
    def __init__(self, arg0: int, arg1: int, arg2: numpy.ndarray, arg3: numpy.ndarray, arg4: numpy.ndarray, arg5: numpy.ndarray) -> None: 
        """
        Get stereo camera calibration file location

        Parameters
        ----------
        calibration_filepath : str
            Stereo calibration file path location



        Load calibration file detail

        Parameters
        ----------
        width : int
            Image width of calibration file
        height : int
            Image height of calibration file
        camera_matrix : numpy.ndarray
            Camera Matrix of calibration file
        distortion_coefficients : numpy.ndarray
            Distortion coefficients of calibration file
        rectification_matrix : numpy.ndarray
            Rectification matrix of calibration file
        projection_matrix : numpy.ndarray
            Projection Matrix of calibration file
        """
    @typing.overload
    def __init__(self, arg0: str) -> None: ...
    @staticmethod
    def calibrationFromIdeal(arg0: int, arg1: int, arg2: float, arg3: float, arg4: float, arg5: float) -> CameraCalibration: 
        """
        Load calibration files from ideal, i.e. without distortion

        Parameters
        ----------
        width : int
            Image width of calibration file
        height : int
            Image height of calibration file
        pixel_pitch : float
            Pixel pitch of calibration file
        focal_length : float
            Focal length of calibration file
        translation_x : float
            Translation in x axis of calibration file
        translation_y : float
            Translation in y axis of calibration file
        """
    def getCameraCX(self) -> float: 
        """
        Get the cameraCX of calibration file

        Returns
        -------
        cameraCX : float
            CameraCX of calibration file
        """
    def getCameraCY(self) -> float: 
        """
        Get the cameraCY of calibration file

        Returns
        -------
        cameraCY : float
            CameraCY of calibration file
        """
    def getCameraFX(self) -> float: 
        """
        Get the cameraFX of calibration file

        Returns
        -------
        cameraFX : float
            CameraFX of calibration file
        """
    def getCameraFY(self) -> float: 
        """
        Get the cameraFY of calibration file

        Returns
        -------
        cameraFY : float
            CameraFY of calibration file
        """
    def getCameraMatrix(self) -> numpy.ndarray: 
        """
        Get the camera matrix of calibration file

        Returns
        -------
        camera_matrix : numpy.ndarray                
            Camera matrix of calibration file
        """
    def getDistortionCoefficients(self) -> numpy.ndarray: 
        """
        Get the distortion coefficients of calibration file

        Returns
        -------
        distortion_coefficients : numpy.ndarray  
            Distortion coefficients of calibration file
        """
    def getDownsampleFactor(self) -> float: 
        """
        Get the downsample factor

        Returns
        -------
        value : float
            Value of downsample factor
        """
    def getImageHeight(self) -> int: 
        """
        Get the image height from calibration

        Returns
        -------
        height : int
            Value of image height from calibration file
        """
    def getImageWidth(self) -> int: 
        """
        Get the image width from calibration

        Returns
        -------
        width : int
            Value of image width from calibration file
        """
    def getProjectionCX(self) -> float: 
        """
        Get the productionCX of calibration file

        Returns
        -------
        projectionCX : float
            ProductionCX of calibration file
        """
    def getProjectionCY(self) -> float: 
        """
        Get the productionCY of calibration file

        Returns
        -------
        projectionCY : float
            ProductionCY of calibration file
        """
    def getProjectionFX(self) -> float: 
        """
        Get the productionFX of calibration file

        Returns
        -------
        projectionFX : float
            ProductionFX of calibration file
        """
    def getProjectionFY(self) -> float: 
        """
        Get the productionFY of calibration file

        Returns
        -------
        projectionFY : float
            ProductionFY of calibration file
        """
    def getProjectionMatrix(self) -> numpy.ndarray: 
        """
        Get the projection matrix of calibration file

        Returns
        -------
        projection_matrix : numpy.ndarray  
            Projection matrix of calibration file
        """
    def getProjectionTX(self) -> float: 
        """
        Get the productionTX of calibration file

        Returns
        -------
        projectionTX : float
            ProductionTX of calibration file
        """
    def getRectificationMatrix(self) -> numpy.ndarray: 
        """
        Get the rectification matrix of calibration file

        Returns
        -------
        rectification_matrix : numpy.ndarray  
            Rectification matrix of calibration file
        """
    def isValid(self) -> bool: 
        """
        Check if the calibration file pair is valid 

        Returns
        -------
        bool
            True is calibration is valid
        """
    def remapPoint(self, arg0: phase.pyphase.types.Point2i) -> phase.pyphase.types.Point2i: 
        """
        Remap point

        Parameters
        ----------
        point : phase.pyphase.types.Point2i

        Returns
        -------
        remapped_point : phase.pyphase.types.Point2i
        """
    def setDownsampleFactor(self, arg0: float) -> None: 
        """
        Set the downsample factor

        Parameters
        ----------
        value : float
        """
    pass
class StereoCameraCalibration():
    """
    Variables of stereo camera calibration file
    """
    def __init__(self, arg0: CameraCalibration, arg1: CameraCalibration) -> None: 
        """
        Load left and right calibration file

        Parameters
        ----------
        left_calibration : phase.pyphase.calib.CameraCalibration
            Left calibration file
        right_calibration : phase.pyphase.calib.CameraCalibration
            Right calibration file
        """
    @staticmethod
    def calibrationFromIdeal(arg0: int, arg1: int, arg2: float, arg3: float, arg4: float) -> StereoCameraCalibration: 
        """
        Load calibration files with ideal variables

        Parameters
        ----------
        width : int
            Image width of calibration file
        height : int
            Image height of calibration file
        pixel_pitch : float
            Pixel pitch of calibration file
        focal_length : float
            Focal length of calibration file
        baseline : float
            Baseline value of calibration file
        """
    @staticmethod
    def calibrationFromYAML(arg0: str, arg1: str) -> StereoCameraCalibration: 
        """
        Load calibration files in yaml format

        Parameters
        ----------
        left_calibration_filepath : str
            Left side calibration file path directory
        right_calibration_filepath : str
            Right side calibration file path directory
        """
    def getBaseline(self) -> float: 
        """
        Get the baseline value of calibration file

        Returns
        -------
        value : float
            Baseline value of calibration file
        """
    def getDownsampleFactor(self) -> float: 
        """
        Get downsample factor

        Returns
        -------
        value : float
            Downsample value of calibration files
        """
    def getHFOV(self) -> float: 
        """
        Get horitonzal Field Of View of camera from Q matrix

        Returns
        -------
        fov_x : float
            Horitonzal Field Of View of camera from Q matrix
        """
    def getQ(self) -> numpy.ndarray: 
        """
        Get the Q matrix in numpy.ndarray

        Returns
        -------
        Q : numpy.ndarray
            Q matrix of calibration file
        """
    def isValid(self) -> bool: 
        """
        Check if the calibration file is valid

        Returns
        -------
        bool
            True if calibration file is valid
        """
    def isValidSize(self, arg0: int, arg1: int) -> bool: 
        """
        Check if the calibration file in valid size

        Returns
        -------
        bool
            True if calibration file is valid in size
        """
    def rectify(self, arg0: numpy.ndarray, arg1: numpy.ndarray) -> phase.pyphase.types.StereoImagePair: 
        """
        Rectify stereo image pair from calibration file

        Parameters
        ----------
        left_image : numpy.ndarray
            Stereo camera left image
        right_image : numpy.ndarray
            Stereo camera right image
        left_rect_image : numpy.ndarray
            numpy.ndarray to store left rectified image
        right_rect_image : numpy.ndarray
            numpy.ndarray to store right rectified image
        """
    def remapPoint(self, arg0: phase.pyphase.types.Point2i, arg1: phase.pyphase.types.LeftOrRight) -> phase.pyphase.types.Point2i: 
        """
        Remap point from calibration

        Parameters
        ----------
        point : phase.pyphase.types.Point2i
        camera_selection : enum

        Returns
        -------
        remapped_point : phase.pyphase.types.Point2i
        """
    def saveToYAML(self, arg0: str, arg1: str, arg2: CalibrationFileType) -> bool: 
        """
        Flip image horizontally or vertically based on flip code.

        Parameters
        ----------
        left_calibration_filepath : str
            Desired path directory to save calibration file
        right_calibration_filepath : str
            Desired path directory to save calibration file
        cal_file_type : enum
            Type of calibration file, e.g. ROS_YAML/OPENCV_YAML

        Returns
        -------
        bool
            True if calibration yaml files are saved
        """
    def setDownsampleFactor(self, arg0: float) -> None: 
        """
        Set downsample factor

        Parameters
        ----------
        value : float
            Desired value of downsample factor
        """
    @property
    def left_calibration(self) -> CameraCalibration:
        """
                    Store variables of Left calibration

                    

        :type: CameraCalibration
        """
    @left_calibration.setter
    def left_calibration(self, arg0: CameraCalibration) -> None:
        """
        Store variables of Left calibration
        """
    @property
    def right_calibration(self) -> CameraCalibration:
        """
                    Store variables of Left calibration

                    

        :type: CameraCalibration
        """
    @right_calibration.setter
    def right_calibration(self, arg0: CameraCalibration) -> None:
        """
        Store variables of Left calibration
        """
    pass
INVALID: phase.pyphase.calib.CalibrationFileType # value = <CalibrationFileType.INVALID: 2>
OPENCV_YAML: phase.pyphase.calib.CalibrationFileType # value = <CalibrationFileType.OPENCV_YAML: 1>
ROS_YAML: phase.pyphase.calib.CalibrationFileType # value = <CalibrationFileType.ROS_YAML: 0>
