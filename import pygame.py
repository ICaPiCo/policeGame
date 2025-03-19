import pygame
import sys
import math
import random
import time
from pygame import gfxdraw

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
GRAVITY = 0.2
DAMPING = 0.95
THRUST_POWER = 0.25
ROTATION_SPEED = 3
MAX_SPEED = 10
PLANET_SIZES = [50, 100, 150, 200, 250]
BULLET_SPEED = 15
ENEMY_TYPES = ['scout', 'fighter', 'destroyer']
UPGRADE_TYPES = ['fuel', 'shield', 'weapon', 'engine']
STAR_COUNT = 200

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
TURQUOISE = (64, 224, 208)
PLANET_COLORS = [(206, 147, 116), (160, 160, 160), (150, 200, 255),
                 (100, 200, 100), (255, 200, 100), (200, 100, 200)]

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cosmic Voyager")
clock = pygame.time.Clock()

# Fonts
title_font = pygame.font.Font(None, 74)
menu_font = pygame.font.Font(None, 50)
game_font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# Game states
MENU = 0
PLAYING = 1
PAUSED = 2
GAME_OVER = 3
LEVEL_COMPLETE = 4
UPGRADE = 5
TUTORIAL = 6

# Load sounds and music (placeholder functions - in a real game, load actual files)
def load_sound(name):
    return pygame.mixer.Sound(name) if pygame.mixer.get_init() else None

def load_music(name):
    try:
        pygame.mixer.music.load(name)
    except:
        pass

# Sound placeholders
try:
    thrust_sound = load_sound("thrust.wav")
    shoot_sound = load_sound("shoot.wav")
    explosion_sound = load_sound("explosion.wav")
    upgrade_sound = load_sound("upgrade.wav")
    menu_select_sound = load_sound("menu_select.wav")
except:
    # Provide feedback but continue if sounds can't be loaded
    print("Warning: Sound files not found")
    thrust_sound = None
    shoot_sound = None
    explosion_sound = None
    upgrade_sound = None
    menu_select_sound = None

class Particle:
    def __init__(self, x, y, color=(255, 255, 255), size=2, lifetime=30):
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
        self.size = max(0, self.size * 0.95)
        return self.lifetime > 0
    
    def draw(self, surface):
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        color = (self.color[0], self.color[1], self.color[2], alpha)
        radius = int(self.size)
        if radius > 0:
            gfxdraw.filled_circle(surface, int(self.x), int(self.y), radius, color)
            gfxdraw.aacircle(surface, int(self.x), int(self.y), radius, color)

class Star:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.size = random.uniform(0.1, 3)
        self.brightness = random.uniform(0.5, 1.0)
        self.speed = random.uniform(0.05, 0.5)  # For parallax effect
    
    def update(self, dx=0, dy=0):
        # Move stars based on player movement for parallax effect
        self.x -= dx * self.speed
        self.y -= dy * self.speed
        
        # Loop around if offscreen
        if self.x < 0:
            self.x = SCREEN_WIDTH
        elif self.x > SCREEN_WIDTH:
            self.x = 0
        if self.y < 0:
            self.y = SCREEN_HEIGHT
        elif self.y > SCREEN_HEIGHT:
            self.y = 0
    
    def draw(self, surface):
        # Apply twinkling effect
        brightness = self.brightness * (0.7 + 0.3 * math.sin(time.time() * 3 + self.x))
        color = tuple(int(c * brightness) for c in (255, 255, 255))
        if self.size < 1:
            surface.set_at((int(self.x), int(self.y)), color)
        else:
            pygame.draw.circle(surface, color, (int(self.x), int(self.y)), math.ceil(self.size))

class Bullet:
    def __init__(self, x, y, dx, dy, owner, power=1):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.speed = BULLET_SPEED
        self.owner = owner  # 'player' or 'enemy'
        self.radius = 3
        self.power = power
        self.lifetime = 90  # Bullet disappears after this many frames
        
    def update(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed
        self.lifetime -= 1
        return self.lifetime > 0 and 0 <= self.x <= SCREEN_WIDTH and 0 <= self.y <= SCREEN_HEIGHT
    
    def draw(self, surface):
        if self.owner == 'player':
            color = GREEN
        else:
            color = RED
        
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.radius)
        # Add a glow effect
        pygame.draw.circle(surface, (color[0]//2 + 128, color[1]//2 + 128, color[2]//2 + 128), 
                          (int(self.x), int(self.y)), self.radius + 2, 1)

class Spaceship:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.angle = -90  # Pointing up
        self.radius = 15
        self.thrust = False
        self.shield = 2000
        self.max_shield = 100
        self.fuel = 1000
        self.max_fuel = 100
        self.fuel_consumption = 0.5
        self.weapon_power = 1
        self.weapon_level = 1
        self.engine_level = 1
        self.shoot_cooldown = 0
        self.thrust_particles = []
        self.invulnerable = 0  # Invulnerability frames
        self.score = 0
        
    def update(self, thrust=False, rotate_left=False, rotate_right=False, planets=[]):
        # Rotation
        if rotate_left:
            self.angle -= ROTATION_SPEED * self.engine_level
        if rotate_right:
            self.angle += ROTATION_SPEED * self.engine_level
        
        # Normalizing angle
        self.angle %= 360
        
        # Thrust
        self.thrust = thrust
        if thrust and self.fuel > 0:
            # Calculate thrust components based on ship's angle
            thrust_dx = THRUST_POWER * self.engine_level * math.cos(math.radians(self.angle))
            thrust_dy = THRUST_POWER * self.engine_level * math.sin(math.radians(self.angle))
            
            # Apply thrust
            self.dx += thrust_dx
            self.dy += thrust_dy
            
            # Reduce fuel
            self.fuel = max(0, self.fuel - self.fuel_consumption)
            
            # Create thrust particles
            self.add_thrust_particles()
            
            # Play thrust sound
            if thrust_sound and random.random() < 0.1:
                thrust_sound.play()
        
        # Apply planet gravity
        for planet in planets:
            dx = planet.x - self.x
            dy = planet.y - self.y
            dist = math.sqrt(dx*dx + dy*dy)
            if dist < 1:  # Avoid division by zero
                dist = 1
            
            # Calculate gravitational force (stronger for larger planets)
            force = GRAVITY * planet.radius / (dist * dist)
            angle = math.atan2(dy, dx)
            
            # Apply force components
            self.dx += force * math.cos(angle)
            self.dy += force * math.sin(angle)
        
        # Apply damping (space friction)
        self.dx *= DAMPING
        self.dy *= DAMPING
        
        # Limit speed
        speed = math.sqrt(self.dx*self.dx + self.dy*self.dy)
        if speed > MAX_SPEED:
            self.dx = self.dx / speed * MAX_SPEED
            self.dy = self.dy / speed * MAX_SPEED
        
        # Update position
        self.x += self.dx
        self.y += self.dy
        
        # Screen wrapping
        if self.x < 0:
            self.x = SCREEN_WIDTH
        elif self.x > SCREEN_WIDTH:
            self.x = 0
        if self.y < 0:
            self.y = SCREEN_HEIGHT
        elif self.y > SCREEN_HEIGHT:
            self.y = 0
        
        # Update thrust particles
        self.update_particles()
        
        # Update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
            
        # Update invulnerability
        if self.invulnerable > 0:
            self.invulnerable -= 1
    
    def add_thrust_particles(self):
        # Calculate the position behind the ship
        back_angle = (self.angle + 180) % 360
        back_x = self.x + 15 * math.cos(math.radians(back_angle))
        back_y = self.y + 15 * math.sin(math.radians(back_angle))
        
        # Add particles with varied colors
        for _ in range(3):
            color_r = random.randint(200, 255)
            color_g = random.randint(100, 200)
            color_b = random.randint(0, 100)
            self.thrust_particles.append(
                Particle(back_x, back_y, (color_r, color_g, color_b), 
                        random.uniform(3, 6), random.randint(10, 20))
            )
    
    def update_particles(self):
        self.thrust_particles = [p for p in self.thrust_particles if p.update()]
    
    def shoot(self):
        if self.shoot_cooldown <= 0:
            # Calculate bullet direction based on ship's angle
            bullet_dx = math.cos(math.radians(self.angle))
            bullet_dy = math.sin(math.radians(self.angle))
            
            # Create bullet at the front of the ship
            front_x = self.x + self.radius * math.cos(math.radians(self.angle))
            front_y = self.y + self.radius * math.sin(math.radians(self.angle))
            
            # Create bullets based on weapon level
            bullets = []
            if self.weapon_level == 1:
                bullets.append(Bullet(front_x, front_y, bullet_dx, bullet_dy, 'player', self.weapon_power))
            elif self.weapon_level == 2:
                # Dual bullets
                spread = 10  # degrees
                bullets.append(Bullet(front_x, front_y, 
                                    math.cos(math.radians(self.angle - spread)), 
                                    math.sin(math.radians(self.angle - spread)), 
                                    'player', self.weapon_power))
                bullets.append(Bullet(front_x, front_y, 
                                    math.cos(math.radians(self.angle + spread)), 
                                    math.sin(math.radians(self.angle + spread)), 
                                    'player', self.weapon_power))
            elif self.weapon_level >= 3:
                # Triple bullets
                bullets.append(Bullet(front_x, front_y, bullet_dx, bullet_dy, 'player', self.weapon_power))
                spread = 15  # degrees
                bullets.append(Bullet(front_x, front_y, 
                                    math.cos(math.radians(self.angle - spread)), 
                                    math.sin(math.radians(self.angle - spread)), 
                                    'player', self.weapon_power))
                bullets.append(Bullet(front_x, front_y, 
                                    math.cos(math.radians(self.angle + spread)), 
                                    math.sin(math.radians(self.angle + spread)), 
                                    'player', self.weapon_power))
            
            # Set cooldown based on weapon level
            self.shoot_cooldown = max(5, 15 - self.weapon_level * 2)
            
            # Play sound
            if shoot_sound:
                shoot_sound.play()
                
            return bullets
        return []
    
    def take_damage(self, damage):
        if self.invulnerable <= 0:
            self.shield -= damage
            self.invulnerable = 30  # Half a second of invulnerability
            return True
        return False
    
    def draw(self, surface):
        # Calculate ship's corners based on angle
        ship_points = [
            (self.x + self.radius * math.cos(math.radians(self.angle)),
             self.y + self.radius * math.sin(math.radians(self.angle))),
            (self.x + self.radius * math.cos(math.radians(self.angle + 120)),
             self.y + self.radius * math.sin(math.radians(self.angle + 120))),
            (self.x + self.radius * 0.5 * math.cos(math.radians(self.angle + 180)),
             self.y + self.radius * 0.5 * math.sin(math.radians(self.angle + 180))),
            (self.x + self.radius * math.cos(math.radians(self.angle - 120)),
             self.y + self.radius * math.sin(math.radians(self.angle - 120)))
        ]
        
        # Draw thrust particles
        for particle in self.thrust_particles:
            particle.draw(surface)
        
        # Draw ship
        if self.invulnerable <= 0 or (self.invulnerable // 4) % 2 == 0:  # Blinking when invulnerable
            pygame.draw.polygon(surface, WHITE, ship_points)
            pygame.draw.polygon(surface, BLUE, ship_points, 2)
        
        # Draw shield indicator
        shield_percentage = self.shield / self.max_shield
        shield_color = (
            int(255 * (1 - shield_percentage)),
            int(255 * shield_percentage),
            0
        )
        
        # Draw shield glow if active
        if self.invulnerable > 0:
            s = pygame.Surface((self.radius * 4, self.radius * 4), pygame.SRCALPHA)
            pygame.draw.circle(s, (*BLUE, 100), (self.radius * 2, self.radius * 2), self.radius + 5)
            surface.blit(s, (self.x - self.radius * 2, self.y - self.radius * 2))

class Enemy:
    def __init__(self, x, y, enemy_type='scout', level=1):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.angle = random.randint(0, 359)
        self.enemy_type = enemy_type
        self.level = level
        
        # Set attributes based on enemy type
        if enemy_type == 'scout':
            self.radius = 10
            self.max_health = 30 * level
            self.speed = 3
            self.color = RED
            self.score_value = 100 * level
            self.damage = 10
            self.shoot_cooldown_max = 60
        elif enemy_type == 'fighter':
            self.radius = 15
            self.max_health = 60 * level
            self.speed = 2
            self.color = ORANGE
            self.score_value = 200 * level
            self.damage = 15
            self.shoot_cooldown_max = 45
        elif enemy_type == 'destroyer':
            self.radius = 25
            self.max_health = 120 * level
            self.speed = 1
            self.color = PURPLE
            self.score_value = 500 * level
            self.damage = 25
            self.shoot_cooldown_max = 90
        
        self.health = self.max_health
        self.shoot_cooldown = random.randint(0, self.shoot_cooldown_max)
        self.behavior_timer = random.randint(60, 180)
        self.behavior = 'wander'
    
    def update(self, player_x, player_y):
        # Occasionally change behavior
        self.behavior_timer -= 1
        if self.behavior_timer <= 0:
            self.behavior_timer = random.randint(120, 240)
            behaviors = ['wander', 'chase', 'retreat', 'orbit']
            weights = [0.2, 0.4, 0.2, 0.2]
            self.behavior = random.choices(behaviors, weights)[0]
        
        # Calculate distance and angle to player
        dx = player_x - self.x
        dy = player_y - self.y
        dist = math.sqrt(dx*dx + dy*dy)
        target_angle = math.degrees(math.atan2(dy, dx)) % 360
        
        # Update behavior
        if self.behavior == 'wander':
            if random.random() < 0.02:
                self.angle += random.randint(-30, 30)
            
            self.dx += math.cos(math.radians(self.angle)) * 0.1
            self.dy += math.sin(math.radians(self.angle)) * 0.1
        
        elif self.behavior == 'chase':
            # Gradually turn towards player
            angle_diff = (target_angle - self.angle) % 360
            if angle_diff > 180:
                angle_diff -= 360
            
            self.angle += angle_diff * 0.1
            
            # Accelerate towards player
            self.dx += math.cos(math.radians(self.angle)) * 0.2
            self.dy += math.sin(math.radians(self.angle)) * 0.2
        
        elif self.behavior == 'retreat':
            # Run away from player
            angle_diff = (target_angle - self.angle + 180) % 360
            if angle_diff > 180:
                angle_diff -= 360
            
            self.angle += angle_diff * 0.1
            
            # Accelerate away from player
            self.dx += math.cos(math.radians(self.angle)) * 0.15
            self.dy += math.sin(math.radians(self.angle)) * 0.15
        
        elif self.behavior == 'orbit':
            # Try to maintain a certain distance while circling
            ideal_dist = 200
            
            if dist < ideal_dist - 50:
                # Too close, move away
                self.angle = (target_angle + 180) % 360
                self.dx += math.cos(math.radians(self.angle)) * 0.2
                self.dy += math.sin(math.radians(self.angle)) * 0.2
            elif dist > ideal_dist + 50:
                # Too far, move closer
                self.angle = target_angle
                self.dx += math.cos(math.radians(self.angle)) * 0.2
                self.dy += math.sin(math.radians(self.angle)) * 0.2
            else:
                # At good distance, circle around
                orbit_angle = (target_angle + 90) % 360
                self.angle = orbit_angle
                self.dx += math.cos(math.radians(self.angle)) * 0.2
                self.dy += math.sin(math.radians(self.angle)) * 0.2
        
        # Apply damping to avoid too much speed
        self.dx *= 0.95
        self.dy *= 0.95
        
        # Limit speed
        speed = math.sqrt(self.dx*self.dx + self.dy*self.dy)
        max_speed = self.speed
        if speed > max_speed:
            self.dx = self.dx / speed * max_speed
            self.dy = self.dy / speed * max_speed
        
        # Update position
        self.x += self.dx
        self.y += self.dy
        
        # Screen wrapping
        if self.x < 0:
            self.x = SCREEN_WIDTH
        elif self.x > SCREEN_WIDTH:
            self.x = 0
        if self.y < 0:
            self.y = SCREEN_HEIGHT
        elif self.y > SCREEN_HEIGHT:
            self.y = 0
        
        # Update shoot cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
    
    def shoot(self, player_x, player_y):
        if self.shoot_cooldown <= 0:
            # Calculate direction towards player
            dx = player_x - self.x
            dy = player_y - self.y
            length = math.sqrt(dx*dx + dy*dy)
            
            if length > 0:
                dx /= length
                dy /= length
            
            # Add some inaccuracy based on enemy type
            if self.enemy_type == 'scout':
                inaccuracy = 0.2
            elif self.enemy_type == 'fighter':
                inaccuracy = 0.1
            else:
                inaccuracy = 0.05
                
            dx += random.uniform(-inaccuracy, inaccuracy)
            dy += random.uniform(-inaccuracy, inaccuracy)
            
            # Normalize direction again
            length = math.sqrt(dx*dx + dy*dy)
            if length > 0:
                dx /= length
                dy /= length
            
            # Create bullet
            bullet = Bullet(self.x, self.y, dx, dy, 'enemy', self.damage / 10)
            
            # Reset cooldown
            self.shoot_cooldown = self.shoot_cooldown_max
            
            return bullet
        return None
    
    def take_damage(self, damage):
        self.health -= damage
        # If hit, sometimes change behavior to chase
        if random.random() < 0.3:
            self.behavior = 'chase'
            self.behavior_timer = random.randint(120, 180)
        return self.health <= 0
    
    def draw(self, surface):
        # Draw enemy based on type
        if self.enemy_type == 'scout':
            # Draw triangular ship
            ship_points = [
                (self.x + self.radius * math.cos(math.radians(self.angle)),
                 self.y + self.radius * math.sin(math.radians(self.angle))),
                (self.x + self.radius * math.cos(math.radians(self.angle + 130)),
                 self.y + self.radius * math.sin(math.radians(self.angle + 130))),
                (self.x + self.radius * math.cos(math.radians(self.angle - 130)),
                 self.y + self.radius * math.sin(math.radians(self.angle - 130)))
            ]
            pygame.draw.polygon(surface, self.color, ship_points)
            
        elif self.enemy_type == 'fighter':
            # Draw diamond shape
            ship_points = [
                (self.x + self.radius * math.cos(math.radians(self.angle)),
                 self.y + self.radius * math.sin(math.radians(self.angle))),
                (self.x + self.radius * 0.7 * math.cos(math.radians(self.angle + 90)),
                 self.y + self.radius * 0.7 * math.sin(math.radians(self.angle + 90))),
                (self.x + self.radius * 0.5 * math.cos(math.radians(self.angle + 180)),
                 self.y + self.radius * 0.5 * math.sin(math.radians(self.angle + 180))),
                (self.x + self.radius * 0.7 * math.cos(math.radians(self.angle - 90)),
                 self.y + self.radius * 0.7 * math.sin(math.radians(self.angle - 90)))
            ]
            pygame.draw.polygon(surface, self.color, ship_points)
            
        elif self.enemy_type == 'destroyer':
            # Draw hexagon shape
            ship_points = []
            for i in range(6):
                angle = self.angle + i * 60
                ship_points.append(
                    (self.x + self.radius * math.cos(math.radians(angle)),
                     self.y + self.radius * math.sin(math.radians(angle)))
                )
            pygame.draw.polygon(surface, self.color, ship_points)
        
        # Draw health bar
        health_percentage = self.health / self.max_health
        bar_width = int(self.radius * 2 * health_percentage)
        health_bar = pygame.Rect(self.x - self.radius, self.y - self.radius - 10, 
                                bar_width, 5)
        pygame.draw.rect(surface, (255 * (1 - health_percentage), 255 * health_percentage, 0), health_bar)

class Planet:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = random.choice(PLANET_COLORS)
        self.features = []
        
        # Generate random surface features
        num_features = random.randint(3, 10)
        for _ in range(num_features):
            angle = random.uniform(0, 2 * math.pi)
            dist = random.uniform(0.3, 0.9) * radius
            size = random.uniform(0.1, 0.3) * radius
            feature_color = tuple(max(0, min(255, c + random.randint(-40, 40))) for c in self.color)
            self.features.append((angle, dist, size, feature_color))
    
    def draw(self, surface):
        # Draw main planet body
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
        
        # Draw atmosphere glow
        s = pygame.Surface((self.radius * 2 + 20, self.radius * 2 + 20), pygame.SRCALPHA)
        atmo_color = tuple(min(255, c + 40) for c in self.color) + (100,)
        pygame.draw.circle(s, atmo_color, (self.radius + 10, self.radius + 10), self.radius + 10)
        surface.blit(s, (self.x - self.radius - 10, self.y - self.radius - 10))
        
        # Draw surface features (craters, mountains, etc.)
        for angle, dist, size, color in self.features:
            feature_x = self.x + dist * math.cos(angle)
            feature_y = self.y + dist * math.sin(angle)
            pygame.draw.circle(surface, color, (int(feature_x), int(feature_y)), int(size))
        
        # Draw highlight (simple light reflection)
        highlight_size = self.radius * 0.2
        highlight_pos = (int(self.x - self.radius * 0.5), int(self.y - self.radius * 0.5))
        highlight_color = tuple(min(255, c + 70) for c in self.color)
        pygame.draw.circle(surface, highlight_color, highlight_pos, int(highlight_size))

class Upgrade:
    def __init__(self, x, y, upgrade_type):
        self.x = x
        self.y = y
        self.type = upgrade_type
        self.radius = 15
        self.angle = 0  # For rotation effect
        
        # Set color based on upgrade type
        if upgrade_type == 'fuel':
            self.color = YELLOW
        elif upgrade_type == 'shield':
            self.color = BLUE
        elif upgrade_type == 'weapon':
            self.color = RED
        elif upgrade_type == 'engine':
            self.color = GREEN
    
    def update(self):
        # Rotate the upgrade for visual effect
        self.angle = (self.angle + 2) % 360
    
    def draw(self, surface):
        # Draw base circle
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
        
        # Draw symbol based on type
        if self.type == 'fuel':
            # Draw fuel symbol (F)
            text = game_font.render("F", True, BLACK)
            text_rect = text.get_rect(center=(self.x, self.y))
            surface.blit(text, text_rect)
            
        elif self.type == 'shield':
            # Draw shield symbol (semi-circle)
            rect = pygame.Rect(self.x - 10, self.y - 10, 20, 20)
            pygame.draw.arc(surface, WHITE, rect, math.radians(0), math.radians(180), 3)
            
        elif self.type == 'weapon':
            # Draw weapon symbol (W)
            text = game_font.render("W", True, BLACK)
            text_rect = text.get_rect(center=(self.x, self.y))
            surface.blit(text, text_rect)
            
        elif self.type == 'engine':
            # Draw engine symbol (E)
            text = game_font.render("E", True, BLACK)
            text_rect = text.get_rect(center=(self.x,self.y))
            text_rect = text.get_rect(center=(self.x, self.y))
            surface.blit(text, text_rect)
        
        # Draw pulsing glow effect
        glow_size = self.radius + 5 + 2 * math.sin(time.time() * 5)
        s = pygame.Surface((int(glow_size * 2), int(glow_size * 2)), pygame.SRCALPHA)
        glow_color = (*self.color, 100)  # Add alpha for transparency
        pygame.draw.circle(s, glow_color, (int(glow_size), int(glow_size)), int(glow_size))
        surface.blit(s, (self.x - glow_size, self.y - glow_size))

def check_collision(x1, y1, r1, x2, y2, r2):
    """Helper function to check circular collision between objects"""
    dx = x1 - x2
    dy = y1 - y2
    distance = math.sqrt(dx*dx + dy*dy)
    return distance < r1 + r2

def draw_ui(surface, player, level, state):
    """Draw user interface elements"""
    # Draw shield bar
    shield_pct = player.shield / player.max_shield
    shield_bar = pygame.Rect(20, 20, 200 * shield_pct, 20)
    pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(20, 20, 200, 20), 0)
    pygame.draw.rect(surface, (int(255 * (1 - shield_pct)), int(255 * shield_pct), 0), shield_bar)
    shield_text = game_font.render(f"Shield: {int(player.shield)}/{player.max_shield}", True, WHITE)
    surface.blit(shield_text, (25, 22))
    
    # Draw fuel bar
    fuel_pct = player.fuel / player.max_fuel
    fuel_bar = pygame.Rect(20, 50, 200 * fuel_pct, 20)
    pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(20, 50, 200, 20), 0)
    pygame.draw.rect(surface, YELLOW, fuel_bar)
    fuel_text = game_font.render(f"Fuel: {int(player.fuel)}/{player.max_fuel}", True, WHITE)
    surface.blit(fuel_text, (25, 52))
    
    # Draw score
    score_text = game_font.render(f"Score: {player.score}", True, WHITE)
    surface.blit(score_text, (SCREEN_WIDTH - score_text.get_width() - 20, 20))
    
    # Draw level
    level_text = game_font.render(f"Level: {level}", True, WHITE)
    surface.blit(level_text, (SCREEN_WIDTH - level_text.get_width() - 20, 50))
    
    # Draw weapon and engine levels
    weapon_text = small_font.render(f"Weapon Lvl: {player.weapon_level}", True, RED)
    surface.blit(weapon_text, (20, 80))
    engine_text = small_font.render(f"Engine Lvl: {player.engine_level}", True, GREEN)
    surface.blit(engine_text, (20, 100))
    
    # Draw game state-specific UI
    if state == PAUSED:
        paused_text = title_font.render("PAUSED", True, WHITE)
        surface.blit(paused_text, (SCREEN_WIDTH // 2 - paused_text.get_width() // 2, 
                                  SCREEN_HEIGHT // 2 - paused_text.get_height() // 2))
        resume_text = menu_font.render("Press P to Resume", True, WHITE)
        surface.blit(resume_text, (SCREEN_WIDTH // 2 - resume_text.get_width() // 2, 
                                  SCREEN_HEIGHT // 2 + 50))
    
    elif state == GAME_OVER:
        game_over_text = title_font.render("GAME OVER", True, RED)
        surface.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 
                                     SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
        restart_text = menu_font.render("Press R to Restart", True, WHITE)
        surface.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 
                                   SCREEN_HEIGHT // 2 + 50))
        menu_text = menu_font.render("Press M for Menu", True, WHITE)
        surface.blit(menu_text, (SCREEN_WIDTH // 2 - menu_text.get_width() // 2, 
                               SCREEN_HEIGHT // 2 + 100))
    
    elif state == LEVEL_COMPLETE:
        level_complete_text = title_font.render(f"Level {level} Complete!", True, GREEN)
        surface.blit(level_complete_text, (SCREEN_WIDTH // 2 - level_complete_text.get_width() // 2, 
                                         SCREEN_HEIGHT // 2 - level_complete_text.get_height() // 2))
        continue_text = menu_font.render("Press Space to Continue", True, WHITE)
        surface.blit(continue_text, (SCREEN_WIDTH // 2 - continue_text.get_width() // 2, 
                                    SCREEN_HEIGHT // 2 + 50))

def generate_level(level):
    """Generate level content based on level number"""
    planets = []
    enemies = []
    upgrades = []
    
    # Determine number of objects based on level
    num_planets = min(3, 1 + level // 2)
    num_enemies = 5 + level * 2
    num_upgrades = 2 + level // 2
    
    # Generate random planet positions (ensuring they don't overlap)
    for _ in range(num_planets):
        while True:
            size = random.choice(PLANET_SIZES)
            x = random.randint(size, SCREEN_WIDTH - size)
            y = random.randint(size, SCREEN_HEIGHT - size)
            
            # Check for overlap with existing planets
            overlap = False
            for planet in planets:
                if check_collision(x, y, size + 50, planet.x, planet.y, planet.radius + 50):
                    overlap = True
                    break
            
            if not overlap:
                planets.append(Planet(x, y, size))
                break
    
    # Generate enemies with increasing difficulty based on level
    for _ in range(num_enemies):
        # Determine enemy type with weighted probabilities
        if level <= 2:
            weights = [0.8, 0.2, 0.0]  # Mostly scouts early on
        elif level <= 5:
            weights = [0.5, 0.4, 0.1]  # More fighters in mid-levels
        else:
            weights = [0.3, 0.4, 0.3]  # More destroyers in later levels
        
        enemy_type = random.choices(ENEMY_TYPES, weights=weights)[0]
        
        # Determine enemy level (slightly random around current level)
        enemy_level = max(1, min(level, level - 1 + random.randint(0, 2)))
        
        # Generate position away from player starting point
        while True:
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 50)
            
            # Ensure enemy is not too close to player start
            if math.sqrt((x - SCREEN_WIDTH // 2)**2 + (y - SCREEN_HEIGHT // 2)**2) > 200:
                # Check for overlap with planets
                overlap = False
                for planet in planets:
                    if check_collision(x, y, 30, planet.x, planet.y, planet.radius + 30):
                        overlap = True
                        break
                
                if not overlap:
                    enemies.append(Enemy(x, y, enemy_type, enemy_level))
                    break
    
    # Generate upgrades
    for _ in range(num_upgrades):
        upgrade_type = random.choice(UPGRADE_TYPES)
        
        while True:
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 50)
            
            # Check for overlap with planets
            overlap = False
            for planet in planets:
                if check_collision(x, y, 20, planet.x, planet.y, planet.radius + 20):
                    overlap = True
                    break
            
            if not overlap:
                upgrades.append(Upgrade(x, y, upgrade_type))
                break
    
    return planets, enemies, upgrades

def draw_menu(surface):
    """Draw the main menu"""
    # Draw title
    title_text = title_font.render("COSMIC VOYAGER", True, TURQUOISE)
    title_shadow = title_font.render("COSMIC VOYAGER", True, (0, 0, 50))
    surface.blit(title_shadow, (SCREEN_WIDTH // 2 - title_text.get_width() // 2 + 4, 
                               SCREEN_HEIGHT // 4 - title_text.get_height() // 2 + 4))
    surface.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 
                             SCREEN_HEIGHT // 4 - title_text.get_height() // 2))
    
    # Draw menu options
    start_text = menu_font.render("Start Game (S)", True, WHITE)
    tutorial_text = menu_font.render("Tutorial (T)", True, WHITE)
    quit_text = menu_font.render("Quit (Q)", True, WHITE)
    
    surface.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, 
                             SCREEN_HEIGHT // 2))
    surface.blit(tutorial_text, (SCREEN_WIDTH // 2 - tutorial_text.get_width() // 2, 
                                SCREEN_HEIGHT // 2 + 60))
    surface.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, 
                            SCREEN_HEIGHT // 2 + 120))
    
    # Draw animated spaceship
    current_time = time.time()
    ship_x = SCREEN_WIDTH // 2 + 150 * math.cos(current_time * 0.5)
    ship_y = SCREEN_HEIGHT * 3 // 4 + 50 * math.sin(current_time)
    ship_angle = math.degrees(math.atan2(
        math.sin(current_time), math.cos(current_time * 0.5))) - 90
    
    ship_points = [
        (ship_x + 20 * math.cos(math.radians(ship_angle)),
         ship_y + 20 * math.sin(math.radians(ship_angle))),
        (ship_x + 20 * math.cos(math.radians(ship_angle + 120)),
         ship_y + 20 * math.sin(math.radians(ship_angle + 120))),
        (ship_x + 20 * 0.5 * math.cos(math.radians(ship_angle + 180)),
         ship_y + 20 * 0.5 * math.sin(math.radians(ship_angle + 180))),
        (ship_x + 20 * math.cos(math.radians(ship_angle - 120)),
         ship_y + 20 * math.sin(math.radians(ship_angle - 120)))
    ]
    
    pygame.draw.polygon(surface, WHITE, ship_points)
    pygame.draw.polygon(surface, BLUE, ship_points, 2)
    
    # Draw copyright
    copyright_text = small_font.render("© 2023 Cosmic Voyager Games", True, WHITE)
    surface.blit(copyright_text, (SCREEN_WIDTH - copyright_text.get_width() - 10, 
                                 SCREEN_HEIGHT - copyright_text.get_height() - 10))

def draw_tutorial(surface):
    """Draw the tutorial screen"""
    # Title
    title_text = title_font.render("TUTORIAL", True, WHITE)
    surface.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))
    
    # Controls
    y_pos = 150
    controls = [
        "WASD / Arrow Keys: Move ship",
        "Space: Fire weapons",
        "P: Pause game",
        "ESC: Return to menu",
        "",
        "GAMEPLAY TIPS:",
        "- Collect fuel (yellow) to refill your ship's tank",
        "- Collect shield (blue) to repair your ship",
        "- Collect weapon (red) to upgrade your weapons",
        "- Collect engine (green) to improve maneuverability",
        "- Beware of planets' gravity",
        "- Destroy all enemies to complete the level"
    ]
    
    for line in controls:
        if line.startswith("GAMEPLAY"):
            text = menu_font.render(line, True, YELLOW)
        elif line == "":
            text = menu_font.render(line, True, WHITE)
        else:
            text = game_font.render(line, True, WHITE)
        
        surface.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y_pos))
        y_pos += 40
    
    # Back to menu instruction
    back_text = menu_font.render("Press ESC to return to menu", True, WHITE)
    surface.blit(back_text, (SCREEN_WIDTH // 2 - back_text.get_width() // 2, 
                            SCREEN_HEIGHT - 100))

def create_explosion(x, y, size=1.0, color=None):
    """Create a set of particles for an explosion effect"""
    particles = []
    num_particles = int(30 * size)
    
    if color is None:
        colors = [(255, 200, 50), (255, 120, 50), (255, 50, 50)]
    else:
        # Create variations of the specified color
        r, g, b = color
        colors = [(r, g, b), 
                 (min(255, r + 50), min(255, g + 50), min(255, b + 50)),
                 (max(0, r - 50), max(0, g - 50), max(0, b - 50))]
    
    for _ in range(num_particles):
        particle_color = random.choice(colors)
        particle_size = random.uniform(2, 6) * size
        particle_lifetime = random.randint(20, 40)
        particles.append(Particle(x, y, particle_color, particle_size, particle_lifetime))
    
    return particles

def main():
    """Main game function"""
    # Game variables
    game_state = MENU
    current_level = 1
    stars = [Star() for _ in range(STAR_COUNT)]
    
    # Create player
    player = None
    
    # Level content
    planets = []
    enemies = []
    bullets = []
    upgrades = []
    particles = []
    
    try:
        # Main game loop
        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                if event.type == pygame.KEYDOWN:
                    # Global key handlers
                    if event.key == pygame.K_ESCAPE:
                        if game_state in [PLAYING, PAUSED]:
                            game_state = MENU
                        elif game_state == TUTORIAL:
                            game_state = MENU
                    
                    # Menu controls
                    if game_state == MENU:
                        if event.key == pygame.K_s:
                            # Start new game
                            game_state = PLAYING
                            current_level = 1
                            player = Spaceship(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                            planets, enemies, upgrades = generate_level(current_level)
                            bullets = []
                            particles = []
                            
                            if menu_select_sound:
                                menu_select_sound.play()
                        
                        elif event.key == pygame.K_t:
                            game_state = TUTORIAL
                            
                            if menu_select_sound:
                                menu_select_sound.play()
                        
                        elif event.key == pygame.K_q:
                            running = False
                    
                    # Playing controls
                    elif game_state == PLAYING:
                        if event.key == pygame.K_p:
                            game_state = PAUSED
                    
                    # Paused controls
                    elif game_state == PAUSED:
                        if event.key == pygame.K_p:
                            game_state = PLAYING
                    
                    # Game over controls
                    elif game_state == GAME_OVER:
                        if event.key == pygame.K_r:
                            # Restart game
                            game_state = PLAYING
                            current_level = 1
                            player = Spaceship(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                            planets, enemies, upgrades = generate_level(current_level)
                            bullets = []
                            particles = []
                        
                        elif event.key == pygame.K_m:
                            game_state = MENU
                    
                    # Level complete controls
                    elif game_state == LEVEL_COMPLETE:
                        if event.key == pygame.K_SPACE:
                            # Start next level
                            current_level += 1
                            game_state = PLAYING
                            # Keep player stats but reset position
                            player.x = SCREEN_WIDTH // 2
                            player.y = SCREEN_HEIGHT // 2
                            player.dx = 0
                            player.dy = 0
                            player.angle = -90
                            # Refill some fuel and shield
                            player.fuel = min(player.max_fuel, player.fuel + player.max_fuel * 0.5)
                            player.shield = min(player.max_shield, player.shield + player.max_shield * 0.3)
                            
                            planets, enemies, upgrades = generate_level(current_level)
                            bullets = []
                            particles = []
            
            # Clear screen
            screen.fill(BLACK)
            
            # Update and draw stars (background in all game states)
            for star in stars:
                star_dx, star_dy = 0, 0
                if game_state == PLAYING and player:
                    star_dx, star_dy = player.dx * 0.1, player.dy * 0.1
                star.update(star_dx, star_dy)
                star.draw(screen)
            
            # Handle different game states
            if game_state == MENU:
                draw_menu(screen)
                
            elif game_state == TUTORIAL:
                draw_tutorial(screen)
                
            elif game_state in [PLAYING, PAUSED, GAME_OVER, LEVEL_COMPLETE]:
                # Update game objects if playing
                if game_state == PLAYING:
                    # Get input for player movement
                    keys = pygame.key.get_pressed()
                    thrust = keys[pygame.K_w] or keys[pygame.K_UP]
                    rotate_left = keys[pygame.K_a] or keys[pygame.K_LEFT]
                    rotate_right = keys[pygame.K_d] or keys[pygame.K_RIGHT]
                    shooting = keys[pygame.K_SPACE]
                    
                    # Update player
                    player.update(thrust, rotate_left, rotate_right, planets)
                    
                    # Player shooting
                    if shooting:
                        new_bullets = player.shoot()
                        bullets.extend(new_bullets)
                    
                    # Update enemies
                    for enemy in enemies[:]:
                        enemy.update(player.x, player.y)
                        
                        # Enemy shooting
                        if random.random() < 0.02:  # Occasional shooting
                            bullet = enemy.shoot(player.x, player.y)
                            if bullet:
                                bullets.append(bullet)
                        
                        # Check collision with player
                        if check_collision(enemy.x, enemy.y, enemy.radius, 
                                          player.x, player.y, player.radius):
                            if player.take_damage(enemy.damage):
                                particles.extend(create_explosion(player.x, player.y, 1.5, WHITE))
                                if explosion_sound:
                                    explosion_sound.play()
                            
                            particles.extend(create_explosion(enemy.x, enemy.y, 1.0, enemy.color))
                            enemies.remove(enemy)
                            player.score += enemy.score_value // 2  # Half points for collision
                            
                            if explosion_sound:
                                explosion_sound.play()
                    
                    # Update bullets
                    for bullet in bullets[:]:
                        if not bullet.update():
                            bullets.remove(bullet)
                            continue
                        
                        # Check collision with player
                        if bullet.owner == 'enemy' and check_collision(
                                bullet.x, bullet.y, bullet.radius, 
                                player.x, player.y, player.radius):
                            if player.take_damage(bullet.power * 10):
                                particles.extend(create_explosion(bullet.x, bullet.y, 0.5, GREEN))
                            bullets.remove(bullet)
                            continue
                        
                        # Check collision with enemies
                        for enemy in enemies[:]:
                            if bullet.owner == 'player' and check_collision(
                                    bullet.x, bullet.y, bullet.radius,
                                    enemy.x, enemy.y, enemy.radius):
                                if enemy.take_damage(bullet.power * 10):
                                    particles.extend(create_explosion(enemy.x, enemy.y, 1.0, enemy.color))
                                    enemies.remove(enemy)
                                    player.score += enemy.score_value
                                    
                                    # Chance to drop upgrade
                                    if random.random() < 0.2:
                                        upgrades.append(Upgrade(enemy.x, enemy.y, 
                                                              random.choice(UPGRADE_TYPES)))
                                    
                                    if explosion_sound:
                                        explosion_sound.play()
                                else:
                                    particles.extend(create_explosion(bullet.x, bullet.y, 0.3, RED))
                                
                                bullets.remove(bullet)
                                break
                        
                        # Check collision with planets
                        for planet in planets:
                            if check_collision(bullet.x, bullet.y, bullet.radius,
                                             planet.x, planet.y, planet.radius):
                                particles.extend(create_explosion(bullet.x, bullet.y, 0.3))
                                bullets.remove(bullet)
                                break
                    
                    # Update upgrades
                    for upgrade in upgrades[:]:
                        upgrade.update()
                        
                        # Check collision with player
                        if check_collision(upgrade.x, upgrade.y, upgrade.radius,
                                         player.x, player.y, player.radius):
                            # Apply upgrade effect
                            if upgrade.type == 'fuel':
                                player.fuel = player.max_fuel
                            elif upgrade.type == 'shield':
                                player.shield = player.max_shield
                            elif upgrade.type == 'weapon':
                                player.weapon_level += 1
                                player.weapon_power += 0.5
                            elif upgrade.type == 'engine':
                                player.engine_level += 1
                            
                            upgrades.remove(upgrade)
                            
                            if upgrade_sound:
                                upgrade_sound.play()
                    
                    # Update particles
                    particles = [p for p in particles if p.update()]
                    
                    # Check for collision with planets
                    for planet in planets:
                        if check_collision(player.x, player.y, player.radius,
                                         planet.x, planet.y, planet.radius):
                            # Crash into planet
                            particles.extend(create_explosion(player.x, player.y, 2.0, WHITE))
                            player.shield = 0
                            
                            if explosion_sound:
                                explosion_sound.play()
                    
                    # Check player status
                    if player.shield <= 0:
                        game_state = GAME_OVER
                    
                    # Check if level is complete (all enemies destroyed)
                    if len(enemies) == 0:
                        game_state = LEVEL_COMPLETE
                
                # Draw game objects
                # Draw planets
                for planet in planets:
                    planet.draw(screen)
                
                # Draw upgrades
                for upgrade in upgrades:
                    upgrade.draw(screen)
                
                # Draw bullets
                for bullet in bullets:
                    bullet.draw(screen)
                
                # Draw enemies
                for enemy in enemies:
                    enemy.draw(screen)
                
                # Draw player
                player.draw(screen)
                
                # Draw particles
                for particle in particles:
                    particle.draw(screen)
                
                # Draw UI
                draw_ui(screen, player, current_level, game_state)
            
            # Update display
            pygame.display.flip()
            clock.tick(FPS)
    
    finally:
        # Clean up
        pygame.quit()

if __name__ == "__main__":
    main()