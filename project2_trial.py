import pygame
import random
import math

pygame.init()

# Window size (scaled output)
WIN_W, WIN_H = 800, 600

# Low internal resolution (pixel look)
LOW_W, LOW_H = 200, 150
SCALE = 4

screen = pygame.display.set_mode((WIN_W, WIN_H))
low_surface = pygame.Surface((LOW_W, LOW_H))

clock = pygame.time.Clock()

# --- Create scanline overlay ---
scanlines = pygame.Surface((WIN_W, WIN_H), pygame.SRCALPHA)
for y in range(0, WIN_H, 2):
    pygame.draw.line(scanlines, (0, 0, 0, 60), (0, y), (WIN_W, y))

# --- Create vignette (CRT dark edges) ---
vignette = pygame.Surface((WIN_W, WIN_H), pygame.SRCALPHA)
cx, cy = WIN_W // 2, WIN_H // 2
max_dist = math.hypot(cx, cy)

for y in range(WIN_H):
    for x in range(WIN_W):
        d = math.hypot(x - cx, y - cy)
        alpha = int((d / max_dist) * 120)
        vignette.set_at((x, y), (0, 0, 0, alpha))

# Demo object
x, y = 20, 40
vx, vy = 1, 1

running = True
while running:
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Draw in low resolution ---
    low_surface.fill((10, 10, 30))

    # Move square (retro sprite)
    x += vx
    y += vy
    if x <= 0 or x >= LOW_W - 10:
        vx *= -1
    if y <= 0 or y >= LOW_H - 10:
        vy *= -1

    pygame.draw.rect(low_surface, (0, 255, 120), (x, y, 10, 10))

    # Draw some retro stars
    for i in range(40):
        sx = (i * 37) % LOW_W
        sy = (i * 53 + pygame.time.get_ticks() // 20) % LOW_H
        low_surface.set_at((sx, sy), (200, 200, 200))

    # --- Scale up with nearest neighbor (pixelated) ---
    scaled = pygame.transform.scale(low_surface, (WIN_W, WIN_H))
    screen.blit(scaled, (0, 0))

    # --- CRT flicker ---
    flicker = random.randint(0, 20)   # only positive
    flicker_surf = pygame.Surface((WIN_W, WIN_H), pygame.SRCALPHA)
    flicker_surf.fill((flicker, flicker, flicker, 0))
    screen.blit(flicker_surf, (0, 0), special_flags=pygame.BLEND_RGB_ADD)


    # --- Overlay effects ---
    screen.blit(scanlines, (0, 0))
    screen.blit(vignette, (0, 0))

    pygame.display.flip()

pygame.quit()
