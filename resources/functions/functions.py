import cv2
import os
import threading
import numpy as np
from resources.classes.class_file import File


# RESIZE FUNCTION
def resize(img, down_width, down_height):
    return cv2.resize(img, (down_width, down_height), interpolation=cv2.INTER_LINEAR)


# SEARCH FUNCTION
def search_image(threads_configuration, query, file_list, repo_features_extraction, flann_config, ransac_configuration):
    # managing SIFT
    sift = cv2.SIFT_create(nfeatures=repo_features_extraction.get_features_number(),
                           contrastThreshold=repo_features_extraction.get_contrast_threshold(),
                           edgeThreshold=repo_features_extraction.get_edge_threshold(),
                           sigma=repo_features_extraction.get_sigma(),
                           nOctaveLayers=repo_features_extraction.get_octave_layers())

    # managing FLANN matcher object
    flann = cv2.FlannBasedMatcher(flann_config.get_index_params(), flann_config.get_search_params())

    for filename in os.listdir(file_list.get_folder()):
        while threading.active_count() >= threads_configuration.get_max_threads_number():  # waiting an ending thread if the maximum number of threads available has been reached
            pass
        t = threading.Thread(target=process_image,
                             args=(query, filename, file_list, sift, flann, flann_config,
                                   ransac_configuration))  # starting a new thread
        t.start()
        threads_configuration.get_threads_list().append(t)

    for t in threads_configuration.get_threads_list():  # waiting the end of each thread
        t.join()


# PROCESS FUNCTION
def process_image(query, filename, file_list, sift, flann, flann_config, ransac_configuration):
    # loading image as GRAYSCALE
    img = cv2.imread(os.path.join(file_list.get_folder(), filename), cv2.IMREAD_GRAYSCALE)
    if (img.shape[0] != query.get_resolution_value()[0]) or (img.shape[1] != query.get_resolution_value()[1]):
        img = resize(cv2.imread(os.path.join(file_list.get_folder(), filename), cv2.IMREAD_GRAYSCALE),
                     query.get_resolution_value()[0], query.get_resolution_value()[1])

    # managing image's features extraction with SIFT
    kp, des = sift.detectAndCompute(img, None)  # computing keypoint and descriptors in once

    # managing FLANN matcher object
    if des is not None and len(des) > 1:  # searching matches only if there are keypoints inside the image
        matches = flann.knnMatch(query.get_descriptors(), des, k=2)
        good_matches = []
        for m, n in matches:
            if m.distance < flann_config.get_lowe_ratio() * n.distance:  # ratio test to filter out ambiguous matches
                good_matches.append(m)

        # don't use RANSAC
        if not ransac_configuration.get_use_ransac():
            resultant_matches = cv2.drawMatches(query.get_image(), query.get_keypoints(), img, kp, good_matches, None,
                                                flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
            # saving results for each image
            distances = [m.distance for m in good_matches]
            if len(distances) != 0:
                file_list.get_files().append(File(path=file_list.get_folder(), name=filename, image=img, keypoints=kp,
                                                  descriptor=des, matches=resultant_matches, distances=distances))

        # use RANSAC
        else:
            # extracting keypoints from good matches
            query_kp = query.get_keypoints()
            query_points = np.float32([query_kp[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
            repo_image_points = np.float32([kp[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

            # executing homography with RANSAC
            if len(query_points) >= 4 and len(repo_image_points) >= 4:
                M, mask = cv2.findHomography(query_points, repo_image_points, cv2.RANSAC,
                                             ransac_configuration.get_reprojection_error_threshold())
                inliers = [m for i, m in enumerate(good_matches) if mask[i][0] == 1]
                resultant_matches = cv2.drawMatches(query.get_image(), query.get_keypoints(), img, kp, inliers, None,
                                                    flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

                # saving results for each image
                distances = [m.distance for m in inliers]
                if len(distances) != 0:
                    file_list.get_files().append(File(path=file_list.get_folder(),
                                                      name=filename,
                                                      image=img,
                                                      keypoints=kp,
                                                      descriptor=des,
                                                      matches=resultant_matches,
                                                      distances=distances))
