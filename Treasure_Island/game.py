from generate_map import *
from processing_hint import *
import os 

class Game():
    def __init__(self,filename):
        with open(filename) as f:
            self.map=[]
            self.w,self.h=None
            self.reveal_prison_turn=None
            self.release_turn=None
            self.num_of_region=None
            self.treasure_pos=None
            self.teleport=False
            self.action=['verification','move_scan_small','move_large','scan_large']
            self.pirate_pos=None

    def input(self,filename):
        with open(filename) as f:
            self.w,self.h=f.readline().replace('\n','').split(' ')
            self.w,self.h=int(self.w),int(self.h)
            self.reveal_prison_turn=int(f.readline().replace('\n',''))
            self.release_turn=int(f.readline().replace('\n',''))
            self.num_of_region=int(f.readline().replace('\n',''))
            self.treasure_pos=f.readline().replace('\n','').split(' ')
            self.treasure_pos=[int(self.treasure_pos[0]),int(self.treasure_pos[1])]
            for i in range(self.h):
                data=f.readline().replace('\n','').replace(' ','').split(';')
                self.map.append(data)
    
    def visualize_map(self):
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                print('{:>2}'.format(self.map[i][j]),end=' ')
            print()
    def play():
        

   
cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory
print("Files in %r: %s" % (cwd, files))      
t=Game('Treasure_Island/input/MAP02.txt')
t.visualize_map()