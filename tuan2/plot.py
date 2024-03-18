plot.py
import matplotlib.pyplot as plt
import numpy as np
import math 

data_dir = '/home/manh/Documents/python/aco-tsp/aco-tsp/result.txt'
save_dir  = '/home/manh/Documents/python/aco-tsp/aco-tsp/result2.png'

arr = np.loadtxt(data_dir,delimiter=",")
# print(arr[0])
a =[]
b =[]
c=[]
d=[]
e=[]
f=[]
g=[]

for i in range (len(arr)):
    a.append(arr[i][0])
    b.append(arr[i][1])
    c.append(arr[i][2])
    d.append(arr[i][3])
    e.append(arr[i][4])
    f.append(arr[i][5])
    g.append(arr[i][6])

plt.figure()
m=0
n=7

plt.plot(e[16:20],g[16:20], color='green', label='evap_coeff=0.4')
plt.plot(e[20:24],g[20:24], color='blue', label='evap_coeff=0.5')
plt.plot(e[24:28],g[24:28], color='yellow', label='evap_coeff=0.6')
plt.legend()
plt.grid(True)
plt.title("Quãng đường nhỏ nhất khi thay đổi tham số vết mùi")
plt.xlabel("Số kiến (con)")
plt.ylabel("Quãng đường nhỏ nhất (m)")
# print(len(self.a),len(self.b),len(self.c),len(self.d))
plt.savefig(save_dir,dpi=500)
plt.show()