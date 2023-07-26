# SIFT CONFIGURATION CLASS
class SIFTConfiguration:
    def __init__(self, features_number=0, contrast_threshold=0.005, edge_threshold=100, sigma=1.6, octave_layers=5):
        self.__features_number = features_number
        self.__contrast_threshold = contrast_threshold
        self.__edge_threshold = edge_threshold
        self.__sigma = sigma
        self.__octave_layers = octave_layers

    def get_features_number(self):
        return self.__features_number

    def set_features_number(self, features_number):
        self.__features_number = features_number

    def get_contrast_threshold(self):
        return self.__contrast_threshold

    def set_contrast_threshold(self, contrast_threshold):
        self.__contrast_threshold = contrast_threshold

    def get_edge_threshold(self):
        return self.__edge_threshold

    def set_edge_threshold(self, edge_threshold):
        self.__edge_threshold = edge_threshold

    def get_sigma(self):
        return self.__sigma

    def set_sigma(self, sigma):
        self.__sigma = sigma

    def get_octave_layers(self):
        return self.__octave_layers

    def set_octave_layers(self, octave_layers):
        self.__octave_layers = octave_layers
