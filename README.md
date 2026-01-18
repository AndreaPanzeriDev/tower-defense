# tower-defense
100% vide coded. Model: MiMo-V2-Flash (free). Prompt: realize a 2d game as a tower defense

## How to Run without Python locally

This project is set up to run using Docker, so you don't need to install Python or Pygame on your machine.

### Prerequisites

1.  **Docker Desktop** installed and running.
2.  **Display Server (Optional for legacy Windows)**:
    *   If you are on **Windows 11** or recent **Windows 10** with **WSLg**, it should work out of the box.
    *   Otherwise, install [VcXsrv](https://sourceforge.net/projects/vcxsrv/) and run it with "Disable access control" checked.

### Running the game

Open your terminal in the project directory and run:

```bash
docker-compose up --build
```

The game window should appear on your desktop.

### Troubleshooting Display

If the window doesn't appear:
- Ensure Docker Desktop is running.
- If using VcXsrv, make sure its icon is in the system tray.
- Try setting the `DISPLAY` environment variable manually:
  `$env:DISPLAY="your-ip:0.0"` (in PowerShell) before running `docker-compose up`.


10. Game Controls

    Mouse Left Click: Select tower / Place tower / Click UI buttons
    Mouse Right Click: Deselect tower / Cancel placement
    Space: Start wave (when not active)
    P: Pause/Unpause game
    ESC: Cancel placement / Deselect tower / Quit game

11. Game Features

    4 Tower Types:
        Basic: Standard damage, good all-rounder
        Sniper: Long range, high damage, slow fire rate
        Splash: Area damage, good against clusters
        Slow: Reduces enemy speed

    Enemy Types:
        Normal: Balanced stats
        Fast: Lower health, high speed
        Tank: High health, slow speed

    Wave System:
        Increasing difficulty
        Wave management UI
        Automatic spawning

    Economy:
        Money from defeating enemies
        Tower costs and upgrades
        Selling towers for refunds

12. Expansions (Optional)

You can enhance the game with:

    Visual Effects: Particles, explosions, screen shakes
    More Towers: Different attack patterns (lasers, mines, etc.)
    Terrain: Path variations, obstacles
    Upgrades: Multiple upgrade paths for towers
    Save/Load: Save game progress
    Mobile Support: Touch controls for mobile
