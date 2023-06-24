from sympy.solvers import solve # solve quartic equation for x
from sympy import Symbol # symbol class for the library to recognise x
from math import atan, pi # arctan to find the angles and pi to convert to degrees
import matplotlib.pyplot as plt

SMALL_SIZE = 50
MEDIUM_SIZE = 75
BIGGER_SIZE = 75

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)

x = Symbol('x') # horizontal distance the lifeguard must travel before entering the water
Vs, Vw = 2.7, 0.9 # speed in sand and speed in water

Ds = 10 # distance from the lifeguard to the beach (0 <= Ds <= 10)
Dw = 50 # distance from the beach to the target (0 <= Dw <= 500)
l = 0 # total horizontal distance between the lifeguard and target

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

	if best_T != 9e18: # if there was a valid solution, best_T would be set to something other than 9e18, so if it is not 9e18, a valid solution was found
		X = best_x; T = best_T # set the optimal horizontal distance and time 

		theta_s = atan(X/Hs)*180/pi; theta_w = atan((l-X)/Hw)*180/pi # find the angles that the lifeguard enters and leaves the beach from the normal in degrees

		y = (Hs*l)/(Hs+Hw) # find horizontal distance to the beach if the path was straight
		T_prime = find_T(y,Hs,Hw,l) # find the time to traverse the straight path

		return round(X,3), round(theta_s,3), round(theta_w,3), round(T,3), round(T_prime,3)
	return None, None, None, None, None # if best_T is still 9e18, then no valid solutions were found

ind = []
dep1 = []
dep2 = []

print('x values that could not be calculated:',end=' ')
for l in range(0,150,5): # loop through various total horizontal distances
	_x, _theta_s, _theta_w, t, t_prime = calculate(l,Ds,Dw,Vs,Vw) # calculate values with the given l
	# somtimes solve does not return valid solutions for l values that should have a solution, those l values are skipped
	if _x != None: # if the distance was valid
		ind.append(l) # append l to the list of values for the independent variable
		dep1.append(t) # append t and t_prime to the lists for the dependent variables
		dep2.append(t_prime)
	else: print(l,end=', ') # print any l values that yeiled no valid solutions
print()

# choose whether to display both the optimal and straight paths (comparison) or just their difference (delta)
display = 'delta' # comparison or delta

# set up the plot for the given setting
if display == 'comparison': 
    plt.title(f'Times for Optimal Path and Straight Path\nDs = {Ds}m, Dw = {Dw}m',fontsize=30)
    plt.ylabel('Time (s)',fontsize=20)
    plt.plot(ind,dep1,label='$T$')
    plt.plot(ind,dep2,label='$Tʼ$')
    plt.legend(fontsize=20)
elif display == 'delta':
	plt.title('Difference Between Times for Optimal Path and Straight Path\n$d_{s}$ = 10m, $d_{w}$ = 50m',fontsize=30)
	plt.ylabel('∆T (s)',fontsize=30)
	dep3 = []
	for i in range(len(dep1)): # create list of delta values
		dep3.append(dep2[i]-dep1[i])
	plt.plot(ind,dep3,label='Difference Between Times for Optimal Path and Straight Path')

plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.xlabel('$l$ (m)',fontsize=30)

plt.show()
plt.clf()
plt.close()