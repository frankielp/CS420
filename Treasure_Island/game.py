from generate_map import *
from processing_hint import *
from hint import *
from config import *
from map import *
import os 

class Game():
    def __init__(self):
        self.map=Map()
        self.reveal_prison_turn=None
        self.release_turn=None
        self.pirate=False
        self.teleport=False
        self.action_list=['verification','move_scan_small','move_large','scan_large']
        self.visited_hint=[]
        self.hint=[]
        self.result=None
        self.turn=0
        self.small_scan=3
        self.large_scan=5

    def input(self,filename):
        self.map.input(filename)
        with open(filename) as f:
            f.readline()
            self.reveal_prison_turn=int(f.readline().replace('\n',''))
            self.release_turn=int(f.readline().replace('\n',''))
    def get_hint(self):
        # p = 0.045 for hints that are rare
        while True:
            choice = np.random.choice(a=np.arange(1, 16, 1, dtype=int), p = (0.07, 0.07, 0.07, 0.07, 0.07, 0.07, (1-0.07*12)/3, 0.07, 0.07, 0.07, 0.07, (1-0.07*12)/3, 0.07, (1-0.07*12)/3, 0.07))
            if choice not in self.visited_hint: break
        self.hint.append(choice)
        self.visited_hint.append(choice)
    def action(self,choice):
        action_log='ACTION: '+self.action_list[choice].upper()+'\n'
        if self.action_list[choice]=='verification':
            if len(self.hint)==0 and len(self.visited_hint==15): 
                action_log+='No hint left\n'
                return action_log
            hint_choice=self.hint.pop(0)
            hint,log=generateHint(hint_choice,self.map.board,self.map.region)
            veri_flag=self.map.masking(hint)
            action_log+='HINT: '+log+' - '
            action_log+='Verification: '+str(veri_flag)+'\n'
        elif self.action_list[choice]=='move_scan_small':
            pass
        elif self.action_list[choice]=='move_large':
            pass
        elif self.action_list[choice]=='scan_large':
            pass
        return action_log
    def free_pirate(self):
        self.pirate=True
        x,y=self.map.pirate_pos
    def pirate_move(self):
        direction=''
        px,py=self.map.pirate_pos
        tx,ty=self.map.treasure_pos
        self.map.board[px][py]=str(self.map.board[px][py]).replace(PIRATE,'')
        if px==tx:
            if py-ty>0:
                py-=min(2,abs(py-ty))
                direction+='W'
            else:
                py+=min(2,abs(py-ty))
                direction+='E'
        elif py==ty:
            if px-tx>0:
                px-=min(2,abs(px-tx))
                direction+='N'
            else:
                px+=min(2,abs(px-tx))
                direction+='S'
        else:
            if px-tx>0:
                px-=1
                direction+='N'
            else:
                px+=1
                direction+='S'
            if py-ty>0:
                py-=1
                direction+='W'
            else:
                py+=1
                direction+='E'
        self.map.board[px][py]=str(self.map.board[px][py])+PIRATE
        if px==tx and py==ty:
            self.result='LOSE'
        self.map.pirate_pos=(px,py)
    def scan(self,size):
        x,y=self.map.agent_pos
        tx,ty=self.map.treasure_pos
        for i in range(x-size//2,x+size//2+1):
            for j in range(y-size//2,y+size//2+1):
                if i==tx and j==ty:
                    self.result='WIN'
                    continue
                self.map.board[i][j]=='XX'
    def play(self):
        self.map.init_agent()
        while self.result is None:
            log=''
            self.turn+=1
            print('--------------------------------------')
            print(f'TURN {self.turn}')
            if self.turn==self.reveal_prison_turn:
                px,py=self.map.pirate_pos
                log+=f'The prison of pirate locate at x={px},y={py}\n'
            if self.turn==self.release_turn:
                log+='Pirate has been released\n'
                self.free_pirate()
            if self.pirate:
                self.pirate_move()
            if len(self.visited_hint)<15:
                self.get_hint()
            action_choice=random.randint(0,len(self.action_list)-1)
            # action_choice=1
            log+=self.action(action_choice)
            self.map.visualize()
            print()
            print('LOG\n'+log)
            input('Press Enter to continue')

        

   
cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory
print("Files in %r: %s" % (cwd, files))      
t=Game()
t.input('Treasure_Island/input/MAP02.txt')
t.play()