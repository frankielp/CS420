from generate_map import *
from processing_hint import *
from hint import *
from config import *
from map import *
import sys
import os 

class Game():
    def __init__(self):
        self.testcase=None
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
        self.log=''
        self.view=True

    def input(self,filename):
        self.testcase=int(filename[-6:-4])
        self.map.input(filename)
        with open(filename) as f:
            f.readline()
            self.reveal_prison_turn=int(f.readline().replace('\n',''))
            self.release_turn=int(f.readline().replace('\n',''))
    def get_hint(self):
        # p = 0.045 for hints that are rare
        # hint 6 and hint 13 prison shouldnt be <reveal and >=release
        if self.turn>=self.reveal_prison_turn and self.turn<self.release_turn:
            choice = np.random.choice(a=np.arange(1, 16, 1, dtype=int), p = (0.07, 0.07, 0.07, 0.07, 0.07, 0.07, (1-0.07*12)/3, 0.07, 0.07, 0.07, 0.07, (1-0.07*12)/3, 0.07, (1-0.07*12)/3, 0.07))
        else:
            choice = np.random.choice(a=np.arange(1, 16, 1, dtype=int), p = (0.07, 0.07, 0.07, 0.07, 0.07, 0, (1-0.07*12)/3+0.07, 0.07, 0.07, 0.07, 0.07, (1-0.07*12)/3+0.07, 0, (1-0.07*12)/3, 0.07))
        
        # debug
        # choice=4

        hint,log=generateHint(choice,self.map.board,self.map.region)
        self.hint.append([hint,log])
        log='Pirate give hint: '+log+'\nAdd hint to hint list\n'
        return log
    def action(self,choice,direction=None):
        action_log='\nACTION: '+self.action_list[choice].upper()+'\n'
        if self.action_list[choice]=='verification':
            hint,log=self.hint.pop(0)     
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
        px,py=self.map.pirate_pos
        self.map.board[px][py]+=PIRATE
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
                if flag: 
                    break
            veri_flag=self.map.masking(hint)
            action_log='First hint is always true\n'
            action_log+='HINT: '+log+'\n'
            action_log+='Verification: '+str(veri_flag)+'\n'
            return action_log
            
    def agent_move(self,choice,pi_direction=None):
        ax,ay=self.map.agent_pos
        self.map.board[ax][ay]=str(self.map.board[ax][ay]).replace(AGENT,'')
        if choice=='large':
            step=random.randint(4,5)
        elif choice=='small':
            step=3

        #Decide direction based on not scan
        direction=''
        direction_count={'N':0,'E':0,'W':0,'S':0}
        for i in range(self.map.h):
            for j in range(self.map.w):
                if self.map.board[i][j]!=OCEAN and not (isinstance(self.map.board[i][j],str) and MASKED in self.map.board[i][j]):
                    if i<ax: direction_count['N']+=1
                    elif i>ax: direction_count['S']+=1
                    if j<ay: direction_count['W']+=1
                    elif i>ay: direction_count['E']+=1
        direction_count=sorted(direction_count.keys(),key= lambda x:direction_count[x],reverse=True) 
        if  (str(direction_count[0])=='N' and str(direction_count[1])=='S') or (str(direction_count[1])=='N' and str(direction_count[0])=='S') or (str(direction_count[0])=='E' and str(direction_count[1])=='W') or (str(direction_count[1])=='E' and str(direction_count[0])=='W'):
            direction+=str(direction_count[0])+str(direction_count[2])
        else:
            direction+=str(direction_count[0])+str(direction_count[1])
        if self.pirate:
            direction=pi_direction
        #     common=''
        #     for w in direction:
        #         if w in pi_direction:
        #             common+=w 
        # else:
            
        print(direction)
        for i in range(len(direction)):
            if i==len(direction)-1:
                tmp_step=step
            else:
                tmp_step=step//2+1
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
        ax,ay=self.map.agent_pos
        self.map.board[ax][ay]=str(self.map.board[ax][ay]).replace(AGENT,'')
        ax,ay=self.map.pirate_pos   
        step=3
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

    def choose_action(self):
        # self.action_list=['verification','move_scan_small','move_large','scan_large']
        # agent on MASKED and move large first
        ax,ay=self.map.agent_pos
        if isinstance(self.map.board[ax][ay],str) and MASKED in self.map.board[ax][ay]:
            action_choice_1=2
        else:
            action_choice_1=random.randint(0,len(self.action_list)-1)
        while True:
            action_choice_2=random.randint(0,len(self.action_list)-1)
            # no move_scan_small -> scan large
            if action_choice_2!=action_choice_1 and (action_choice_1!=1 or action_choice_1!=3): break

        return action_choice_1,action_choice_2

    def play(self):
        log=self.map.init_agent()
        log+=f'The pirate’s prison is going to reveal the at the beginning of {self.reveal_prison_turn} turn\n'
        log+=f'The pirate is free at the beginning of the {self.release_turn}th turn\n'
        self.log+='START GAME\n'+log
        print('START GAME\n'+log,end='')
        while self.result is None:
            self.turn+=1
            log=f'\nTURN {self.turn}\n'
            print('--------------------------------------')
            print(f'TURN {self.turn}')

            # Reveal prison
            if self.turn==self.reveal_prison_turn:
                px,py=self.map.pirate_pos
                log+=f'The prison of pirate locate at x={px},y={py}\n'

            # Release
            if self.turn==self.release_turn:
                log+='Pirate has been released\n'
                self.free_pirate()
            if self.turn==1:
                log+=self.get_first_hint()
            log+=self.get_hint()

            # Choose action
            action_choice_1,action_choice_2=self.choose_action()

            # Conduct action
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

            # Visualization
            self.map.visualize()

            # Print Log
            print()
            print('LOG\n'+log)
            self.log+=log
            if self.view:
                input('Press Enter to continue')
        if self.result=='LOSE':
            log='Pirate found the treasure.\n'
            self.log+=log
            print(log)
        print('GAME RESULT:',self.result)

    def export(self,output):
        outfile=f'LOG{self.testcase}.txt'
        with open (output+outfile,'w+') as f:
            f.write(str(len(self.log.split('\n')))+'\n')
            f.write(self.result.upper()+'\n')
            f.write(self.log)

def main(input,output):   
    for filename in os.listdir(input):
        if filename[-4:]!='.txt': continue
        t=Game()
        t.input(input+filename)
        t.play()
        if not t.result is None:
            t.export(output)

if __name__=='__main__':

    if (len(sys.argv) != 3):
        print('usage:\t python game.py <input_dir> <output_dir>')
        sys.exit(0)
    main(sys.argv[1],sys.argv[2])