from PIL import Image, ImageChops
import sys, os

def tint_image(vargs=None):
    if vargs is None:
        vargs=sys.argv
    file, ext = os.path.splitext(vargs[1])
    image = Image.open("%s" % vargs[1])
    newImage =  ImageChops.multiply(image, Image.new('RGB', image.size, vargs[2]))
    newImage.save(file+"n","JPEG")
    
if __name__ == "__main__":
    tint_image()