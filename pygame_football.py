import pygame
import sys
pygame.init()
WIDTH,HEIGHT= 800,600
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Bresenham algorithm")
WHITE=(255,255,255)
BLACK=(0,0,0)


def bresenham(x1,y1,x2,y2):
    dx=x2-x1
    dy=y2-y1
    if x2>x1:
        lx=1
    else: 
        lx=-1
    if y2>y1:
        ly=1
    else: 
        ly=-1
    x=x1
    y=y1
    if dx>dy:
        p=(2*dy)-dx
        while (x!=x2):
            if p<0:
                x=x+lx
                y=y
                p=p+(2*dy)
            else:
                x=x+lx
                y=y+ly
                p=p+(2*dy)-(2*dx)
            screen.set_at((round(x),round(y)),WHITE)
    else:
        p=2*dx-dy
        while (y!=y2):
            if p<0:
                x=x
                y=y+ly
                p=p+(2*dx)
            else:
                x=x+lx
                y=y+ly
                p=p+(2*dx)-(2*dy)
            screen.set_at((round(x),round(y)),WHITE)

def main():
    # x1=int(input("Enter x1:"))
    # y1=int(input("Enter y1:"))
    # x2=int(input("Enter x2:"))
    # y2=int(input("Enter y2:"))
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT: 
                pygame.quit()
                sys.exit()
        screen.fill(BLACK)       # Outer boundary
        # bresenham(x1,y1,x2,y2)
       # Outer boundary
        bresenham(50,100,350,100)    # Top boundary
        bresenham(50,250,350,250)    # Bottom boundary
        bresenham(50,100,50,250)     # Left boundary
        bresenham(350,100,350,250)   # Right boundary

# Center line
        bresenham(200,100,200,250)

# Left goal box
        bresenham(50,140,90,140)
        bresenham(50,210,90,210)
        bresenham(90,140,90,210)

# Right goal box
        bresenham(310,140,350,140)
        bresenham(310,210,350,210)
        bresenham(310,140,310,210)

    
        pygame.display.flip()
        
if __name__=="__main__":
    main()