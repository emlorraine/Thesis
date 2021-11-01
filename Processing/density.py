from skimage.measure.entropy import shannon_entropy
from skimage import io

def entropy():

    simple_img = io.imread("simple_tree.png") 
    print(shannon_entropy(simple_img[:,:,0]))

    complex_img = io.imread("tree.png") 
    print(shannon_entropy(complex_img[:,:,0]))




