import numpy as np
import random as rn
import matplotlib.pyplot as plot

def evaluate(num):
    if num % 2 == 0:
        num = num/2
        return num
    elif num % 2 == 1:
        num = 3*num+1
        return num

y = rn.randint(1,1000)
init=y
x=0
data = np.zeros((2,2),dtype=int)
i=0
data=np.append(data,[x,y])

while True:
    x=i
    new_y=evaluate(y)
    y=new_y
    data= np.append(data,[x,y])
    if y==1:
        print("Entered to 4-2-1 loop")
        break
    i+=i
plot.plot(data)
plot.title(init)
plot.show()
