import pygame
import math
import datetime

pygame.init()

W, H = 600, 600
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Analog Clock")

clock = pygame.time.Clock()

CENTER = (W // 2, H // 2)
RADIUS = 250

font = pygame.font.SysFont(None, 28)

def draw_hand(angle_deg, length, width, color):
    angle_rad = math.radians(angle_deg - 90)
    x = CENTER[0] + length * math.cos(angle_rad)
    y = CENTER[1] + length * math.sin(angle_rad)
    pygame.draw.line(screen, color, CENTER, (x, y), width)

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # background 
    screen.fill((30, 30, 40))

    # clock face 
    pygame.draw.circle(screen, (230, 230, 230), CENTER, RADIUS)
    pygame.draw.circle(screen, (20, 20, 20), CENTER, RADIUS, 4)

    # hour marks 
    for i in range(12):
        ang = math.radians(i * 30)
        x1 = CENTER[0] + (RADIUS - 20) * math.cos(ang - math.pi/2)
        y1 = CENTER[1] + (RADIUS - 20) * math.sin(ang - math.pi/2)
        x2 = CENTER[0] + (RADIUS - 5) * math.cos(ang - math.pi/2)
        y2 = CENTER[1] + (RADIUS - 5) * math.sin(ang - math.pi/2)
        pygame.draw.line(screen, (0, 0, 0), (x1, y1), (x2, y2), 4)

    # numbers 
    for i in range(1, 13):
        ang = math.radians(i * 30)
        x = CENTER[0] + (RADIUS - 45) * math.cos(ang - math.pi/2)
        y = CENTER[1] + (RADIUS - 45) * math.sin(ang - math.pi/2)
        text = font.render(str(i), True, (0, 0, 0))
        rect = text.get_rect(center=(x, y))
        screen.blit(text, rect)

    # current time
    now = datetime.datetime.now()
    h, m, s = now.hour % 12, now.minute, now.second

    # angles
    sec_angle = s * 6
    min_angle = m * 6 + s * 0.1
    hr_angle = h * 30 + m * 0.5

    # hands
    draw_hand(hr_angle, 120, 8, (0, 0, 0))
    draw_hand(min_angle, 170, 6, (0, 0, 0))
    draw_hand(sec_angle, 200, 2, (200, 0, 0))

    # center dot
    pygame.draw.circle(screen, (0, 0, 0), CENTER, 8)

    pygame.display.flip()

pygame.quit()
