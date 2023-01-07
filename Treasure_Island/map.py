from termcolor import colored,cprint
from generate_map import *
from processing_hint import *
from hint import *
from config import *

class Map():
    def __init__(self) -> None:
        self.board=[]
        self.w,self.h=None,None
        self.region=[]
        self.treasure_pos=None
        self.pirate_pos=None
        self.agent_pos=None
    
    def input(self,filename):
        with open(filename) as f:
            self.w,self.h=f.readline().replace('\n','').split(' ')
            self.w,self.h=int(self.w),int(self.h)
            f.readline()
            f.readline()
            num_of_region=int(f.readline().replace('\n',''))
            for i in range(num_of_region):
                self.region.append(i)
            self.treasure_pos=f.readline().replace('\n','').split(' ')
            self.treasure_pos=(int(self.treasure_pos[0]),int(self.treasure_pos[1]))
            for i in range(self.h):
                data=f.readline().replace('\n','').replace(' ','').split(';')
                for i in range(len(data)):
                    try:
                        data[i]=int(data[i])
                    except:
                        pass
                self.board.append(data)
            self.init_pirate()
    def init_agent(self):
        x=0
        y=0
        while self.board[x][y]==0 or isinstance(self.board[x][y], str) :
            x=random.randint(0,self.h-1)
            y=random.randint(0,self.w-1)
        self.board[x][y]=str(self.board[x][y])+AGENT
        self.agent_pos=(x,y)
        log=f'Agent is allocated at ({x},{y})\n'
        return log
    def init_pirate(self):
        prison_pos=[]
        for i in range(self.h):
            for j in range(self.w):
                type=str(self.board[i][j])[-1:]
                if type==PRISON:
                    prison_pos.append([i,j])
        self.pirate_pos=tuple(random.choice(prison_pos))
    def masking(self,hint):
        veri_flag,mask=self.generate_mask(hint)
        for x,y in mask:
            try:
                self.board[x][y]=int(self.board[x][y])
            except:
                pass
            if isinstance(self.board[x][y],str): 
                if MASKED in self.board[x][y]: continue
                self.board[x][y]=MASKED+self.board[x][y][-1]
            else:
                self.board[x][y]=MASKED
        return veri_flag
    def visualize(self):
        print('{:>4}'.format(''),end='')
        for i in range(len(self.board)):
            print('{:>4}'.format(i),end='')
        print()
        for i in range(len(self.board)):
            print('{:>4}'.format(i),end='')
            for j in range(len(self.board[i])):
                if isinstance(self.board[i][j],str):
                    if AGENT in self.board[i][j]:
                        color=COLOR['AGENT']
                    elif TREASURE in self.board[i][j]:
                        color=COLOR['TREASURE']
                    elif PIRATE in self.board[i][j]:
                        color=COLOR['PIRATE']
                    elif MASKED in self.board[i][j]:
                        color=COLOR['MASKED']
                elif self.board[i][j]==OCEAN:
                    color=COLOR['OCEAN']
                else:
                    region=int(str(self.board[i][j])[:1])
                    color=COLOR['REGION'][region%len(COLOR['REGION'])]
                text = colored('{:>4}'.format(self.board[i][j]), color, attrs=["reverse", "blink"])
                print(text,end='')
            print()
    def generate_mask(self,hint):
        w,h=self.w,self.h
        mask=set()
        if hint[0]+1==1:
            if verify_hint_1 (hint, self.treasure_pos):
                veri_flag=True
                for i in range(1, len(hint)):
                    mask.add(hint[i])
            else:
                veri_flag=False
                for i in range(h):
                    for j in range(w):
                        if (i,j) not in hint:
                            mask.add((i,j))
        elif hint[0]+1==2:
            treasure_region=int(self.board[self.treasure_pos[0]][self.treasure_pos[1]][:1])
            if verify_hint_2 (hint, treasure_region):
                veri_flag=True
                for i in range(h):
                    for j in range(w):
                        if isinstance(self.board[i][j],str) and self.board[i][j][0]=='X': continue
                        region=int(str(self.board[i][j])[:1])
                        if region not in hint[1:]:
                            mask.add((i,j))
            else:
                veri_flag=False
                for i in range(h):
                    for j in range(w):
                        if isinstance(self.board[i][j],str) and self.board[i][j][0]=='X': continue
                        region=int(str(self.board[i][j])[:1])
                        if region in hint[1:]:
                            mask.add((i,j))
        elif hint[0]+1==3:
            treasure_region=int(self.board[self.treasure_pos[0]][self.treasure_pos[1]][:1])
            if verify_hint_3 (hint, treasure_region):
                veri_flag=True
                for i in range(h):
                    for j in range(w):
                        if isinstance(self.board[i][j],str) and self.board[i][j][0]=='X': continue
                        region=int(str(self.board[i][j])[:1])
                        if region in hint[1:]:
                            mask.add((i,j))
            else:
                veri_flag=False
                for i in range(h):
                    for j in range(w):
                        if isinstance(self.board[i][j],str) and self.board[i][j][0]=='X': continue
                        region=int(str(self.board[i][j])[:1])
                        if region not in hint[1:]:
                            mask.add((i,j))
        elif hint[0]+1==4:
            '''
            Hint 4: [3, top x, bottom x, left y, right y]: A large rectangle area that has the treasure. (< half: small; >= half: large)
            '''
            if verify_hint_4 (hint, self.treasure_pos):
                veri_flag=True
                for i in range(h):
                    for j in range(w):
                        if not(hint[1]<=i<=hint[2] and hint[3]<=j<=hint[4]):
                            mask.add((i,j))
            else:
                veri_flag=False
                for i in range(h):
                    for j in range(w):
                        if hint[1]<=i<=hint[2] and hint[3]<=j<=hint[4]:
                            mask.add((i,j))
        elif hint[0]+1==5:
            '''
            Hint 5: [4, top, bottom, left, right]: A small rectangle area that doesn't has the treasure. (< half: small; >= half: large)
            '''
            if verify_hint_5 (hint, self.treasure_pos):
                veri_flag=True
                for i in range(h):
                    for j in range(w):
                        if hint[1]<=i<=hint[2] and hint[3]<=j<=hint[4]:
                            mask.add((i,j))
            else:
                veri_flag=False
                for i in range(h):
                    for j in range(w):
                        if not(hint[1]<=i<=hint[2] and hint[3]<=j<=hint[4]):
                            mask.add((i,j))
        elif hint[0]+1==6:
            '''
            Hint 6: [5]: He tells you that you are the nearest person to the treasure (between you and the prison he is staying).
            '''
            agent_x, agent_y = self.agent_pos
            prison_x, prison_y = self.pirate_pos
            if verify_hint_6 (hint, self.treasure_pos,self.agent_pos,self.pirate_pos):
                veri_flag=True
                for x in range(h):
                    for y in range(w):
                        agent_dist = abs(y - agent_y) + abs(x - agent_x)
                        pirate_dist = abs(x - prison_x) + abs(y - prison_y)
                        if agent_dist > pirate_dist:
                            mask.add((x,y))
            else:
                veri_flag=False
                for x in range(h):
                    for y in range(w):
                        agent_dist = abs(y - agent_y) + abs(x - agent_x)
                        pirate_dist = abs(x - prison_x) + abs(y - prison_y)
                        if agent_dist < pirate_dist:
                            mask.add((x,y))
        elif hint[0]+1==7:
            '''
            Hint 7: [6, 0: Row/ 1: Column, x]: A column and/or a row that contain the treasure (rare)
            '''
            if verify_hint_7 (hint, self.treasure_pos):
                veri_flag=True
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
                veri_flag=False
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
                veri_flag=True
                if hint[1]==0:
                    i=hint[2]
                    for j in range(w):
                        mask.add((i,j))
                else:
                    j=hint[2]
                    for i in range(h):
                        mask.add((i,j))
            else:
                veri_flag=False
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
                if isinstance(self.board[i][j],str) and self.board[i][j][0]=='X': return False
                region=int(str(self.board[i][j])[:1])
                if region!=region1 or region!=region2: return False
                x=[-1,0,1,0]
                y = [0,1,0,-1]
                for t in range(4):
                    try:
                        tile_region=int(self.board[i+x[t]][j+y[t]][:1])
                        if (region==region1 and tile_region==region2) or (region==region2 and tile_region==region1): return True
                    except:
                        continue
                return False
            region1,region2=hint[1],hint[2]
            if verify_hint_9 (hint, self.board,self.treasure_pos):
                veri_flag=True
                for i in range(h):
                    for j in range(w):
                        if not is_boundary_2(i,j,region1,region2):
                            mask.add((i,j))
            else:
                veri_flag=False
                for i in range(h):
                    for j in range(w):
                        if is_boundary_2(i,j,region1,region2):
                            mask.add((i,j))
        elif hint[0]+1==10:
            '''
            Hint 10: [9]: The treasure is somewhere in a boundary of 2 regions.
            '''
            def is_boundary(i,j):
                if isinstance(self.board[i][j],str) and self.board[i][j][0]=='X': return False
                region=int(str(self.board[i][j])[:1])
                if region==0: return False
                x=[-1,0,1,0]
                y = [0,1,0,-1]
                for t in range(4):
                    try:
                        tile_region=int(self.board[i+x[t]][j+y[t]][:1])
                        if (tile_region!=region): return True
                    except:
                        continue
                return False
            if verify_hint_10 (hint, self.treasure_pos):
                veri_flag=True
                for i in range(h):
                    for j in range(w):
                        if not is_boundary(i,j):
                            mask.add((i,j))
            else:
                veri_flag=False
                for i in range(h):
                    for j in range(w):
                        if is_boundary(i,j):
                            mask.add((i,j))
        elif hint[0]+1==11:
            '''
            Hint 11: [10, 2/3]: The treasure is somewhere in an area bounded by 2-3 tiles from sea.
            '''
            def bounded_ocean(i,j,dist):
                if isinstance(self.board[i][j],str) and self.board[i][j][0]=='X': return False
                region=int(str(self.board[i][j])[:1])
                if region==0: return False
                x=[-1,0,1,0]
                y = [0,1,0,-1]
                for d in range(1,dist):
                    for t in range(4):
                        try:
                            tile_region=int(self.board[i+x[t]*d][j+y[t]*d][:1])
                            if tile_region==0:return True
                        except:
                            continue
                return False
            dist=hint[1]
            if verify_hint_11 (hint,self.board,self.treasure_pos):
                veri_flag=True
                for i in range(h):
                    for j in range(w):
                        if not bounded_ocean(i,j,dist):
                            mask.add((i,j))
            else:
                veri_flag=False
                for i in range(h):
                    for j in range(w):
                        if bounded_ocean(i,j,dist):
                            mask.add((i,j))
        elif hint[0]+1==12:
            '''
            Hint 12: [11, 1: Half right / 2: Half left / 3: Half top / 4: Half bottom]: A half of the map without treasure (rare).
            '''
            pos = hint[1]
            size=self.w
            if verify_hint_12 (hint, size,self.treasure_pos):
                veri_flag=True
                if (pos==1):
                    for i in range(h):
                        for j in range(size//2,w):
                                mask.add((i,j))
                elif (pos==2):
                    for i in range(h):
                        for j in range(0,size//2):
                                mask.add((i,j))
                elif (pos==3):
                    for i in range(0,size//2):
                        for j in range(w):
                                mask.add((i,j))
                else:
                    for i in range(size//2,h):
                        for j in range(w):
                                mask.add((i,j))
            else:
                veri_flag=False
                if (pos==2):
                    for i in range(h):
                        for j in range(size//2,w):
                                mask.add((i,j))
                elif (pos==1):
                    for i in range(h):
                        for j in range(0,size//2):
                                mask.add((i,j))
                elif (pos==4):
                    for i in range(0,size//2):
                        for j in range(w):
                                mask.add((i,j))
                else:
                    for i in range(size//2,h):
                        for j in range(w):
                                mask.add((i,j))
        elif hint[0]+1==13:
            '''
        Hint 13: [12, 1: Center / 2: Prison, 1: N / 2: S / 3: W / 4: E / 5: SE / 6: SW / 7: NE / 8: NW]:
        From the center of the map/from the prison that he's staying,
        he tells you a direction that has the treasure (W, E, N, S or SE, SW, NE, NW)
        (The shape of area when the hints are either W, E, N or S is triangle).
            '''
            size=self.w
            pos_choice, direction = hint[1], hint[2]
            tmp_mask=set()
            if pos_choice==1:
                    x,y=self.h//2,self.w//2
            elif pos_choice==2:
                x,y=self.pirate_pos
            if direction==1: #N
                row=x #current row
                while row>=0:
                    padding=abs(x-row)
                    for j in range(y-padding,y+padding+1):
                        if j<0 or j>=self.w: continue
                        tmp_mask.add((row,j))
                    row-=1
            elif direction==2: #S
                row=x #current row
                while row<self.h:
                    padding=abs(x-row)
                    for j in range(y-padding,y+padding+1):
                        if j<0 or j>=self.w: continue
                        tmp_mask.add((row,j))
                    row+=1
            elif direction==3: #W
                col=y #current col
                while col>=0:
                    padding=abs(y-col)
                    for i in range(x-padding,x+padding+1):
                        if i<0 or i>=self.h: continue
                        tmp_mask.add((i,col))
                    col-=1
            elif direction==4: #E
                col=y #current col
                while col<self.w:
                    padding=abs(y-col)
                    for i in range(x-padding,x+padding+1):
                        if i<0 or i>=self.h: continue
                        tmp_mask.add((i,col))
                    col+=1
            elif direction==5: #SE
                for i in range(x,self.h):
                    for j in range(y,self.w):
                        tmp_mask.add((i,j))
            elif direction==6: #SW
                for i in range(x,self.h):
                    for j in range(0,y+1):
                        tmp_mask.add((i,j))
            elif direction==7: #NE
                for i in range(0,x):
                    for j in range(y,self.w):
                        tmp_mask.add((i,j))
            elif direction==8: #NW
                for i in range(0,x+1):
                    for j in range(0,y+1):
                        tmp_mask.add((i,j))
            if verify_hint_13 (hint, size,self.pirate_pos,self.treasure_pos):
                veri_flag=True
                for i in range(self.h):
                    for j in range(self.w):
                        if (i,j) not in tmp_mask:
                            mask.add((i,j))
            else:
                veri_flag=False
                mask=tmp_mask         

        elif hint[0]+1==14:
            '''
            Hint 14: [13, top_big, bottom_big, left_big, right_big, top_small, bottom_small, left_small, right_small]: 
            2 squares that are different in size, the small one is placed inside the bigger one, the treasure is somewhere inside the gap between 2 squares. (rare)
            '''
            topBig, bottomBig, leftBig, rightBig = hint[1],hint[2], hint[3], hint[4]
            topSmall, bottomSmall, leftSmall, rightSmall = hint[5], hint[6], hint[7], hint[8]
            if verify_hint_14 (hint, self.treasure_pos):
                veri_flag=True
                for x in range(h):
                    for y in range(w):
                        if not (((topBig<=x<topSmall or bottomSmall<x<=bottomBig) and leftBig<=y<=rightBig) or (topBig<=x<=bottomBig and (leftBig<=y<leftSmall or rightSmall<y<=rightBig))):
                            mask.add((x,y))
            else:
                veri_flag=False
                for x in range(topBig,bottomSmall+1):
                    for y in range(leftBig,rightBig+1):
                        if not (topSmall<=x<=bottomSmall and leftSmall<=y<=rightSmall):
                            mask.add((x,y))
        elif hint[0]+1==15:
            '''
            The treasure is in regions that has mountain
            '''
            if verify_hint_15 (map=self.board, treasurePos=self.treasure_pos):
                veri_flag=True
                for x in range(h):
                    for y in range(w):
                        type=str(self.board[x][y][-1:])
                        if type!=MOUNTAIN:
                            mask.add((x,y))

            else:
                veri_flag=False
                for x in range(h):
                    for y in range(w):
                        type=str(str(self.board[x][y])[-1:])
                        if type==MOUNTAIN:
                            mask.add((x,y))
        return veri_flag,mask
