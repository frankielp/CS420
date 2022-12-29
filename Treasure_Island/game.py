from generate_map import *
from processing_hint import *
from hint import *
import os 

class Game():
    def __init__(self):
        self.map=[]
        self.w,self.h=None,None
        self.reveal_prison_turn=None
        self.release_turn=None
        self.region=[]
        self.treasure_pos=None
        self.teleport=False
        self.action=['verification','move_scan_small','move_large','scan_large']
        self.pirate_pos=None
        self.agent_pos=None
        self.visited_hint=[]
        self.hint=[]
        self.game_status=None
        self.turn=0

    def input(self,filename):
        with open(filename) as f:
            self.w,self.h=f.readline().replace('\n','').split(' ')
            self.w,self.h=int(self.w),int(self.h)
            self.reveal_prison_turn=int(f.readline().replace('\n',''))
            self.release_turn=int(f.readline().replace('\n',''))
            num_of_region=int(f.readline().replace('\n',''))
            for i in range(num_of_region):
                self.region.append(i)
            self.treasure_pos=f.readline().replace('\n','').split(' ')
            self.treasure_pos=[int(self.treasure_pos[0]),int(self.treasure_pos[1])]
            for i in range(self.h):
                data=f.readline().replace('\n','').replace(' ','').split(';')
                self.map.append(data)
    
    def visualize_map(self):
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                print('{:>3}'.format(self.map[i][j]),end=' ')
            print()
    def masking(self,mask):
        pass
    def generate_mask(self,hint):
        w,h=self.w,self.h
        mask=set()
        if hint[0]+1==1:
            if verify_hint_1 (hint, self.treasure_pos):
                for i in range(1, len(hint)):
                    mask.add(hint[i])
                else:
                    for i in range(h):
                        for j in range(w):
                            if (i,j) not in hint:
                                mask.add((i,j))
        elif hint[0]+1==2:
            treasure_region=int(self.map[self.treasure_pos[0]][self.treasure_pos[1]][:1])
            if verify_hint_2 (hint, treasure_region):
                for i in range(h):
                    for j in range(w):
                        region=int(self.map[i][j][:1])
                        if region not in hint[1:]:
                            mask.add((i,j))
            else:
                for i in range(h):
                    for j in range(w):
                        region=int(self.map[i][j][:1])
                        if region in hint[1:]:
                            mask.add((i,j))
        elif hint[0]+1==3:
            treasure_region=int(self.map[self.treasure_pos[0]][self.treasure_pos[1]][:1])
            if verify_hint_3 (hint, treasure_region):
                for i in range(h):
                    for j in range(w):
                        region=int(self.map[i][j][:1])
                        if region in hint[1:]:
                            mask.add((i,j))
            else:
                for i in range(h):
                    for j in range(w):
                        region=int(self.map[i][j][:1])
                        if region not in hint[1:]:
                            mask.add((i,j))
        elif hint[0]+1==4:
            if verify_hint_4 (hint, self.treasure_pos):
                for i in range(h):
                    for j in range(w):
                        if i<hint[1] or i>hint[2] or j<hint[3] or j>hint[4]:
                            mask.add((i,j))
            else:
                for i in range(h):
                    for j in range(w):
                        if i>=hint[1] or i<=hint[2] or j>=hint[3] or j<=hint[4]:
                            mask.add((i,j))
        elif hint[0]+1==5:
            '''
            Hint 5: [4, top, bottom, left, right]: A small rectangle area that doesn't has the treasure. (< half: small; >= half: large)
            '''
            if verify_hint_5 (hint, self.treasure_pos):
                for i in range(h):
                    for j in range(w):
                        if i>=hint[1] or i<=hint[2] or j>=hint[3] or j<=hint[4]:
                            mask.add((i,j))
            else:
                for i in range(h):
                    for j in range(w):
                        if i<hint[1] or i>hint[2] or j<hint[3] or j>hint[4]:
                            mask.add((i,j))
        elif hint[0]+1==6:
            '''
            Hint 6: [5]: He tells you that you are the nearest person to the treasure (between you and the prison he is staying).
            '''
            agent_x, agent_y = self.agent_pos
            prison_x, prison_y = self.pirate_pos
            if verify_hint_6 (hint, self.treasure_pos,self.agent_pos,self.pirate_pos):
                for x in range(h):
                    for y in range(w):
                        agent_dist = abs(y - agent_y) + abs(x - agent_x)
                        pirate_dist = abs(x - prison_x) + abs(y - prison_y)
                        if agent_dist > pirate_dist:
                            mask.add((i,j))
            else:
                for x in range(h):
                    for y in range(w):
                        agent_dist = abs(y - agent_y) + abs(x - agent_x)
                        pirate_dist = abs(x - prison_x) + abs(y - prison_y)
                        if agent_dist < pirate_dist:
                            mask.add((i,j))
        elif hint[0]+1==7:
            '''
            Hint 7: [6, 0: Row/ 1: Column, x]: A column and/or a row that contain the treasure (rare)
            '''
            if verify_hint_7 (hint, self.treasure_pos):
                if hint[1]==0:
                    for i in range(h):
                        if i==hint[2]:continue
                        for j in range(w):
                            mask.add((i,j))
                else:
                    for j in range(w):
                        if j==hint[2]:continue
                        for i in range(h):
                            mask.add((i,j))
            else:
                if hint[1]==0:
                    i=hint[2]
                    for j in range(w):
                        mask.add((i,j))
                else:
                    j=hint[2]
                    for i in range(h):
                        mask.add((i,j))
        elif hint[0]+1==8:
            '''
            Hint 8: [7, 0: Row/ 1: Column, x]: A column and/or a row that do not contain the treasure.
            '''
            if verify_hint_8 (hint, self.treasure_pos):
                if hint[1]==0:
                    i=hint[2]
                    for j in range(w):
                        mask.add((i,j))
                else:
                    j=hint[2]
                    for i in range(h):
                        mask.add((i,j))
            else:
                if hint[1]==0:
                    for i in range(h):
                        if i==hint[2]:continue
                        for j in range(w):
                            mask.add((i,j))
                else:
                    for j in range(w):
                        if j==hint[2]:continue
                        for i in range(h):
                            mask.add((i,j))
        elif hint[0]+1==9:
            '''
            Hint 9: [8, x, y]: 2 regions that the treasure is somewhere in their boundary
            '''
            def is_boundary_2(i,j,region1,region2):
                region=int(self.map[i][j][:1])
                if region!=region1 and region!=region2: return False
                x=[-1,0,1,0]
                y = [0,1,0,-1]
                for t in range(4):
                    try:
                        tile_region=int(self.map[i+x[t]][j+y[t]][:1])
                        if (region==region1 and tile_region==region2) or (region==region2 and tile_region==region1): return True
                    except:
                        continue
                return False
            region1,region2=hint[1],hint[2]
            if verify_hint_9 (hint, self.map,self.treasure_pos):
                for i in range(h):
                    for j in range(w):
                        if not is_boundary_2(i,j,region1,region2):
                            mask.add((i,j))
            else:
                for i in range(h):
                    for j in range(w):
                        if is_boundary_2(i,j,region1,region2):
                            mask.add((i,j))
        elif hint[0]+1==10:
            '''
            Hint 10: [9,x,y]: The treasure is somewhere in a boundary of 2 regions.
            '''
            def is_boundary_2(i,j,region1,region2):
                region=int(self.map[i][j][:1])
                if region!=region1 and region!=region2: return False
                x=[-1,0,1,0]
                y = [0,1,0,-1]
                for t in range(4):
                    try:
                        tile_region=int(self.map[i+x[t]][j+y[t]][:1])
                        if (region==region1 and tile_region==region2) or (region==region2 and tile_region==region1): return True
                    except:
                        continue
                return False
            region1,region2=hint[1],hint[2]
            if verify_hint_10 (hint, game.treasure_pos):
                pass
            else:
                pass
        elif hint[0]+1==11:
            if verify_hint_11 (hint, game.treasure_pos):
                pass
            else:
                pass
        elif hint[0]+1==12:
            if verify_hint_12 (hint, game.treasure_pos):
                pass
            else:
                pass
        elif hint[0]+1==13:
            if verify_hint_13 (hint, game.treasure_pos):
                pass
            else:
                pass
        elif hint[0]+1==14:
            if verify_hint_14 (hint, game.treasure_pos):
                pass
            else:
                pass
        elif hint[0]+1==15:
            if verify_hint_15 (hint, game.treasure_pos):
                pass
            else:
                pass
        
    def play(self):
        while self.status is None:
            self.turn+=1
        

   
cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory
print("Files in %r: %s" % (cwd, files))      
t=Game()
t.input('Treasure_Island/input/MAP02.txt')
t.visualize_map()