# 游戏音效系统 / Sound Effects System

## 概述 / Overview

游戏现在包含完整的音效系统，支持背景音乐和两个游戏音效：
- 🎵 **背景音乐**：游戏开始时播放
- 🔫 **射击音效**：玩家点击开枪时
- 🎯 **过度音效**：子弹用完后进入结算界面前

## 功能详情 / Feature Details

### 1. 背景音乐 (Background Music)
- **文件**：`background_sound.mp3`
- **播放时机**：游戏启动立即开始
- **播放方式**：仅播放一次（不循环）
- **淡出**：退出或重新开始时 2 秒淡出
- **音量**：可在代码中调整（默认 0.7）

### 2. 射击音效 (Shoot Sound)
- **文件**：`shoot.mp3` 或 `shoot.wav`
- **播放时机**：玩家点击鼠标进行射击时
- **特点**：
  - 每次射击都会触发音效
  - 即使没有击中飞盘也会播放
  - 支持音效叠加播放（连续射击）

### 3. 过度音效 (Transition Sound)
- **文件**：`bullet_change.mp3` 或 `bullet_change.wav`
- **播放时机**：第 6 发子弹射出后
- **用途**：为射击结束和结算界面的过渡提供反馈
- **特点**：
  - 播放后等待一小段时间进入结算界面
  - 为游戏流程提供自然的音效衔接

## 文件结构 / File Structure

```
d:\code_data\M&M-McBean\
├── main.py                    # 主程序（包含 SoundEffectManager 类）
├── background_sound.mp3       # 背景音乐文件（必需）
├── shoot.mp3                  # 射击音效文件（可选，支持 .wav）
├── bullet_change.mp3          # 过度音效文件（可选，支持 .wav）
├── AUDIO_SETUP.md            # 音效设置详细说明
└── SOUND_EFFECTS.md          # 本文件
```

## 代码架构 / Code Architecture

### SoundEffectManager 类

```python
class SoundEffectManager:
    """管理游戏音效"""
    def __init__(self):
        self.shoot_sound = None
        self.transition_sound = None
        self.load_sounds()
    
    def load_sounds(self):
        """加载音效文件"""
        # 自动检测 .mp3 或 .wav 文件
    
    def play_shoot(self):
        """播放射击音效"""
    
    def play_transition(self):
        """播放过度音效"""
```

### 集成点 / Integration Points

**Game 类初始化**：
```python
self.sound_effects = SoundEffectManager()
```

**射击时触发**（handle_events 方法）：
```python
self.sound_effects.play_shoot()
```

**子弹用完时触发**（handle_events 方法）：
```python
self.sound_effects.play_transition()
```

## 安装音效文件 / Installing Sound Files

### 选项 1：使用现成的音效库

推荐来源：
- **Freesound.org** - 大量免费音效
- **Zapsplat.com** - 游戏音效库
- **OpenGameArt.org** - 游戏专用音效
- **Pixabay** - 免版税音效
- **YouTube Audio Library** - YouTube 音频库

### 选项 2：使用在线 AI 音效生成器

- **Runway ML** - AI 音效生成
- **AIVA** - 音乐生成 AI

### 选项 3：从游戏中提取（仅供个人使用）

某些复古游戏的音效可以提取并转换为 MP3/WAV 格式。

## 音效文件要求 / Audio File Requirements

- **格式**：MP3 或 WAV（优先 MP3）
- **采样率**：16000 Hz 或更高推荐
- **位深度**：16-bit 推荐
- **文件大小**：越小越好（用于快速加载）

### 示例规格 / Example Specs

| 类型 | 建议长度 | 建议音量 |
|------|---------|---------|
| 射击音效 | 200-500ms | 0.6-0.8 |
| 过度音效 | 500-1500ms | 0.5-0.7 |
| 背景音乐 | 30-60s（循环) | 0.7 |

## 故障排除 / Troubleshooting

### 问题：没有声音输出

**解决方案**：
1. 检查系统音量
2. 验证文件在项目根目录且命名正确
3. 确认文件格式为 MP3 或 WAV
4. 检查游戏启动时的控制台输出是否有错误信息

### 问题：音效文件未找到

**输出**：
```
shoot.mp3 or shoot.wav not found
bullet_change.mp3 or bullet_change.wav not found
```

**解决方案**：
1. 如果文件不存在，游戏将继续运行，但不播放该音效
2. 将相应的音效文件放入项目根目录
3. 重新启动游戏

### 问题：音效播放重复或卡顿

**解决方案**：
1. 检查音效文件是否损坏，尝试重新编码为 MP3/WAV
2. 降低采样率或比特率
3. 尝试转换为不同的音频格式

## 自定义选项 / Customization Options

### 修改音效播放音量

在 `main.py` 的 `SoundEffectManager` 类中修改（如需要）：

```python
def play_shoot(self):
    """播放射击音效"""
    if not AUDIO_ENABLED or self.shoot_sound is None:
        return
    try:
        self.shoot_sound.set_volume(0.8)  # 设置音量 (0.0-1.0)
        self.shoot_sound.play()
    except Exception as e:
        print(f"Failed to play shoot sound: {e}")
```

### 添加新的音效

1. 在 `SoundEffectManager.__init__()` 中添加新属性
2. 在 `load_sounds()` 中加载文件
3. 创建新的 `play_xxx()` 方法
4. 在游戏逻辑中调用

示例：
```python
def __init__(self):
    self.hit_sound = None  # 新增
    self.load_sounds()

def load_sounds(self):
    # 现有代码...
    if os.path.exists("hit.mp3"):
        self.hit_sound = pygame.mixer.Sound("hit.mp3")

def play_hit(self):
    """播放命中音效"""
    if not AUDIO_ENABLED or self.hit_sound is None:
        return
    try:
        self.hit_sound.play()
    except Exception as e:
        print(f"Failed to play hit sound: {e}")
```

## 游戏流程中的音效时序 / Audio Timeline in Gameplay

```
游戏启动
  │
  ├─ 加载背景音乐 (background_sound.mp3)
  ├─ 加载射击音效 (shoot.mp3)
  ├─ 加载过度音效 (bullet_change.mp3)
  │
  ├─ 进入介绍界面
  │  └─ 背景音乐开始播放
  │
  ├─ 进入游戏
  │  └─ 玩家 1-5 次射击
  │     └─ 每次射击触发 shoot.mp3 ✓
  │
  ├─ 第 6 次射击
  │  ├─ 触发 shoot.mp3 ✓
  │  └─ 立即触发 bullet_change.mp3 ✓
  │
  ├─ 结算界面显示
  │  └─ 背景音乐继续播放
  │
  ├─ 玩家选择重新开始或退出
  │  └─ 背景音乐 2 秒淡出
  │
  └─ 游戏结束或重启
```

## 性能考虑 / Performance Considerations

- **音效加载**：在游戏初始化时加载，不会在运行时阻塞
- **并发播放**：Pygame mixer 支持多个音效同时播放
- **内存占用**：音效文件存储在内存中，建议保持文件大小合理
- **CPU 使用**：音效播放的 CPU 占用极低

## 禁用音效 / Disabling Audio

如需临时禁用所有音效和音乐，在 `main.py` 顶部修改：

```python
AUDIO_ENABLED = False  # 改为 False 禁用音频
```

## 更新日志 / Changelog

### v1.1.0 - 音效系统更新
- ✅ 添加 `SoundEffectManager` 类用于管理音效
- ✅ 实现射击音效 (shoot.mp3)
- ✅ 实现过度音效 (bullet_change.mp3)
- ✅ 支持 MP3 和 WAV 格式自动检测
- ✅ 添加详细的音效设置文档
- ✅ 集成音效播放到游戏流程

---

**最后更新**：2025-10-23
