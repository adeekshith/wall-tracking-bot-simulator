# hop.py

# by Kerstin Voigt, Sept 2014; a dot appears on a gridded canvas;
# with each click, the dot moves to a new random position; click in
# the lower right corner will break the loop; with additional clicks,
# the graphics window closes;

# this simple program is meant as a piece of starter code to help with
# programming more "intelligent" behavior in CSE 512; e.g., this program
# can be adopted for "wumpus world" from Nils Nilsons textbook; 

# uses graphics library graphics.py by John Zelle, author of
# "Python Programming: An Introduction to Computer Science"


from graphics import *
import random

def main():
    win = GraphWin("Hop", 500, 500)

    for i in range(20,1000,20):
        hline = Line(Point(0,i),Point(500,i))
        hline.draw(win)
        vline = Line(Point(i,0),Point(i,500))
        vline.draw(win)

    dot = Oval(Point(100,100),Point(120,120))
    dot.setFill("red")
    dot.draw(win)

    max = 0
    while True:
        max += 1
        click = win.getMouse()
        if click.getX() >= 450 and click.getY() >= 450:
            break
            
        inx = random.randint(2,10) * 20
        iny = random.randint(2,10) * 20
        if random.randint(1,10) % 2 == 0:
            inx = - inx
        if random.randint(1,10) % 2 == 0:
            iny = -iny

        cent = dot.getCenter()
        cx = cent.getX()
        cy = cent.getY()
        
        while not (cx + inx >= 10 and cx + inx <= 490):
            inx = random.randint(2,10) * 20
            if random.randint(1,10) % 2 == 0:
                inx = - inx
                
        while not (cy + iny >= 10 and cy + iny <= 490):
            iny = random.randint(2,10) * 20
            if random.randint(1,10) % 2 == 0:
                iny = - iny

        dot.undraw()
        dot.move(inx,iny)
        dot.draw(win)
        
    # just click to close canvas

    Text(Point(200,100), "CLICK ANYWHERE TO QUIT ...").draw(win)
    win.getMouse()
    win.getMouse()
    win.close()

main()

    
            
