# Sound Effects System

## Overview

The game now includes a complete sound effects system supporting background music and two game sound effects:
- 🎵 **Background Music**: Plays when game starts
- 🔫 **Shoot Sound**: When player clicks to shoot
- 🎯 **Transition Sound**: After 6 bullets used, before results screen

## Feature Details

### 1. Background Music
- **File**: `background_sound.mp3`
- **Playback**: Starts on game launch
- **Mode**: Plays once (no looping)
- **Fadeout**: 2 seconds when exiting or restarting
- **Volume**: Adjustable in code (default 0.7)

### 2. Shoot Sound
- **File**: `shoot.mp3` or `shoot.wav`
- **Trigger**: Each mouse click during shooting
- **Features**:
  - Plays for each shot
  - Plays even if no hit
  - Supports stacked playback (rapid firing)

### 3. Transition Sound
- **File**: `bullet_change.mp3` or `bullet_change.wav`
- **Trigger**: After 6th bullet fired
- **Purpose**: Audio feedback for end of round and transition to results
- **Features**:
  - Plays before results screen
  - Provides natural audio bridge in game flow

## File Structure

```
d:\code_data\M&M-McBean\
├── main.py                    # Main program (includes SoundEffectManager)
├── background_sound.mp3       # Background music file (required)
├── shoot.mp3                  # Shoot sound file (optional, supports .wav)
├── bullet_change.mp3          # Transition sound file (optional, supports .wav)
├── AUDIO_SETUP.md            # Audio setup guide
└── SOUND_EFFECTS.md          # This file
```

## Code Architecture

### SoundEffectManager Class

```python
class SoundEffectManager:
    """Manage game sound effects"""
    def __init__(self):
        self.shoot_sound = None
        self.transition_sound = None
        self.load_sounds()
    
    def load_sounds(self):
        """Load sound effect files"""
        # Auto-detects .mp3 or .wav files
    
    def play_shoot(self):
        """Play shoot sound effect"""
    
    def play_transition(self):
        """Play transition sound effect"""
```

### Integration Points

**Game class initialization**:
```python
self.sound_effects = SoundEffectManager()
```

**When shooting** (handle_events method):
```python
self.sound_effects.play_shoot()
```

**When round ends** (handle_events method):
```python
self.sound_effects.play_transition()
```

## Installing Sound Files

### Option 1: Use Free Sound Effect Libraries

Recommended sources:
- **Freesound.org** - Large free sound effects library
- **Zapsplat.com** - Game sound effects library
- **OpenGameArt.org** - Game-specific sounds
- **Pixabay** - Royalty-free sound effects
- **YouTube Audio Library** - YouTube audio library

### Option 2: Use Online AI Sound Generators

- **Runway ML** - AI sound generation
- **AIVA** - Music generation AI

### Option 3: Extract from Games (personal use only)

Some retro game sounds can be extracted and converted to MP3/WAV format.

## Audio File Requirements

- **Format**: MP3 or WAV (MP3 preferred)
- **Sample Rate**: 16000 Hz or higher recommended
- **Bit Depth**: 16-bit recommended
- **File Size**: Smaller is better (faster loading)

### Recommended Specifications

| Type | Recommended Length | Recommended Volume |
|------|-------------------|-------------------|
| Shoot Sound | 200-500ms | 0.6-0.8 |
| Transition Sound | 500-1500ms | 0.5-0.7 |
| Background Music | 30-60s (loops) | 0.7 |

## Troubleshooting

### Issue: No sound output

**Solution**:
1. Check system volume
2. Verify audio files are in project root
3. Confirm file format is MP3 or WAV
4. Check console output for error messages

### Issue: Sound files not found

**Output**:
```
shoot.mp3 or shoot.wav not found
bullet_change.mp3 or bullet_change.wav not found
```

**Solution**:
1. Game will continue running without these sounds
2. Place audio files in project root directory
3. Restart game

### Issue: Audio playback stuttering or delayed

**Solution**:
1. Check if audio file is corrupted; try re-encoding to MP3/WAV
2. Lower sample rate or bitrate
3. Try different audio format

## Customization Options

### Adjust Sound Effect Playback Volume

In `main.py`, modify `SoundEffectManager` class if needed:

```python
def play_shoot(self):
    """Play shoot sound effect"""
    if not AUDIO_ENABLED or self.shoot_sound is None:
        return
    try:
        self.shoot_sound.set_volume(0.8)  # Set volume (0.0-1.0)
        self.shoot_sound.play()
    except Exception as e:
        print(f"Failed to play shoot sound: {e}")
```

### Add New Sound Effects

1. Add new property in `SoundEffectManager.__init__()`
2. Load file in `load_sounds()` method
3. Create new `play_xxx()` method
4. Call method in game logic

Example:
```python
def __init__(self):
    self.hit_sound = None  # New property
    self.load_sounds()

def load_sounds(self):
    # Existing code...
    if os.path.exists("hit.mp3"):
        self.hit_sound = pygame.mixer.Sound("hit.mp3")

def play_hit(self):
    """Play hit sound effect"""
    if not AUDIO_ENABLED or self.hit_sound is None:
        return
    try:
        self.hit_sound.play()
    except Exception as e:
        print(f"Failed to play hit sound: {e}")
```

## Audio Timeline in Gameplay

```
Game Startup
  │
  ├─ Load background music (background_sound.mp3)
  ├─ Load shoot sound (shoot.mp3)
  ├─ Load transition sound (bullet_change.mp3)
  │
  ├─ Enter intro screen
  │  └─ Background music starts playing
  │
  ├─ Enter gameplay
  │  └─ Player fires 1-5 shots
  │     └─ Each shot triggers shoot.mp3 ✓
  │
  ├─ Fire 6th shot
  │  ├─ Triggers shoot.mp3 ✓
  │  └─ Immediately triggers bullet_change.mp3 ✓
  │
  ├─ Results screen displays
  │  └─ Background music continues
  │
  ├─ Player chooses restart or quit
  │  └─ Background music fades out over 2 seconds
  │
  └─ Game ends or restarts
```

## Performance Considerations

- **Sound Loading**: Loads during game initialization, no runtime blocking
- **Concurrent Playback**: Pygame mixer supports multiple simultaneous sounds
- **Memory Usage**: Sounds stored in memory; keep file sizes reasonable
- **CPU Usage**: Sound playback has minimal CPU overhead

## Disabling Audio

To temporarily disable all sound effects and music, modify `main.py` top section:

```python
AUDIO_ENABLED = False  # Change to False to disable all audio
```

## Changelog

### v1.1.0 - Sound Effects System Update
- ✅ Added `SoundEffectManager` class for sound management
- ✅ Implemented shoot sound (shoot.mp3)
- ✅ Implemented transition sound (bullet_change.mp3)
- ✅ Support MP3 and WAV format auto-detection
- ✅ Added detailed audio setup documentation
- ✅ Integrated sound playback into game flow

---

**Last Updated**: 2025-10-23
