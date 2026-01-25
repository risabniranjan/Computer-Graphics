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

def translation(x1, y1,x2,y2, tx, ty):
    x_new1 = x1 + tx
    y_new1 = y1 + ty
    x_new2 = x2 + tx
    y_new2 = y2 + ty
    return x_new1, y_new1, x_new2, y_new2

def scale(x1, y1, x2, y2, sx, sy):
    x_new1 = x1 * sx
    y_new1 = y1 * sy
    x_new2 = x2 * sx
    y_new2 = y2 * sy
    return x_new1, y_new1, x_new2, y_new2

def rotate(x1, y1, x2, y2, angle):
    import math
    angle_rad = math.radians(angle)
    x_new1 = x1 * math.cos(angle_rad) - y1 * math.sin(angle_rad)
    y_new1 = x1 * math.sin(angle_rad) + y1 * math.cos(angle_rad)
    x_new2 = x2 * math.cos(angle_rad) - y2 * math.sin(angle_rad)
    y_new2 = x2 * math.sin(angle_rad) + y2 * math.cos(angle_rad)
    return round(x_new1), round(y_new1), round(x_new2), round(y_new2)

def main():
    x1=int(input("Enter x1:"))
    y1=int(input("Enter y1:"))
    x2=int(input("Enter x2:"))
    y2=int(input("Enter y2:"))
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT: 
                pygame.quit()
                sys.exit()
        screen.fill(BLACK)       
        bresenham(x1,y1,x2,y2)
        a,b,c,d = translation(x1, y1, x2, y2, 100, 50)
        bresenham(a,b,c,d)
        e,f,g,h = scale(x1, y1, x2, y2, 2, 2)
        bresenham(e,f,g,h)
        i,j,k,l = rotate(x1, y1, x2, y2, 45)
        bresenham(i,j,k,l)
        


        pygame.display.flip()
        
if __name__=="__main__":
    main()