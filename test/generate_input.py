import os
from random import randint

def smallTestCase(file):
    classNum = randint(1,3)
    size = randint(10,40)

    sumW, minW = 9,10000
    weight = list()

    for i in range(size):
        newW = randint(1,10000)
        sumW = sumW + newW
        minW = min(minW, newW)
        weight.append(newW)

    value = list()
    for i in range(size):
        value.append(randint(1,10000))

    label = list()
    for i in range(size):
        label.append(randint(1,classNum))

    W = randint(minW, sumW)

    f=open(file, 'w')
    f.write('{}\n'.format(W))
    f.write('{}\n'.format(classNum))
    for item in weight:
        f.write(f"{item} ")
    f.write("\n")
    for item in value:
        f.write(f"{item} ")
    f.write("\n")
    for item in label:
        f.write(f"{item} ")
    f.close()

smallTestCase(os.path.dirname(os.path.dirname(__file__))+'\\data\\input\\input_004.txt')