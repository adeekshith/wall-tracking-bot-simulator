# searchbot.py

# by Kerstin Voigt, Sept 2014; inspired by Nils Nilsson, Introduction to
# Artificial Intelligence: A New Synthesis

# robot has to traverse a space of obstacles; which path should it take?


from graphics import *
import random

# global vars
WORLD_MAX_X = 500
WORLD_MAX_Y = 500
GRID = 20
WALL = {}
LINKS = {}
MYBOT = None
GOAL = None

# a piece of wall (one square)

class Wall:
    def __init__(self):
        global WALL
        prompt = Text(Point(8*GRID, WORLD_MAX_Y - 2*GRID),\
                      "Click one square per click, twice for the last")
        prompt.draw(win)
        prompt_on = True

        click = win.getMouse()
        click1x = click.x - click.x % GRID
        click1y = click.y - click.y % GRID

        while True:
            if prompt_on:
                prompt_on = False
                prompt.undraw()

            WALL[(click1x,click1y)] = Rectangle(Point(click1x,click1y),\
                                                Point(click1x + GRID,\
                                                      click1y + GRID))
            WALL[(click1x,click1y)].setFill("black")
            WALL[(click1x,click1y)].draw(win)

            click = win.getMouse()
            click2x = click.x - click.x % GRID
            click2y = click.y - click.y % GRID

            if (click1x,click1y) == (click2x,click2y):
                break
    
            click1x = click2x
            click1y = click2y

    def draw(self):
        for loc in WALL.keys():
            WALL[loc].draw(win)

    def undraw(self):
        for loc in WALL.keys():
            WALL[loc].undraw()
            

class Net:
    def __init__(self):
        #global LINKS
        prompt = Text(Point(8*GRID, WORLD_MAX_Y - 2*GRID),\
                      "Click from and to squares of link, same square 2x to quit")
        prompt.draw(win)
        prompt_on = True

        self.thelinks = {}
        # loop quits when same square is clicked twice
        while True:
            # two next points
            click  = win.getMouse()
            firstx = click.x - click.x % GRID
            firsty = click.y - click.y % GRID
            click  = win.getMouse()
            secondx = click.x - click.x % GRID
            secondy = click.y - click.y % GRID
            
            if prompt_on:
                prompt_on = False
                prompt.undraw()

            # double click, quite
            if (firstx,firsty) == (secondx,secondy):
                break
            # cannot have wall
            if WALL.has_key((firstx,firsty)) or WALL.has_key((secondx,secondy)):
                continue
            # cannot move into bot
            if (secondx,secondy) == MYBOT.location:
                continue
            # links must be horizontal  or vertical
            if not horizontal((firstx,firsty),(secondx,secondy)) and\
               not vertical((firstx,firsty),(secondx,secondy)):
                continue

            # beginning of one link must be the end of another, unless
            # it is the  bot location itself

            if self.thelinks== {}: 
                end_of_other = True
            elif is_bot((firstx, firsty)):
                end_of_other = True
            else:
                end_of_other = False
                print self.thelinks
                for ends in self.thelinks.values():
                    if (firstx,firsty) in ends:
                        end_of_other  = True
                        break
            if end_of_other == False:
                continue

            if self.thelinks.has_key((firstx,firsty)):
                self.thelinks[(firstx,firsty)].append((secondx,secondy))
            else:
                self.thelinks[(firstx,firsty)] = [(secondx,secondy)]

            #print "link %d,%d -- %d,%d added ..." %(firstx,firsty,\
            #                                      secondx,secondy)

            # draw endpoint 1
            path = Rectangle(Point(firstx,firsty),\
                                    Point(firstx + GRID, firsty + GRID))
            if not is_bot((firstx,firsty)) and\
               not is_goal((firstx,firsty)):
                path.setFill("green")
            else:
                path.setOutline("green")
            path.draw(win)

            # draw endpoint 2
            path = Rectangle(Point(secondx,secondy),\
                                Point(secondx + GRID, secondy + GRID))
            if not is_bot((secondx,secondy)) and\
               not is_goal((secondx,secondy)):
                path.setFill("green")
            else:
                path.setOutline("green")
            path.draw(win)
                
            # draw between end 1 and end 2, with arrow markers
            if horizontal((firstx,firsty),(secondx,secondy)):
                horiz_dir_path((firstx,firsty),(secondx,secondy))
            else:   
                vertic_dir_path((firstx,firsty),(secondx,secondy))
                
    def list_links(self, k, start):
        print"\n\n"
        for i in range(k):
            print "_",
        print "(%d,%d)" % (start[0], start[1])
        if self.thelinks.has_key((start[0],start[1])):
            for lnk in self.thelinks[(start[0],start[1])]:
                self.list_links(k+1, lnk)
        else:
            return
    
        
def horiz_dir_path(xy1, xy2):
    if left2right(xy1,xy2):
        firstx = xy1[0]
        firsty = xy1[1]
        secondx = xy2[0]
        secondy = xy2[1]
        orient = "l2r"
    else:
        firstx = xy2[0]
        firsty = xy2[1]
        secondx = xy1[0]
        secondy = xy1[1]
        orient = "r2l"

    nextx = firstx + GRID
    nexty = firsty
    while nextx <= secondx - GRID:
        path = Rectangle(Point(nextx,nexty),\
                         Point(nextx + GRID, nexty + GRID))
        path.setFill("green")
        path.draw(win)
        arrow = Arrow(path.p1, "horiz", orient)
        arrow.draw()
        nextx = nextx + GRID

def vertic_dir_path(xy1,xy2):
    if top2bot(xy1,xy2):
        print "top to bottom ..."
        firstx = xy1[0]
        firsty = xy1[1]
        secondx = xy2[0]
        secondy = xy2[1]
        orient = "t2b"
    else:
        print "bottom to top ..."
        firstx = xy2[0]
        firsty = xy2[1]
        secondx = xy1[0]
        secondy = xy1[1]
        orient = "b2t"

    nextx = firstx
    nexty = firsty+GRID
    while nexty <= secondy - GRID:
        path = Rectangle(Point(nextx,nexty),\
                         Point(nextx + GRID, nexty + GRID))
        path.setFill("green")
        path.draw(win)
        arrow = Arrow(path.p1, "vertic",orient)
        arrow.draw()
        nexty = nexty + GRID

        
class Arrow:
    def __init__(self, anc, dir = "horiz", orient = "l2r"):
        self.anchor = anc
        if dir == "horiz":
            self.line = Line(Point(anc.x, anc.y + GRID/2),\
                                   Point(anc.x + GRID, anc.y + GRID/2))
            if orient == "l2r":
                self.line.setArrow("last")
            else:
                self.line.setArrow("first")
        else:
            # vertical
            self.line = Line(Point(anc.x + GRID/2, anc.y),\
                            Point(anc.x + GRID/2, anc.y + GRID))
            if orient == "t2b":
                self.line.setArrow("last")
            else:
                self.line.setArrow("first")
        
    def draw(self):
        self.line.draw(win)

    def undraw(self):
        self.line.undraw()
        


    

def horizontal(tup1,tup2):
    return tup1[1] == tup2[1]

def vertical(tup1,tup2):
    return tup1[0] == tup2[0]

def left2right(tup1,tup2):
    return horizontal(tup1,tup2) and\
           tup1[0] <= tup2[0]


def right2left(tup1,tup2):
    return horizontal(tup1,tup2) and\
           tup1[0] > tup2[0]

def top2bot(tup1,tup2):
    return vertical(tup1,tup2) and\
           tup1[1] <= tup2[1]

def bot2top(tup1,tup2):
    return vertical(tup1,tup2) and\
           tup1[1] > tup2[1]



def is_goal(tup):
    return tup[0] == GOAL.p1.x and tup[1] == GOAL.p1.y

def is_bot(tup):
    return tup[0] == MYBOT.location.x and tup[1] == MYBOT.location.y


        

# the dotbot robot ...   
class DotBot:
    def __init__(self,loc = Point(5*GRID,5*GRID), col="red", pwr = 100):
        self.location = loc
        self.color = col
        self.the_dotbot = Oval(self.location,\
                               Point(self.location.x + GRID, self.location.y + GRID))
        self.the_dotbot.setFill(self.color)
        self.power = pwr
                               
    def __str__(self):
        return "%s dotbot at (%d,%d) with power %d" % (self.color,\
                                             self.location.x,\
                                             self.location.y,self.power)

    def update_dotbot(self):
        self.the_dotbot.move(self.location.x - self.the_dotbot.p1.x,\
                             self.location.y - self.the_dotbot.p1.y)
        
    def draw(self):
        self.update_dotbot()
        self.the_dotbot.draw(win)

    def undraw(self):
        self.the_dotbot.undraw()

    def go(self,where):
        if where == 1:
            self.move_up()
        elif where == 2:
            self.move_down()
        elif where == 3:
            self.move_left()
        elif where == 4:
            self.move_right()
        else:
            pass
        self.undraw()
        self.draw()
            
    def move_up(self):
        newloc = Point(self.location.x, self.location.y - GRID)
        if self.location.y >= GRID:
            self.location = newloc
      
    def move_down(self):
        newloc = Point(self.location.x, self.location.y + GRID)
        if self.location.y <= WORLD_MAX_Y - GRID:
            self.location = newloc
            
    def move_left(self):
        newloc = Point(self.location.x - GRID, self.location.y)        
        if self.location.x >= GRID:
            self.location = newloc

    def move_right(self):
        newloc = Point(self.location.x + GRID, self.location.y)
        if self.location.x <= WORLD_MAX_X - GRID:
            self.location = newloc



def traverse_net(start,net,mode="bfs"):
    open_lst = [start]
    closed_lst = []

    count = 1
    while open_lst != []:
        next = open_lst[0]
        open_lst = open_lst[1:]
        closed_lst.append(next)
        print "[step-%d] _%s_" % (count, next)
        if net.has_key(next):
            open_lst.extend(net[next])
        print "[open-%d] %s" % (count, open_lst)
        count += 1
        
  # this could be a main function but doesn't have to be ...
# these lines will be executed as part of loading this file ...

win = GraphWin("Dotbot World", WORLD_MAX_X, WORLD_MAX_Y)

for i in range(GRID,WORLD_MAX_Y,GRID):
    hline = Line(Point(0,i),Point(WORLD_MAX_X,i))
    hline.draw(win)
    vline = Line(Point(i,0),Point(i,WORLD_MAX_Y))
    vline.draw(win)

MYBOT = DotBot(Point(GRID,GRID))
MYBOT.draw()

GOAL = Rectangle(Point(WORLD_MAX_X - 2*GRID, WORLD_MAX_Y - 2*GRID),\
                 Point(WORLD_MAX_X - GRID, WORLD_MAX_Y - GRID))
GOAL.setFill("blue")
GOAL.draw(win)

mywall = Wall()
MYNET = Net()

start = Text(Point(8*GRID, WORLD_MAX_Y-2*GRID), "How will the dotbot reach the blue square?")
start.draw(win)

MYNET.list_links(0,(MYBOT.location.x, MYBOT.location.y))

traverse_net((MYBOT.location.x, MYBOT.location.y),MYNET.thelinks)

win.getMouse()
win.getMouse()



win.cl
    

    
            
