import pygame
import numpy as np
import math

# --- Vector Math Helpers ---
def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm

# --- Classes ---

class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction

class Material:
    def __init__(self, color, ambient=0.1, diffuse=0.7, specular=0.2, shininess=50, reflection=0.5):
        self.color = np.array(color)
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess
        self.reflection = reflection

class Sphere:
    def __init__(self, center, radius, material):
        self.center = np.array(center)
        self.radius = radius
        self.material = material

    def intersect(self, ray):
        oc = ray.origin - self.center
        a = np.dot(ray.direction, ray.direction)
        b = 2.0 * np.dot(oc, ray.direction)
        c = np.dot(oc, oc) - self.radius * self.radius
        discriminant = b * b - 4 * a * c
        
        if discriminant < 0:
            return float('inf')
        
        sqrt_disc = math.sqrt(discriminant)
        dist1 = (-b - sqrt_disc) / (2 * a)
        dist2 = (-b + sqrt_disc) / (2 * a)
        
        if dist1 > 0.001:
            return dist1
        if dist2 > 0.001:
            return dist2
            
        return float('inf')

    def normal(self, point):
        return normalize(point - self.center)

class Plane:
    def __init__(self, point, normal, material):
        self.point = np.array(point)
        self.normal = normalize(np.array(normal))
        self.material = material

    def intersect(self, ray):
        denom = np.dot(ray.direction, self.normal)
        if abs(denom) > 1e-6:
            t = np.dot(self.point - ray.origin, self.normal) / denom
            if t > 0.001:
                return t
        return float('inf')

    def normal_at(self, point):
        return self.normal

# --- Ray Tracer Engine ---

def get_closest_object(ray, objects):
    closest_dist = float('inf')
    closest_obj = None
    
    for obj in objects:
        dist = obj.intersect(ray)
        if dist < closest_dist:
            closest_dist = dist
            closest_obj = obj
            
    return closest_obj, closest_dist

def trace_ray(ray, objects, lights, depth):
    if depth > 3:
        return np.zeros(3)

    closest_obj, closest_dist = get_closest_object(ray, objects)

    if closest_obj is None:
        return np.zeros(3) # Background color (black)

    # Hit point and normal
    hit_point = ray.origin + ray.direction * closest_dist
    
    # Handle normal calculation differently for Plane vs Sphere
    if isinstance(closest_obj, Sphere):
        normal = closest_obj.normal(hit_point)
    else: # Plane
        normal = closest_obj.normal_at(hit_point)

    # Nudge hit point slightly along normal to avoid self-intersection artifacts
    hit_point = hit_point + normal * 1e-4

    material = closest_obj.material
    color = np.zeros(3)
    
    # Ambient
    color += material.color * material.ambient

    # Lights (Diffuse + Specular + Shadows)
    for light_pos, light_color in lights:
        to_light = normalize(light_pos - hit_point)
        dist_to_light = np.linalg.norm(light_pos - hit_point)
        
        # Shadow check
        shadow_ray = Ray(hit_point, to_light)
        shadow_obj, shadow_dist = get_closest_object(shadow_ray, objects)
        
        # If no object is blocking the light (or object is further than the light)
        if shadow_dist >= dist_to_light:
            # Diffuse
            illumination = max(0, np.dot(normal, to_light))
            color += material.color * material.diffuse * illumination * light_color
            
            # Specular
            to_camera = normalize(ray.origin - hit_point)
            reflected_light = normalize(2 * np.dot(normal, to_light) * normal - to_light)
            specular = max(0, np.dot(reflected_light, to_camera)) ** material.shininess
            color += np.array([1.0, 1.0, 1.0]) * material.specular * specular * light_color

    # Reflection (Recursive)
    if material.reflection > 0:
        reflected_dir = normalize(ray.direction - 2 * np.dot(ray.direction, normal) * normal)
        reflected_ray = Ray(hit_point, reflected_dir)
        reflected_color = trace_ray(reflected_ray, objects, lights, depth + 1)
        color = color * (1 - material.reflection) + reflected_color * material.reflection

    return np.clip(color, 0, 1)

# --- Main Configuration & Loop ---

def main():
    WIDTH, HEIGHT = 400, 300 # Low res for performance in pure Python
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mini Ray Tracer")

    # Scene Setup
    materials = {
        'red': Material([1.0, 0.0, 0.0], reflection=0.2),
        'green': Material([0.0, 1.0, 0.0], reflection=0.2),
        'blue': Material([0.0, 0.0, 1.0], reflection=0.2),
        'mirror': Material([0.9, 0.9, 0.9], reflection=0.8, diffuse=0.1),
        'gray_floor': Material([0.5, 0.5, 0.5], reflection=0.3)
    }

    objects = [
        Sphere([0, 0, -5], 1, materials['red']),
        Sphere([-2, 0, -6], 1, materials['mirror']),
        Sphere([2, 0, -4], 1, materials['green']),
        Plane([0, -1, 0], [0, 1, 0], materials['gray_floor']) # Floor
    ]

    lights = [
        (np.array([5, 5, -5]), np.array([1, 1, 1])), # White light
        (np.array([-5, 5, -5]), np.array([0.5, 0.5, 0.5])) # Dimmer light
    ]

    camera_pos = np.array([0, 1, 0])
    
    # Precompute rays
    ratio = WIDTH / HEIGHT
    screen_arr = np.zeros((WIDTH, HEIGHT, 3))
    
    print("Rendering...")
    
    # Scanline rendering
    for y in range(HEIGHT):
        # Handle events to keep window responsive
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        for x in range(WIDTH):
            # Screen space coordinates
            # Map x from [0, WIDTH] to [-1, 1] * ratio
            # Map y from [0, HEIGHT] to [1, -1]
            
            px = (2 * (x + 0.5) / WIDTH - 1) * ratio * math.tan(math.pi / 4) # FOV 90
            py = (1 - 2 * (y + 0.5) / HEIGHT) * math.tan(math.pi / 4)
            
            direction = normalize(np.array([px, py, -1]))
            ray = Ray(camera_pos, direction)
            
            color = trace_ray(ray, objects, lights, 0)
            screen_arr[x, y] = color * 255

        # Update display every few lines to show progress
        if y % 10 == 0:
            surf = pygame.surfarray.make_surface(screen_arr)
            screen.blit(surf, (0, 0))
            pygame.display.flip()

    print("Rendering Complete!")
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        surf = pygame.surfarray.make_surface(screen_arr)
        screen.blit(surf, (0, 0))
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
