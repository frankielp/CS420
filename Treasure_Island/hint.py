import random
from config import *
def generateHint1(map):
  hint = [0]
  num = random.randint(1,12)

  for i in range(num):
    row_index = random.randint(0,len(map) - 1)
    col_index = random.randint(0,len(map) - 1)
    hint.append((row_index, col_index))

  return hint

def verify_hint_1 (hint: list, treasurePos):
  # Hint 1: [0, tuple (x, y - x: row, y: col)]: A list of random tiles that doesn't contain the treasure (1 to 12).
  x, y = treasurePos
  for i in range(1, len(hint)):
    if (x, y) == hint[i]:
      return False
    return True

def generateHint2(regions):
  num = random.randint(2, 5)
  hint = [1]

  for i in range(num):
    random_region = random.randint(0, len(regions))
    if (random_region in hint):
      i-=1
      continue
    hint.append(random_region)

  return hint

def verify_hint_2 (hint: list, treasure_region):
  # Hint 2: [1, 2 - 5 số từ 1 - 5]: 2-5 regions that 1 of them has the treasure.
  for i in range(1, len(hint)):
    if hint[i] == treasure_region:
      return True
  return False

def generateHint3(regions):
  num = random.randint(2, 3)
  hint = [2]

  for i in range(num):
    random_region = random.randint(0, len(regions))
    if (random_region in hint):
      i-=1
      continue
    hint.append(random_region)

  return hint

def verify_hint_3 (hint: list, treasure_region):
  # Hint 3: [2, 2 - 3 số từ 1 - 5]: 1-3 regions that do not contain the treasure.
  for i in range(1, len(hint)):
    if hint[i] == treasure_region:
      return False
  return True

def generateHint4(map):
  hint = [3]
  area = random.randint(int(len(map)/2), len(map) - 1)
  random_row = random.randint(0,len(map) - 1)
  random_col = random.randint(0,len(map) - 1)
  # print(area)
  left = random_col - area
  if (left < 0): left = 0
  right = random_col + area
  if (right >= len(map)): right = len(map) - 1
  top = random_row - area
  if (top < 0): top = 0
  bottom = random_row + area
  if (bottom >= len(map)): bottom = len(map) - 1

  return [3, top, bottom, left, right]

def verify_hint_4 (hint: list, treasurePos):
  x, y = treasurePos
  # Hint 4: [3, top x, bottom x, left y, right y]: A large rectangle area that has the treasure. (< half: small; >= half: large)
  if x - hint[1] < 0:
    return False
  if hint[2] - x < 0:
    return False
  if y - hint[3] < 0:
    return False
  if hint[4] - y < 0:
    return False
  return True

def generateHint5(map):
  no_treasure_row = random.randint(0,len(map) - 1)
  no_treasure_col = random.randint(0,len(map) - 1)

  # print([no_treasure_row, no_treasure_col])

  area = random.randint(int(len(map) / 8),int(len(map) / 6))
  # print(np.arange(0, area_expand, 1, dtype=int))
  # print(area)
  left = no_treasure_col - area
  if (left < 0): left = 0
  right = no_treasure_col + area
  if (right >= len(map)): right = len(map) - 1
  top = no_treasure_row - area
  if (top < 0): top = 0
  bottom = no_treasure_row + area
  if (bottom >= len(map)): bottom = len(map) - 1

  return [4, top, bottom, left, right]

def verify_hint_5 (hint: list, treasurePos):
  # Hint 5: [4, top, bottom, left, right]: A small rectangle area that doesn't has the treasure. (< half: small; >= half: large)
  x, y = treasurePos
  if x >= hint[1] and hint[2] >= x and y >= hint[3] and hint[4] >= y:
    return False
  return True

def generateHint6():
  return [5]

def verify_hint_6 (hint: list, treasurePos, agentPos, prisonPos):
  # Hint 6: [5]: He tells you that you are the nearest person to the treasure (between you and the prison he is staying).
  x, y = treasurePos
  agent_x, agent_y = agentPos
  prison_x, prison_y = prisonPos
  agent_dist = abs(y - agent_y) + abs(x - agent_x)
  pirate_dist = abs(x - prison_x) + abs(y - prison_y)
  if agent_dist > pirate_dist: return False
  return True

def generateHint7(map):

  choice = random.randint(0, 1)
  random_row_col = random.randint(0,len(map) - 1)
  # print(random_row_col)

  return [6, choice, random_row_col]

def verify_hint_7 (hint: list, treasurePos):
  # Hint 7: [6, 0: Row/ 1: Column, x]: A column and/or a row that contain the treasure (rare)
  x, y = treasurePos
  if hint[1] == 0:
    if hint[2] != x: return False
  else:
    if hint[2] != y: return False
  return True

# Hint 8: [7, 0: Row/ 1: Column, x]: A column and/or a row that do not contain the treasure.
def generateHint8(m: int):
    return [7, random.randint(0,1), random.randint(0,m-1)];

def verify_hint_8 (hint: list, treasurePos):
  # Hint 8: [7, 0: Row/ 1: Column, x]: A column and/or a row that do not contain the treasure.
  x, y = treasurePos
  if hint[1] == 0:
    if hint[2] == x: return False
  else:
    if hint[2] == y: return False
  return True

# Hint 9: [8, x, y]: 2 regions that the treasure is somewhere in their boundary

def generateHint9(map: list):
    boundary = set()
    m = len(map)

    xp = [-1,0,1,0]
    yp = [0,1,0,-1]

    def getRegion(region):
      if isinstance(region,str):
        s = str(region[0])
      else:
        s=str(region)
      for i in reversed(range(0, len(s))):
        if "0" <= s[i] <= "9":
          return int(s[0:i+1])

    def isInside(x: int, y: int, m: int) -> bool:
        return (0<=x<m and 0<=y<m)

    for x in range(m):
        for y in range(m):
          region1 = getRegion(map[x][y])
          if (region1==0): continue
          for i in range(4):
              xt,yt = x+xp[i], y+yp[i]
              if not isInside(xt, yt, m): continue
              region2 = getRegion(map[xt][yt])
              # print(region1, region2)
              if (region2!=0 and region2!=region1):
                boundary.add((min(region1, region2),max(region1,region2)))
    print(boundary)
    chosenBoundary = random.choice(list(boundary))
    
    # print(chosenBoundary)
    return [8, chosenBoundary[0], chosenBoundary[1]]

def verify_hint_9(hint: list, map: list, treasurePos) -> bool:
    x,y = treasurePos

    xp = [-1,0,1,0]
    yp = [0,1,0,-1]

    area1 = hint[1]
    area2 = hint[2]

    def isInside(x,y,m) -> bool:
        return (0<=x<m and 0<=y<m)

    for i in range(4):
        xt,yt = x+xp[i], y+yp[i]
        if (isInside(xt,yt,len(map)) and ((map[xt][yt]==area1 and map[x][y]==area2) or (map[xt][yt]==area2 and map[x][y]==area1))):
            return True

    return False

def isInside(x, y, m):
  return (0 <= x < m and 0 <= y < m)

# Hint 10: [9]: The treasure is somewhere in a boundary of 2 regions.
def generateHint10():
    return [9]

def verify_hint_10(map: list, treasurePos) -> bool:
    xp = [-1, 0, 1, 0]
    yp = [0, 1, 0, -1]

    x, y = treasurePos
    if isinstance(map[x][y],str):
      pos_region=int(map[x][y][0])
    else:
      pos_region=map[x][y]
    for i in range(4):
        xt = x + xp[i]
        yt = y + yp[i]
        if isinstance(map[xt][yt],str):
          region=int(map[xt][yt][0])
        else:
          region=map[xt][yt]
        if (isInside(xt,yt,len(map)) and region!=OCEAN and region!=pos_region):
            return True

    return False

# Hint 11: [10, 2/3]: The treasure is somewhere in an area bounded by 2-3 tiles from sea.
def generateHint11():
    return [10, random.randint(2,3)]

def verify_hint_11(hint: list, map: list, treasurePos):
    x,y = treasurePos
    dist = hint[1]

    xp = [-1,0,1,0]
    yp = [0,1,0,-1]

    def isInside(x, y, m):
        return (0<=x<m and 0<=y<m)

    for i in range(4):
      for d in range(1, dist):
        xt = x+xp[i]*d
        yt = y+yp[i]*d
        if isinstance(map[xt][yt],str):
          region=int(map[xt][yt][0])
        else:
          region=map[xt][yt]
        if (isInside(xt,yt,len(map)) and region==OCEAN):
            return True

    return False

# Hint 12: [11, 1: Half right / 2: Half left / 3: Half top / 4: Half bottom]: A half of the map without treasure (rare).
def generateHint12():
    return [11, random.randint(1,4)]

def verify_hint_12(hint: list, mapSize, treasurePos):
    x,y = treasurePos

    pos = hint[1]

    if (pos==1):
        return not y>=mapSize/2
    elif (pos==2):
        return not y<mapSize/2
    elif (pos==3):
        return not x<mapSize/2
    else:
        return not x>=mapSize/2

# Hint 13: [12, 1: Center / 2: Prison, 1: N / 2: S / 3: W / 4: E / 5: SE / 6: SW / 7: NE / 8: NW]:
# From the center of the map/from the prison that he's staying,
# he tells you a direction that has the treasure (W, E, N, S or SE, SW, NE, NW)
# (The shape of area when the hints are either W, E, N or S is triangle).

def generateHint13():
    return [12, random.randint(1, 2), random.randint(1, 8)]

def verify_hint_13(hint: list, mapSize, prisonPos, treasurePos) -> bool:
    treasureX,treasureY = treasurePos
    pos, direction = hint[1], hint[2]

    # if from center
    if (pos==1):
        half = mapSize//2
        # if north
        if (direction==1):
            if (treasureX>=half):
                return False
            dist = half-treasureX
            return half-dist<=treasureY<=half+dist-1
        # if south
        elif (direction==2):
            if (treasureX<half):
                return False
            dist = treasureX-half
            return half-dist<=treasureY<=half+dist-1
        # if west
        elif (direction==3):
            if (treasureY>=half):
                return False
            dist = half-treasureY
            return half-dist<=treasureX<=half+dist-1
        # if east
        elif (direction==4):
            if (treasureY<half):
                return False
            dist = treasureY-half
            return half-dist<=treasureX<=half+dist-1
        # if south east
        elif (direction==5):
            return (half<=treasureX and half<=treasureY)
        # if south west
        elif (direction==6):
            return (half<=treasureX and treasureY<half)
        # if north east
        elif (direction==7):
            return (treasureX<half and half<=treasureY)
        # if north west
        else:
            return (treasureX<half and treasureY<half)
    else:
        prisonX, prisonY = prisonPos
        # if north
        if (direction==1):
            if (treasureX>=prisonX):
                return False
            dist = prisonX-treasureX
            return prisonY-dist<=treasureY<=prisonY+dist
        # if south
        elif (direction==2):
            if (treasureX<prisonX):
                return False
            dist = treasureX-prisonX
            return prisonY-dist<=treasureY<=prisonY+dist
        # if west
        elif (direction==3):
            if (treasureY>=prisonY):
                return False
            dist = prisonY-treasureY
            return prisonX-dist<=treasureX<=prisonX+dist
        # if east
        elif (direction==4):
            if (treasureY<prisonY):
                return False
            dist = treasureY-prisonY
            return prisonX-dist<=treasureX<=prisonX+dist
        # if south east
        elif (direction==5):
            return (prisonX<=treasureX and prisonY<=treasureY)
        # if south west
        elif (direction==6):
            return (prisonX<=treasureX and treasureY<prisonY)
        # if north east
        elif (direction==7):
            return (treasureX<prisonX and prisonY<=treasureY)
        # if north west
        else:
            return (treasureX<prisonX and treasureY<prisonY)

# Hint 14: [13, top_big, bottom_big, left_big, right_big, top_small, bottom_small, left_small, right_small]: 
# 2 squares that are different in size, the small one is placed inside the bigger one, the treasure is somewhere inside the gap between 2 squares. (rare)
def generateHint14(mapSize: int):
    topBig = random.randint(0,mapSize-3)
    bottomBig = random.randint(topBig+2,mapSize-1)
    leftBig = random.randint(0,mapSize-3)
    rightBig = random.randint(leftBig+2,mapSize-1)

    # print(f'{topBig}, {leftBig}, {bottomBig}, {rightBig}')

    bigSize = min(bottomBig-topBig, rightBig-leftBig)    
    # print(f'{bigSize}')

    bottomBig = topBig+bigSize
    rightBig = leftBig+bigSize

    topSmall = random.randint(topBig+1,bottomBig-1)
    bottomSmall = random.randint(topSmall,bottomBig-1)
    leftSmall = random.randint(leftBig+1,rightBig-1)
    rightSmall = random.randint(leftSmall,rightBig-1)
    # print(f'{topSmall}, {leftSmall}, {bottomSmall}, {rightSmall}')

    smallSize = min(bottomSmall-topSmall, rightSmall-leftSmall)    
    # print(f'{smallSize}')
    
    bottomSmall = topSmall+smallSize
    rightSmall = leftSmall+smallSize
    return [13, topBig, bottomBig, leftBig, rightBig, topSmall, bottomSmall, leftSmall, rightSmall]

def verify_hint_14(hint:list, treasurePos) -> bool:
    x, y = treasurePos

    topBig, bottomBig, leftBig, rightBig = hint[1],hint[2], hint[3], hint[4]
    topSmall, bottomSmall, leftSmall, rightSmall = hint[5], hint[6], hint[7], hint[8]
    return ((topBig<=x<topSmall or bottomSmall<x<=bottomBig) and leftBig<=y<=rightBig) or (topBig<=x<=bottomBig and (leftBig<=y<leftSmall or rightSmall<y<=rightBig) )

def verify_hint_15(map: list, treasurePos) -> bool:
    x, y = treasurePos
    if len(map[x][y])>=2:
      return map[x][y][-1:] =='M'
    else: return False

