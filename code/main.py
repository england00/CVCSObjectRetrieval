import cv2
import time
from resources.configuration.threads_configuration import ThreadsConfiguration
from resources.configuration.sift_config import SIFTConfiguration
from resources.configuration.flann_config import FLANNConfiguration
from resources.configuration.ransac_config import RANSACConfiguration
from resources.classes.class_file import File
from resources.classes.class_files_list import FilesList
from resources.functions.functions import resize, search_image

# THREAD PARAMS
threads_configuration = ThreadsConfiguration(max_threads_number=12)

# SIFT PARAMS
query_features_extraction = SIFTConfiguration(features_number=20, contrast_threshold=0.02, edge_threshold=10, sigma=1.6, octave_layers=7)
repo_features_extraction = SIFTConfiguration(features_number=0, contrast_threshold=0.005, edge_threshold=100, sigma=1.6, octave_layers=7)

# FLANN PARAMS
flann_confing = FLANNConfiguration(algorithm_type=1, trees_number=11, checks_number=50, lowe_ratio=0.65)

# RANSAC
ransac_configuration = RANSACConfiguration(use_ransac=True, reprojection_error_threshold=5.0)

# IMAGES PARAMS
query = File(path="../files/_queries/object_1/3.png", resolution_value=(640, 480))  # query definition with path and resolution limit
file_list = FilesList(folder="../files/_repository", query_path=query.get_path(), writing_path="../files/_results")  # folder name
BEST_RESULTS_NUMBER = 3
ENABLE_DRAWING = True
ENABLE_WRITING = False

# MAIN
if __name__ == "__main__":
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
    search_image(threads_configuration, query, file_list, repo_features_extraction, flann_confing, ransac_configuration)

    # first result by smaller average distance inside the higher number of matches
    file_list.sort_by_average_distance_inside_matches_classes(BEST_RESULTS_NUMBER)  # solution metric

    # timer end
    print(" ---> END: the method took %.3f sec." % (time.time() - start))

    # printing results
    print("RESULTS:")
    file_list.printer(drawing=ENABLE_DRAWING, writing=ENABLE_WRITING)
