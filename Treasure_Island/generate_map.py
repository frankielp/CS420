import random
from config import *
class MapGenerator:
    def __init__(self,size,num_of_region,num_of_prison,num_of_mountain):
        self.map=[]
        self.size=size
        self.num_of_region=num_of_region
        self.num_of_prison=num_of_prison
        self.num_of_mountain=num_of_mountain
        
        for i in range(self.size):
            self.map.append([])
            for j in range(self.size):
                self.map[i].append(-1)
                
        self.create_ocean()
        self.create_region()
        self.allocate_mountain()
        self.allocate_prison()
        self.treasure_pos=self.allocate_treasure()
    def create_ocean(self):
        prob1=0.5
        prob2=0.1
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if i==0 or i==len(self.map)-1 or j==0 or j==len(self.map)-1:
                    self.map[i][j]=OCEAN
                    expand=random.randint(0,1)
                    self.expand_prob(i,j,prob1)
                    if self.size//10>=3:
                        for x in [-1,0,1]:
                            for y in [-1,0,1]:
                                if x==0 and y==0: continue
                                try:
                                    if self.map[i+x][j+y]==OCEAN:
                                        self.expand_prob(i+x,j+y,prob2)
                                except: pass
                            
    def expand_prob(self,i,j,prob):
#         expand with expanded probability 0->1
        value=self.map[i][j] 
        prob=[1]*int(prob*10)+[0]*int((1-prob)*10)
        expand=random.choice(prob)
        if expand:
            for x in [-1,0,1]:
                for y in [-1,0,1]:
                    if x==0 and y==0: continue
                    if x!=0 and y!=0: continue
                    try:
                        self.map[i+x][j+y]=max(self.map[i+x][j+y],value)
                    except: pass
    def divide_region(self):
        region_ratio=[]
        for i in range(self.num_of_region-1):
            rate=random.choice([1/self.num_of_region,1/self.num_of_region+1/self.num_of_region/5])
            region_ratio.append(rate)
        region_ratio.append(1-sum(region_ratio))         
        total=self.size**2
        ocean_count=0
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j]==OCEAN:
                    ocean_count+=1
        total-=ocean_count
        region_tile={}
        for i in range(self.num_of_region):
            region_tile[i+1]=round(total*region_ratio[i])
        if sum(region_tile.values())+ocean_count!=self.size**2:
            region_tile[self.num_of_region]+=self.size**2-sum(region_tile.values())-ocean_count
        
        return region_tile
                    
    def visualize (self):
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                print('{:>2}'.format(self.map[i][j]),end=' ')
            print()
    def expand_tile(self,i,j,region,tile): #expand with number of tile
        queue=[[i,j]]
        while tile>0 and len(queue)>0:
            index=queue.pop(0)
            self.map[index[0]][index[1]]=region
            tile-=1
            i,j=index[0],index[1]
            for x in [-1,0,1]:
                for y in [-1,0,1]:
                    if x==0 and y==0: continue
                    if self.map[i+x][j+y]==-1 and [i+x,j+y] not in queue:
                        queue.append([i+x,j+y])

        

    def create_region(self):
        region_tile=self.divide_region()
        for region in region_tile.keys():
            region_flag=False
            for i in range(len(self.map)):
                for j in range(len(self.map[i])):
                    if self.map[i][j]==-1:
                        self.expand_tile(i,j,region,region_tile[region])
                        region_flag=True
                        break
                if region_flag:
                    break
        # final check
        for i in range(len(self.map)):
                for j in range(len(self.map[i])):
                    if self.map[i][j]==-1:
                        self.map[i][j]=self.map[i-1][j]
    def allocate_mountain(self):
        moutain_length=min(self.size//self.num_of_mountain,10)
        for i in range(self.num_of_mountain):
            count=moutain_length
            x=0
            y=0
            while self.map[x][y]==0 or isinstance(self.map[x][y], str) :
                x=random.randint(0,self.size-1)
                y=random.randint(0,self.size-1)
            self.map[x][y]=str(self.map[x][y])+MOUNTAIN
            count-=1
            a=b=0
            while count>0:
                visited=[]
                while (a!=0 and b!=0) or self.map[x+a][y+b]==0 or isinstance(self.map[x+a][y+b], str):
                    tmp_a=random.choice([-1,1,0])
                    tmp_b=random.choice([-1,1,0])
                    if [tmp_a,tmp_b] in visited:
                        continue
                    else:
                        visited.append([a,b])
                        a,b=tmp_a,tmp_b
                x=x+a
                y=y+b
                self.map[x][y]=str(self.map[x][y])+MOUNTAIN
                count-=1
                a=b=1
                   
    def allocate_treasure(self):
        x=0
        y=0
        while self.map[x][y]==0 or isinstance(self.map[x][y], str) or self.map[x][y][-1:]==MOUNTAIN:
            x=random.randint(0,self.size-1)
            y=random.randint(0,self.size-1)
        self.map[x][y]=str(self.map[x][y])+TREASURE
        return [x,y]
    def allocate_prison(self):
        for i in range(self.num_of_prison):
            x=0
            y=0
            while self.map[x][y]==0 or isinstance(self.map[x][y], str) :
                x=random.randint(0,self.size-1)
                y=random.randint(0,self.size-1)
            self.map[x][y]=str(self.map[x][y])+PRISON
        
    def export(self,filename):
        with open (filename,'a') as f:
            f.write(f'{self.size} {self.size}\n') #size
            if self.size//10>3:
                f.write(f'{random.randint(2,4)}\n') #turn reveal prison
            else: 
                f.write(f'{random.randint(3,4)}\n')
            f.write(f'{random.randint(self.size/2,self.size/2+self.size//10)}\n') #turn release pirate
            f.write(f'{self.num_of_region}\n')
            f.write(f'{self.treasure_pos[0]} {self.treasure_pos[1]}\n')
#             map
            for i in range(len(self.map)):
                for j in range(len(self.map[i])):
                    if j==len(self.map[i])-1:
                        f.write('{:>2}\n'.format(self.map[i][j]))
                    else:
                        f.write('{:>2};'.format(self.map[i][j]))