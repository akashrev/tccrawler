import glob
import numpy
from PIL import Image
import scipy.misc


image_name = 'download.gif'
infiles = glob.glob('image/' + image_name)
infile = "".join(infiles)

im = Image.open(infile)

avg = numpy.average(im, axis=0)
print(avg)
numavg = (numpy.average(avg, axis=0))
image_json = (numavg.tolist())
print(image_json)






rgb_im = im.convert('RGB')
r, g, b = rgb_im.getpixel((1, 1))
print(r,g,b)


imm = scipy.misc.imread(infile, flatten=False, mode='RGB')
print(imm.shape)
y,x,z = imm.shape

# color = tuple(imm[y][x])
# r, g, b = color
print(y,x)