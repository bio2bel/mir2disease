# -*- coding: utf-8 -*-

import os

from bio2bel.utils import get_connection, get_data_dir

MODULE_NAME = "mir2disease"
DATA_DIR = get_data_dir(MODULE_NAME)
DEFAULT_CACHE_CONNECTION = get_connection(MODULE_NAME)
DATA_URL = "http://watson.compbio.iupui.edu:8080/miR2Disease/download/AllEntries.txt"
DATA_FILE_PATH = os.path.join(DATA_DIR, "mir2diseaseRawData.tsv")
col_names = ["miRNA ID", "MeSHDisease term", "Relationship", "Detection Method", "Year", "Description"]