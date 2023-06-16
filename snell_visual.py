import pygame
from sympy.solvers import solve # solve quartic equation for x
from sympy import Symbol # symbol class for the library to recognise x
from math import atan, pi # arctan to find the angles and pi to convert to degrees

x = Symbol('x') # horizontal distance the lifeguard must travel before entering the water
X = 0
Vs, Vw = 8.8, 2.9 # speed in sand and speed in water

Ds = 30 # distance from the lifeguard to the beach (0 <= Ds <= 30)
Dw = 150 # distance from the beach to the target (0 <= Dw <= 300)
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

	y = (Hs*l)/(Hs+Hw) # find horizontal distance to the beach if the path was straight
	if best_T != 9e18: # if there was a valid solution, best_T would be set to something other than 9e18, so if it is not 9e18, a valid solution was found
		X = best_x; T = best_T # set the optimal horizontal distance and time 

		theta_s = atan(X/Hs)*180/pi; theta_w = atan((l-X)/Hw)*180/pi # find the angles that the lifeguard enters and leaves the beach from the normal in degrees

		T_prime = find_T(y,Hs,Hw,l) # find the time to traverse the straight path

		return round(X,3), round(y,3), round(theta_s,3), round(theta_w,3), round(T,3), round(T_prime,3)
	return None, y, None, None, None, None # if best_T is still 9e18, then no valid solutions were found

color_lookup = [
    '#282c34', # background
    '#c678dd', # purple
    '#98c379', # green
    '#e06c75', # red
    '#61afef', # blue
    '#d19a66', # orange
    '#56b6c2', # teal
    '#e5c07b', # yellow
    '#abb2bf', # white
    '#20242d'] # hud


pygame.init()
# pygame.font.init()
B = 4 # horizontal pad on left
C = 4 # vertical pad
p = 6 # unit pixel size
h = 30*p + 300*p + (2*C+1)*p # 30 m sand + 150 m water + 2 m padding
w = 150*p + (2)*p # 150m + Bm left padding + 1m right padding
screen = pygame.display.set_mode((w,h))
pygame.display.set_caption(f'Ds : {Ds} , Dw : {Dw}')
pygame.event.set_blocked(pygame.MOUSEMOTION)

X, Y, _theta_s, _theta_w, T, T_prime = calculate(l,Ds,Dw,Vs,Vw)

while __name__ == '__main__':
    screen.fill(color_lookup[9])
    pygame.draw.rect(screen, color_lookup[7], (p,p,150*p,(30+C)*p))
    pygame.draw.rect(screen, color_lookup[4], (p,(30+C)*p,150*p,(300+C)*p))
    change = False


    for event in pygame.event.get():
        if event.type == pygame.QUIT: exit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]: exit()
    elif keys[pygame.K_w]: Ds += 1; change = True
    elif keys[pygame.K_s]: Ds -= 1; change = True
    elif keys[pygame.K_UP]: Dw -= 1; change = True
    elif keys[pygame.K_DOWN]: Dw += 1; change = True
    elif keys[pygame.K_LEFT]: l -= 1; change = True
    elif keys[pygame.K_RIGHT]: l += 1; change = True
    
    Ds = max(min(30,Ds),0)
    Dw = max(min(300,Dw),0)
    l = max(min(150,l),0)
    pygame.draw.circle(screen, color_lookup[0], (p*B,p*(30+C-Ds)), 10) # lifegaurd
    pygame.draw.circle(screen, color_lookup[0], (p*(B+l),p*(30+C+Dw)), 10) # target

    jp_color = color_lookup[0]
    if change:
        _x, Y, _theta_s, _theta_w, t, t_prime = calculate(l,Ds,Dw,Vs,Vw) # calculate values with the given l
        # somtimes solve does not return valid solutions for l values that should have a solution, those l values are skipped
        if _x != None: # if the distance was valid
            X = _x
            T = t
            T_prime = t_prime
        elif _x == None or not float(_x): jp_color = color_lookup[3]


    pygame.draw.circle(screen, color_lookup[0], (p*(B+X), p*(30+C)), 10) # jump point
    pygame.draw.circle(screen, color_lookup[0], (p*(B+Y), p*(30+C)), 10) # straight point

    pygame.draw.line(screen, color_lookup[0], (p*B,p*(30+C-Ds)), (p*(B+X),p*(30+C))) # lifeguard to jump point
    pygame.draw.line(screen, color_lookup[0], (p*(B+X),p*(30+C)), (p*(B+l),p*(30+C+Dw))) # jump point to target

    pygame.draw.line(screen, color_lookup[3], (p*B,p*(30+C-Ds)), (p*(B+Y),p*(30+C))) # lifeguard to straight point
    pygame.draw.line(screen, color_lookup[3], (p*(B+Y),p*(30+C)), (p*(B+l),p*(30+C+Dw))) # straight point to target

    pygame.time.delay(40)
    pygame.display.set_caption(f'Ds : {Ds} , Dw : {Dw}, l : {l}, optimal time : {T} , straight time : {T_prime} , ∆T : {round(T_prime-T,2)}')
    pygame.display.update()
