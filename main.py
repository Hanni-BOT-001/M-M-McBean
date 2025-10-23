import pygame
import random
import sys
from PIL import Image
import numpy as np
import math
import os

# Font selection: prioritize system fonts that support Chinese characters
def get_cjk_font(size, bold=False, italic=False):
    """Return a font object that supports Chinese as much as possible, fallback to default if not found"""
    # 1) Prioritize loading from local fonts directory (recommended to put fonts in ./fonts)
    local_font_dir = os.path.join(os.path.dirname(__file__), "fonts")
    local_candidates = [
        "NotoSansSC-Regular.otf", "NotoSansSC-Regular.ttf",
        "SourceHanSansSC-Regular.otf", "SourceHanSansSC-Regular.ttf",
        "SourceHanSansCN-Regular.otf", "SourceHanSansCN-Regular.ttf",
        "MiSans-Regular.ttf", "LXGWWenKai-Regular.ttf",
    ]
    if os.path.isdir(local_font_dir):
        for fname in local_candidates:
            fpath = os.path.join(local_font_dir, fname)
            if os.path.exists(fpath):
                try:
                    return pygame.font.Font(fpath, size)
                except Exception:
                    pass

    # 2) Then try common Chinese fonts in system fonts
    candidates = [
        "Microsoft YaHei UI",
        "Microsoft YaHei",
        "SimHei",
        "SimSun",
        "NSimSun",
        "DengXian",
        "KaiTi",
        "FangSong",
        "PingFang SC",
        "Hiragino Sans GB",
        "Noto Sans CJK SC",
        "Source Han Sans SC",
        "Arial Unicode MS",
    ]
    for name in candidates:
        try:
            path = pygame.font.match_font(name, bold=bold, italic=italic)
        except TypeError:
            # Older pygame versions don't support keyword arguments
            path = pygame.font.match_font(name)
        if path:
            try:
                return pygame.font.Font(path, size)
            except Exception:
                continue
    # Fallback to default font (may not support Chinese, will display squares)
    return pygame.font.Font(None, size)


# Music Manager
class MusicManager:
    """Manages background music fade in/out and playback"""
    def __init__(self):
        self.music_file = "background_sound.mp3"  # Use specified music file
        self.is_playing = False
        self.fade_out_duration = 2000  # milliseconds
        self.current_volume = 0.7  # default volume
    
    def load_music(self):
        """Load music file"""
        if not AUDIO_ENABLED:
            return
        
        try:
            # Check specified music file
            if os.path.exists(self.music_file):
                pygame.mixer.music.load(self.music_file)
                print(f"Loaded music: {self.music_file}")
            else:
                # Try other common music files
                for alt_file in ["music.mp3", "bg_music.mp3", "music.wav", "bg.ogg"]:
                    if os.path.exists(alt_file):
                        self.music_file = alt_file
                        pygame.mixer.music.load(self.music_file)
                        print(f"Loaded music: {self.music_file}")
                        return
                print(f"Music file not found: {self.music_file}")
        except Exception as e:
            print(f"Failed to load music: {e}")
    
    def play(self, loops=0):
        """Play music (loops=-1 for infinite loop, 0 for play once)"""
        if not AUDIO_ENABLED or self.is_playing:
            return
        try:
            pygame.mixer.music.play(loops)
            pygame.mixer.music.set_volume(self.current_volume)
            self.is_playing = True
        except Exception as e:
            print(f"Failed to play music: {e}")
    
    def fadeout(self, duration_ms):
        """Fade out music"""
        if not AUDIO_ENABLED:
            return
        try:
            pygame.mixer.music.fadeout(duration_ms)
            self.is_playing = False
        except Exception as e:
            print(f"Failed to fadeout music: {e}")
    
    def set_volume(self, volume):
        """Set volume (0.0-1.0)"""
        self.current_volume = max(0.0, min(1.0, volume))
        if AUDIO_ENABLED:
            try:
                pygame.mixer.music.set_volume(self.current_volume)
            except Exception as e:
                print(f"Failed to set music volume: {e}")


# Sound Effects Manager
class SoundEffectManager:
    """Manages game sound effects"""
    def __init__(self):
        self.shoot_sound = None
        self.transition_sound = None
        self.load_sounds()
    
    def load_sounds(self):
        """Load sound effect files"""
        if not AUDIO_ENABLED:
            return
        
        try:
            # Load shoot sound effect
            if os.path.exists("shoot.mp3"):
                self.shoot_sound = pygame.mixer.Sound("shoot.mp3")
            elif os.path.exists("shoot.wav"):
                self.shoot_sound = pygame.mixer.Sound("shoot.wav")
            else:
                print("shoot.mp3 or shoot.wav not found")
            
            # Load transition sound effect
            if os.path.exists("bullet_change.mp3"):
                self.transition_sound = pygame.mixer.Sound("bullet_change.mp3")
            elif os.path.exists("bullet_change.wav"):
                self.transition_sound = pygame.mixer.Sound("bullet_change.wav")
            else:
                print("bullet_change.mp3 or bullet_change.wav not found")
        except Exception as e:
            print(f"Failed to load sound effects: {e}")
    
    def play_shoot(self):
        """Play shoot sound effect"""
        if not AUDIO_ENABLED or self.shoot_sound is None:
            return
        
        try:
            self.shoot_sound.play()
        except Exception as e:
            print(f"Failed to play shoot sound: {e}")
    
    def play_transition(self):
        """Play transition sound effect"""
        if not AUDIO_ENABLED or self.transition_sound is None:
            return
        
        try:
            self.transition_sound.play()
        except Exception as e:
            print(f"Failed to play transition sound: {e}")

# Overwatch style font selection (Big Noodle Titling, etc.)
def get_overwatch_font(size, bold=False, italic=False):
    """Try to load Overwatch style fonts (Big Noodle Titling), fallback to similar system fonts or default."""
    local_font_dir = os.path.join(os.path.dirname(__file__), "fonts")
    local_candidates = [
        "Overwatch.ttf", "Overwatch.otf",
        "BigNoodleTitling.ttf", "BigNoodleTitling.otf",
        "BigNoodleTitlingOblique.otf", "BigNoodleTitlingOblique.ttf",
    ]
    if os.path.isdir(local_font_dir):
        for fname in local_candidates:
            fpath = os.path.join(local_font_dir, fname)
            if os.path.exists(fpath):
                try:
                    return pygame.font.Font(fpath, size)
                except Exception:
                    pass

    # Common system font names (not necessarily identical, but similar style)
    candidates = [
        "Big Noodle Titling",
        "BigNoodleTitling",
        "Futura Condensed ExtraBold",
        "Futura Condensed",
        "Futura",
        "DIN Condensed",
        "Impact",
        "Arial Narrow",
    ]
    for name in candidates:
        try:
            path = pygame.font.match_font(name, bold=bold, italic=italic)
        except TypeError:
            path = pygame.font.match_font(name)
        if path:
            try:
                return pygame.font.Font(path, size)
            except Exception:
                continue
    return pygame.font.Font(None, size)

# Initialize Pygame
pygame.init()

# Initialize Pygame mixer (audio)
try:
    pygame.mixer.init()
    AUDIO_ENABLED = True
except Exception as e:
    print(f"Audio initialization failed: {e}")
    AUDIO_ENABLED = False

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 206, 235)  # Sky blue
SAND = (238, 214, 175)  # Desert color
BROWN = (139, 90, 43)

# Extract colors from background image
def extract_background_colors(image_path="background2.jpg"):
    """Extract main colors and regions from background image"""
    try:
        img = Image.open(image_path)
        img = img.resize((SCREEN_WIDTH, SCREEN_HEIGHT))
        img_array = np.array(img)
        
        # Divide image into different regions to extract main colors
        height, width = img_array.shape[:2]
        
        # Top sky region (0-40%)
        sky_region = img_array[0:int(height*0.4), :]
        sky_color = tuple(np.mean(sky_region, axis=(0, 1)).astype(int).tolist())
        
        # Middle region (40-70%)
        middle_region = img_array[int(height*0.4):int(height*0.7), :]
        middle_color = tuple(np.mean(middle_region, axis=(0, 1)).astype(int).tolist())
        
        # Bottom ground region (70-100%)
        ground_region = img_array[int(height*0.7):, :]
        ground_color = tuple(np.mean(ground_region, axis=(0, 1)).astype(int).tolist())
        
        return {
            'sky': sky_color,
            'middle': middle_color,
            'ground': ground_color,
            'full_array': img_array
        }
    except Exception as e:
        print(f"Failed to load background image: {e}")
        # Return default colors
        return {
            'sky': (135, 206, 235),
            'middle': (200, 180, 150),
            'ground': (238, 214, 175),
            'full_array': None
        }

# Extract background colors
BG_COLORS = extract_background_colors()
SKY_COLOR = BG_COLORS['sky']
MIDDLE_COLOR = BG_COLORS['middle']
GROUND_COLOR = BG_COLORS['ground']

# Game states
STATE_INTRO = 0
STATE_WALK = 1
STATE_GAMEPLAY = 2
STATE_GAMEOVER = 3


def pixelate_image(image_path, target_size=(100, 100), pixel_size=4):
    """Convert image to pixel art style"""
    try:
        img = Image.open(image_path)
        # Maintain original image aspect ratio
        img.thumbnail(target_size, Image.Resampling.LANCZOS)
        
        # Convert to RGBA to maintain transparency
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        img_array = np.array(img)
        height, width = img_array.shape[:2]
        
        # Create pixelated image array
        pixelated = np.zeros_like(img_array)
        
        for y in range(0, height, pixel_size):
            for x in range(0, width, pixel_size):
                y_end = min(y + pixel_size, height)
                x_end = min(x + pixel_size, width)
                
                # Get region
                region = img_array[y:y_end, x:x_end]
                
                # If region is mostly transparent, keep transparent
                alpha_values = region[:, :, 3]
                avg_alpha = np.mean(alpha_values)
                
                if avg_alpha < 50:  # Mostly transparent
                    pixel_color = [0, 0, 0, 0]
                else:
                    # Use center point color
                    y_center = min(y + pixel_size // 2, height - 1)
                    x_center = min(x + pixel_size // 2, width - 1)
                    center_color = img_array[y_center, x_center].copy()
                    
                    # Enhance color saturation, reduce gray
                    rgb = center_color[:3].astype(float)
                    
                    # If not close to black or white, enhance saturation
                    brightness = np.mean(rgb)
                    if 30 < brightness < 225:
                        # Find max and min color channels
                        max_val = np.max(rgb)
                        min_val = np.min(rgb)
                        
                        # If color is too gray, slightly enhance contrast
                        if max_val - min_val < 50:  # Color too gray
                            # Overall enhance contrast while maintaining hue
                            rgb = np.clip((rgb - 128) * 1.15 + 128, 0, 255)
                        else:
                            # Non-gray regions slightly enhance contrast
                            rgb = np.clip((rgb - 128) * 1.05 + 128, 0, 255)
                    
                    center_color[:3] = rgb.astype(np.uint8)
                    pixel_color = center_color.tolist()
                
                # Fill pixel block
                pixelated[y:y_end, x:x_end] = pixel_color
        
        # Convert back to PIL image
        pixelated_img = Image.fromarray(pixelated.astype('uint8'), 'RGBA')
        
        # Create pygame surface
        mode = pixelated_img.mode
        size = pixelated_img.size
        data = pixelated_img.tobytes()
        
        py_image = pygame.image.fromstring(data, size, mode)
        
        # Adjust to target size
        final_surface = pygame.Surface(target_size, pygame.SRCALPHA)
        # Center draw
        x_offset = (target_size[0] - size[0]) // 2
        y_offset = (target_size[1] - size[1]) // 2
        final_surface.blit(py_image, (x_offset, y_offset))
        
        # Add outline
        # Create outline surface
        outline_surface = pygame.Surface(target_size, pygame.SRCALPHA)
        outline_color = (0, 0, 0, 255)  # Black outline
        
        # Detect edges and draw outline
        for y in range(target_size[1]):
            for x in range(target_size[0]):
                try:
                    current_alpha = final_surface.get_at((x, y))[3]
                    
                    if current_alpha > 128:  # Current pixel opaque
                        # Check if neighboring pixels are transparent
                        is_edge = False
                        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < target_size[0] and 0 <= ny < target_size[1]:
                                neighbor_alpha = final_surface.get_at((nx, ny))[3]
                                if neighbor_alpha < 128:  # Neighbor transparent
                                    is_edge = True
                                    break
                            else:
                                is_edge = True
                                break
                        
                        if is_edge:
                            outline_surface.set_at((x, y), outline_color)
                except:
                    pass
        
        # Merge outline
        final_with_outline = pygame.Surface(target_size, pygame.SRCALPHA)
        final_with_outline.blit(final_surface, (0, 0))
        final_with_outline.blit(outline_surface, (0, 0))
        
        return final_with_outline
        
    except Exception as e:
        print(f"Failed to load image {image_path}: {e}")
        # Return placeholder
        surface = pygame.Surface(target_size, pygame.SRCALPHA)
        surface.fill((255, 220, 0))
        return surface


class Player:
    """Player character class (McBean)"""
    def __init__(self):
        # Load pixelated images, size increased to 125x125 (1.25x original 100)
        self.image_normal = pixelate_image("huangdou.png", (125, 125), pixel_size=3)
        self.image_shoot = pixelate_image("huangdou2.png", (125, 125), pixel_size=3)
        
        self.current_image = self.image_normal
        self.rect = self.current_image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
        self.is_shooting = False
        self.shoot_timer = 0
    
    def shoot(self):
        """Shooting action"""
        self.is_shooting = True
        self.shoot_timer = 10  # Show shooting state for 10 frames
        self.current_image = self.image_shoot
    
    def update(self):
        """Update player state"""
        if self.is_shooting:
            self.shoot_timer -= 1
            if self.shoot_timer <= 0:
                self.is_shooting = False
                self.current_image = self.image_normal
    
    def draw(self, screen):
        """Draw player"""
        screen.blit(self.current_image, self.rect)


class Plate:
    """Flying disc/plate class"""
    def __init__(self):
        self.width = 60
        self.height = 40
        
        # Four flying trajectories
        self.trajectory = random.randint(0, 3)
        
        if self.trajectory == 0:
            # From bottom-right to top-left
            self.x = SCREEN_WIDTH + 50
            self.y = SCREEN_HEIGHT - 100
            self.speed_x = random.uniform(-3, -2)  # Move left
            self.start_y = SCREEN_HEIGHT - 100
            self.end_y = SCREEN_HEIGHT * 0.1
            
        elif self.trajectory == 1:
            # From top-right to bottom-left
            self.x = SCREEN_WIDTH + 50
            self.y = SCREEN_HEIGHT * 0.1
            self.speed_x = random.uniform(-3, -2)  # Move left
            self.start_y = SCREEN_HEIGHT * 0.1
            self.end_y = SCREEN_HEIGHT - 100
            
        elif self.trajectory == 2:
            # From top-left to bottom-right
            self.x = -50
            self.y = SCREEN_HEIGHT * 0.1
            self.speed_x = random.uniform(2, 3)  # Move right
            self.start_y = SCREEN_HEIGHT * 0.1
            self.end_y = SCREEN_HEIGHT - 100
            
        else:  # trajectory == 3
            # From bottom-left to top-right
            self.x = -50
            self.y = SCREEN_HEIGHT - 100
            self.speed_x = random.uniform(2, 3)  # Move right
            self.start_y = SCREEN_HEIGHT - 100
            self.end_y = SCREEN_HEIGHT * 0.1
        
        # Parabolic motion parameters
        self.distance_traveled = 0
        self.total_distance = SCREEN_WIDTH + 100
        
        self.color = (200, 200, 200)
        self.alive = True
        self.broken = False
        self.broken_pieces = []
    
    def update(self):
        """Update disc position"""
        if not self.broken:
            self.x += self.speed_x
            self.distance_traveled += abs(self.speed_x)
            
            # Calculate progress (0 to 1)
            progress = min(1.0, self.distance_traveled / self.total_distance)
            
            # Linear move to target height
            self.y = self.start_y + (self.end_y - self.start_y) * progress
            
            # Add parabolic curve (curve most at center)
            parabola_factor = 4 * progress * (1 - progress)  # Max value 1 at progress=0.5
            
            # Add parabolic offset based on trajectory direction
            if self.trajectory in [0, 3]:  # Upward trajectories, curve upward
                parabola_offset = parabola_factor * 100  # Curve up
            else:  # Downward trajectories, curve downward
                parabola_offset = parabola_factor * (-100)  # Curve down
            
            self.y += parabola_offset
            
            # Disc flies off screen
            if self.x < -100 or self.x > SCREEN_WIDTH + 100:
                self.alive = False
        else:
            # Update broken pieces
            for piece in self.broken_pieces:
                piece['x'] += piece['vx']
                piece['y'] += piece['vy']
                piece['vy'] += 0.5  # Gravity
            
            # Check if all pieces have fallen off screen
            if all(p['y'] > SCREEN_HEIGHT for p in self.broken_pieces):
                self.alive = False
    
    def break_plate(self):
        """Break the disc"""
        self.broken = True
        # Create pieces
        for _ in range(8):
            piece = {
                'x': self.x,
                'y': self.y,
                'vx': random.uniform(-3, 3),
                'vy': random.uniform(-5, -1),
                'size': random.randint(5, 15)
            }
            self.broken_pieces.append(piece)
    
    def draw(self, screen):
        """Draw disc"""
        if not self.broken:
            # Draw intact disc (ellipse)
            pygame.draw.ellipse(screen, self.color, 
                              (int(self.x - self.width/2), int(self.y - self.height/2), 
                               self.width, self.height))
            pygame.draw.ellipse(screen, BLACK, 
                              (int(self.x - self.width/2), int(self.y - self.height/2), 
                               self.width, self.height), 2)
        else:
            # Draw pieces
            for piece in self.broken_pieces:
                pygame.draw.circle(screen, self.color, 
                                 (int(piece['x']), int(piece['y'])), piece['size'])
    
    def is_clicked(self, pos):
        """Check if clicked"""
        if self.broken:
            return False
        dist_x = abs(pos[0] - self.x)
        dist_y = abs(pos[1] - self.y)
        return dist_x < self.width/2 and dist_y < self.height/2


class Tumbleweed:
    """Tumbleweed class"""
    def __init__(self):
        self.x = -50
        self.y = SCREEN_HEIGHT - 100
        self.size = 40
        self.rotation = 0
        self.speed = 3
        # Pixel art style colors
        self.brown_dark = (101, 67, 33)
        self.brown_medium = (139, 90, 43)
        self.brown_light = (160, 110, 60)
    
    def update(self):
        """Update position"""
        self.x += self.speed
        self.rotation += 5
    
    def draw(self, screen):
        """Draw pixel art style hollow tumbleweed"""
        center_x = int(self.x)
        center_y = int(self.y)
        
        # Build tumbleweed's hollow sphere structure using pixel blocks
        pixel_size = 6  # Doubled from 3 to 6
        
        # Draw multi-layer circular structure to create hollow effect
        # Outer layer
        for angle in range(0, 360, 20):  # Adjust interval to avoid density
            rad = math.radians(angle + self.rotation)
            # Outer circle branches
            for r in range(int(self.size * 0.6), self.size, pixel_size):
                x = center_x + int(r * math.cos(rad))
                y = center_y + int(r * math.sin(rad))
                
                # Randomly choose light/dark color for layered effect
                if (angle + self.rotation) % 40 < 20:
                    color = self.brown_dark
                else:
                    color = self.brown_medium
                
                pygame.draw.circle(screen, color, (x, y), pixel_size // 2)
        
        # Draw crossed branches to create web structure
        num_branches = 10  # Slightly reduce to avoid density
        for i in range(num_branches):
            angle = (360 / num_branches) * i + self.rotation
            rad = math.radians(angle)
            
            # Branches extending from center
            for dist in range(pixel_size, self.size, pixel_size * 2):
                x = center_x + int(dist * math.cos(rad))
                y = center_y + int(dist * math.sin(rad))
                
                # Choose color based on distance
                if dist < self.size * 0.5:
                    color = self.brown_light
                elif dist < self.size * 0.75:
                    color = self.brown_medium
                else:
                    color = self.brown_dark
                
                pygame.draw.rect(screen, color, (x - pixel_size//2, y - pixel_size//2, pixel_size, pixel_size))
        
        # Add some random branch fragments for detail
        for i in range(12):  # Slightly reduce quantity
            angle = (360 / 12) * i + self.rotation * 0.5
            rad = math.radians(angle)
            dist = self.size * 0.7
            x = center_x + int(dist * math.cos(rad))
            y = center_y + int(dist * math.sin(rad))
            
            # Draw small pixel blocks, also doubled
            pygame.draw.rect(screen, self.brown_medium, (x - 2, y - 2, 4, 4))


class Game:
    """Main game class"""
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("M&M McBean")
        self.clock = pygame.time.Clock()
        self.bg_surface = self.create_background()
        self.state = STATE_INTRO
        self.player = Player()
        self.plates = []
        self.tumbleweed = None
        self.score = 0
        self.bullets = 6
        self.round = 1
        self.total_rounds = 1  # Changed to 1 round
        self.round_hits = 0  # Hits in current round
        self.round_results = []  # Store each round's result [(hits, total), ...]
        self.intro_timer = 0
        self.walk_timer = 0
        self.player_walk_x = -100
        self.spawn_timer = 0
        # Use Overwatch style font (local fonts/ or system match), unified English display
        self.font = get_overwatch_font(36)
        self.big_font = get_overwatch_font(72)
        self.selected_option = 0  # Game over screen selected option 0=restart, 1=quit
        # Music management
        self.music_manager = MusicManager()
        self.music_manager.load_music()
        # Start music immediately when game launches, play once (loops=0)
        self.music_manager.play(loops=0)
        # Sound effects management
        self.sound_effects = SoundEffectManager()
    
    def create_background(self):
        """Create pixelated background based on background image"""
        bg_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        if BG_COLORS['full_array'] is not None:
            # Use actual image to create pixelated background
            img_array = BG_COLORS['full_array']
            pixel_size = 4  # Smaller pixel block size for clearer edges
            
            for y in range(0, SCREEN_HEIGHT, pixel_size):
                for x in range(0, SCREEN_WIDTH, pixel_size):
                    # Get center point color of region instead of average, maintain edge clarity
                    y_center = min(y + pixel_size // 2, SCREEN_HEIGHT - 1)
                    x_center = min(x + pixel_size // 2, SCREEN_WIDTH - 1)
                    
                    # Use center point color
                    center_color = tuple(img_array[y_center, x_center].tolist())
                    
                    # Check color variation in region (edge detection)
                    y_end = min(y + pixel_size, SCREEN_HEIGHT)
                    x_end = min(x + pixel_size, SCREEN_WIDTH)
                    region = img_array[y:y_end, x:x_end]
                    
                    # Calculate color standard deviation, large variation indicates edges
                    std_dev = np.std(region, axis=(0, 1))
                    is_edge = np.mean(std_dev) > 15  # Edge threshold
                    
                    if is_edge:
                        # Edge region use smaller blocks or median color
                        median_color = tuple(np.median(region, axis=(0, 1)).astype(int).tolist())
                        pygame.draw.rect(bg_surface, median_color, 
                                       (x, y, pixel_size, pixel_size))
                    else:
                        # Non-edge region use center color
                        pygame.draw.rect(bg_surface, center_color, 
                                       (x, y, pixel_size, pixel_size))
        else:
            # Use extracted colors to create gradient background
            # Top sky
            for y in range(0, int(SCREEN_HEIGHT * 0.4)):
                color_ratio = y / (SCREEN_HEIGHT * 0.4)
                color = tuple(int(SKY_COLOR[i] * (1 - color_ratio * 0.3)) for i in range(3))
                pygame.draw.line(bg_surface, color, (0, y), (SCREEN_WIDTH, y))
            
            # Middle
            for y in range(int(SCREEN_HEIGHT * 0.4), int(SCREEN_HEIGHT * 0.7)):
                pygame.draw.line(bg_surface, MIDDLE_COLOR, (0, y), (SCREEN_WIDTH, y))
            
            # Bottom ground
            for y in range(int(SCREEN_HEIGHT * 0.7), SCREEN_HEIGHT):
                pygame.draw.line(bg_surface, GROUND_COLOR, (0, y), (SCREEN_WIDTH, y))
        
        return bg_surface
    
    def reset_round(self):
        """Reset round"""
        self.plates = []
        self.bullets = 6
        self.round_hits = 0  # Reset current round hits
        self.spawn_timer = 0
    
    def handle_events(self):
        """Handle events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.MOUSEBUTTONDOWN and self.state == STATE_GAMEPLAY:
                if self.bullets > 0:
                    # Check if disc is hit
                    pos = pygame.mouse.get_pos()
                    hit = False
                    for plate in self.plates:
                        if plate.is_clicked(pos) and not plate.broken:
                            plate.break_plate()
                            self.score += 1
                            self.round_hits += 1
                            hit = True
                            break
                    
                    # Shoot (whether hit or not)
                    self.bullets -= 1
                    self.player.shoot()
                    # Play shoot sound effect
                    self.sound_effects.play_shoot()
                    
                    # If this is the 6th bullet (last bullet), settle round immediately
                    if self.bullets == 0:
                        # Play transition sound effect
                        self.sound_effects.play_transition()
                        # Record this round's result
                        self.round_results.append((self.round_hits, 6))
                        
                        if self.round < self.total_rounds:
                            self.round += 1
                            self.reset_round()
                        else:
                            # All rounds complete, enter game over state
                            self.state = STATE_GAMEOVER
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.state == STATE_GAMEOVER:
                    # Restart game
                    if self.selected_option == 0:
                        # Fade out music then reinitialize
                        self.music_manager.fadeout(2000)
                        self.__init__()
                    else:
                        # Fade out music when quitting
                        self.music_manager.fadeout(2000)
                        import time
                        time.sleep(2.1)  # Wait for fadeout to complete
                        return False
                
                # Game over screen up/down key selection
                if self.state == STATE_GAMEOVER:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.selected_option = 0
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.selected_option = 1
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        # Enter key to confirm selection
                        if self.selected_option == 0:
                            # Fade out music then reinitialize
                            self.music_manager.fadeout(2000)
                            self.__init__()
                        else:
                            # Fade out music when quitting
                            self.music_manager.fadeout(2000)
                            import time
                            time.sleep(2.1)  # Wait for fadeout to complete
                            return False
        
        return True
    
    def update(self):
        """Update game logic"""
        if self.state == STATE_INTRO:
            # Intro screen, show McBean character
            self.intro_timer += 1
            if self.intro_timer > 120:  # After 2 seconds, enter walk scene
                self.state = STATE_WALK
                self.tumbleweed = Tumbleweed()
        
        elif self.state == STATE_WALK:
            # McBean walks into desert
            self.walk_timer += 1
            self.player_walk_x += 2
            
            # Update tumbleweed
            if self.tumbleweed:
                self.tumbleweed.update()
            
            if self.walk_timer > 180:  # After 3 seconds, enter gameplay
                self.state = STATE_GAMEPLAY
                self.player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
        
        elif self.state == STATE_GAMEPLAY:
            # Game in progress
            self.player.update()
            
            # Spawn discs
            self.spawn_timer += 1
            if self.spawn_timer > 60 and len(self.plates) < 3:  # Spawn every second, max 3
                self.plates.append(Plate())
                self.spawn_timer = 0
            
            # Update discs
            for plate in self.plates[:]:
                plate.update()
                if not plate.alive:
                    self.plates.remove(plate)
    
    def draw(self):
        """Draw game screen"""
        if self.state == STATE_INTRO:
            # Intro screen
            self.screen.blit(self.bg_surface, (0, 0))
            # Center display McBean
            temp_rect = self.player.image_normal.get_rect()
            temp_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            self.screen.blit(self.player.image_normal, temp_rect)
            
            title = self.big_font.render("M&M McBean", True, BLACK)
            title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
            self.screen.blit(title, title_rect)
        
        elif self.state == STATE_WALK:
            # Desert scene
            self.screen.blit(self.bg_surface, (0, 0))
            
            # Draw tumbleweed
            if self.tumbleweed:
                self.tumbleweed.draw(self.screen)
            
            # Draw walking McBean
            temp_rect = self.player.image_normal.get_rect()
            temp_rect.center = (self.player_walk_x, SCREEN_HEIGHT - 100)
            self.screen.blit(self.player.image_normal, temp_rect)
        
        elif self.state == STATE_GAMEPLAY:
            # Game screen
            self.screen.blit(self.bg_surface, (0, 0))
            
            # Draw discs
            for plate in self.plates:
                plate.draw(self.screen)
            
            # Draw player
            self.player.draw(self.screen)
            
            # UI (English with OW font)
            # Bullets
            bullet_text = self.font.render(f"Bullets: {self.bullets}", True, BLACK)
            self.screen.blit(bullet_text, (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 50))
            
            # Score
            score_text = self.font.render(f"Score: {self.score}", True, BLACK)
            self.screen.blit(score_text, (20, 20))
            
            # Round
            round_text = self.font.render(f"Round: {self.round}/{self.total_rounds}", True, BLACK)
            self.screen.blit(round_text, (20, 60))
        
        elif self.state == STATE_GAMEOVER:
            # Game Over screen - Black background with white text
            self.screen.fill(BLACK)
            
            gameover_text = self.big_font.render("GAME OVER!", True, WHITE)
            gameover_rect = gameover_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
            self.screen.blit(gameover_text, gameover_rect)
            
            # Final Score
            score_text = self.big_font.render(f"FINAL SCORE: {self.score}/6", True, WHITE)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
            self.screen.blit(score_text, score_rect)
            
            # Hit ratio
            if self.round_results:
                hits, total = self.round_results[0]
                ratio_text = self.font.render(f"HIT RATIO: {hits}/{total}", True, WHITE)
                ratio_rect = ratio_text.get_rect(center=(SCREEN_WIDTH // 2, 280))
                self.screen.blit(ratio_text, ratio_rect)
            
            # Options menu
            menu_y = 360
            
            # Option 1: Restart
            restart_color = (100, 255, 100) if self.selected_option == 0 else WHITE
            restart_text = self.font.render(("▶ RESTART" if self.selected_option == 0 else "  RESTART"), True, restart_color)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, menu_y))
            self.screen.blit(restart_text, restart_rect)
            
            # Option 2: Quit
            quit_color = (255, 100, 100) if self.selected_option == 1 else WHITE
            quit_text = self.font.render(("▶ QUIT" if self.selected_option == 1 else "  QUIT"), True, quit_color)
            quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, menu_y + 50))
            self.screen.blit(quit_text, quit_rect)
            
            # Hint text
            hint_text = self.font.render("Use ↑↓ to select, Enter/Space to confirm", True, (180, 180, 180))
            hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, menu_y + 120))
            self.screen.blit(hint_text, hint_rect)
        
        pygame.display.flip()
    
    def run(self):
        """Game main loop"""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()


def main():
    """Main function"""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
