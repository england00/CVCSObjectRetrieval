import sys
import cv2
import time
import os
import numpy as np
from resources.configuration.threads_configuration import ThreadsConfiguration
from resources.configuration.sift_config import SIFTConfiguration
from resources.configuration.flann_config import FLANNConfiguration
from resources.configuration.ransac_config import RANSACConfiguration
from resources.utility.metrics_printer import MetricsPrinter
from resources.classes.class_file import File
from resources.classes.class_files_list import FilesList
from resources.functions.functions import resize, search_image

# THREAD PARAMS
threads_configuration = ThreadsConfiguration(max_threads_number=12)

# SIFT PARAMS
query_features_extraction = SIFTConfiguration(features_number=20, contrast_threshold=0.02, edge_threshold=10, sigma=1.6, octave_layers=7)
repo_features_extraction = SIFTConfiguration(features_number=0, contrast_threshold=0.005, edge_threshold=100, sigma=1.6, octave_layers=7)

# FLANN PARAMS
flann_config = FLANNConfiguration(algorithm_type=1, trees_number=11, checks_number=50, lowe_ratio=0.7)

# RANSAC
ransac_configuration = RANSACConfiguration(use_ransac=True, reprojection_error_threshold=5.0)

# IMAGES PARAMS
query = File(path="../files/_queries/object_1/1.png", resolution_value=(640, 480))  # query definition with path and resolution limit
queries_list = FilesList(folder="../files/_queries")  # folder name
file_list = FilesList(folder="../files/_repository", query_path=query.get_path(), writing_path="../files/_results")  # folder name
BEST_RESULTS_NUMBER = 1
ENABLE_DRAWING = False
ENABLE_WRITING = True

# METRICS
reference_counter = 0
times = []
best_matched_keypoints = []
best_average_distances = []


# MAIN
if __name__ == "__main__":
    # copying stdout to 'metric.txt' file
    sys.stdout = MetricsPrinter(file_list.get_writing_path())

    # scrolling queries
    for directory in os.listdir(queries_list.get_folder()):
        for filename in os.listdir(str(queries_list.get_folder()) + "/" + str(directory)):
            # setting current query
            print("FILE: " + str(queries_list.get_folder()) + "/" + str(directory) + "/" + str(filename))
            query.set_path(str(queries_list.get_folder()) + "/" + str(directory) + "/" + str(filename))
            file_list.set_query_path(query.get_path())

            # timer init
            print("TIMES:")
            if ransac_configuration.get_use_ransac():
                print(" ---> START: Finding similar objects with SIFT, FLANN matcher and RANSAC.")
            else:
                print(" ---> START: Finding similar objects with SIFT and FLANN matcher.")
            start = time.time()

            # loading query image as GRAYSCALE
            query.set_image(cv2.imread(query.get_path(), cv2.IMREAD_GRAYSCALE))
            if (query.get_image().shape[0] != query.get_resolution_value()[0]) or (
                    query.get_image().shape[1] != query.get_resolution_value()[1]):
                query.set_image(
                    resize(cv2.imread(query.get_path(), cv2.IMREAD_GRAYSCALE), query.get_resolution_value()[0], query.get_resolution_value()[1]))

            # managing query's features extraction with SIFT
            sift = cv2.SIFT_create(nfeatures=query_features_extraction.get_features_number(),
                                   contrastThreshold=query_features_extraction.get_contrast_threshold(),
                                   edgeThreshold=query_features_extraction.get_edge_threshold(),
                                   sigma=query_features_extraction.get_sigma(),
                                   nOctaveLayers=query_features_extraction.get_octave_layers())
            kp, des = sift.detectAndCompute(query.get_image(), None)  # computing keypoint and descriptors in once
            query.set_keypoints(kp)
            query.set_descriptors(des)

            # images comparison from given folder
            search_image(threads_configuration, query, file_list, repo_features_extraction, flann_config, ransac_configuration)

            # first result by smaller average distance inside the higher number of matches
            file_list.sort_by_average_distance_inside_matches_classes(BEST_RESULTS_NUMBER)  # solution metric

            # timer end
            end = time.time() - start
            print(" ---> END: the method took %.3f sec." % end)
            times.append(end)

            # printing results
            print("RESULTS:")
            reference_counter, matches_number, average_distance = file_list.printer(counter=reference_counter,
                                                                                    drawing=ENABLE_DRAWING,
                                                                                    destroy_drawings_on_iteration=False,
                                                                                    writing=ENABLE_WRITING)
            best_matched_keypoints.append(matches_number)
            best_average_distances.append(average_distance)

            # emptying file list
            file_list.set_files([])

            # printing current metrics
            print('CURRENT METRICS:')
            print(" ---> TIMES:\n ---> Average: ", np.mean(times).round(3), ", Variance: ", np.var(times).round(3),
                  ", Standard Deviation: ", np.std(times).round(3), ", Max value: ", np.max(times).round(3),
                  ", Min value: ", np.min(times).round(3))
            print(" ---> MATCHED KEYPOINT:\n ---> Average: ", np.mean(best_matched_keypoints).round(3), ", Variance: ",
                  np.var(best_matched_keypoints).round(3), ", Standard Deviation: ",
                  np.std(best_matched_keypoints).round(3), ", Max value: ", np.max(best_matched_keypoints).round(3),
                  ", Min value: ", np.min(best_matched_keypoints).round(3))
            print(" ---> AVERAGE DISTANCES:\n ---> Average: ", np.mean(best_average_distances).round(3), ", Variance: ",
                  np.var(best_average_distances).round(3), ", Standard Deviation: ",
                  np.std(best_average_distances).round(3), ", Max value: ", np.max(best_average_distances).round(3),
                  ", Min value: ", np.min(best_average_distances).round(3))
            print('\n')

    # final metrics
    print('FINAL METRICS:')
    print(" ---> TIMES:\n ---> Average: ", np.mean(times).round(3), ", Variance: ", np.var(times).round(3),
          ", Standard Deviation: ", np.std(times).round(3), ", Max value: ", np.max(times).round(3),
          ", Min value: ", np.min(times).round(3))
    print(" ---> MATCHED KEYPOINT:\n ---> Average: ", np.mean(best_matched_keypoints).round(3), ", Variance: ",
          np.var(best_matched_keypoints).round(3), ", Standard Deviation: ", np.std(best_matched_keypoints).round(3),
          ", Max value: ", np.max(best_matched_keypoints).round(3), ", Min value: ",
          np.min(best_matched_keypoints).round(3))
    print(" ---> AVERAGE DISTANCES:\n ---> Average: ", np.mean(best_average_distances).round(3), ", Variance: ",
          np.var(best_average_distances).round(3), ", Standard Deviation: ", np.std(best_average_distances).round(3),
          ", Max value: ", np.max(best_average_distances).round(3), ", Min value: ",
          np.min(best_average_distances).round(3))

    # destroy all drawings
    cv2.waitKey(0)
    cv2.destroyAllWindows()
