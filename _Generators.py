from noise import snoise2;
import math
from tqdm import tqdm
import random

from Classes import *
from VectorMath import *
from Map import *

class MapGen_Base:

    def __init__(self):    # Constructor of the class
        self.progress = 0;
        self.totalProgress = mapSize * mapSize;
        self.isFinished = False;
        self.pbar = tqdm(total = mapSize * mapSize);
        self.pbar.clear();
        self.smartGenerationEnabled = False;
        self.x = 0;
        self.y = 0;

    def GeneratePixel(self, x, y): # generate one pixel
        self.x += 1;
        if (self.x >= mapSize):
            self.x = 0;
            self.y += 1;
            if (self.y >= mapSize):
                self.isFinished = True;
                self.pbar.close();
        print(x + " " + y);

    def GenerateSmart(self): # will be used for multiprocessing
        self.smartGenerationEnabled = True;
        self.GeneratePixel(self.x,self.y);

    def GenerateFull(self): # fully generate
        for x in range(0, mapSize):
            for y in range(0, mapSize):
                self.Generate(x,y);

class MapGen_Main(MapGen_Base): # get base perlin height, make terrain and water

    def Generate(self, x, y): 

        if (self.smartGenerationEnabled):
            self.x += 1;
            if (self.x >= mapSize):
                self.x = 0;
                self.y += 1;
                if (self.y >= mapSize):
                    self.isFinished = True;
                    self.pbar.close();
        
        basePerlinValue = (snoise2(float(x)*perlinScale, float(y)*perlinScale, octaves=8, persistence=0.5, lacunarity=2.0, repeatx=2048, repeaty=2048, base=perlinOffset) + 1)/2.0;

        ## pixel height

        distance = DistanceNormalized(x,y, mapCenter[0], mapCenter[1], mapSize);

        basePerlinValue -= math.pow(distance, 0.5);
        if (basePerlinValue <= 0):
            basePerlinValue = 0;

        heightMap[x][y] = basePerlinValue;

        ## pixel color

        if (heightMap[x][y] > landThreshold): # land

            detailPerlinValue = (snoise2(float(x)*perlinScale, float(y)*perlinScale, octaves=12, persistence=0.8, lacunarity=2.0, repeatx=2048, repeaty=2048, base=perlinOffset) + 1)/2.0;

            normalizedHeight = (detailPerlinValue - landThreshold);
            normalizedHeight *= normalizedHeight*normalizedHeight; # normalized height ^3

            noiseValue = (snoise2(float(x)*colorPerlinScale, float(y)*colorPerlinScale, octaves=2, persistence=0.5, lacunarity=2.0, repeatx=2048, repeaty=2048, base=perlinOffset) + 1)/2.0;
            randomColorOffset = (random.random()-0.5)*8 + 24.0*noiseValue + normalizedHeight*256.0;

            r = paperColor.r + randomColorOffset;
            g = paperColor.g + randomColorOffset;
            b = paperColor.b + randomColorOffset;
            colorMap[x][y].SetColor(r,g,b);

        else: # water

            #detailPerlinValue = (snoise2(float(x)*perlinScale, float(y)*perlinScale, octaves=12, persistence=0.8, lacunarity=2.0, repeatx=2048, repeaty=2048, base=perlinOffset) + 1)/2.0;

            #normalizedHeight = (detailPerlinValue - landThreshold);
            #normalizedHeight *= normalizedHeight*normalizedHeight; # normalized height ^3

            normalizedHeight = (heightMap[x][y]);
            #normalizedHeight *= normalizedHeight;

            if (normalizedHeight < 0):
                normalizedHeight = 0;

            waterNoisePerlinScale = 0.01;

            noiseValue = (snoise2(float(x)*waterNoisePerlinScale, float(y)*waterNoisePerlinScale, octaves=2, persistence=0.5, lacunarity=2.0, repeatx=2048, repeaty=2048, base=perlinOffset) + 1)/2.0;
            randomColorOffset = (random.random()-0.5)*4 + 12.0*noiseValue + normalizedHeight*96.0;

            r = waterColor.r + randomColorOffset;
            g = waterColor.g + randomColorOffset;
            b = waterColor.b + randomColorOffset;

            if (r < 0):
                r = 0;
            if (g < 0):
                g = 0;
            if (b < 0):
                b = 0;

            colorMap[x][y].SetColor(r,g,b);

        self.pbar.update(1); # update progress bar