from sympy.solvers import solve # solve quartic equation for x
from sympy import Symbol # symbol class for the library to recognise x
from math import atan, pi # arctan to find the angles and pi to convert to degrees
import matplotlib.pyplot as plt

x = Symbol('x') # horizontal distance the lifeguard must travel before entering the water
Vs, Vw = 2.7, 0.9 # speed in sand and speed in water (m/s)

Ds = 10 # distance (m) from the lifeguard to the beach (0 <= Ds <= 10)
Dw = 0 # distance (m) from the beach to the target (0 <= Dw <= 500)
l = 0 # total horizontal distance (m) between the lifeguard and target (0 <= l <= 150)

def find_T(x,Hs,Hw,l): # find the time required to traverse a given path specified by x, Hs, Hw, and l
	return (((Hs**2)+(x**2))**0.5)/Vs + (((Hw**2)+((l-x)**2))**0.5)/Vw

def calculate(l,Hs,Hw,Vs,Vw): # with given values, find x, the angles of refraction, time to traverse the refracted path, and time to traverse the straight path
	V = Vw/Vs # the ratio between the speeds occurs often within the quartic equation for x, so it is calculated once separately
	# use sympy.solvers to solve the quartic equation for x
	S = solve((x**4)*(1-V**2) - 2*l*(x**3)*(1-V**2) + (x**2)*(Hs**2-(V**2)*(Hw**2)+(l**2)*(1-V**2)) - 2*l*(Hs**2)*x + (Hs**2)*(l**2), x)
	# solve can yield multiple real positive solutions so a candidate test is needed
	best_T = 9e18 # set a ludicrously high best time so that it is guaranteed to be reduced
	best_x = 0 # set a throwaway best x candidate
	for s in S: # for each candidate solution s in the list of solutions ...
		try:
			float(s)
			if s >= 0: # check if s is a real positive number
				candidate_T = find_T(s,Hs,Hw,l) # find the time using the candidate s
				if candidate_T < best_T: # set the best time and best x if the candidate s yields a faster time than the current best
					best_T = candidate_T
					best_x = s
		except: pass

	y = (Hs*l)/(Hs+Hw)
	if best_T != 9e18: # if there was a valid solution, best_T would be set to something other than 9e18, so if it is not 9e18, a valid solution was found
		try:
			X = best_x; T = best_T; theta_s = atan(X/Hs)*180/pi; theta_w = atan((l-X)/Hw)*180/pi # find the angles that the lifeguard enters and leaves the beach from the normal in degrees
			T_prime = find_T(y,Hs,Hw,l) # find the time to traverse the straight path
			return round(X,3), round(theta_s,3), round(theta_w,3), round(T,3), round(T_prime,3)
		except: pass

	return None, None, None, None, None # if best_T is still 9e18, then no valid solutions were found

ind = []
dep1 = []
dep2 = []

dwr = 250
lr = 150

h = [0 for _ in range(0,lr+5,5)]
heatmap = [h]

from random import randint

for Dw in range(5,dwr+5,5): # loop through various total horizontal distances
	heatmap.append([0])
	for l in range(5,lr+5,5):
		_x, _theta_s, _theta_w, t, t_prime = calculate(l,Ds,Dw,Vs,Vw) # calculate values with the given l
		if _x != None and t != None and t_prime != None: # if the distance was valid
			delta = round(float(t_prime-t),3)
			print(delta)
			heatmap[-1].append(delta)
		else:
			heatmap[-1].append(0)

print()

# choose whether to display both the optimal and straight paths (comparison) or just their difference (delta)
display = 'delta' # comparison or delta

# set up the plot for the given setting
if display == 'comparison': 
    plt.ylabel('Time (s)')
    plt.title('Times for Optimal Path and Straight-Line Path\n$d_{s}$ = {0} ft , Dw = {Dw} ft',fontsize=40)
    plt.plot(ind,dep1,label='$T_{Optimal}$')
    plt.plot(ind,dep2,label='$T_{Straight}$')
elif display == 'delta':
	plt.title('Difference Between T and Tʼ\n$d_{s}$ = 10 m',fontsize=30)
	import seaborn as sns
	print(len(heatmap))
	print(len(heatmap[0]))
	print(len(heatmap[-1]))
	sns.set_context("paper", font_scale=2.5)
	ax = sns.heatmap(heatmap,square=True,cbar_kws={'label':'∆T (s)','ticks':[i for i in range(0,60,5)],'shrink':1}) 
	ax.set_xlabel('$l$ (m)',fontsize=30)
	ax.set_ylabel('$d_{w}$ (m)',fontsize=30)
	ax.set_xticks([4*i+1 for i in range((lr+20)//20)])
	ax.set_yticks([4*i+1 for i in range((dwr+20)//20)])
	ax.set_xticklabels([i for i in range(0,lr+10,20)],fontsize=20)
	ax.set_yticklabels([i for i in range(0,dwr+10,20)],fontsize=20)
	ax.xaxis.tick_top()

plt.show()
plt.clf()
plt.close()
