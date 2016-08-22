from Classes import *
import random

perlinOffset = random.random()*2048; # random offset

mapSize = 2048; # size in pixels
perlinScale = 0.0025;
mapCenter = (mapSize/2, mapSize/2);

landThreshold = 0.1;

heightMap = [[0]*mapSize for x in range(mapSize)]
colorMap = [[Color() for j in range(mapSize)] for i in range(mapSize)]

randomColorRange = 10;
colorPerlinScale = 0.025;