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
        self.teleport=False
        self.action_list=['verification','move_scan_small','move_large','scan_large']
        self.visited_hint=[]
        self.hint=[]
        self.result=None
        self.turn=0

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
        action_log=self.action_list[choice]+'\n'
        if self.action_list[choice]=='verification':
            hint_choice=self.hint.pop(0)
            hint,log=generateHint(hint_choice,self.map.board,self.map.region)
            veri_flag=self.map.masking(hint)
            action_log+='HINT: '+log+' '
            action_log+='Verification: '+str(veri_flag)
        elif self.action_list[choice]=='move_scan_small':
            pass
        elif self.action_list[choice]=='move_large':
            pass
        elif self.action_list[choice]=='scan_large':
            pass
        return action_log
    def play(self):
        self.map.init_agent()
        log=None
        while self.result is None:
            self.turn+=1
            print('--------------------------------------')
            print(f'TURN {self.turn}')
            self.get_hint()
            # action_choice=random.randint(0,len(self.action_list)-1)
            action_choice=0
            log=self.action(action_choice)
            self.map.visualize()
            print(log)
            input('Press Enter to continue')

        

   
cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory
print("Files in %r: %s" % (cwd, files))      
t=Game()
t.input('Treasure_Island/input/MAP02.txt')
t.play()