import matplotlib.pyplot as plt
import numpy as np

from skimage import data
from skimage.util import img_as_ubyte
from skimage.filters.rank import entropy
from skimage.morphology import disk

from skimage.measure.entropy import shannon_entropy
from skimage import io


import gspread
from gspread_dataframe import set_with_dataframe

from PIL import Image

import os 
import pandas as pd

from access import pull_reddit_data

posts_dict = {"Date": [], "Page": [], "Title": [], "Post Text": [], "ID": [], "Total Comments": [], "Likes": [],  "Post URL": [], "Entropy_Grayscale":[]}

data = pull_reddit_data()

def find_index(supplied_index):
    for row in data[0]:
        if(supplied_index == (row['ID'])):
            print("Successfully found:",supplied_index)
            return row

def calc_entropy(filepath):
    try:
        img = io.imread(filepath.name)
        return (shannon_entropy(img[:,:,0]))
    except:
        print("An exception occurred")

def push_to_svg_sheet(df):
    data = pd.DataFrame(df)
    credentials = {
        # TODO: https://docs.gspread.org/en/latest/oauth2.html#for-end-users-using-oauth-client-id
    } 
    gc = gspread.service_account_from_dict(credentials)
    sh = gc.open("filtered_data")
    worksheet = sh.add_worksheet(title="greyscale_analyzed_reddit_manual_screenshots", rows="500", cols="15")
    set_with_dataframe(worksheet, data)


final_data = []
path = 'greyscale/output_manual_focus/'
files = os.listdir(path)
for file in files:
    if os.path.isfile(os.path.join(path, file)):
        f = open(os.path.join(path, file),'r')
        index = str(file[0:6])
        ent = calc_entropy(f)
        df = find_index(index)
        if(df and ent):
            df['Entropy']=ent
            final_data.append(df)

push_to_svg_sheet(final_data)
