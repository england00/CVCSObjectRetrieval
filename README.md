# CVCSObjectRetrieval
CV & CS Object Retrieval project pipelines:
- baseline: SIFT + K-D Tree
- variation with further selection: SIFT + K-D Tree + RANSAC


## Index
- [Object Retrieval Project](#CV_CS_Object_Retrieval)
    - [Code](#code)
        - [Main program](#main.py) 
	    - [Metrics program](#metrics.py)
    - [Files](#files)
        - [Queries](#_queries)
            - [Each type of query object in one directory](#object_*)
	    - [Repository](#_repository)
	    - [Results](#_results)
    - [Resources](#resources)
        - [Classes](#classes)
        - [Configuration](#configuration)
        - [Functions](#functions)
        - [Utility](#utility)


# Usage baseline: SIFT + K-D Tree
- add a query image inside "files/_queries/object_*";
- add repository images inside "files/_repository";
- open main.py program;
- go to "# SIFT PARAMS" and set "features_number=10" inside the definition of the SIFTConfiguration object;
- go to "# RANSAC" and set "use_ransac=False" inside the definition of the RANSACConfiguration object;
- go to "# IMAGE PARAMS" and set "path="../files/_queries/object_*"' inside the definition of the File object;
- run the program and see first three best matches.
NOTE: it's possible collecting results images inside "../files/_results" directory setting "ENABLE_WRITING = True" in # SIFT PARAMS


# Usage variation with further selection: SIFT + K-D Tree + RANSAC
- add a query image inside "files/_queries/object_*";
- add repository images inside "files/_repository";
- open main.py program;
- go to "# SIFT PARAMS" and set "features_number=20" inside the definition of the SIFTConfiguration object;
- go to "# RANSAC" and set "use_ransac=True" inside the definition of the RANSACConfiguration object;
- go to "# IMAGE PARAMS" and set "path="../files/_queries/object_*"' inside the definition of the File object;
- run the program and see first three best matches.
NOTE: it's possible collecting results images inside "../files/_results" directory setting "ENABLE_WRITING = True" in # SIFT PARAMS


# Usage Metrics for baseline: SIFT + K-D Tree
- add some query images inside "files/_queries", with one type of object inside each directory "/object_*";
- add repository images inside "files/_repository";
- open metrics.py program;
- go to "# SIFT PARAMS" and set "features_number=10" inside the definition of the SIFTConfiguration object
- go to "# RANSAC" and set "use_ransac=False" inside the definition of the RANSACConfiguration object
- go to "# IMAGE PARAMS" and set "path="../files/_queries/object_*"' inside the definition of the File object
- run the program and collect results inside "../files/_results" directory, with metrics collected inside "metrics.txt" file inside the directory.


# Usage Metrics variation with further selection: SIFT + K-D Tree + RANSAC
- add some query images inside "files/_queries", with one type of object inside each directory "/object_*";
- add repository images inside "files/_repository";
- open metrics.py program;
- go to "# SIFT PARAMS" and set "features_number=20" inside the definition of the SIFTConfiguration object
- go to "# RANSAC" and set "use_ransac=True" inside the definition of the RANSACConfiguration object
- go to "# IMAGE PARAMS" and set "path="../files/_queries/object_*"' inside the definition of the File object
- run the program and collect results inside "../files/_results" directory, with metrics collected inside "metrics.txt" file inside the directory.