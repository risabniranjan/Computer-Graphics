#midpoint ellipse drawing algorithm
import pygame
import sys
pygame.init()
WIDTH,HEIGHT= 800,600
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Midpoint Ellipse algorithm")
WHITE=(255,255,255)
BLACK=(0,0,0)

def draw_ellipse_midpoint( xc, yc,rx,ry):
    x = 0
    y = ry

    # Initial decision parameter of region 1
    p1 = (ry * ry) - (rx * rx * ry) + (0.25 * rx * rx)
    dx = 2 * ry * ry * x
    dy = 2 * rx * rx * y


    # For region 1
    while dx <= dy:
        if p1 < 0:
            x += 1
            dx = dx + (2 * ry * ry)
            p1 = p1 + dx + (ry * ry)
        else:
            x += 1
            y -= 1
            dx = dx + (2 * ry * ry)
            dy = dy - (2 * rx * rx)
            p1 = p1 + dx - dy + (ry * ry)
        screen.set_at((xc + x, yc + y), WHITE)
        screen.set_at((xc - x, yc + y), WHITE)
        screen.set_at((xc + x, yc - y), WHITE)
        screen.set_at((xc - x, yc - y), WHITE)


    # Initial decision parameter of region 2
    p2 = ((ry * ry) * ((x + 0.5) * (x + 0.5))) + ((rx * rx) * ((y - 1) * (y - 1))) - (rx * rx * ry * ry)

    # For region 2
    while y >= 0:
        if p2 > 0:
            y -= 1
            dy = dy - (2 * rx * rx)
            p2 = p2 + (rx * rx) - dy
        else:
            y -= 1
            x += 1
            dx = dx + (2 * ry * ry)
            dy = dy - (2 * rx * rx)
            p2 = p2 + dx - dy + (rx * rx)
        screen.set_at((xc + x, yc + y), WHITE)
        screen.set_at((xc - x, yc + y), WHITE)
        screen.set_at((xc + x, yc - y), WHITE)
        screen.set_at((xc - x, yc - y), WHITE)


def main():
    xc=int(input("Enter xc:"))
    yc=int(input("Enter yc:"))
    rx=int(input("Enter rx:"))
    ry=int(input("Enter ry:"))
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT: 
                pygame.quit()
                sys.exit()
        screen.fill(BLACK)

        draw_ellipse_midpoint(xc,yc,rx,ry)


        pygame.display.flip()

if __name__=="__main__":
    main()