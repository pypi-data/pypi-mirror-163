from urllib.request import urlretrieve
from urllib.error import HTTPError
import warnings
import pandas as pd
import pyreadr
from pyreadr import read_r


def _download_and_import_RData_file(url):
    filename, headers = urlretrieve(url)

    # Load the RData file into R and get the name of the new variable created
    r_obj_name = pyreadr.read_r(filename)

    data = r_obj_name[list(r_obj_name)[0]]# let's check what objects we got

    # create the dataframe
    df = pd.DataFrame(data)

    return df


def importAURN(site, years):
    site = site.upper()

    # If a single year is passed then convert to a list with a single value
    if type(years) is int:
        years = [years]

    downloaded_data = []
    errors_raised = False

    for year in years:
        # Generate correct URL and download to a temporary file
        url = f"https://uk-air.defra.gov.uk/openair/R_data/{site}_{year}.RData"

        try:
            df = _download_and_import_RData_file(url)
        except HTTPError:
            errors_raised = True
            continue

        df = df.set_index('date')

        downloaded_data.append(df)

    if len(downloaded_data) == 0:
        final_dataframe = pd.DataFrame()
    else:
        final_dataframe = pd.concat(downloaded_data)

    if errors_raised:
        warnings.warn('Some data files were not able to be downloaded, check resulting DataFrame carefully')
    if len(final_dataframe) == 0:
        warnings.warn('Resulting DataFrame is empty')

    return final_dataframe


def importMetadata():
    df = _download_and_import_RData_file("http://uk-air.defra.gov.uk/openair/R_data/AURN_metadata.RData")

    df = df.drop_duplicates(subset=['site_id'])
    
    return df