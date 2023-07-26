import cv2


# FILELIST CLASS
class FilesList:
    def __init__(self, folder=None, query_path="", writing_path=""):
        self.__folder = folder
        self.__query_path = query_path
        self.__writing_path = writing_path
        self.__files = []
        self.__output = []

    def get_folder(self):
        return self.__folder

    def set_folder(self, folder):
        self.__folder = folder

    def get_query_path(self):
        return self.__query_path

    def set_query_path(self, query_path):
        self.__query_path = query_path

    def get_writing_path(self):
        return self.__writing_path

    def set_writing_path(self, writing_path):
        self.__writing_path = writing_path

    def get_files(self):
        return self.__files

    def set_files(self, files):
        self.__files = files

    def sort_by_matches_number(self, n):
        self.__output.append(
            sorted(self.__files, key=lambda x: len(x.get_distances()), reverse=True))  # decreasing order
        self.__output[len(self.__output) - 1] = self.__output[len(self.__output) - 1][
                                                0:n]  # maintaining only first n elements

    def sort_by_average_distance(self, n):
        self.__output.append(sorted(self.__files, key=lambda x: x.get_average_distance()))  # increasing order
        self.__output[len(self.__output) - 1] = self.__output[len(self.__output) - 1][
                                                0:n]  # maintaining only first n elements

    def sort_by_average_distance_inside_matches_classes(self, n):
        self.sort_by_matches_number(len(self.__files))

        output_dict = {}
        for file in self.__output[len(self.__output) - 1]:
            if len(file.get_distances()) not in output_dict:  # grouping elements by number of matches
                output_dict[len(file.get_distances())] = []
            output_dict[len(file.get_distances())].append(file)

        for key in output_dict:
            output_dict[key].sort(
                key=lambda x: x.get_average_distance())  # sorting elements within each group by average distance

        self.__output[len(self.__output) - 1] = [item for sublist in output_dict.values() for item in sublist]
        self.__output[len(self.__output) - 1] = self.__output[len(self.__output) - 1][
                                                0:n]  # maintaining only first n elements

    def printer(self, counter=0, drawing=True, destroy_drawings_on_iteration=True, writing=False):
        title = "{}".format((str(self.__query_path).split('/')[3] + "/" + str(str(self.__query_path)).split('/')[4]))
        control = False
        matches_number = 0
        average_distance = 0
        for __list in self.__output:
            for file in __list:
                counter += 1
                print(f" ---> Image {counter}: {file.get_name()}, "
                      f"matched keypoint: {len(file.get_distances())},  "
                      f"distance: {file.get_average_distance()}")

                if not control:
                    control = True
                    matches_number = len(file.get_distances())
                    average_distance = file.get_average_distance()

                if drawing:
                    cv2.imshow("{} - {}".format(title, counter), file.get_matches())
                if writing:
                    cv2.imwrite("{}/{}.jpg".format(self.__writing_path, str(counter)), file.get_matches())
        self.__output = []

        if destroy_drawings_on_iteration:
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            cv2.waitKey(1000)

        return counter, matches_number, average_distance
