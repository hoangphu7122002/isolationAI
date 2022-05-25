#STATE:
FREE = 0
BLOCK = 2
ACTIVE_P1 = 1 #component
ACTIVE_P2 = -1 #component
ACTIVE = {1 : ACTIVE_P1, -1 : ACTIVE_P2}

#cell neighbor position
dx = [-1,0,1,1,1,0,-1,-1]
dy = [1,1,1,0,-1,-1,-1,0]

#hyper_parameter
WIDTH = 6

#left_direction
L_DIRECTION = [(-1,0),(-1,1),(-1,-1)]
R_DIRECTION = [(1,0),(1,1),(1,-1)]
U_DIRECTION = [(-1,1),(0,1),(1,1)]
D_DIRECTION = [(-1,-1),(0,-1),(1,-1)]

DIRECTION = {
    "left" : L_DIRECTION,
    "right" : R_DIRECTION,
    "up" : U_DIRECTION,
    "down" : D_DIRECTION
}

DIRECTION_LABEL = ["left","right","up","down"]

#color for display GUI python
blue = (104, 149, 197)
black = (0, 0, 0)
white = (255,255,255)
red = (255,69,0)
yellow = (255,255,0)
blue_second = (130,202,250)
red_first = (244,41,65)