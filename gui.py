import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import cairosvg
import chess
import engine
from constants import *




class ChessboardApp:
    def __init__(self, game_window, picam): # picam
        self.color_buttons = []  # To store color buttons for updating state
        self.difficulty_buttons = []  # To store difficulty buttons for updating state
        self.difficulty = ""
        self.depth = 2
        self.player_color = Turn.WHITE
        self.board = chess.Board()
        self.game_window = game_window
        self.picam = picam
        self.turn = Turn.WHITE

        self.labels = []  # Keep track of added labels
        self.moves = []
    ###### Functions 

    def start_gui(self):
        # Create the main window
        self.start_window = tk.Tk()
        sw = self.start_window
        self.start_window.title("Smarcess")
        self.start_window.geometry("480x300")
        
        quit_button = tk.Button(sw, text="Quit", anchor=tk.NW, command=self.exit_popup)
        quit_button.pack(side=tk.TOP, anchor=tk.NW)
        # Create and pack title label
        title_label = tk.Label(sw, text="Smarcess", font=("DejaVu Sanstica", 24))
        title_label.pack()

        difficulty_frame = tk.Frame(sw)
        difficulty_frame.pack()

        difficulties = ["Easy", "Medium", "Hard"]
        
        easy_button = tk.Button(difficulty_frame,font=default_font, text=difficulties[0], command=lambda: self.set_difficulty(difficulties[0]), width=10, height=2)
        easy_button.pack(side=tk.LEFT, padx=10)
        self.difficulty_buttons.append(easy_button)
            
        medium_button = tk.Button(difficulty_frame,font=default_font, text=difficulties[1], command=lambda: self.set_difficulty(difficulties[1]), width=10, height=2)
        medium_button.pack(side=tk.LEFT, padx=10)
        self.difficulty_buttons.append(medium_button)

        hard_button = tk.Button(difficulty_frame,font=default_font, text=difficulties[2], command=lambda: self.set_difficulty(difficulties[2]), width=10, height=2)
        hard_button.pack(side=tk.LEFT, padx=10)
        self.difficulty_buttons.append(hard_button)

        # Create mutable buttons for color options
        color_frame = tk.Frame(sw)
        color_frame.pack()


        color_options = {Turn.WHITE: "White", Turn.BLACK: "Black"}
        white_button = tk.Button(color_frame, text="White",font=default_font, command=lambda: self.set_color("White"), width=10, height=2)
        white_button.pack(side=tk.LEFT, padx=10)
        self.color_buttons.append(white_button)

        black_button = tk.Button(color_frame, text="Black",font=default_font, command=lambda: self.set_color("Black"), width=10, height=2)
        black_button.pack(side=tk.LEFT, padx=10)
        self.color_buttons.append(black_button)
        #hello sinan

        # Create and pack Play button
        self.play_button = tk.Button(sw, text="Play",font=default_font, command=self.open_game_window, state=tk.DISABLED, width=10, height=5)
        self.play_button.pack(pady=20)

        # Add event bindings to update button states
        for button in self.difficulty_buttons:
            button.bind("<Button-1>", lambda event, b=button: self.update_difficulty_button_state(b))

        for button in self.color_buttons:
            button.bind("<Button-1>", lambda event, b=button: self.update_color_button_state(b))
        
        
        self.start_window.mainloop()
        # Add a trace on difficulty_var to enable/disable Play button based on selection
    def update_play_button_state(self):
        if self.difficulty != "":
            self.play_button.config(state=tk.NORMAL)
        else:
            self.play_button.config(state=tk.DISABLED)

    #self.difficulty.trace_add("write", update_play_button_state)
    #self.player_color.trace_add("write", update_play_button_state)

    def illegal_move(self, fen, color, title):
        global img
        global popup
        popup = tk.Toplevel()
        popup.title(title)
        popup.geometry("250x250")
        create_chessboard_svg(fen, color, None, True)
        svg_to_png(True)
        original_image = Image.open("./images/png/error.png")
        resized_image = original_image.resize((150, 150))
        img = ImageTk.PhotoImage(resized_image)
        label = tk.Label(popup, image=img).pack()
        ok_button = tk.Button(popup, text="Ok",font=default_font, command=popup.destroy, width=10, height=3)
        ok_button.pack()

    def open_game_window(self):
        board_ready, self.detected_fen = engine.equal_position(self.board.fen(),self.picam, self.player_color)
        if not board_ready:
            messagebox.showinfo("Error", "Set chessboard at starting position")
        else:
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
            
            self.info_button = tk.Button(tlf, text="Info",command=self.info_move, width=10, height=2)
            self.info_button.grid(column = 0, row = 0)     

            self.resign_button = tk.Button(tlf, text="Resign", command=self.exit_popup, width=10, height=2)
            self.resign_button.grid(column = 1, row = 0)
            

            original_image = Image.open("./images/png/start.png")
            
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

            self.move_button = tk.Button(rf, text="New Move",font=default_font, command=self.new_gui_move, width=20, height=2)
            self.move_button.pack()
            if self.player_color == Turn.BLACK:
                response = engine.getRequestToStockfishAPI(self.board.fen(), self.depth, "bestmove")  # Stockfish API request to get evaluation or best move/line
                json_response = engine.json.loads(response)    # convert bytes response into json object
                self.update_gui_move(chess.Move.from_uci(json_response['data'].split(' ')[1]), None)    # 'data' contains string with the best move
            self.start_window.destroy()
            self.game_window.deiconify()
            self.game_window.mainloop()

    def set_color(self, color):
        #print("button color: " + str(color))
        if color == 'White':
            self.player_color = Turn.WHITE
        else:
            self.player_color = Turn.BLACK
    
    def set_difficulty(self, difficulty):
        #print("button difficulty: " + str(difficulty))
        self.difficulty = difficulty
        self.update_play_button_state()
        if difficulty == "Easy":
            self.depth = 1
        elif difficulty == "Medium":
            self.depth = 5
        else:
            self.depth = 10

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
    
    def on_scroll(self, *args):
        self.scroll_canvas.yview(*args)     
        

    def exit_popup(self):
        self.exit_window = tk.Toplevel(self.game_window)
        ew = self.exit_window
        self.exit_window.geometry("250x250")
        self.exit_window.title("Exit")
        tk.Label(ew, text="Do you want to exit?", pady=20).pack()
        self.exit_buttons_frame = tk.Frame(ew)
        ebf = self.exit_buttons_frame
        self.no_button = tk.Button(ebf, text="No", font=default_font, command=ew.destroy, width=5, height=2)
        self.no_button.grid(column = 0, row = 0)  
        self.yes_button = tk.Button(ebf, text="Yes",font=default_font, command=self.exit_fuction, width=5, height=2)
        self.yes_button.grid(column = 1, row = 0)  
        self.exit_buttons_frame.pack()
        
    def new_gui_move(self):
        if self.player_color == self.turn:
            #print("player part")
            current_move, self.stockfish_move, self.detected_fen = engine.new_move(self.turn, self.player_color, self.depth, self.board.copy(), self.picam)
            if current_move != None:
                self.update_gui_move(current_move, self.stockfish_move)
            else:
                self.illegal_move(self.detected_fen, self.player_color, "Illegal move")
        else:
             #print("stock part")
             board_clone = self.board.copy()
             board_clone.push(self.stockfish_move)
             is_equal, self.detected_fen = engine.equal_position(board_clone.fen(), self.picam, self.player_color)
             if is_equal:
                 self.update_gui_move(self.stockfish_move, None)
                 self.board.push(self.stockfish_move)
             else:
                 self.illegal_move(self.detected_fen, self.player_color, "Not stockfish move")
                
                
    def exit_fuction(self):
        self.game_window.destroy()
        self.picam.close()
        exit()
    
    def update_gui_move(self, current_move, second_move):
        #print(self.turn)
        #print("current move: " + self.board.san(current_move))
        label_move = self.board.san(current_move)
        self.board.push(current_move)
        
        create_chessboard_svg(self.board.fen(), self.player_color, second_move)
        svg_to_png()
        
        new_original_image = Image.open("./images/png/chessboard.png")
        new_resized_image = new_original_image.resize((240, 240))
        new_chessboard_photo = ImageTk.PhotoImage(new_resized_image)

        # Update the canvas with the new image
        self.image_canvas.config(width=240, height=240)
        self.image_canvas.delete("all")  # Remove the previous image
        self.image_canvas.create_image(0, 0, anchor=tk.NW, image=new_chessboard_photo)

        # Update the reference to the current image
        self.chessboard_photo = new_chessboard_photo
        
        if self.turn == Turn.WHITE:
            label = tk.Label(self.scroll_canvas, text=label_move)
            self.turn = Turn.BLACK
        else:
            lab = self.labels.pop()
            first_move = self.moves[-1]
            complete_move = first_move + "\t\t" + label_move
            lab.destroy()
            label = tk.Label(self.scroll_canvas, text=complete_move)
            self.turn = Turn.WHITE
        if second_move != None:
            self.move_button.config(text=self.board.san(second_move))
        else:
            self.move_button.config(text="New move")        
        self.scroll_canvas.create_window((0, len(self.labels) * 30), window=label, anchor='nw')
        self.labels.append(label)
        self.moves.append(label_move)
        self.scroll_canvas.update_idletasks()
        self.scroll_canvas.config(scrollregion=self.scroll_canvas.bbox("all"))
        self.scroll_canvas.yview_moveto('1.0')
    
    def info_move(self):
        global info_popup
        info_popup = tk.Toplevel()
        info_popup.title("Info")
        popup.geometry("250x250")
        label2 = tk.Label(info_popup, text=f"Difficulty:{self.difficulty}").pack(pady=10)
        label3 = tk.Label(info_popup, text="Created by:\nAlessandro De Vidi, Daniele Marisa, Enrico Tenuti").pack(pady=10)
        ok_button = tk.Button(info_popup, text="Ok", command=info_popup.destroy, width=10, height=3)
        ok_button.pack()
            
def create_chessboard_svg(fen_position, player_color, second_move, error = False):
    board = chess.Board(fen_position)
    if second_move != None:
        second_move_string = "B"+second_move.uci()
        if player_color == Turn.BLACK:  
            svg_content = chess.svg.board(board=board,size=350, orientation=chess.BLACK, arrows=[chess.svg.Arrow.from_pgn(second_move_string)])
        else:
            svg_content = chess.svg.board(board=board,size=350, arrows=[chess.svg.Arrow.from_pgn(second_move_string)])
    else:
        if player_color == Turn.BLACK:  
            svg_content = chess.svg.board(board=board,size=350, orientation=chess.BLACK)
        else:
            svg_content = chess.svg.board(board=board,size=350)
    if error:
        with open("./images/svg/error.svg", "w") as svg_file:
            svg_file.write(svg_content)
    else:
        with open("./images/svg/chessboard.svg", "w") as svg_file:
            svg_file.write(svg_content)

def svg_to_png(error = False):
    if error:
        cairosvg.svg2png(url='./images/svg/error.svg', write_to='./images/png/error.png')
    else:
        cairosvg.svg2png(url='./images/svg/chessboard.svg', write_to='./images/png/chessboard.png')
    
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
