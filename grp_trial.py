import pygame

# ---------------- INIT ----------------
pygame.init()

# ---------------- WINDOW ----------------
W, H = 800, 500
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Sprite Animation Engine")
clock = pygame.time.Clock()

# ---------------- LOAD SPRITE SHEET ----------------
sheet = pygame.image.load("sprite_sheet.png").convert_alpha()
print("Sheet size:", sheet.get_width(), sheet.get_height())

# ---------------- FRAME SETTINGS ----------------
FRAME_W = 60  # width of one frame
FRAME_H = 45  # height of one frame
SCALE = 2     # 2x bigger on screen

# ---------------- FUNCTION TO EXTRACT FRAMES ----------------
def get_frames(row, count):
    frames = []
    sheet_w, sheet_h = sheet.get_size()
    for i in range(count):
        x = i * FRAME_W
        y = row * FRAME_H
        if x + FRAME_W > sheet_w or y + FRAME_H > sheet_h:
            print(f"Skipping frame: row {row}, index {i}")
            continue
        rect = pygame.Rect(x, y, FRAME_W, FRAME_H)
        frames.append(sheet.subsurface(rect))
    return frames

# ---------------- ANIMATIONS ----------------
# Only 1 row exists in your sheet, so all states use the same row
animations = {
    "idle": get_frames(row=0, count=10),  # first frame shows when idle
    "walk": get_frames(row=0, count=10),
    "run":  get_frames(row=0, count=10),
}

# ---------------- STATE MACHINE ----------------
state = "idle"
frame_index = 0
frame_timer = 0
frame_speed = {
    "idle": 200,  # not used (idle frozen)
    "walk": 120,
    "run": 80
}

# ---------------- POSITION ----------------
x, y = 350, 200
speed = 3

# ---------------- MAIN LOOP ----------------
running = True
while running:
    dt = clock.tick(60)

    # -------------- EVENTS ----------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # -------------- INPUT & STATE ----------------
    keys = pygame.key.get_pressed()
    moving = False

    # movement left/right
    if keys[pygame.K_LEFT]:
        x -= speed
        moving = True
    if keys[pygame.K_RIGHT]:
        x += speed
        moving = True

    # state machine
    if moving and keys[pygame.K_LSHIFT]:
        state = "run"
    elif moving:
        state = "walk"
    else:
        state = "idle"

    # -------------- ANIMATION UPDATE ----------------
    if moving:  # only animate when moving
        frame_timer += dt
        if frame_timer >= frame_speed[state]:
            frame_timer = 0
            frame_index = (frame_index + 1) % len(animations[state])
    else:
        frame_index = 0  # freeze idle at first frame

    # -------------- DRAW ----------------
    screen.fill((30, 30, 40))

    frame = animations[state][frame_index]
    frame_scaled = pygame.transform.scale(frame, (FRAME_W * SCALE, FRAME_H * SCALE))
    screen.blit(frame_scaled, (x, y))

    # debug text
    font = pygame.font.SysFont(None, 28)
    txt = font.render(f"State: {state}", True, (255,255,255))
    screen.blit(txt, (10, 10))

    pygame.display.flip()

pygame.quit()
