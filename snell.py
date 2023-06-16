from sympy.solvers import solve
from sympy import Symbol
from math import atan, pi
import matplotlib.pyplot as plt

x = Symbol('x')
#Hs = Symbol('Hs')
#Hw = Symbol('Hw')
#l = Symbol('l')
Vs, Vw = 8.8, 2.9

Ds = 30
Dw = 150
l = 0

def find_T(x,Hs,Hw,l):
	return (((Hs**2)+(x**2))**0.5)/Vs + (((Hw**2)+((l-x)**2))**0.5)/Vw


def calculate(l,Hs,Hw,Vs,Vw):
	V = Vw/Vs
	S = solve((x**4)*(1-V**2) - 2*l*(x**3)*(1-V**2) + (x**2)*(Hs**2-(V**2)*(Hw**2)+(l**2)*(1-V**2)) - 2*l*(Hs**2)*x + (Hs**2)*(l**2), x)
	#print(l,S)
	best_T = 9e18
	best_x = 0
	for s in S:
		try:
			float(s)
			if s >= 0:
				candidate_T = find_T(s,Hs,Hw,l)
				if candidate_T < best_T:
					best_T = candidate_T
					best_x = s
		except: pass

	if best_T != 9e18:
		X = best_x
		T = best_T

		theta_s = atan(X/Hs)*180/pi
		theta_w = atan((l-X)/Hw)*180/pi

		#T = (((Hs**2)+(X**2))**0.5)/Vs + (((Hw**2)+((l-X)**2))**0.5)/Vw

		y = (Hs*l)/(Hs+Hw)
		#T_prime = (((Hs**2)+(y**2))**0.5)/Vs + (((Hw**2)+((l-y)**2))**0.5)/Vw
		T_prime = find_T(y,Hs,Hw,l)

		return round(X,3), round(theta_s,3), round(theta_w,3), round(T,3), round(T_prime,3)
	return None, None, None, None, None


#print(calculate(l,Hs,Hw,Vs,Vw))

ind = []
dep1 = []
dep2 = []

#print(
#find_T(59.41635475,Ds,Dw,5))

for l in range(0,160,5):
	#print(l,end=' ')
	_x, _theta_s, _theta_w, t, t_prime = calculate(l,Ds,Dw,Vs,Vw)
	if _x != None:
		ind.append(l)
		dep1.append(t)
		dep2.append(t_prime)
		#print(l,_x,t,t_prime)
	else: print(l)
	#print(ind,dep1,dep2)

#plt.plot(ind,dep1,label='$T_{Optimal}$')
#plt.plot(ind,dep2,label='$T_{Straight}$')

dep3 = []
for i in range(len(dep1)):
	dep3.append(dep2[i]-dep1[i])
plt.plot(ind,dep3,label='Difference Between Times for Optimal Path and Straight-Line Path')

#plt.title('Times for Optimal Path and Straight-Line Path\n$_{Ds = 30 ft , Dw = 150 ft}$')
plt.title('Difference Between Times for Optimal Path and Straight-Line Path\n$_{Ds = 30 ft , Dw = 150 ft}$')
plt.ylabel('∆T (s)')
plt.xlabel('Horizontal Distance ($l$) in ft')
#plt.legend()

plt.show()
plt.clf()
plt.close()
