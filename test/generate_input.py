import os
from random import randint

def scaleDownClass(label):
    s = set(label)
    curLabel=1
    while (len(s)>0):
        curMin = min(s)
        if (min(s)!=curLabel):
            label[label==curMin]=curLabel
        curLabel = curLabel+1
        s.remove(curMin)

    return (curLabel-1, label)

def smallTestCase(file):
    classNum = randint(5,10)
    size = randint(50,1000)

    sumW, minW = 0, 1
    weight = []

    for i in range(size):
        newW = randint(1,1000)
        sumW = sumW + newW
        minW = min(minW, newW)
        weight.append(newW)

    value = list()
    for i in range(size):
        value.append(randint(1,1000))

    label = list()
    for i in range(size):
        label.append(randint(1,classNum))

    W = randint(minW, sumW)
    classNum, label = scaleDownClass(label)

    f=open(file, 'w')
    f.write('{}\n'.format(W))
    f.write('{}\n'.format(classNum))
    for item in weight:
        f.write(f"{item}, ")
    f.write("\n")
    for item in value:
        f.write(f"{item}, ")
    f.write("\n")
    for item in label:
        f.write(f"{item}, ")
    f.close()

smallTestCase(os.path.dirname(os.path.dirname(__file__))+'\\data\\input\\input_010.txt')