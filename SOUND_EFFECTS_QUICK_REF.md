# 音效系统快速参考 / Sound Effects Quick Reference

## 📋 需要准备的文件 / Required Files

```
项目根目录 (d:\code_data\M&M-McBean\)
├── background_sound.mp3      ✓ 必需 (Required) - 背景音乐
├── shoot.mp3                 ○ 可选 (Optional) - 射击音效
└── bullet_change.mp3         ○ 可选 (Optional) - 过度音效
```

**注**：支持 `.wav` 格式作为备选，游戏会自动检测

## 🎵 音效播放时机 / When Sounds Play

| 音效 | 触发条件 | 文件 |
|------|---------|------|
| 🎼 背景音乐 | 游戏启动立即播放 | `background_sound.mp3` |
| 🔫 射击音效 | 玩家每次点击鼠标射击 | `shoot.mp3` |
| 🎯 过度音效 | 第 6 发子弹射出后 | `bullet_change.mp3` |

## 🎛️ 代码位置 / Code Locations

### 音效管理器类
- **位置**：`main.py` 第 117-171 行
- **类名**：`SoundEffectManager`
- **方法**：
  - `load_sounds()` - 加载音效文件
  - `play_shoot()` - 播放射击音效
  - `play_transition()` - 播放过度音效

### 集成点
1. **Game.__init__()** - 初始化音效管理器
   ```python
   self.sound_effects = SoundEffectManager()
   ```

2. **Game.handle_events()** - 玩家射击时
   ```python
   self.sound_effects.play_shoot()
   ```

3. **Game.handle_events()** - 子弹用完时
   ```python
   self.sound_effects.play_transition()
   ```

## 📥 音效文件推荐 / Recommended Sound Files

### 射击音效特性
- 长度：200-500 毫秒
- 类型：枪声、激光音、打击音
- 来源建议：
  - Freesound.org (搜索 "gun shoot" 或 "laser")
  - Zapsplat.com (游戏音效库)

### 过度音效特性
- 长度：500-1500 毫秒
- 类型：过渡效果、铃声、系统音效
- 来源建议：
  - Freesound.org (搜索 "transition" 或 "notification")
  - OpenGameArt.org (游戏音效)

### 背景音乐特性
- 长度：30-60 秒（会循环）
- 风格：游戏配乐、复古 8-bit/16-bit 风格
- 来源建议：
  - YouTube Audio Library
  - OpenGameArt.org (搜索 "game music")
  - Itch.io (搜索免版税音乐)

## ⚙️ 故障排除 / Quick Troubleshooting

### 症状：游戏启动提示 "file not found"

**原因**：音效文件不在项目根目录

**解决方案**：
1. 确认文件在 `d:\code_data\M&M-McBean\` 目录下
2. 检查文件名是否正确（区分大小写）
3. 文件放入后重启游戏

### 症状：没有声音输出

**原因**：系统音量低或文件不兼容

**解决方案**：
1. 检查 Windows 系统音量 (右下角音量图标)
2. 检查游戏音量设置
3. 尝试转换音文件格式（ffmpeg）

### 症状：音效播放有延迟

**原因**：文件编码或系统性能

**解决方案**：
1. 重新编码音效为较低比特率
2. 确保硬盘有足够空间
3. 关闭后台程序释放资源

## 🎚️ 调整音量 / Adjusting Volume

### 背景音乐音量
`main.py` 第 67 行：
```python
self.current_volume = 0.7  # 改为 0.0-1.0 之间的值
```

### 游戏音效音量
`main.py` 第 154 和 164 行中添加：
```python
def play_shoot(self):
    if not AUDIO_ENABLED or self.shoot_sound is None:
        return
    try:
        self.shoot_sound.set_volume(0.8)  # ← 添加这行
        self.shoot_sound.play()
    except Exception as e:
        print(f"Failed to play shoot sound: {e}")
```

## 🔧 完全禁用音频 / Disable All Audio

在 `main.py` 第一部分找到：
```python
AUDIO_ENABLED = True
```

改为：
```python
AUDIO_ENABLED = False
```

## 📊 推荐音频设置 / Recommended Audio Settings

| 参数 | 值 | 说明 |
|------|-----|------|
| 采样率 | 44100 Hz | 标准 CD 质量 |
| 比特率 | 128-256 kbps | MP3 格式 |
| 位深度 | 16-bit | 标准立体声 |
| 格式 | MP3/WAV | 最兼容 |
| 文件位置 | 项目根目录 | 直接放在 `main.py` 同级 |

## 🎬 测试清单 / Test Checklist

- [ ] `background_sound.mp3` 放在项目根目录
- [ ] 游戏启动后无错误信息
- [ ] 点击鼠标时听到射击音效 (如有 `shoot.mp3`)
- [ ] 射出第 6 发子弹后听到过度音效 (如有 `bullet_change.mp3`)
- [ ] 游戏结算界面音乐继续播放
- [ ] 选择"重新开始"时音乐淡出

## 📞 获取帮助 / Getting Help

如果仍有问题，请参考：
1. `AUDIO_SETUP.md` - 详细设置说明
2. `SOUND_EFFECTS.md` - 完整功能文档
3. `main.py` 中的注释 - 代码详解

---

**提示**：游戏首次启动时，如果音效文件未找到，会在控制台输出提示信息，但游戏会继续正常运行。
