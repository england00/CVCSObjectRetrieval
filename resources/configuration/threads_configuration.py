# THREADS CONFIGURATION CLASS
class ThreadsConfiguration:
    def __init__(self, max_threads_number=12):
        self.__threads_list = []
        self.__max_threads_number = max_threads_number

    def get_threads_list(self):
        return self.__threads_list

    def get_max_threads_number(self):
        return self.__max_threads_number

    def set_max_threads_number(self, max_threads_number):
        self.__max_threads_number = max_threads_number
