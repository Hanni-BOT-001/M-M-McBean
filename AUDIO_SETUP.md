# 游戏音效设置说明 / Audio Setup Guide

## 背景音乐 / Background Music

游戏支持播放背景音乐。要启用音乐，请按照以下步骤操作：

### 支持的音频格式 / Supported Formats
- MP3 (.mp3)
- WAV (.wav)
- OGG Vorbis (.ogg)

### 背景音乐文件放置 / Background Music File Placement

将你的背景音乐文件放在项目根目录，文件名必须是：
- `background_sound.mp3` (默认)

或者以下任意一个作为备选：
- `music.mp3`
- `music.wav`
- `music.ogg`
- `bg_music.mp3`

### 音乐播放逻辑 / Music Playback Logic

1. **游戏启动** - 背景音乐立即开始播放（仅播放一次，不循环）
2. **游戏进行中** - 音乐持续播放
3. **关闭游戏或重新开始** - 音乐淡出 2 秒后停止

### 音乐控制 / Music Control

在 `main.py` 中的 `MusicManager` 类可调整：
- `fade_out_duration` - 淡出时间（毫秒），默认 2000ms
- `current_volume` - 初始音量（0.0-1.0），默认 0.7

---

## 游戏音效 / Sound Effects

游戏现已支持以下两个音效：

### 射击音效 / Shoot Sound

- **文件名**：`shoot.mp3` 或 `shoot.wav`
- **播放时机**：玩家点击鼠标射击时
- **放置位置**：项目根目录

### 过度音效 / Transition Sound

- **文件名**：`bullet_change.mp3` 或 `bullet_change.wav`
- **播放时机**：第 6 发子弹射出后，游戏进入结算界面前
- **放置位置**：项目根目录
- **用途**：为游戏射击结束和结算的过渡提供音效反馈

### 音效文件放置 / Sound Effect File Placement

```
项目根目录/
├── main.py
├── background_sound.mp3      (背景音乐)
├── shoot.mp3                 (射击音效)
└── bullet_change.mp3         (过度音效)
```

### 支持的音效格式 / Supported Effect Formats
- MP3 (.mp3) - 推荐格式
- WAV (.wav) - 备选格式

**注意**：如果 MP3 文件不存在，游戏会自动查找 WAV 文件。

### 快速开始 / Quick Start
1. 准备三个音频文件：
   - `background_sound.mp3` - 游戏背景音乐
   - `shoot.mp3` - 射击音效
   - `bullet_change.mp3` - 过度音效
2. 将它们全部放在项目根目录
3. 运行游戏，音效应自动播放

---

## 故障排除 / Troubleshooting

- **如果看到 "file not found" 消息**：确保音频文件放在项目根目录
- **如果没有声音输出**：
  - 检查系统音量
  - 确保 pygame mixer 初始化成功
  - 尝试调整 `current_volume` 值
- **音频格式不支持**：尝试将文件转换为 MP3 或 WAV 格式
- **游戏启动时的音频警告可以忽略**：如果音效文件未找到，游戏仍可正常运行，只是不会播放相应的音效

```
