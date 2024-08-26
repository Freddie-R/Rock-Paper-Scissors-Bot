# Rock, Paper, Scissors Bot

## Overview

This Python program uses Pygame to create a graphical interface for playing Rock, Paper, Scissors against a bot. The bot uses a strategy based on analyzing the player's past moves to make its choices. The game tracks statistics such as win rates and performs statistical tests to evaluate the bot's performance.

## Features

- **Graphical Interface**: Displays Rock, Paper, and Scissors images.
- **Bot Strategy**: Bot uses historical data to predict the player's next move.
- **Statistics**: Shows the number of rounds played, win rates for both the bot and player, and the result of a statistical test on the bot's performance.
- **Interactive**: Player can click on images to make their move.

## Requirements

- Python 3.x
- Pygame library
- SciPy library

You can install the required libraries using pip:

```bash
pip install pygame scipy
```

## Setup

1. **Download the Code**: Clone or download the repository containing this script.

2. **Prepare Images**: Place the images `rock.png`, `paper.png`, and `scissors.png` in the same directory as the script. These images are used for the game's graphical elements.

3. **Run the Script**: Execute the script using Python:

    ```bash
    python script_name.py
    ```

   Replace `script_name.py` with the actual name of the script file.

## Usage

1. **Start the Game**: The game window will open displaying the Rock, Paper, Scissors images.

2. **Make a Move**: Click on one of the images to choose Rock, Paper, or Scissors.

3. **Game Feedback**: The game will indicate whether you won, lost, or drew the round, and update the statistics accordingly.

4. **Statistics Display**: The game shows the number of rounds played, the win rates of both the bot and the player, and the result of a statistical test on the bot's performance.

## Functions

- `create_display(state)`: Updates the display based on the game state (`"win"`, `"lose"`, `"draw"`, or `"Normal"`).
- `win_rate_test()`: Calculates the p-value for the bot's performance using a two-tailed z-test.
- `effect(state)`: Updates the display and statistics based on the round outcome.
- `create_square(top_right_corner, size, width, thing)`: Draws a square outline for the Rock, Paper, and Scissors images.
- `get_move_from_location(position)`: Determines which move (Rock, Paper, or Scissors) the player selected based on the mouse click location.
- `pick_move()`: Chooses the bot's move based on the player's past moves.
- `get_last_moves(count)`: Retrieves the most recent moves made by the player.

## Notes

- The bot's strategy relies on analyzing the frequency and pattern of the player's past moves.
- The statistical test used to evaluate the bot's performance assumes a null hypothesis of equal probability for each move.

## Troubleshooting

- **Images Not Loading**: Ensure that `rock.png`, `paper.png`, and `scissors.png` are in the same directory as the script and correctly named.
- **Library Errors**: Make sure that Pygame and SciPy are properly installed and up to date.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
