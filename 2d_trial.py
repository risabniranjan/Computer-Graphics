import pygame
import sys
import math

pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bresenham Algorithm with Transformations")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Bresenham Line Drawing Algorithm
def bresenham(x1, y1, x2, y2):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    lx = 1 if x2 > x1 else -1
    ly = 1 if y2 > y1 else -1

    x, y = x1, y1
    screen.set_at((x, y), WHITE)

    if dx > dy:
        p = 2 * dy - dx
        while x != x2:
            x += lx
            if p < 0:
                p += 2 * dy
            else:
                y += ly
                p += 2 * dy - 2 * dx
            screen.set_at((x, y), WHITE)
    else:
        p = 2 * dx - dy
        while y != y2:
            y += ly
            if p < 0:
                p += 2 * dx
            else:
                x += lx
                p += 2 * dx - 2 * dy
            screen.set_at((x, y), WHITE)

# Translation
def translation(x1, y1, x2, y2, tx, ty):
    return x1 + tx, y1 + ty, x2 + tx, y2 + ty

# Scaling (about origin)
def scale(x1, y1, x2, y2, sx, sy):
    return int(x1 * sx), int(y1 * sy), int(x2 * sx), int(y2 * sy)

# Rotation (about origin)
def rotate(x1, y1, x2, y2, angle):
    rad = math.radians(angle)

    x_new1 = x1 * math.cos(rad) - y1 * math.sin(rad)
    y_new1 = x1 * math.sin(rad) + y1 * math.cos(rad)

    x_new2 = x2 * math.cos(rad) - y2 * math.sin(rad)
    y_new2 = x2 * math.sin(rad) + y2 * math.cos(rad)

    return round(x_new1), round(y_new1), round(x_new2), round(y_new2)

def main():
    x1 = int(input("Enter x1: "))
    y1 = int(input("Enter y1: "))
    x2 = int(input("Enter x2: "))
    y2 = int(input("Enter y2: "))

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)

        # Original line
        bresenham(x1, y1, x2, y2)

        # Translated line
        a, b, c, d = translation(x1, y1, x2, y2, 100, 50)
        bresenham(a, b, c, d)

        # Scaled line
        e, f, g, h = scale(x1, y1, x2, y2, 2, 2)
        bresenham(e, f, g, h)

        # Rotated line
        i, j, k, l = rotate(x1, y1, x2, y2, 45)
        bresenham(i, j, k, l)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
