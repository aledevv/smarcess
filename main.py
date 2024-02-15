import engine
import gui

if __name__ == "__main__":
    
    # Replace the FEN position with your desired position
    fen_position = "rnbqkbnr/pppp1ppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    
    #create_chessboard_svg(fen_position)
    #svg_to_png()

    
    root = gui.tk.Tk()
    root.withdraw()
    app = gui.ChessboardApp(root)
    app.start()
