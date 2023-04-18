from numpy import pi


Va = 24 #Tensao de armadura
Ra = 1.45 #Resistencia de Armadura
La = 0.000454 #Indutancia de Armadura, 454u
Rf = 75 # resistencia de campo
Lf = 2 #indutancia de campo
J = 0.0015 #momento de inercia
B = 0.098 #coeficiente de atrito viscoso
Ia = 4 #corrente nominal de armadura
If = 1 #corrente nominal de campo 
Nrpm = 240 #Velocidade nominal (RPM)

#Velocidade nominal em rad/s (wm)
wm = (Nrpm*pi)/30
print('Velocidade nominal wm: ' + str(wm))

#Indutancia Mútua (armadura-campo) (Laf)
Laf = (Va-(Ia*Ra))/(If*wm)
print('Indutancia Mutua: ' + str(Laf))

#Constante KFi
KFi = Laf*If
print('Cte KFi: ' + str(KFi))

#Tensão Induzida (Ea)
Ea = KFi*wm
print('Tensao Induzida: ' + str(Ea))

#Torque Eletromagnético (Te)
Te = KFi*Ia
print('Torque Eletromagnético: ' + str(Te))

#--------------------------#
from numpy import array
#Matrizes de Entrada
A = array([[(-Ra/La), (-KFi/La)], [(KFi/J), (-B/J)]]) #Matriz A
B = array([[1/La], [0]]) #Matriz B

#Matrizes de Saída
C = array([[1, 0],  [0, 1]]) #Matriz C
D = array([[0], [0]]) #Matriz D

#--------------------#
from scipy.signal import StateSpace
from numpy.linalg import inv
from numpy import matmul
ssm = StateSpace(A, B, C, D)
#print(ssm)

X = matmul(-inv(A), B*Va) 
print('ia:' + str(X[0]))
print('RPM' + str(X[1]*(30/pi)))

#------------------#
from numpy import linspace
from numpy import full
t = linspace(0, 0.2, 4000)
f = full(4000, Va)

#------------------#
from scipy.signal import lsim
[t1, y1, x1] = lsim(ssm, f, t)

#------------------#
from matplotlib.pyplot import plot, grid, show
ia = X[0]
RPM = X[1]*(30/pi)
var1 = y1[0: 4000, 0]
var2 = (30/pi)*y1[0: 4000, 1]

plot(t, var1)
grid()
show()
plot(t, var2)
grid()
show()
