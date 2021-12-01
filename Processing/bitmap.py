from PIL import Image
import numpy as np
import os 
import pyvips


def save_as_png():
    image = pyvips.Image.new_from_file("11-27-21_cnn.com-interactive-2019-business-us-minimum-wage-by-year-index.html.svg", dpi=300)
    image.write_to_file("img.png")

    

def find_data():
    if not os.listdir('../data/new'):
        print("Directory is empty")
        cairosvg.svg2png(url="../data/new/11-27-21_cnn.com-interactive-2019-business-us-minimum-wage-by-year-index.html.svg", write_to="../data/pngs/output.png")
        # convertToBitMap("../data/new/11-27-21_cnn.com-interactive-2019-business-us-minimum-wage-by-year-index.html")
    else:    
        print("Directory is not empty")


def convertToBitMap(fileName):
    img = Image.open(fileName)
    ary = np.array(img)
    # Split the three channels
    r,g,b = np.split(ary,3,axis=2)
    r=r.reshape(-1)
    g=r.reshape(-1)
    b=r.reshape(-1)
    # Standard RGB to grayscale 
    bitmap = list(map(lambda x: 0.299*x[0]+0.587*x[1]+0.114*x[2], 
    zip(r,g,b)))
    bitmap = np.array(bitmap).reshape([ary.shape[0], ary.shape[1]])
    bitmap = np.dot((bitmap > 128).astype(float),255)
    im = Image.fromarray(bitmap.astype(np.uint8))
    bitMapImageName = fileName[0:(len(fileName)-4)] + "BitMap.bmp"
    im.save("output/"+bitMapImageName)

save_as_png()
