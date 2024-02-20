

# Smartchess

<div align='center'>
<img src="assets/chess2.png" alt="drawing" width="150"/>
</div>

<br>

![Author](https://img.shields.io/badge/Author-Alessandro_De_Vidi-blue)
![Author](https://img.shields.io/badge/Author-Daniele_Marisa-blue)
![Author](https://img.shields.io/badge/Author-Enrico_Tenuti-blue)

![Version](https://img.shields.io/badge/Version-1.0-brightgreen)
![Platform](https://img.shields.io/badge/Platform-Python-orange)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

Application for Raspberry PI to play chess games on a real chessboard against Stockfish chess engine.


## Demo

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/gtDqMxrO9MM/0.jpg)](https://www.youtube.com/watch?v=gtDqMxrO9MM)


## Files and directories
- _main.py_: main application

- _gui.py_: the code of the user interface

- _2fen_pgn_: function to convert 2 FEN images to PGN move

- constants.py: file in which all constant values and parameters are present

- _engine.py_: code of ML models for position inference and game management

- _images_ folder contains pictures to process.

- _weights_: folder containing model weights for detections


> [!WARNING]
> **Weights are tuned using our chessboard and pieces**.
> If you want to use yours, you have to fine-tune a new model (this applies to both corner and pieces detection)

## Project layout


```bash
├── 2fen_pgn.py
├── README.md
├── assets
│   ├── chess2.png
│   ├── corners
│   │   ├── batch_training.jpeg
│   │   ├── charts.png
│   │   ├── corners.png
│   │   ├── labels.jpeg
│   │   └── p-curve.png
│   ├── corners_.png
│   ├── grid_.png
│   ├── photo_.jpeg
│   ├── pieces
│   │   ├── conf_matrix.png
│   │   ├── conf_matrix_normalized.png
│   │   ├── correlogram.jpeg
│   │   ├── labels.png
│   │   ├── plots.png
│   │   ├── pr_curve.png
│   │   ├── results.csv
│   │   ├── roboflow_deploy
│   │   │   ├── model_artifacts.json
│   │   │   ├── results.csv
│   │   │   ├── results.png
│   │   │   └── state_dict.pt
│   │   └── roboflow_deploy.zip
│   ├── pieces_.png
│   └── virtual_.png
├── constants.py
├── engine.py
├── fen2pgn.py
├── gui.py
├── images
│   ├── png
│   │   ├── 1.jpeg
│   │   └── chessboard.png
│   └── svg
│       └── chessboard.svg
├── libcairo.2.dylib
├── main.py
├── requirements.txt
└── weights
    ├── new_corners.pt
    └── pieces.pt
```
## Detection process
1. When user makes a move, is taken a photo of their chessboard.
    <br> <img src="assets/photo_.jpeg" width="500"/>
2. A first model detects corners of the chessboard.
   <br> <img src="assets/corners_.png" width="500"/>
3. Image is cropped and transformed from 3D into 2D and squares position is mapped through a grid.
   <br> <img src="assets/grid_.png" width="500"/>
> [!NOTE]  
> Since the camera has wide angle the image results to be distorted, as a result the **grid could not be perfectly aligned** to the squares. An __offset__ parameter has been applied to adjust the grid position once the camera is set on a fixed position.

6. Pieces are detected with a second model
   <br> <img src="assets/pieces_.png" width="500"/>
8. Piece positions are infered by intersecating bounding box areas with grid cells
9. FEN is written and it can be exported to Lichess or sent to a Stockfish API for analysis
    <br> <img src="assets/virtual_.png" width="500"/> <br>
The same process is described in [this repo](https://github.com/shainisan/real-life-chess-vision?ref=blog.roboflow.com).

## Training
We used YOLOv8n models to both train corners and pieces recognition.
Some training details are shown below.
### Corners
<table id="pics" style="border: 0">
    <tr>
      <td><img src="assets/corners/corners.png" width="500" /></td>
      <td><img src="assets/corners/charts.png" width="500"/></td>
    </tr>
    <tr>
      <td><img src="assets/corners/labels.jpeg" width="500"/></td>
      <td><img src="assets/corners/batch_training.jpeg" width="500"/></td>
    </tr>
</table>


### Pieces
<table id="pics" style="border: 0">
    <tr>
      <td><img src="assets/pieces/conf_matrix_normalized.png" width="500" /></td>
      <td><img src="assets/pieces/plots.png" width="500"/></td>
    </tr>
    <tr>
      <td><img src="assets/pieces/labels.png" width="500"/></td>
      <td><img src="assets/pieces/correlogram.jpeg" width="500"/></td>
    </tr>
</table>


## Requirements

![](https://img.shields.io/badge/Raspberry%20Pi-A22846?style=for-the-badge&logo=Raspberry%20Pi&logoColor=white)


### Hardware
- Raspberry (PI 3/4 suggested)
- Camera      [OV5647]
- LCD display [K-0403]
- FFC cable 15 pin
- Structure: base 34x34cm height 36cm


### Software and Dependencies
- How to set up the environment Rasperry, camera and see if they are working...
- Every time  we train a model we do an helth dataset check which shows the disposition of every piece on the board and how many time it appears on each square.
  We re-trained the model in the areas where pieces were less rapresented, we did this to improve as much as possible the generalization.


## Installation

Clone respository   [TO UPDATE]

```bash
git clone https://github.com/aledevv/smarcess.git
```
Install requirements
```bash
pip install -r -requirements.txt
```
Install tk-inter for gui
```bash
sudo apt-get install python-tk
```
## Usage

```bash
python main.py
```
The opening windows will ask you to choose difficulty and which color you are going to play. Pressing "Play" a position check will be launched to verify whether the pieces are set in the starting postion, if they don't an error pop-up will be shown, otherwise the game window will appear.

<div align="center"><img src="assets/opening_win.jpeg" width="500"/></div>

The game window will show the current board position.

If you are **playing with the white pices** you have to play a move and press "New move". 

If you are **playing with the black pieces** you have to make engine's move, then yours and press "New Move".

<div align="center"><img src="assets/game_win.jpeg" width="500"/></div>

Moves are stored on the right side of the window (white's move on the left and black's ones on the right).
Each time the engine or the player will make a move a **positional check** has to be excuted to veify the correctness of the position. In case of illegal move or if the player made engine's move wrongly an **error pop-up** will be shown, asking to correct the mistake.
The games ends either according to chess game rules (checkmate, stalemate, repetition...) or by using the "Resign" button for the user.

> [!CAUTION]
> **Resign button is heighly suggested to exit the game**.
> 
> If you want to quit the game, use the "Resign" button instead of closing a window. By opening the game again camera issues could happen.


## Links

- [YouTube video link](https://youtu.be/gtDqMxrO9MM)

- [Presentation link](https://docs.google.com/presentation/d/12JJgGUjxVQPKkN6xJS_Uz7CiUyjn4UuTajRMokCkEvQ/edit?usp=sharing)

  
## Authors

- [Alessandro De Vidi](https://www.github.com/aledevv)
- [Daniele Marisa](https://github.com/DanMa02)
- [Enrico Tenuti](https://github.com/enricotenuti)


## License

MIT License click [here](https://choosealicense.com/licenses/mit/) for more details.

