from hint import *
import numpy as np


# Hint 1: [0, tuple (x, y - x: row, y: col)]: A list of random tiles that doesn't contain the treasure (1 to 12).
# Hint 2: [1, 2 - 5 số từ 1 - 5]: 2-5 regions that 1 of them has the treasure.
# Hint 3: [2, 2 - 3 số từ 1 - 5]: 1-3 regions that do not contain the treasure.
# Hint 4: [3, top, bottom, left, right]: A large rectangle area that has the treasure. (< half: small; >= half: large)
# Hint 5: [4, top, bottom, left, right]: A small rectangle area that doesn't has the treasure. (< half: small; >= half: large)
# Hint 6: [5]: He tells you that you are the nearest person to the treasure (between you and the prison he is staying).
# Hint 7: [6, 0: Row/ 1: Column, x]: A column and/or a row that contain the treasure (rare)
# Hint 8: [7, 0: Row/ 1: Column, x]: A column and/or a row that do not contain the treasure.
# Hint 9: [8, x, y]: 2 regions that the treasure is somewhere in their boundary
# Hint 10: [9]: The treasure is somewhere in a boundary of 2 regions.
# Hint 11: [10, 2/3]: The treasure is somewhere in an area bounded by 2-3 tiles from sea.
# Hint 12: [11, 1: Half right / 2: Half left / 3: Half top / 4: Half bottom]: A half of the map without treasure (rare).
# Hint 13: [12, 1: Center / 2: Prison, 1: N / 2: S / 3: W / 4: E / 5: SE / 6: SW / 7: NE / 8: NW]: From the center of the map/from the prison that he's staying, 
  # he tells you a direction that has the treasure 
  # (W, E, N, S or SE, SW, NE, NW) 
  # (The shape of area when the hints are either W, E, N or S is triangle).
# Hint 14: [13, top_big, bottom_big, left_big, right_big, top_small, bottom_small, left_small, right_small]: 
  # 2 squares that are different in size, the small one is placed inside the bigger one, the treasure is somewhere inside the gap between 2 squares. (rare)
# Hint 15: [14]: The treasure is in a region that has mountain.

def generateHint(index,Map, regions):
  hint = []
  logMsg = ""
  # index = 3
  index=index-1
  if index == 0:

    # Hint 1: [0, tuple (x, y - x: row, y: col)]: A list of random tiles that doesn't contain the treasure (1 to 12).

    hint = generateHint1(Map)

    logMsg = "These tile(s) do not contain the treasure: " + ', '.join(map(str, hint[1:]))

  elif index == 1:

    # Hint 2: [1, 2 - 5 số từ 1 - 5]: 2-5 regions that 1 of them has the treasure.

    hint = generateHint2(regions)

    logMsg = "Treasure is in one of these region(s): " + ', '.join(map(str, hint[1:]))

  elif index == 2:

    # Hint 3: [2, 2 - 3 số từ 1 - 5]: 1-3 regions that do not contain the treasure.

    hint = generateHint3(regions)

    logMsg = "These region(s) do not contain the treasure: " + ', '.join(map(str, hint[1:]))

  elif index == 3:

    # Hint 4: [3, top, bottom, left, right]: A large rectangle area that has the treasure. (< half: small; >= half: large)

    hint = generateHint4(Map)

    logMsg = "This area contains the treasure: From row "+str(hint[1])+" to row "+str(hint[2])+", from column "+str(hint[3])+" to column "+str(hint[4])
      
  elif index == 4:

    # Hint 5: [4, top, bottom, left, right]: A small rectangle area that doesn't has the treasure. (< half: small; >= half: large)

    hint = generateHint5(Map)

    logMsg = "This area does not contain the treasure: From row "+str(hint[1])+" to row "+str(hint[2])+", from column "+str(hint[3])+" to column "+str(hint[4])

  elif index == 5:

    # Hint 6: [5]: He tells you that you are the nearest person to the treasure (between you and the prison he is staying).

    hint = generateHint6()

    logMsg = "You are the nearest person to the treasure (between you and the prison the pirate is staying)"

  elif index == 6:

    # Hint 7: [6, 0: Row/ 1: Column, x]: A column and/or a row that contain the treasure (rare)

    hint = generateHint7(Map)

    if (hint[1] == 0): logMsg = "Row "
    else: logMsg = "Column "

    logMsg += str(hint[2]) + " contains the treasure"

  elif index == 7:

    # Hint 8: [7, 0: Row/ 1: Column, x]: A column and/or a row that do not contain the treasure.

    hint = generateHint8(len(Map))

    if (hint[1] == 0): logMsg = "Row "
    else: logMsg = "Column "

    logMsg += str(hint[2]) + " does not contain the treasure"

  elif index == 8:

    # Hint 9: [8, x, y]: 2 regions that the treasure is somewhere in their boundary

    hint = generateHint9(Map)

    logMsg += "Treasure is somewhere in these two regions' boudaries: Region " + str(hint[1]) + " and region " + str(hint[2])

  elif index == 9:

    # Hint 10: [9]: The treasure is somewhere in a boundary of 2 regions.

    hint = generateHint10()

    logMsg += "The treasure is somewhere in a boundary of 2 regions"

  elif index == 10:

    # Hint 11: [10, 2/3]: The treasure is somewhere in an area bounded by 2-3 tiles from sea.

    hint = generateHint11()

    logMsg += "The treasure is somewhere in an area bounded by 2-3 tiles from sea"

  elif index == 11:
    
    # Hint 12: [11, 1: Half right / 2: Half left / 3: Half top / 4: Half bottom]: A half of the map without treasure (rare)

    hint = generateHint12()

    if hint[1] == 1:
      logMsg = "A half right"
    elif hint[1] == 2:
      logMsg = "A half left"
    elif hint[1] == 3:
      logMsg = "A half top"
    else:
      logMsg = "A half bottom"

    logMsg += " of the map does not have treasure"

  elif index == 12:

    # Hint 13: [12, 1: Center / 2: Prison, 1: N / 2: S / 3: W / 4: E / 5: SE / 6: SW / 7: NE / 8: NW]: From the center of the map/from the prison that he's staying, 
      # he tells you a direction that has the treasure 
      # (W, E, N, S or SE, SW, NE, NW) 
      # (The shape of area when the hints are either W, E, N or S is triangle).

    hint = generateHint13()

    direction =""
    starting_point =""

    if hint[1] == 1: starting_point = "center of the map"
    else: starting_point = "prison where the pirate's staying"

    if hint[2] == 1: direction = "North"
    elif hint[2] == 2: direction = "South"
    elif hint[2] == 3: direction = "West"
    elif hint[2] == 4: direction = "East"
    elif hint[2] == 5: direction = "South East"
    elif hint[2] == 6: direction = "South West"
    elif hint[2] == 7: direction = "North East"
    else: direction = "North West"

    logMsg += "From the "+starting_point+", the treasure is in the " + direction+ " direction"

  elif index == 13:

    # Hint 14: [13, top_big, bottom_big, left_big, right_big, top_small, bottom_small, left_small, right_small]: 
      # 2 squares that are different in size, the small one is placed inside the bigger one, the treasure is somewhere inside the gap between 2 squares. (rare)

    hint = generateHint14(mapSize=len(Map))

    logMsg = "the treasure is somewhere inside the gap between 2 squares:\n\t"
    logMsg += "The bigger square bounded by row "+str(hint[1])+" on top; row " +str(hint[2])+" at the bottom; "
    logMsg += "column "+str(hint[3])+" on the left and column "+str(hint[4])+ " on the right\n\t"
    logMsg += "The smaller square bounded by row "+str(hint[5])+" on top; row " +str(hint[6])+" at the bottom; "
    logMsg += "column "+str(hint[7])+" on the left and column "+str(hint[8])+ " on the right\n\t"

  elif index == 14:
    # Hint 15: [14]: The treasure is in a region that has mountain.
    hint = [14]
    logMsg = "The treasure is in a region that has mountain."

  else:
    pass

  return hint, logMsg

  
