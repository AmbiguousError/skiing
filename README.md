# Horace Skis Again! - Clouds!

## Description

"Horace Skis Again! - Clouds!" is a fun, fast-paced arcade-style skiing game. Take control of Horace as he speeds down a snowy mountain, navigating through treacherous trees and challenging flag gates. The goal is to ski as far as possible, racking up points by successfully passing through gates, while avoiding obstacles. The game features a dynamic parallax background with mountains, hills, snow, and even foreground clouds for an immersive experience!

## Gameplay

You control Horace, the skier, who is constantly moving down the slope. Your objective is to:

* **Steer** Horace left and right to avoid crashing into trees.
* **Ski between the flag pairs** (green on the left, red on the right) to score points.
* Survive as long as you can! The game's speed increases as your score gets higher.

A collision with a tree or missing a gate will end the game.

## How to Play

* **Left Arrow Key:** Move Horace to the left.
* **Right Arrow Key:** Move Horace to the right.
* **Enter Key (on Start Screen):** Start the game.
* **'R' Key (on Game Over Screen):** Return to the Start Screen to play again.

## Features

* **Endless Skiing Fun:** The slope goes on forever!
* **Dynamic Obstacles:** Navigate around randomly spawning trees.
* **Scoring Gates:** Pass between pairs of flags (green/left, red/right) to earn 10 points per gate.
* **Increasing Difficulty:** The scrolling speed of the game increases as you score more points, making it more challenging.
* **Parallax Scrolling Background:** Multi-layered background with sky, distant mountains, closer hills, textured snow, and foreground clouds that move at different speeds, creating a sense of depth.
* **Animated Player:** Horace's skis and poles change direction as you steer.
* **High Score System:** The game saves your top scores locally in `horace_high_scores.txt`. The top 3 scores are displayed on the start screen.
* **Clear Game States:** Distinct start screen, gameplay screen, and game over screen.

## Running the Game

### From Source Code (`ski.py`)

To run the game from the Python source code, you will need:

1.  **Python 3.x:** If you don't have Python installed, download it from [python.org](https://www.python.org/).
2.  **Pygame:** This is the library used to create the game. You can install it using pip:
    ```bash
    pip install pygame
    ```

Once Python and Pygame are set up, navigate to the directory containing `ski.py` in your terminal or command prompt and run:

```bash
python ski.py
Using the Executable (ski.exe)A pre-compiled version of the game, ski.exe, is available in the dist folder (if it has been created using a tool like PyInstaller).Navigate to the dist folder.Double-click on `ski.exe