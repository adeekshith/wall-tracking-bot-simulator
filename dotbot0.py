# dotbot0.py

# by Kerstin Voigt, Sept 2014; inspired by Nils Nilsson, Introduction to
# Artificial Intelligence: A New Synthesis


from graphics import *
import random

# global vars
WORLD_MAX_X = 500
WORLD_MAX_Y = 500
GRID = 20
WALL = {}

# brick by brick wall
wallAt=[]
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
            
            print "Wall at %d,%d" % (click1x, click1y)
            wallAt.append([click1x, click1y])

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
            

initialBotLocation=[5*GRID,5*GRID]
# the dotbot robot ...   
class DotBot:
    def __init__(self,loc = Point(initialBotLocation[0],initialBotLocation[1]), col="blue", pwr = 100):
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

    def botLocation(self):
        return [self.location.x,self.location.y]

    def botNeighborhood(self):
        botSurrounding=[0,0,0,0,0] # self, top, right, bottom, left

        try:
            botSurrounding[0]=wallAt.index([self.location.x,self.location.y])
            print "Bot is on the wall"
            botSurrounding[0]=1
        except ValueError:
            botSurrounding[0]=0

        # Checking wall upwards
        if self.location.y >= GRID:
            newloc = Point(self.location.x, self.location.y - GRID)
            try:
                botSurrounding[1]=wallAt.index([newloc.x,newloc.y])
                print "Bot is on the wall"
                botSurrounding[1]=1
            except ValueError:
                botSurrounding[1]=0

        # Checking wall right
        if self.location.x <= WORLD_MAX_X - GRID:
            newloc = Point(self.location.x + GRID, self.location.y)
            try:
                botSurrounding[2]=wallAt.index([newloc.x,newloc.y])
                print "Wall to the right"
                botSurrounding[2]=1
            except ValueError:
                botSurrounding[2]=0

        # Checking wall down
        if self.location.y <= WORLD_MAX_Y - GRID:
            newloc = Point(self.location.x, self.location.y + GRID)
            try:
                botSurrounding[3]=wallAt.index([newloc.x,newloc.y])
                print "Wall at the bottom"
                botSurrounding[3]=1
            except ValueError:
                botSurrounding[3]=0

        # Checking wall left
        if self.location.x >= GRID:
            newloc = Point(self.location.x - GRID, self.location.y)        
            try:
                botSurrounding[4]=wallAt.index([newloc.x,newloc.y])
                print "Wall on the left"
                botSurrounding[4]=1
            except ValueError:
                botSurrounding[4]=0
        return botSurrounding

# this could be a main function but doesn't have to be ...
# these lines will be executed as part of loading this file ...

win = GraphWin("Dotbot World", WORLD_MAX_X, WORLD_MAX_Y)

for i in range(GRID,WORLD_MAX_Y,GRID):
    hline = Line(Point(0,i),Point(WORLD_MAX_X,i))
    hline.draw(win)
    vline = Line(Point(i,0),Point(i,WORLD_MAX_Y))
    vline.draw(win)

mybot = DotBot()
mybot.draw()

mywall = Wall()

start = Text(Point(8*GRID, WORLD_MAX_Y-2*GRID), "Click to start the action -- twice to stop")
start.draw(win)

click = win.getMouse()
clickx1 = click.x - click.x % GRID
clicky1 = click.y - click.y % GRID

print "click at %d,%d" % (clickx1, clicky1)

start.undraw()
previous_move=0
botPreviousLocation=[-1,-1]
prevAroundBot=[-1,-1,-1,-1,-1]
while True:
    #mybot.go(random.randint(1,4))
    aroundBot=mybot.botNeighborhood()
    if aroundBot[3]==1:             # Wall at bottom
        if aroundBot[2]==0:             # Continue Right
            mybot.go(4)
        else:                           
            mybot.go(1)                 # Right to top
    elif aroundBot[2]==1:           # Wall towards right
        if aroundBot[1]==0:             
            mybot.go(1)                 # Continue Top
        else:
            mybot.go(3)                 # Top to left
    elif aroundBot[4]==1:           # Wall towards left
        if aroundBot[3]==0:
            mybot.go(2)                 # Continue bottom
        else:
            mybot.go(4)                 # Bottom to right
    elif aroundBot[1]==1:
        if aroundBot[4]==0:         # Wall at top
            mybot.go(3)                 # Continue left
        else:
            mybot.go(2)                 # Left to bottom
    elif prevAroundBot[3]==1:
        if prevAroundBot[2]==0:
            mybot.go(2)                 # Right to bottom
        else:
            mybot.go(4)
    elif prevAroundBot[2]==1:
        if prevAroundBot[1]==0:
            mybot.go(4)                 # Top to Right
        else:
            mybot.go(1)
    elif prevAroundBot[4]==1:
        if prevAroundBot[3]==0:
            mybot.go(3)                 # Bottom to left
        else:
            mybot.go(2)
    elif prevAroundBot[1]==1:
        if prevAroundBot[4]==0:
            mybot.go(1)                 # Left to top
        else:
            mybot.go(3)
    else:
        botLocationNow=mybot.botLocation()
        if previous_move==0:
            if botLocationNow!=botPreviousLocation:
                mybot.go(3)
            else:
                previous_move=1
                mybot.go(previous_move)
        elif previous_move==1 or previous_move==5:
            if botLocationNow!=botPreviousLocation:
                mybot.go(1)
            else:
                previous_move=4
                mybot.go(previous_move)
        elif previous_move==4:
            previous_move=2
            mybot.go(previous_move)
        elif previous_move==2:
            if botLocationNow!=botPreviousLocation:
                mybot.go(previous_move)
            else:
                previous_move=5
                mybot.go(4)

        botPreviousLocation=botLocationNow
        print "Searching for wall!! O_O"
    
    print "bot is at: "+str(mybot.botLocation())

    #mybot.go(1)

    click = win.getMouse()
    clickx2 = click.x - click.x % GRID
    clicky2 = click.y - click.y % GRID

    print "click at %d,%d" % (clickx2, clicky2)

    if clickx1 == clickx2 and clicky1 == clicky2:
        #clicked same square twice --> quit
        enough = Text(Point(clickx1, clicky1), "Enough of that!")
        enough.draw(win)
        break

    print "bot moved ..."

    clickx1 = clickx2
    clicky1 = clicky2
    prevAroundBot=aroundBot

win.getMouse()
win.getMouse()
win.close()
