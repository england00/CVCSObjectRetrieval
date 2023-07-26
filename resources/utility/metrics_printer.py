import sys


# METRICS PRINTER CONFIGURATION CLASS
class MetricsPrinter(object):
    def __init__(self, file_path):
        self.__terminal = sys.stdout
        self.__file = open(str(file_path + "/metrics.txt"), 'w')

    def write(self, message):
        self.__terminal.write(message)
        self.__file.write(message)

    def flush(self):
        pass
