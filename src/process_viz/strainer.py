from PIL import Image
import numpy as np
import os 

# import pyvips
import cairosvg

import gspread
from gspread_dataframe import get_as_dataframe, set_with_dataframe

import xml.etree.cElementTree as ET
import pandas as pd


#Pull the urls from the posts I scraped and inspected them to identify keywords that would indicate the presence of a viz
def inspect_data():
    data = []
    outlets = ['chart', 'charts', 'interactive', 'interatives', 'viz', 'visualization','visualizations', ' graph ', 'graphs']
    credentials = {
        # TODO: https://docs.gspread.org/en/latest/oauth2.html#for-end-users-using-oauth-client-id
    } 
    gc = gspread.service_account_from_dict(credentials)
    # for sheet in sheets:
    sh = gc.open("reddit_march")
    for wk in sh:
        wh_data = wk.get_all_records()
        for record in wh_data:
            if any(outlet in record['Post URL'] for outlet in outlets):
                data.append(record)
    push_to_svg_sheet(data)
    return data 


#This pushes the posts with evidence of a viz to their own sheet
def push_to_svg_sheet(df):
    data = pd.DataFrame(df)
    credentials = {
        # TODO: https://docs.gspread.org/en/latest/oauth2.html#for-end-users-using-oauth-client-id
    } 
    gc = gspread.service_account_from_dict(credentials)
    sh = gc.open("expanded")
    worksheet = sh.add_worksheet(title="december_expanded_data", rows="1700", cols="15")
    set_with_dataframe(worksheet, data)

inspect_data()