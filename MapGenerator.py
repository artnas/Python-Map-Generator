print("Setting up... \n");

from PIL import Image

from Map import *
from _Generators import *
from Classes import *
from VectorMath import *

image = Image.new("RGB", (mapSize,mapSize))
targetGenerator = None

# future multiproc stuff

#import multiprocessing
#
#
#def worker(index):
#    print("worker spawned ",index)
#    while(True):
#        if (targetGenerator == None or targetGenerator.isFinished):
#            break;
#        targetGenerator.GenerateAutomated();
#    for x in range(0, mapSize):
#        for y in range(0, mapSize):
#            im.putpixel((x,y), colorMap[x][y].GetTuple());

#threadsAmount = 1
#threads = []

#if __name__ == '__main__':

#    for i in range(threadsAmount):
#        print("starting process ", i);
#        t = multiprocessing.Process(target=worker, args=(i,))
#        threads.append(t)
#        t.start()

#    for i in range(threadsAmount):
#        threads[i].join();

targetGenerator = MapGen_Main();

print("Generating... \n");

targetGenerator.GenerateFull();

print("\n\nGeneration finished. Saving output as Generated.png.");

for x in range(0, mapSize):
    for y in range(0, mapSize):
        image.putpixel((x,y), colorMap[x][y].GetTuple());

image.save("Generated.png");
image.show();
