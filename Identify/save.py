import cairosvg
import os 

def traverse():
    directory = "../data/svgs"
    entries = os.listdir(directory)
    for entry in entries:
        if entry.endswith(".svg"):
            (os.chdir(r"/Users/emmabaker/Documents/GitHub/Thesis/data/svgs/"))
            directory = str(os.getcwd())
            path = directory + "/"+ entry
            newFileName = entry.replace(".svg", ".png")
            newPath = r"/Users/emmabaker/Documents/GitHub/Thesis/data/new/" + newFileName
            print(newPath)
            cairosvg.svg2png(url=path, write_to=newPath)
        else:
            continue

traverse()
