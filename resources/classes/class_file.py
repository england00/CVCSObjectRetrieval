# FILE CLASS
class File:
    def __init__(self, path=None, name=None, image=None, keypoints=None, descriptor=None, matches=None, distances=None, resolution_value=None):
        self.__path = path
        self.__name = name
        self.__image = image
        self.__keypoints = keypoints
        self.__descriptor = descriptor
        self.__matches = matches
        self.__distances = distances
        self.__resolution_value = resolution_value

        if self.__name is None:
            self.__name = str(path).split('/')[len(str(path).split('/')) - 1]

    def get_path(self):
        return self.__path

    def set_path(self, path):
        self.__path = path

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__path = name

    def get_image(self):
        return self.__image

    def set_image(self, image):
        self.__image = image

    def get_keypoints(self):
        return self.__keypoints

    def set_keypoints(self, keypoints):
        self.__keypoints = keypoints

    def get_descriptors(self):
        return self.__descriptor

    def set_descriptors(self, descriptors):
        self.__descriptor = descriptors

    def get_matches(self):
        return self.__matches

    def set_matches(self, matches):
        self.__matches = matches

    def get_distances(self):
        return self.__distances

    def set_distances(self, distances):
        self.__distances = distances

    def get_resolution_value(self):
        return self.__resolution_value

    def set_resolution_value(self, resolution_value):
        self.__resolution_value = resolution_value

    def get_average_distance(self):
        return sum(self.__distances) / len(self.__distances)
