import pygame
import sys
pygame.init()
WIDTH,HEIGHT= 800,600
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("DDA algorithm")
WHITE=(255,255,255)
BLACK=(0,0,0)



def dda_line_draw(x1,y1,x2,y2):
    dx=x2-x1
    dy=y2-y1
    if dx>dy:
        step=dx
    else: 
        step=dy
    Xinc=dx/step
    Yinc=dy/step
    x=x1
    y=y1
    for i in range(step-1):
        x=x+Xinc
        y=y+Yinc
        screen.set_at((round(x),round(y)),WHITE)


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
        
        dda_line_draw(x1,y1,x2,y2)
        pygame.display.flip()
        
if __name__=="__main__":
    main()