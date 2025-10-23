import pygame
import random
import sys
from PIL import Image
import numpy as np
import math
import os

# 字体选择：优先选择支持中文的系统字体
def get_cjk_font(size, bold=False, italic=False):
    """返回一个尽可能支持中文的字体对象，如果找不到则退回默认字体"""
    # 1) 优先从项目本地 fonts 目录加载（推荐把字体放到 ./fonts 下）
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

    # 2) 其次尝试系统字体中常见的中文字体
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
            # 旧版pygame不支持关键字参数
            path = pygame.font.match_font(name)
        if path:
            try:
                return pygame.font.Font(path, size)
            except Exception:
                continue
    # 回退到默认字体（可能不支持中文，会显示方块）
    return pygame.font.Font(None, size)


# 音乐管理器
class MusicManager:
    """管理背景音乐淡入淡出和播放"""
    def __init__(self):
        self.music_file = "background_sound.mp3"  # 使用指定的音乐文件
        self.is_playing = False
        self.fade_out_duration = 2000  # 毫秒
        self.current_volume = 0.7  # 默认音量
    
    def load_music(self):
        """加载音乐文件"""
        if not AUDIO_ENABLED:
            return
        
        try:
            # 检查指定的音乐文件
            if os.path.exists(self.music_file):
                pygame.mixer.music.load(self.music_file)
                print(f"Loaded music: {self.music_file}")
            else:
                # 尝试其他常见的音乐文件
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
        """播放音乐（loops=-1表示无限循环，0表示播放一次）"""
        if not AUDIO_ENABLED or self.is_playing:
            return
        try:
            pygame.mixer.music.play(loops)
            pygame.mixer.music.set_volume(self.current_volume)
            self.is_playing = True
        except Exception as e:
            print(f"Failed to play music: {e}")
    
    def fadeout(self, duration_ms):
        """淡出音乐"""
        if not AUDIO_ENABLED:
            return
        try:
            pygame.mixer.music.fadeout(duration_ms)
            self.is_playing = False
        except Exception as e:
            print(f"Failed to fadeout music: {e}")
    
    def set_volume(self, volume):
        """设置音量 (0.0-1.0)"""
        self.current_volume = max(0.0, min(1.0, volume))
        if AUDIO_ENABLED:
            try:
                pygame.mixer.music.set_volume(self.current_volume)
            except Exception as e:
                print(f"Failed to set music volume: {e}")


# 音效管理器
class SoundEffectManager:
    """管理游戏音效"""
    def __init__(self):
        self.shoot_sound = None
        self.transition_sound = None
        self.load_sounds()
    
    def load_sounds(self):
        """加载音效文件"""
        if not AUDIO_ENABLED:
            return
        
        try:
            # 加载射击音效
            if os.path.exists("shoot.mp3"):
                self.shoot_sound = pygame.mixer.Sound("shoot.mp3")
            elif os.path.exists("shoot.wav"):
                self.shoot_sound = pygame.mixer.Sound("shoot.wav")
            else:
                print("shoot.mp3 or shoot.wav not found")
            
            # 加载过度音效
            if os.path.exists("bullet_change.mp3"):
                self.transition_sound = pygame.mixer.Sound("bullet_change.mp3")
            elif os.path.exists("bullet_change.wav"):
                self.transition_sound = pygame.mixer.Sound("bullet_change.wav")
            else:
                print("bullet_change.mp3 or bullet_change.wav not found")
        except Exception as e:
            print(f"Failed to load sound effects: {e}")
    
    def play_shoot(self):
        """播放射击音效"""
        if not AUDIO_ENABLED or self.shoot_sound is None:
            return
        
        try:
            self.shoot_sound.play()
        except Exception as e:
            print(f"Failed to play shoot sound: {e}")
    
    def play_transition(self):
        """播放过度音效"""
        if not AUDIO_ENABLED or self.transition_sound is None:
            return
        
        try:
            self.transition_sound.play()
        except Exception as e:
            print(f"Failed to play transition sound: {e}")
        
    def load_music(self):
        """尝试加载音乐文件"""
        if not AUDIO_ENABLED:
            return False
        
        try:
            if os.path.exists(self.music_file):
                pygame.mixer.music.load(self.music_file)
                return True
            else:
                # 尝试常见的音乐文件名
                for name in ["music.mp3", "music.wav", "music.ogg", "bg_music.mp3"]:
                    if os.path.exists(name):
                        pygame.mixer.music.load(name)
                        return True
                print(f"Music file not found. Create '{self.music_file}' or 'music.mp3/wav/ogg'")
                return False
        except Exception as e:
            print(f"Failed to load music: {e}")
            return False
    
    def play(self, loops=-1):
        """播放音乐（-1表示无限循环，0表示播放一次）"""
        if not AUDIO_ENABLED or self.is_playing:
            return
        
        try:
            pygame.mixer.music.play(loops)
            pygame.mixer.music.set_volume(self.current_volume)
            self.is_playing = True
        except Exception as e:
            print(f"Failed to play music: {e}")
    
    def stop(self):
        """停止音乐"""
        if not AUDIO_ENABLED or not self.is_playing:
            return
        
        try:
            pygame.mixer.music.stop()
            self.is_playing = False
        except Exception as e:
            print(f"Failed to stop music: {e}")
    
    def fadeout(self, duration_ms=None):
        """淡出音乐"""
        if not AUDIO_ENABLED or not self.is_playing:
            return
        
        duration = duration_ms if duration_ms else self.fade_out_duration
        try:
            pygame.mixer.music.fadeout(duration)
            self.is_playing = False
        except Exception as e:
            print(f"Failed to fadeout music: {e}")
    
    def set_volume(self, volume):
        """设置音量 (0.0-1.0)"""
        if not AUDIO_ENABLED:
            return
        self.current_volume = max(0.0, min(1.0, volume))
        try:
            pygame.mixer.music.set_volume(self.current_volume)
        except Exception as e:
            print(f"Failed to set volume: {e}")

# Overwatch 风格字体选择（Big Noodle Titling 等）
def get_overwatch_font(size, bold=False, italic=False):
    """尝试加载 Overwatch 风格字体（Big Noodle Titling），找不到则回退系统接近字体或默认。"""
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

    # 常见系统字体别名（不一定完全一致，但气质接近）
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

# 初始化 Pygame
pygame.init()

# 初始化 Pygame mixer (音频)
try:
    pygame.mixer.init()
    AUDIO_ENABLED = True
except Exception as e:
    print(f"Audio initialization failed: {e}")
    AUDIO_ENABLED = False

# 游戏常量
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 206, 235)  # 天空蓝
SAND = (238, 214, 175)  # 沙漠色
BROWN = (139, 90, 43)

# 从背景图片提取颜色
def extract_background_colors(image_path="background2.jpg"):
    """从背景图片提取主要颜色和区域"""
    try:
        img = Image.open(image_path)
        img = img.resize((SCREEN_WIDTH, SCREEN_HEIGHT))
        img_array = np.array(img)
        
        # 将图片分成不同区域提取主要颜色
        height, width = img_array.shape[:2]
        
        # 上部天空区域 (0-40%)
        sky_region = img_array[0:int(height*0.4), :]
        sky_color = tuple(np.mean(sky_region, axis=(0, 1)).astype(int).tolist())
        
        # 中部区域 (40-70%)
        middle_region = img_array[int(height*0.4):int(height*0.7), :]
        middle_color = tuple(np.mean(middle_region, axis=(0, 1)).astype(int).tolist())
        
        # 下部地面区域 (70-100%)
        ground_region = img_array[int(height*0.7):, :]
        ground_color = tuple(np.mean(ground_region, axis=(0, 1)).astype(int).tolist())
        
        return {
            'sky': sky_color,
            'middle': middle_color,
            'ground': ground_color,
            'full_array': img_array
        }
    except Exception as e:
        print(f"无法加载背景图片: {e}")
        # 返回默认颜色
        return {
            'sky': (135, 206, 235),
            'middle': (200, 180, 150),
            'ground': (238, 214, 175),
            'full_array': None
        }

# 提取背景颜色
BG_COLORS = extract_background_colors()
SKY_COLOR = BG_COLORS['sky']
MIDDLE_COLOR = BG_COLORS['middle']
GROUND_COLOR = BG_COLORS['ground']

# 游戏状态
STATE_INTRO = 0
STATE_WALK = 1
STATE_GAMEPLAY = 2
STATE_GAMEOVER = 3


def pixelate_image(image_path, target_size=(100, 100), pixel_size=4):
    """将图片转换为像素风格"""
    try:
        img = Image.open(image_path)
        # 保持原始图片的宽高比
        img.thumbnail(target_size, Image.Resampling.LANCZOS)
        
        # 转换为RGBA以保持透明度
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        img_array = np.array(img)
        height, width = img_array.shape[:2]
        
        # 创建像素化的图像数组
        pixelated = np.zeros_like(img_array)
        
        for y in range(0, height, pixel_size):
            for x in range(0, width, pixel_size):
                y_end = min(y + pixel_size, height)
                x_end = min(x + pixel_size, width)
                
                # 获取区域
                region = img_array[y:y_end, x:x_end]
                
                # 如果区域大部分是透明的，保持透明
                alpha_values = region[:, :, 3]
                avg_alpha = np.mean(alpha_values)
                
                if avg_alpha < 50:  # 大部分透明
                    pixel_color = [0, 0, 0, 0]
                else:
                    # 使用中心点颜色
                    y_center = min(y + pixel_size // 2, height - 1)
                    x_center = min(x + pixel_size // 2, width - 1)
                    center_color = img_array[y_center, x_center].copy()
                    
                    # 增强颜色饱和度，减少灰色
                    rgb = center_color[:3].astype(float)
                    
                    # 如果不是接近黑色或白色，增强饱和度
                    brightness = np.mean(rgb)
                    if 30 < brightness < 225:
                        # 找到最大和最小的颜色通道
                        max_val = np.max(rgb)
                        min_val = np.min(rgb)
                        
                        # 如果颜色太灰，略微增强对比度
                        if max_val - min_val < 50:  # 颜色太灰
                            # 整体增强对比度，但保持色调
                            rgb = np.clip((rgb - 128) * 1.15 + 128, 0, 255)
                        else:
                            # 非灰色区域轻微增强对比度
                            rgb = np.clip((rgb - 128) * 1.05 + 128, 0, 255)
                    
                    center_color[:3] = rgb.astype(np.uint8)
                    pixel_color = center_color.tolist()
                
                # 填充像素块
                pixelated[y:y_end, x:x_end] = pixel_color
        
        # 转换回PIL图像
        pixelated_img = Image.fromarray(pixelated.astype('uint8'), 'RGBA')
        
        # 创建pygame surface
        mode = pixelated_img.mode
        size = pixelated_img.size
        data = pixelated_img.tobytes()
        
        py_image = pygame.image.fromstring(data, size, mode)
        
        # 调整到目标大小
        final_surface = pygame.Surface(target_size, pygame.SRCALPHA)
        # 居中绘制
        x_offset = (target_size[0] - size[0]) // 2
        y_offset = (target_size[1] - size[1]) // 2
        final_surface.blit(py_image, (x_offset, y_offset))
        
        # 添加轮廓线
        # 创建轮廓surface
        outline_surface = pygame.Surface(target_size, pygame.SRCALPHA)
        outline_color = (0, 0, 0, 255)  # 黑色轮廓
        
        # 检测边缘并绘制轮廓
        for y in range(target_size[1]):
            for x in range(target_size[0]):
                try:
                    current_alpha = final_surface.get_at((x, y))[3]
                    
                    if current_alpha > 128:  # 当前像素不透明
                        # 检查四周是否有透明像素
                        is_edge = False
                        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < target_size[0] and 0 <= ny < target_size[1]:
                                neighbor_alpha = final_surface.get_at((nx, ny))[3]
                                if neighbor_alpha < 128:  # 邻居透明
                                    is_edge = True
                                    break
                            else:
                                is_edge = True
                                break
                        
                        if is_edge:
                            outline_surface.set_at((x, y), outline_color)
                except:
                    pass
        
        # 合并轮廓
        final_with_outline = pygame.Surface(target_size, pygame.SRCALPHA)
        final_with_outline.blit(final_surface, (0, 0))
        final_with_outline.blit(outline_surface, (0, 0))
        
        return final_with_outline
        
    except Exception as e:
        print(f"无法加载图片 {image_path}: {e}")
        # 返回占位图
        surface = pygame.Surface(target_size, pygame.SRCALPHA)
        surface.fill((255, 220, 0))
        return surface


class Player:
    """黄豆人玩家类"""
    def __init__(self):
        # 使用像素化处理加载图片，尺寸增加到125x125 (原来100的1.25倍)
        self.image_normal = pixelate_image("huangdou.png", (125, 125), pixel_size=3)
        self.image_shoot = pixelate_image("huangdou2.png", (125, 125), pixel_size=3)
        
        self.current_image = self.image_normal
        self.rect = self.current_image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
        self.is_shooting = False
        self.shoot_timer = 0
    
    def shoot(self):
        """射击动作"""
        self.is_shooting = True
        self.shoot_timer = 10  # 显示射击状态10帧
        self.current_image = self.image_shoot
    
    def update(self):
        """更新玩家状态"""
        if self.is_shooting:
            self.shoot_timer -= 1
            if self.shoot_timer <= 0:
                self.is_shooting = False
                self.current_image = self.image_normal
    
    def draw(self, screen):
        """绘制玩家"""
        screen.blit(self.current_image, self.rect)


class Plate:
    """飞盘类"""
    def __init__(self):
        self.width = 60
        self.height = 40
        
        # 四种飞行路径
        self.trajectory = random.randint(0, 3)
        
        if self.trajectory == 0:
            # 从右下到左上
            self.x = SCREEN_WIDTH + 50
            self.y = SCREEN_HEIGHT - 100
            self.speed_x = random.uniform(-3, -2)  # 向左
            self.start_y = SCREEN_HEIGHT - 100
            self.end_y = SCREEN_HEIGHT * 0.1
            
        elif self.trajectory == 1:
            # 从右上到左下
            self.x = SCREEN_WIDTH + 50
            self.y = SCREEN_HEIGHT * 0.1
            self.speed_x = random.uniform(-3, -2)  # 向左
            self.start_y = SCREEN_HEIGHT * 0.1
            self.end_y = SCREEN_HEIGHT - 100
            
        elif self.trajectory == 2:
            # 从左上到右下
            self.x = -50
            self.y = SCREEN_HEIGHT * 0.1
            self.speed_x = random.uniform(2, 3)  # 向右
            self.start_y = SCREEN_HEIGHT * 0.1
            self.end_y = SCREEN_HEIGHT - 100
            
        else:  # trajectory == 3
            # 从左下到右上
            self.x = -50
            self.y = SCREEN_HEIGHT - 100
            self.speed_x = random.uniform(2, 3)  # 向右
            self.start_y = SCREEN_HEIGHT - 100
            self.end_y = SCREEN_HEIGHT * 0.1
        
        # 抛物线运动参数
        self.distance_traveled = 0
        self.total_distance = SCREEN_WIDTH + 100
        
        self.color = (200, 200, 200)
        self.alive = True
        self.broken = False
        self.broken_pieces = []
    
    def update(self):
        """更新飞盘位置"""
        if not self.broken:
            self.x += self.speed_x
            self.distance_traveled += abs(self.speed_x)
            
            # 计算进度 (0 到 1)
            progress = min(1.0, self.distance_traveled / self.total_distance)
            
            # 直线移动到目标高度
            self.y = self.start_y + (self.end_y - self.start_y) * progress
            
            # 添加抛物线曲线（在中间弯曲最多）
            parabola_factor = 4 * progress * (1 - progress)  # 在 progress=0.5 时最大值为 1
            
            # 根据轨迹方向添加抛物线偏移
            if self.trajectory in [0, 3]:  # 向上的轨迹，抛物线向上弯
                parabola_offset = parabola_factor * 100  # 向上弯
            else:  # 向下的轨迹，抛物线向下弯
                parabola_offset = parabola_factor * (-100)  # 向下弯
            
            self.y += parabola_offset
            
            # 飞盘飞出屏幕
            if self.x < -100 or self.x > SCREEN_WIDTH + 100:
                self.alive = False
        else:
            # 更新碎片
            for piece in self.broken_pieces:
                piece['x'] += piece['vx']
                piece['y'] += piece['vy']
                piece['vy'] += 0.5  # 重力
            
            # 检查是否所有碎片都落下屏幕
            if all(p['y'] > SCREEN_HEIGHT for p in self.broken_pieces):
                self.alive = False
    
    def break_plate(self):
        """打碎飞盘"""
        self.broken = True
        # 创建碎片
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
        """绘制飞盘"""
        if not self.broken:
            # 绘制完整的飞盘（椭圆形）
            pygame.draw.ellipse(screen, self.color, 
                              (int(self.x - self.width/2), int(self.y - self.height/2), 
                               self.width, self.height))
            pygame.draw.ellipse(screen, BLACK, 
                              (int(self.x - self.width/2), int(self.y - self.height/2), 
                               self.width, self.height), 2)
        else:
            # 绘制碎片
            for piece in self.broken_pieces:
                pygame.draw.circle(screen, self.color, 
                                 (int(piece['x']), int(piece['y'])), piece['size'])
    
    def is_clicked(self, pos):
        """检查是否被点击"""
        if self.broken:
            return False
        dist_x = abs(pos[0] - self.x)
        dist_y = abs(pos[1] - self.y)
        return dist_x < self.width/2 and dist_y < self.height/2


class Tumbleweed:
    """风滚草类"""
    def __init__(self):
        self.x = -50
        self.y = SCREEN_HEIGHT - 100
        self.size = 40
        self.rotation = 0
        self.speed = 3
        # 像素风格颜色
        self.brown_dark = (101, 67, 33)
        self.brown_medium = (139, 90, 43)
        self.brown_light = (160, 110, 60)
    
    def update(self):
        """更新位置"""
        self.x += self.speed
        self.rotation += 5
    
    def draw(self, screen):
        """绘制像素风格的中空风滚草"""
        center_x = int(self.x)
        center_y = int(self.y)
        
        # 使用像素块构建风滚草的中空球形结构
        pixel_size = 6  # 从3增加到6，像素点大一倍
        
        # 绘制多层圆形结构，创建中空效果
        # 外层
        for angle in range(0, 360, 20):  # 调整间隔避免太密集
            rad = math.radians(angle + self.rotation)
            # 外圈的枝条
            for r in range(int(self.size * 0.6), self.size, pixel_size):
                x = center_x + int(r * math.cos(rad))
                y = center_y + int(r * math.sin(rad))
                
                # 随机选择深浅色增加层次感
                if (angle + self.rotation) % 40 < 20:
                    color = self.brown_dark
                else:
                    color = self.brown_medium
                
                pygame.draw.circle(screen, color, (x, y), pixel_size // 2)
        
        # 绘制交叉的枝条创建网状结构
        num_branches = 10  # 略微减少避免太密
        for i in range(num_branches):
            angle = (360 / num_branches) * i + self.rotation
            rad = math.radians(angle)
            
            # 从中心向外的枝条
            for dist in range(pixel_size, self.size, pixel_size * 2):
                x = center_x + int(dist * math.cos(rad))
                y = center_y + int(dist * math.sin(rad))
                
                # 根据距离选择颜色
                if dist < self.size * 0.5:
                    color = self.brown_light
                elif dist < self.size * 0.75:
                    color = self.brown_medium
                else:
                    color = self.brown_dark
                
                pygame.draw.rect(screen, color, (x - pixel_size//2, y - pixel_size//2, pixel_size, pixel_size))
        
        # 添加一些随机的枝条碎片增加细节
        for i in range(12):  # 略微减少数量
            angle = (360 / 12) * i + self.rotation * 0.5
            rad = math.radians(angle)
            dist = self.size * 0.7
            x = center_x + int(dist * math.cos(rad))
            y = center_y + int(dist * math.sin(rad))
            
            # 画小的像素块，也增大一倍
            pygame.draw.rect(screen, self.brown_medium, (x - 2, y - 2, 4, 4))


class Game:
    """游戏主类"""
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
        self.total_rounds = 1  # 改为1回合
        self.round_hits = 0  # 当前回合命中数
        self.round_results = []  # 存储每回合的结果 [(命中数, 总数), ...]
        self.intro_timer = 0
        self.walk_timer = 0
        self.player_walk_x = -100
        self.spawn_timer = 0
        # 使用 Overwatch 风格字体（本地 fonts/ 或系统匹配），统一英文显示
        self.font = get_overwatch_font(36)
        self.big_font = get_overwatch_font(72)
        self.selected_option = 0  # 结算界面选中的选项 0=重新开始, 1=退出
        # 音乐管理
        self.music_manager = MusicManager()
        self.music_manager.load_music()
        # 游戏启动时立即播放音乐，只播放一次（loops=0）
        self.music_manager.play(loops=0)
        # 音效管理
        self.sound_effects = SoundEffectManager()
    
    def create_background(self):
        """创建基于背景图片的像素化背景"""
        bg_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        if BG_COLORS['full_array'] is not None:
            # 使用实际图片创建像素化背景
            img_array = BG_COLORS['full_array']
            pixel_size = 4  # 减小像素块大小使边缘更清晰
            
            for y in range(0, SCREEN_HEIGHT, pixel_size):
                for x in range(0, SCREEN_WIDTH, pixel_size):
                    # 获取该区域的中心点颜色而非平均值，保持边缘清晰
                    y_center = min(y + pixel_size // 2, SCREEN_HEIGHT - 1)
                    x_center = min(x + pixel_size // 2, SCREEN_WIDTH - 1)
                    
                    # 使用中心点颜色
                    center_color = tuple(img_array[y_center, x_center].tolist())
                    
                    # 检查该区域的颜色变化（边缘检测）
                    y_end = min(y + pixel_size, SCREEN_HEIGHT)
                    x_end = min(x + pixel_size, SCREEN_WIDTH)
                    region = img_array[y:y_end, x:x_end]
                    
                    # 计算颜色标准差，如果变化大说明是边缘
                    std_dev = np.std(region, axis=(0, 1))
                    is_edge = np.mean(std_dev) > 15  # 边缘阈值
                    
                    if is_edge:
                        # 边缘区域使用更小的像素块或中位数颜色
                        median_color = tuple(np.median(region, axis=(0, 1)).astype(int).tolist())
                        pygame.draw.rect(bg_surface, median_color, 
                                       (x, y, pixel_size, pixel_size))
                    else:
                        # 非边缘区域使用中心颜色
                        pygame.draw.rect(bg_surface, center_color, 
                                       (x, y, pixel_size, pixel_size))
        else:
            # 使用提取的颜色创建渐变背景
            # 上部天空
            for y in range(0, int(SCREEN_HEIGHT * 0.4)):
                color_ratio = y / (SCREEN_HEIGHT * 0.4)
                color = tuple(int(SKY_COLOR[i] * (1 - color_ratio * 0.3)) for i in range(3))
                pygame.draw.line(bg_surface, color, (0, y), (SCREEN_WIDTH, y))
            
            # 中部
            for y in range(int(SCREEN_HEIGHT * 0.4), int(SCREEN_HEIGHT * 0.7)):
                pygame.draw.line(bg_surface, MIDDLE_COLOR, (0, y), (SCREEN_WIDTH, y))
            
            # 下部地面
            for y in range(int(SCREEN_HEIGHT * 0.7), SCREEN_HEIGHT):
                pygame.draw.line(bg_surface, GROUND_COLOR, (0, y), (SCREEN_WIDTH, y))
        
        return bg_surface
    
    def reset_round(self):
        """重置回合"""
        self.plates = []
        self.bullets = 6
        self.round_hits = 0  # 重置当前回合命中数
        self.spawn_timer = 0
    
    def handle_events(self):
        """处理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.MOUSEBUTTONDOWN and self.state == STATE_GAMEPLAY:
                if self.bullets > 0:
                    # 检查是否击中飞盘
                    pos = pygame.mouse.get_pos()
                    hit = False
                    for plate in self.plates:
                        if plate.is_clicked(pos) and not plate.broken:
                            plate.break_plate()
                            self.score += 1
                            self.round_hits += 1
                            hit = True
                            break
                    
                    # 射击（无论是否命中）
                    self.bullets -= 1
                    self.player.shoot()
                    # 播放射击音效
                    self.sound_effects.play_shoot()
                    
                    # 如果这是第6发子弹（最后一发），立即结算回合
                    if self.bullets == 0:
                        # 播放过度音效
                        self.sound_effects.play_transition()
                        # 记录本回合结果
                        self.round_results.append((self.round_hits, 6))
                        
                        if self.round < self.total_rounds:
                            self.round += 1
                            self.reset_round()
                        else:
                            # 所有回合结束，进入游戏结束状态
                            self.state = STATE_GAMEOVER
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.state == STATE_GAMEOVER:
                    # 重新开始游戏
                    if self.selected_option == 0:
                        # 淡出音乐后重新初始化
                        self.music_manager.fadeout(2000)
                        self.__init__()
                    else:
                        # 退出游戏时淡出音乐
                        self.music_manager.fadeout(2000)
                        import time
                        time.sleep(2.1)  # 等待淡出完成
                        return False
                
                # 结算界面的上下键选择
                if self.state == STATE_GAMEOVER:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.selected_option = 0
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.selected_option = 1
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        # 回车键确认选择
                        if self.selected_option == 0:
                            # 淡出音乐后重新初始化
                            self.music_manager.fadeout(2000)
                            self.__init__()
                        else:
                            # 退出游戏时淡出音乐
                            self.music_manager.fadeout(2000)
                            import time
                            time.sleep(2.1)  # 等待淡出完成
                            return False
        
        return True
    
    def update(self):
        """更新游戏逻辑"""
        if self.state == STATE_INTRO:
            # 介绍界面，显示黄豆人
            self.intro_timer += 1
            if self.intro_timer > 120:  # 2秒后进入行走场景
                self.state = STATE_WALK
                self.tumbleweed = Tumbleweed()
        
        elif self.state == STATE_WALK:
            # 黄豆人走到沙漠
            self.walk_timer += 1
            self.player_walk_x += 2
            
            # 更新风滚草
            if self.tumbleweed:
                self.tumbleweed.update()
            
            if self.walk_timer > 180:  # 3秒后进入游戏
                self.state = STATE_GAMEPLAY
                self.player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
        
        elif self.state == STATE_GAMEPLAY:
            # 游戏进行中
            self.player.update()
            
            # 生成飞盘
            self.spawn_timer += 1
            if self.spawn_timer > 60 and len(self.plates) < 3:  # 每秒生成，最多3个
                self.plates.append(Plate())
                self.spawn_timer = 0
            
            # 更新飞盘
            for plate in self.plates[:]:
                plate.update()
                if not plate.alive:
                    self.plates.remove(plate)
    
    def draw(self):
        """绘制游戏画面"""
        if self.state == STATE_INTRO:
            # 介绍界面
            self.screen.blit(self.bg_surface, (0, 0))
            # 居中显示黄豆人
            temp_rect = self.player.image_normal.get_rect()
            temp_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            self.screen.blit(self.player.image_normal, temp_rect)
            
            title = self.big_font.render("M&M McBean", True, BLACK)
            title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
            self.screen.blit(title, title_rect)
        
        elif self.state == STATE_WALK:
            # 沙漠场景
            self.screen.blit(self.bg_surface, (0, 0))
            
            # 绘制风滚草
            if self.tumbleweed:
                self.tumbleweed.draw(self.screen)
            
            # 绘制行走的黄豆人
            temp_rect = self.player.image_normal.get_rect()
            temp_rect.center = (self.player_walk_x, SCREEN_HEIGHT - 100)
            self.screen.blit(self.player.image_normal, temp_rect)
        
        elif self.state == STATE_GAMEPLAY:
            # 游戏界面
            self.screen.blit(self.bg_surface, (0, 0))
            
            # 绘制飞盘
            for plate in self.plates:
                plate.draw(self.screen)
            
            # 绘制玩家
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
            # Game Over screen
            self.screen.fill(WHITE)
            
            gameover_text = self.big_font.render("GAME OVER!", True, BLACK)
            gameover_rect = gameover_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
            self.screen.blit(gameover_text, gameover_rect)
            
            # Final Score
            score_text = self.big_font.render(f"FINAL SCORE: {self.score}/6", True, BLACK)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
            self.screen.blit(score_text, score_rect)
            
            # Hit ratio
            if self.round_results:
                hits, total = self.round_results[0]
                ratio_text = self.font.render(f"HIT RATIO: {hits}/{total}", True, BLACK)
                ratio_rect = ratio_text.get_rect(center=(SCREEN_WIDTH // 2, 280))
                self.screen.blit(ratio_text, ratio_rect)
            
            # Options menu
            menu_y = 360
            
            # Option 1: Restart
            restart_color = (50, 150, 50) if self.selected_option == 0 else BLACK
            restart_text = self.font.render(("▶ RESTART" if self.selected_option == 0 else "  RESTART"), True, restart_color)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, menu_y))
            self.screen.blit(restart_text, restart_rect)
            
            # Option 2: Quit
            quit_color = (200, 50, 50) if self.selected_option == 1 else BLACK
            quit_text = self.font.render(("▶ QUIT" if self.selected_option == 1 else "  QUIT"), True, quit_color)
            quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, menu_y + 50))
            self.screen.blit(quit_text, quit_rect)
            
            # Hint text
            hint_text = self.font.render("Use ↑↓ to select, Enter/Space to confirm", True, (128, 128, 128))
            hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, menu_y + 120))
            self.screen.blit(hint_text, hint_rect)
        
        pygame.display.flip()
    
    def run(self):
        """游戏主循环"""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()


def main():
    """主函数"""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
