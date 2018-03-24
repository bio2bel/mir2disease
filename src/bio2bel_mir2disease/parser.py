# -*- coding: utf-8 -*-

import logging
import os
from urllib.request import urlretrieve

import pandas as pd

from .constants import DATA_FILE_PATH, DATA_URL, col_names

log = logging.getLogger(__name__)


def download_mir2disease(force_download=False):
    """Download the miR2Disease database as a TSV

    :param bool force_download: If true, forces the data to get downloaded again; defaults to False
    :return: The system file path of the downloaded file
    :rtype: str
    """
    if os.path.exists(DATA_FILE_PATH) and not force_download:
        log.info('using cached data at %s', DATA_FILE_PATH)
    else:
        log.info('downloading %s to %s', DATA_URL, DATA_FILE_PATH)
        urlretrieve(DATA_URL, DATA_FILE_PATH)

    return DATA_FILE_PATH


def get_mir2disease_df(url=None, cache=True, force_download=False):
    """Loads the miR2Disease into a data frame

    1) miRNA ID
    2) MeSHDisease term
    3) Relationship
    4) Detection method
    5) Year
    6) Description

    :param Optional[str] url: A custom path to use for data
    :param bool cache: If true, the data is downloaded to the file system, else it is loaded from the internet
    :param bool force_download: If true, overwrites a previously cached file
    :rtype: pandas.DataFrame
    """
    if url is None and cache:
        url = download_mir2disease(force_download=force_download)

    df = pd.read_csv(
        url or DATA_URL,
        sep='\t',
        names=col_names
    )

    return df
