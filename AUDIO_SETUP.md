# Audio Setup Guide

## Background Music

The game supports background music playback.

### Supported Audio Formats
- MP3 (.mp3)
- WAV (.wav)
- OGG Vorbis (.ogg)

### Background Music File Placement

Place your background music file in the project root directory with one of these names:
- `background_sound.mp3` (default, recommended)
- `music.mp3`
- `music.wav`
- `music.ogg`
- `bg_music.mp3`

### Music Playback Logic

1. **Game Startup** - Background music starts playing immediately
2. **Gameplay** - Music continues playing
3. **Exit/Restart** - Music fades out over 2 seconds before stopping

### Music Control

In `main.py`, adjust the `MusicManager` class:
- `fade_out_duration` - Fadeout time (milliseconds), default 2000ms
- `current_volume` - Initial volume (0.0-1.0), default 0.7

---

## Game Sound Effects

The game now supports the following two sound effects:

### Shoot Sound

- **Filename**: `shoot.mp3` or `shoot.wav`
- **Trigger**: When player clicks mouse to shoot
- **Location**: Project root directory

### Transition Sound

- **Filename**: `bullet_change.mp3` or `bullet_change.wav`
- **Trigger**: After 6th bullet is fired, before results screen appears
- **Location**: Project root directory
- **Purpose**: Audio feedback for end of shooting and transition to results

### Sound Effect File Placement

```
Project Root/
├── main.py
├── background_sound.mp3      (Background music)
├── shoot.mp3                 (Shoot sound effect)
└── bullet_change.mp3         (Transition sound effect)
```

### Supported Effect Formats
- MP3 (.mp3) - Recommended format
- WAV (.wav) - Fallback format

**Note**: If MP3 file doesn't exist, the game will automatically try WAV file.

### Quick Start
1. Prepare three audio files:
   - `background_sound.mp3` - Game background music
   - `shoot.mp3` - Shoot sound effect
   - `bullet_change.mp3` - Transition sound effect
2. Place all files in the project root directory
3. Run the game; sounds should play automatically

---

## Troubleshooting

- **"file not found" message appears**: Ensure audio files are in the project root directory
- **No sound output**:
  - Check system volume
  - Ensure pygame mixer initialized successfully
  - Try adjusting `current_volume` value
- **Audio format not supported**: Try converting file to MP3 or WAV format
- **Audio warnings on startup can be ignored**: Game will run normally even if sound files are missing; only those specific sounds won't play

---

## Recommended Background Music

- 8-bit/16-bit retro game style music
- Royalty-free sources:
  - OpenGameArt.org
  - itch.io (search royalty-free music)
  - YouTube Audio Library
  - Free Music Archive

---

## Audio File Requirements

- **Format**: MP3 or WAV (MP3 preferred)
- **Sample Rate**: 16000 Hz or higher recommended
- **Bit Depth**: 16-bit recommended
- **File Size**: Smaller is better (for faster loading)

### Recommended Specifications

| Type | Recommended Length | Recommended Volume |
|------|-------------------|-------------------|
| Shoot Sound | 200-500ms | 0.6-0.8 |
| Transition Sound | 500-1500ms | 0.5-0.7 |
| Background Music | 30-60s (loops) | 0.7 |
