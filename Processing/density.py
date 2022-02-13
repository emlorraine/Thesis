# from skimage.measure.entropy import shannon_entropy
# from skimage import io

import gspread
from gspread_dataframe import get_as_dataframe, set_with_dataframe

import os 

# conduct search on entry id


path = 'output/'
files = os.listdir(path)
for file in files:
    if os.path.isfile(os.path.join(path, file)):
        f = open(os.path.join(path, file),'r')
        print(f)
        # entropy here

def entropy():

    simple_img = io.imread("simple_tree.png") 
    print(shannon_entropy(simple_img[:,:,0]))

    complex_img = io.imread("tree.png") 
    print(shannon_entropy(complex_img[:,:,0]))




