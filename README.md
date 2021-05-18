# Othello
Othello is a strategy board game for two players (Black and White), played on an 8 by 8 board. The game traditionally begins with four discs placed in the middle of the board. In this game, the human player (Black) plays against an AI agent (White) that utilizes the minimax strategy (via alpha beta pruning) with several evaluation criterias to consistently beat the human player. 

## Technologies
- Python
- Pygame

## Usage
Clone project
```
git clone https://github.com/pearllaw/Othello.git
cd Othello/
```
Run command to play against AI
```
python -m othello
```

## How to Play
- Black always moves first.
- If it is your turn, make a valid move by outflanking any number of discs in one/more rows in any direction (horizontal, vertical, diagonal)
- All disks that are outflanked will be flipped
- Game alternates between black and white until one/both player(s) cannot make a valid move to outflank the opponent
- Click [here](https://www.eothello.com/) for more information about the rules

## Live Demo
*Yellow squares show valid moves for the current player

![othello_demo2](https://user-images.githubusercontent.com/35009493/118733394-068f7b80-b7f1-11eb-964c-e335bf3aae61.gif)

