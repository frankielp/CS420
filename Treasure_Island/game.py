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
        if self.turn==1:
            choice=self.get_first_hint()
        else:
            choice = np.random.choice(a=np.arange(1, 16, 1, dtype=int), p = (0.07, 0.07, 0.07, 0.07, 0.07, 0.07, (1-0.07*12)/3, 0.07, 0.07, 0.07, 0.07, (1-0.07*12)/3, 0.07, (1-0.07*12)/3, 0.07))
        self.hint.append(choice)
    def action(self,choice,direction=None):
        action_log='\nACTION: '+self.action_list[choice].upper()+'\n'
        if self.action_list[choice]=='verification':
            hint_choice=self.hint.pop(0)
            hint,log=generateHint(hint_choice,self.map.board,self.map.region)
            veri_flag=self.map.masking(hint)
            action_log+='HINT: '+log+'\n'
            action_log+='Verification: '+str(veri_flag)+'\n'
        elif self.action_list[choice]=='move_scan_small':
            self.agent_move('small',direction)
            action_log+=f'Agent moves straight small steps into x={self.map.agent_pos[0]} y={self.map.agent_pos[1]}\n'
            action_log+='Conduct small scan\n'
            log=self.scan(self.small_scan)
            action_log+=log
        elif self.action_list[choice]=='move_large':
            self.agent_move('large',direction)
            action_log+=f'Agent moves straight large steps into x={self.map.agent_pos[0]} y={self.map.agent_pos[1]}\n'
        elif self.action_list[choice]=='scan_large':
            action_log+='Conduct large scan\n'
            log=self.scan(self.large_scan)
            action_log+=log
        return action_log
    def free_pirate(self):
        self.pirate=True
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
        return direction
    def scan(self,size):
        log=''
        x,y=self.map.agent_pos
        tx,ty=self.map.treasure_pos
        for i in range(x-size//2,x+size//2+1):
            for j in range(y-size//2,y+size//2+1):
                if i==tx and j==ty:
                    self.map.board[i][j]=MASKED+TREASURE
                    self.result='WIN'
                    log+=f'Found Treasure at x={i} y={j}\n'
                    continue
                try:
                    if isinstance(self.map.board[i][j],str) and AGENT in self.map.board[i][j]:
                        self.map.board[i][j]=MASKED+AGENT
                    else:
                        self.map.board[i][j]=MASKED
                except:
                    pass

        if self.result is None:
            log+='Found nothing\n'
        return log
    def get_first_hint(self):
        flag=False
        while True:
            for i in range(16):
                hint,log=generateHint(i+1,self.map.board,self.map.region)
                if hint[0]+1==1:
                    flag=verify_hint_1(hint,self.map.treasure_pos)
                elif hint[0]+1==2:
                    treasure_region=int(self.map.board[self.map.treasure_pos[0]][self.map.treasure_pos[1]][:1])
                    flag=verify_hint_2(hint,treasure_region)
                elif hint[0]+1==3:
                    treasure_region=int(self.map.board[self.map.treasure_pos[0]][self.map.treasure_pos[1]][:1])
                    flag=verify_hint_3(hint,treasure_region)
                elif hint[0]+1==4:
                    flag=verify_hint_4(hint,self.map.treasure_pos)
                elif hint[0]+1==5:
                    flag=verify_hint_5(hint,self.map.treasure_pos)
                elif hint[0]+1==6:
                    flag=verify_hint_6(hint,self.map.treasure_pos,self.map.agent_pos,self.map.pirate_pos)
                elif hint[0]+1==7:
                    flag=verify_hint_7(hint,self.map.treasure_pos)
                elif hint[0]+1==8:
                    flag=verify_hint_8(hint,self.map.treasure_pos)
                elif hint[0]+1==9:
                    flag=verify_hint_9(hint,self.map.board,self.map.treasure_pos)
                elif hint[0]+1==10:
                    flag=verify_hint_10(self.map.board,self.map.treasure_pos)
                elif hint[0]+1==11:
                    flag=verify_hint_11(hint,self.map.board,self.map.treasure_pos)
                elif hint[0]+1==12:
                    flag=verify_hint_12(hint,self.map.h,self.map.treasure_pos)
                elif hint[0]+1==13:
                    flag=verify_hint_13(hint,self.map.h,self.map.pirate_pos,self.map.treasure_pos)
                elif hint[0]+1==14:
                    flag=verify_hint_14(hint,self.map.treasure_pos)
                elif hint[0]+1==15:
                    flag=verify_hint_15(self.map.board,self.map.treasure_pos)
                if flag: return i+1
            
    def agent_move(self,choice,pi_direction=None):
        ax,ay=self.map.agent_pos
        self.map.board[ax][ay]=str(self.map.board[ax][ay]).replace(AGENT,'')
        if choice=='large':
            step=random.randint(3,4)
        elif choice=='small':
            step=random.randint(1,2)
        if self.pirate:
            direction=pi_direction
        else:
            direction=''
            direction_count={'N':0,'E':0,'W':0,'S':0}
            for i in range(self.map.h):
                for j in range(self.map.w):
                    if self.map.board[i][j]!=OCEAN and (self.map.board[i][j]!=MASKED or self.map.board[i][j]!=MASKED+AGENT):
                        if i<ax: direction_count['N']+=1
                        elif i>ax: direction_count['S']+=1
                        if j<ay: direction_count['W']+=1
                        elif i>ay: direction_count['E']+=1
            direction_count=sorted(direction_count.keys(),key= lambda x:direction_count[x],reverse=True)
            direction+=str(direction_count[0])+str(direction_count[1])
        for i in range(len(direction)):
            if i==len(direction)-1:
                tmp_step=step
            else:
                tmp_step=step//2
            if direction[i]=='N':
                ax-=tmp_step
            elif direction[i]=='S':
                ax+=tmp_step
            elif direction[i]=='E':
                ay+=tmp_step
            elif direction[i]=='W':
                ay-=tmp_step
            step-=tmp_step
        # Correction
        ax=min(max(0,ax),self.map.w-1)
        ay=min(max(0,ay),self.map.h-1)

        self.map.agent_pos=(ax,ay)
        self.map.board[ax][ay]=str(self.map.board[ax][ay])+AGENT
    def teleport_agent(self,direction):
        self.map.agent_pos=self.map.pirate_pos
        ax,ay=self.map.agent_pos
        self.map.board[ax][ay]=str(self.map.board[ax][ay]).replace(AGENT,'')
        step=4
        for i in range(len(direction)):
            if i==len(direction)-1:
                tmp_step=step
            else:
                tmp_step=step//2
            if direction[i]=='N':
                ax-=tmp_step
            elif direction[i]=='S':
                ax+=tmp_step
            elif direction[i]=='E':
                ay+=tmp_step
            elif direction[i]=='W':
                ay-=tmp_step
            step-=tmp_step
        
        self.map.agent_pos=(ax,ay)
        self.map.board[ax][ay]=str(self.map.board[ax][ay])+AGENT
        log=f'Agent teleports to x={ax} y={ay}\n'
        return log
    def play(self):
        log=self.map.init_agent()
        print('START GAME\n'+log,end='')
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
            self.get_hint()
            action_choice_1=random.randint(0,len(self.action_list)-1)
            # action_choice=1
            while True:
                action_choice_2=random.randint(0,len(self.action_list)-1)
                if action_choice_2!=action_choice_1: break
            if self.pirate:
                direction=self.pirate_move()
                if not self.teleport:
                    log+=self.teleport_agent(direction)
                    self.teleport=True
                log+=self.action(action_choice_1,direction)
                log+=self.action(action_choice_2,direction)
            else:
                log+=self.action(action_choice_1)
                log+=self.action(action_choice_2)
            self.map.visualize()
            print()
            print('LOG\n'+log)
            input('Press Enter to continue')
        print('GAME RESULT:',self.result)

        

   
cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory
print("Files in %r: %s" % (cwd, files))      
t=Game()
t.input('map32.txt')
t.play()