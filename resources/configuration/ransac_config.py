# RANSAC CONFIGURATION CLASS
class RANSACConfiguration:
    def __init__(self, use_ransac=False, reprojection_error_threshold=5.0):
        self.__use_ransac = use_ransac
        self.__reprojection_error_threshold = reprojection_error_threshold

    def get_use_ransac(self):
        return self.__use_ransac

    def set_use_ransac(self, use_ransac):
        self.__use_ransac = use_ransac

    def get_reprojection_error_threshold(self):
        return self.__reprojection_error_threshold

    def set_reprojection_error_threshold(self, reprojection_error_threshold):
        self.__reprojection_error_threshold = reprojection_error_threshold
