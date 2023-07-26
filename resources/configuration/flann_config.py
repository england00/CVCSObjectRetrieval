# FLANN CONFIGURATION CLASS
class FLANNConfiguration:
    def __init__(self, algorithm_type=1, trees_number=11, checks_number=50, lowe_ratio=0.7):
        if algorithm_type == 1:  # FLANN_INDEX_KDTREE
            self.__index_params = dict(algorithm=algorithm_type, trees=trees_number)
        self.__search_params = dict(checks=checks_number)
        self.__lowe_ratio = lowe_ratio

    def get_index_params(self):
        return self.__index_params

    def set_index_params(self, index_params):
        self.__index_params = index_params

    def get_search_params(self):
        return self.__search_params

    def set_search_params(self, search_params):
        self.__search_params = search_params

    def get_lowe_ratio(self):
        return self.__lowe_ratio

    def set_lowe_ratio(self, lowe_ratio):
        self.__lowe_ratio = lowe_ratio
