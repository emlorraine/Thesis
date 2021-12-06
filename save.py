import cairosvg

def saveAsPng(path:str):
    fileName = path.replace(".svg", ".png")
    newPath = "./data/new/"+fileName
    svgConvertedToPng = cairosvg.svg2png(url=path, write_to=newPath)
