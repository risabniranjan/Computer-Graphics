
x1=int(input("Enter x1:"))
y1=int(input("Enter y1:"))
x2=int(input("Enter x2:"))
y2=int(input("Enter y2:"))

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
            print("(",x,y,")")
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
            print("(",x,y,")")

bresenham(x1,y1,x2,y2)
