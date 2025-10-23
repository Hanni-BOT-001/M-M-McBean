# Sound Effects Quick Reference

## 📋 Required Files

```
Project Root (d:\code_data\M&M-McBean\)
├── background_sound.mp3      ✓ Required - Background music
├── shoot.mp3                 ○ Optional - Shoot sound effect
└── bullet_change.mp3         ○ Optional - Transition sound effect
```

**Note**: WAV format is supported as fallback; game will auto-detect.

## 🎵 Sound Effects Playback

| Sound | Trigger | File |
|-------|---------|------|
| 🎼 Background Music | Game startup | `background_sound.mp3` |
| 🔫 Shoot Sound | Player clicks to shoot | `shoot.mp3` |
| 🎯 Transition Sound | After 6th bullet fired | `bullet_change.mp3` |

## 🔧 Code Locations

### Sound Effect Manager Class
- **Location**: `main.py` lines 122-171
- **Methods**:
  - `load_sounds()` - Load sound effect files
  - `play_shoot()` - Play shoot sound
  - `play_transition()` - Play transition sound

### Integration Points
1. **Game.__init__()** - Initialize sound manager
   ```python
   self.sound_effects = SoundEffectManager()
   ```

2. **Game.handle_events()** - When player shoots
   ```python
   self.sound_effects.play_shoot()
   ```

3. **Game.handle_events()** - When 6 bullets used
   ```python
   self.sound_effects.play_transition()
   ```

## 📥 Recommended Sound Files

### Shoot Sound Characteristics
- Duration: 200-500 milliseconds
- Type: Gun shot, laser, punch sound
- Sources:
  - Freesound.org (search "gun shoot" or "laser")
  - Zapsplat.com (game sound effects)

### Transition Sound Characteristics
- Duration: 500-1500 milliseconds
- Type: Transition effect, bell, system sound
- Sources:
  - Freesound.org (search "transition" or "notification")
  - OpenGameArt.org (game sounds)

### Background Music Characteristics
- Duration: 30-60 seconds (loops)
- Style: Game soundtrack, retro 8-bit/16-bit
- Sources:
  - YouTube Audio Library
  - OpenGameArt.org (search "game music")
  - Itch.io (search royalty-free music)

## 🔧 Quick Troubleshooting

### Problem: "file not found" message

**Cause**: Sound files not in project root

**Solution**:
1. Confirm files are in `d:\code_data\M&M-McBean\` directory
2. Check filenames are correct
3. Restart game after adding files

### Problem: No sound output

**Cause**: System volume low or file incompatible

**Solution**:
1. Check Windows volume (right corner icon)
2. Check game volume settings
3. Try converting to different format (ffmpeg)

### Problem: Delayed sound playback

**Cause**: File encoding or system performance

**Solution**:
1. Re-encode sound at lower bitrate
2. Ensure disk has free space
3. Close background applications

## 🎚️ Adjusting Volume

### Background Music Volume
`main.py` line 67:
```python
self.current_volume = 0.7  # Change to 0.0-1.0
```

### Game Sound Effects Volume
Add to `main.py` lines 154 and 164:
```python
def play_shoot(self):
    if not AUDIO_ENABLED or self.shoot_sound is None:
        return
    try:
        self.shoot_sound.set_volume(0.8)  # Add this line
        self.shoot_sound.play()
    except Exception as e:
        print(f"Failed to play shoot sound: {e}")
```

## 🔧 Disable All Audio

In `main.py` find:
```python
AUDIO_ENABLED = True
```

Change to:
```python
AUDIO_ENABLED = False
```

## 📊 Recommended Audio Settings

| Parameter | Value | Note |
|-----------|-------|------|
| Sample Rate | 44100 Hz | Standard CD quality |
| Bitrate | 128-256 kbps | MP3 format |
| Bit Depth | 16-bit | Standard stereo |
| Format | MP3/WAV | Most compatible |
| Location | Project root | Same directory as main.py |

## 🎬 Testing Checklist

- [ ] `background_sound.mp3` placed in project root
- [ ] Game starts without error messages
- [ ] Mouse click produces shoot sound (if `shoot.mp3` exists)
- [ ] 6th bullet produces transition sound (if `bullet_change.mp3` exists)
- [ ] Results screen music continues playing
- [ ] Music fades out when restarting

## 📞 Getting Help

For issues, refer to:
1. `AUDIO_SETUP.md` - Detailed setup guide
2. `SOUND_EFFECTS.md` - Complete documentation
3. `main.py` comments - Code explanations

---

**Tip**: On first game startup, if sound files are missing, console will show messages but game continues normally.
