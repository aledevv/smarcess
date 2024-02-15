import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import chess
import chess.svg
import random
import cairosvg
from enum import Enum



class Turn(Enum):
    WHITE = 1
    BLACK = 2

class ChessboardApp:
    def __init__(self, game_window):
        self.color_buttons = []  # To store color buttons for updating state
        self.difficulty_buttons = []  # To store difficulty buttons for updating state
        self.difficulty = ""
        self.player_color = ""
        
        self.game_window = game_window
        
        self.turn = Turn.WHITE

        self.labels = []  # Keep track of added labels
        self.moves = []
    ###### Functions 
    
    def start(self):
        # Create the main window
        self.start_window = tk.Tk()
        sw = self.start_window
        self.start_window.title("smarcess")
        self.start_window.geometry("480x300")

        # Create and pack title label
        title_label = tk.Label(sw, text="smarcess", font=("Helvetica", 16))
        title_label.pack(pady=20)

        difficulty_frame = tk.Frame(sw)
        difficulty_frame.pack()

        difficulties = ["easy", "medium", "hard"]
        self.difficulty = tk.StringVar()



        for difficulty in difficulties:
            difficulty_button = tk.Button(difficulty_frame, text=difficulty, command=lambda diff=difficulty: self.difficulty.set(diff))
            difficulty_button.pack(side=tk.LEFT, padx=10)
            self.difficulty_buttons.append(difficulty_button)

        # Create mutable buttons for color options
        color_frame = tk.Frame(sw)
        color_frame.pack()


        color_options = ["white", "black"]
        self.player_color = tk.StringVar()
        self.player_color.set(color_options[0])  # Default color is white

        for color in color_options:
            color_button = tk.Button(color_frame, text=color, command=lambda col=color: self.player_color.set(col))
            color_button.pack(side=tk.LEFT, padx=10)
            self.color_buttons.append(color_button)
        #hello sinan

        # Create and pack Play button
        play_button = tk.Button(sw, text="Play", command=self.open_game_window, state=tk.DISABLED)
        play_button.pack(pady=20)

        # Add event bindings to update button states
        for button in self.difficulty_buttons:
            button.bind("<Button-1>", lambda event, b=button: self.update_difficulty_button_state(b))

        for button in self.color_buttons:
            button.bind("<Button-1>", lambda event, b=button: self.update_color_button_state(b))

        # Add a trace on difficulty_var to enable/disable Play button based on selection
        def update_play_button_state(*args):
            if self.difficulty.get() and self.player_color.get():
                play_button.config(state=tk.NORMAL)
            else:
                play_button.config(state=tk.DISABLED)

        self.difficulty.trace_add("write", update_play_button_state)
        self.player_color.trace_add("write", update_play_button_state)
        self.start_window.mainloop()
        

    def open_game_window(self):
        self.start_window.destroy()
        
        selected_difficulty = self.difficulty.get()
        selected_color = self.player_color.get()

        self.game_window.title("Smarcess")
        self.game_window.geometry("480x300")

        self.left_frame = tk.Frame(self.game_window, height=240, width=240)
        self.left_frame.grid(column = 0, row = 0)
        lf = self.left_frame
        
        self.right_frame = tk.Frame(self.game_window, height=240, width=240)
        self.right_frame.grid(column = 1, row = 0)  
        rf = self.right_frame
        
        self.top_left_frame = tk.Frame(lf, height=40, width=240)
        self.top_left_frame.pack()
        tlf = self.top_left_frame
        
        self.cancel_button = tk.Button(tlf, text="Cancel", command=self.cancel_move,  width=10, height=2)
        self.cancel_button.grid(column = 0, row = 0)     

        self.resign_button = tk.Button(tlf, text="Resign", command=self.exit_popup,  width=10, height=2)
        self.resign_button.grid(column = 1, row = 0)

        original_image = Image.open("./images/png/chessboard.png")
        resized_image = original_image.resize((240, 240))
        self.chessboard_photo = ImageTk.PhotoImage(resized_image)
        self.image_canvas = tk.Canvas(lf, width=240, height=240)
        self.image_canvas.pack()
        self.image_canvas.create_image(0, 0, anchor=tk.NW, image=self.chessboard_photo)
        
        self.canvas_frame = ttk.Frame(rf)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.scroll_canvas = tk.Canvas(self.canvas_frame, height=200, width=200)
        self.scroll_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=self.scroll_canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.scroll_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.move_button = tk.Button(rf, text="Add Label", command=self.new_move,  width=10, height=2)
        self.move_button.pack(pady=10)

        # Add your game logic here based on the selected difficulty and color
        print(f"Starting game with difficulty: {selected_difficulty} and color: {selected_color}")
        self.game_window.deiconify()
        self.game_window.mainloop()
        


    def update_difficulty_button_state(self, selected_button):
        for button in self.difficulty_buttons:
            if button == selected_button:
                button.config(bg="lightblue")  # Highlight the selected button
            else:
                button.config(bg="gray85")  # Reset the background color

    def update_color_button_state(self, selected_button):
        for button in self.color_buttons:
            if button == selected_button:
                button.config(bg="lightblue")  # Highlight the selected button
            else:
                button.config(bg="gray85")  # Reset the background color
    
    def error(self, text):
        messagebox.showwarning("Error", text)
    
    
    def on_scroll(self, *args):
        self.scroll_canvas.yview(*args)     
        

    def exit_popup(self):
        self.exit_window = tk.Toplevel(self.game_window)
        ew = self.exit_window
        self.exit_window.geometry("250x250")
        self.exit_window.title("Exit")
        tk.Label(ew, text="Do you want to exit?").pack()
        self.exit_buttons_frame = tk.Frame(ew)
        ebf = self.exit_buttons_frame
        self.no_button = tk.Button(ebf, text="No", command=ew.destroy)
        self.no_button.grid(column = 0, row = 0)  
        self.yes_button = tk.Button(ebf, text="Yes", command=self.game_window.destroy)
        self.yes_button.grid(column = 1, row = 0)  
        self.exit_buttons_frame.pack()
        
    def new_move(self):
        move_text = "move"
        print(self.turn)
        if self.turn == Turn.WHITE:
            label = tk.Label(self.scroll_canvas, text=move_text)
            self.turn = Turn.BLACK
        else:
            lab = self.labels.pop()
            first_move = self.moves[-1]
            complete_move = first_move + move_text
            lab.destroy()
            label = tk.Label(self.scroll_canvas, text=complete_move)
            self.turn = Turn.WHITE

        self.scroll_canvas.create_window((0, len(self.labels) * 30), window=label, anchor='nw')
        self.labels.append(label)
        self.moves.append(move_text)
        self.scroll_canvas.update_idletasks()
        self.scroll_canvas.config(scrollregion=self.scroll_canvas.bbox("all"))
        self.scroll_canvas.yview_moveto('1.0')
        
        self.error("THIS IS A SINAN")
    
    def cancel_move(self):
        if len(self.moves) == 0:
            return
        print(self.turn)
        lab = self.labels.pop()
        self.moves.pop()
        lab.destroy()
        if self.turn==Turn.BLACK:
            self.turn=Turn.WHITE
        else:
            first_move = self.moves[-1]
            label = tk.Label(self.scroll_canvas, text=first_move)
            self.scroll_canvas.create_window((0, len(self.labels) * 30), window=label, anchor='nw')
            self.labels.append(label)
            self.moves.append(first_move)
            self.scroll_canvas.update_idletasks()
            self.scroll_canvas.config(scrollregion=self.scroll_canvas.bbox("all"))
            self.scroll_canvas.yview_moveto('1.0')
            self.turn=Turn.BLACK
            
def create_chessboard_svg(fen_position):
    board = chess.Board(fen_position)
    svg_content = chess.svg.board(board=board, fill=dict.fromkeys(board.attacks(chess.E4), "#cc0000cc"),
     arrows=[chess.svg.Arrow(chess.E4, chess.F6, color="#0000cccc")],
     squares=chess.SquareSet(chess.BB_DARK_SQUARES & chess.BB_FILE_B),
     size=350)
    
    with open("chessboard.svg", "w") as svg_file:
        svg_file.write(svg_content)

def svg_to_png():
	cairosvg.svg2png(url='chessboard.svg', write_to='chessboard.png')
    
'''
if __name__ == "__main__":
    
    # Replace the FEN position with your desired position
    fen_position = "rnbqkbnr/pppp1ppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    
    create_chessboard_svg(fen_position)
    svg_to_png()
    game_window = tk.Tk()
    app = ChessboardApp(game_window)
    game_window.mainloop()
'''