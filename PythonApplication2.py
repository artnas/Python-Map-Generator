from PIL import Image
from noise import snoise2;
import math;
import numpy as np;
from tqdm import tqdm
import random;

perlinIterations = 1;

perlinOffset = random.random()*2048;

size = 2048;
scale = 0.0025;

landThreshold = 0.1;

im = Image.new("RGB", (size,size));

heightMap = [[0]*size for x in range(size)]
colorMap = [[Color() for j in range(size)] for i in range(size)]

class Color:

    # 0 -> 255

    r = 0.0;
    g = 0.0;
    b = 0.0;
    a = 1.0;

    def __init__(self, r = 0.0, g = 0.0, b = 0.0):
        self.r = r;
        self.g = g;
        self.b = b;
        self.a = 1;
    def GetTuple(self):
        return (int(self.r),int(self.g),int(self.b));
    def SetColor(self, r, g, b):
        self.r = r;
        self.g = g;
        self.b = b;
    def Copy(self, color):
        self.r = color.r;
        self.g = color.g;
        self.b = color.b;
    def SetWhite(self):
        self.SetColor(1,1,1);
    def SetBlack(self):
        self.SetColor(0,0,0);
    def SetColorFromGrayscale(self, f = 0.0):
        self.SetColor(f,f,f);

paperColor = Color();
paperColor.SetColor(212, 161, 104);

def Distance(ax = 0.0, ay = 0.0, bx = 0.0, by = 0.0):
    x = ax - bx;
    x *= x;
    y = ay - by;
    y*= y;
    return (math.sqrt(x + y));

def GetPerlinValue( x, y ):
   #noiseValue = (snoise2(float(x)*scale, float(y)*scale, octaves=2, persistence=0.25, lacunarity=2.0, repeatx=1024, repeaty=1024, base=0.0) + 1)/2.0;
   noiseValue = (snoise2(float(x)*scale, float(y)*scale, octaves=8, persistence=0.5, lacunarity=2.0, repeatx=2048, repeaty=2048, base=perlinOffset) + 1)/2.0;
   return noiseValue;

##
print("Beginning generation...");

def DistanceNormalized(ax = 0.0, ay = 0.0, bx = 0.0, by = 0.0):
    dist = Distance(ax, ay, bx, by);
    dist /= size;
    return dist;

##
print("Generating...");

def CreateIsland():
    middlePoint = (size/2, size/2);

    print("creating main heightmap");

    pbar = tqdm(total=size*size)

    for x in range(0, size):
        for y in range(0, size):

            perlinValue = 1.0;
            for a in range(1, perlinIterations+1):
                perlinValue *= GetPerlinValue(x/a,y/a);

            ## island

            distance = DistanceNormalized(x,y, middlePoint[0], middlePoint[1]);

            perlinValue -= math.pow(distance, 0.5);
            if (perlinValue <= 0):
                perlinValue = 0;

            #

            heightMap[x][y] = perlinValue;

            pbar.update(1);

    pbar.close();
def ColorImage():
    randomColorRange = 10;

    print("coloring map");

    pbar = tqdm(total=size*size)

    colorPerlinScale = 0.025;

    for x in range(0, size):
        for y in range(0, size):
            if (heightMap[x][y] > landThreshold):

                heightPerlinValue = noiseValue = (snoise2(float(x)*scale, float(y)*scale, octaves=12, persistence=0.8, lacunarity=2.0, repeatx=2048, repeaty=2048, base=perlinOffset) + 1)/2.0;

                normalizedHeight = (heightPerlinValue - landThreshold);
                normalizedHeight*=normalizedHeight*normalizedHeight;

                noiseValue = (snoise2(float(x)*colorPerlinScale, float(y)*colorPerlinScale, octaves=2, persistence=0.5, lacunarity=2.0, repeatx=2048, repeaty=2048, base=perlinOffset) + 1)/2.0;
                randomColorOffset = (random.random()-0.5)*8 + 24.0*noiseValue + normalizedHeight*256.0;

                r = paperColor.r + randomColorOffset;
                g = paperColor.g + randomColorOffset;
                b = paperColor.b + randomColorOffset;
                colorMap[x][y].SetColor(r,g,b);

            else:

                colorMap[x][y].SetColorFromGrayscale((heightMap[x][y]*heightMap[x][y])/landThreshold/2 * 255);

            pbar.update(1);

    pbar.close();

CreateIsland();
ColorImage();

def ApplyColorMapToImage():
    #numpyArray2D = np.array(colorMap);
    #arr = np.array({1,2,3});
    #im = Image.fromarray(arr); 
    for x in range(0, size):
        for y in range(0, size):

            im.putpixel((x,y), colorMap[x][y].GetTuple());

##
print("Generation completed");

##
print("Writing to image");

ApplyColorMapToImage();
im.save("Generated.png");

##
print("Job's done");

im.show();
