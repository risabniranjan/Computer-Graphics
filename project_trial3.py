import math
from PIL import Image

WIDTH = 400
HEIGHT = 300
MAX_DEPTH = 3

# ---------- Vector ----------
class Vec:
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z

    def __add__(self, o): return Vec(self.x+o.x, self.y+o.y, self.z+o.z)
    def __sub__(self, o): return Vec(self.x-o.x, self.y-o.y, self.z-o.z)
    def __mul__(self, k): return Vec(self.x*k, self.y*k, self.z*k)

    def dot(self, o): return self.x*o.x + self.y*o.y + self.z*o.z

    def norm(self):
        m = math.sqrt(self.dot(self))
        return self * (1/m)

    def reflect(self, n):
        return self - n * 2 * self.dot(n)


# ---------- Objects ----------
class Sphere:
    def __init__(self, center, radius, color, reflection=0.3):
        self.center = center
        self.radius = radius
        self.color = color
        self.reflection = reflection

    def intersect(self, origin, dir):
        oc = origin - self.center
        b = 2 * oc.dot(dir)
        c = oc.dot(oc) - self.radius*self.radius
        disc = b*b - 4*c
        if disc < 0:
            return None
        t1 = (-b - math.sqrt(disc)) / 2
        t2 = (-b + math.sqrt(disc)) / 2
        t = min(t1, t2)
        return t if t > 0 else None


# ---------- Scene ----------
camera = Vec(0, 0, -1)
light = Vec(5, 5, -10)

objects = [
    Sphere(Vec(0, 0, 3), 1, (255, 60, 60), 0.4),
    Sphere(Vec(2, 0, 4), 1, (60, 255, 60), 0.3),
    Sphere(Vec(-2, 0, 4), 1, (60, 60, 255), 0.5),
]

# ---------- Ray Trace ----------
def trace(origin, dir, depth):
    hit_obj = None
    min_t = 1e9

    for obj in objects:
        t = obj.intersect(origin, dir)
        if t and t < min_t:
            min_t = t
            hit_obj = obj

    if not hit_obj:
        return (20, 20, 30)  # background

    hit = origin + dir * min_t
    normal = (hit - hit_obj.center).norm()

    # lighting
    light_dir = (light - hit).norm()
    diffuse = max(normal.dot(light_dir), 0)

    # shadow check
    shadow = False
    for obj in objects:
        if obj != hit_obj and obj.intersect(hit + normal*0.001, light_dir):
            shadow = True
            break

    if shadow:
        diffuse *= 0.2

    base = tuple(int(c * diffuse) for c in hit_obj.color)

    # reflection
    if depth <= 0 or hit_obj.reflection <= 0:
        return base

    refl_dir = dir.reflect(normal).norm()
    refl_color = trace(hit + normal*0.001, refl_dir, depth-1)

    return tuple(
        int(base[i]*(1-hit_obj.reflection) + refl_color[i]*hit_obj.reflection)
        for i in range(3)
    )


# ---------- Render ----------
img = Image.new("RGB", (WIDTH, HEIGHT))
pixels = img.load()

for y in range(HEIGHT):
    for x in range(WIDTH):
        # screen space → ray direction
        px = (2*(x+0.5)/WIDTH - 1) * WIDTH/HEIGHT
        py = 1 - 2*(y+0.5)/HEIGHT
        dir = Vec(px, py, 1).norm()

        color = trace(camera, dir, MAX_DEPTH)
        pixels[x, y] = color

    print(f"Row {y+1}/{HEIGHT}")

img.save("raytrace_output.png")
print("Done → saved as raytrace_output.png")
