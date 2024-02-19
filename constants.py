from enum import Enum
import chess
import chess.svg
from PIL import Image, ImageTk
from picamera2 import Picamera2, Preview


class Turn(Enum):
    WHITE = 1
    BLACK = 2
    
default_font=("DejaVu Sans", 12)
CURRENT_IMAGE_PATH ="images/jpeg/current_position.jpeg"
START_FEN_POSITION = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
START_TURN = Turn.WHITE