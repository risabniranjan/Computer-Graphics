x1=int(input("enter x1"))
x2=int(input("enter x2"))
y1=int(input("enter y1"))
y2=int(input("enter y2"))
def dda_line_draw(x1,y1,x2,y2):
    dx= x2-x1
    dy= y2-y2
    if dx>dy:
        step=dx
    else:
        step=dy    
    xinc=dx/step
    yinc=dy/step
    x=x1
    y=y1
    for i in range(step-1):
        x=x+xinc
        y=y+yinc
        print("(",x,y,")")
dda_line_draw( x1,x2,y1,y2)
