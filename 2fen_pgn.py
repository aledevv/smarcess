import chess
import chess.svg

def compare_FEN(fen1, fen2):
    return reducedFEN(fen1) == reducedFEN(fen2) #bool
    

def reducedFEN(fen):
    return fen.split(' ')[0] #i take only the first part of the fen

def Two_fen_to_pgn(fen_before, fen_after): #function to compere two fen
    board = chess.Board(fen_before) #set the boar with the first fen

    for move in board.legal_moves:
        board_clone = board.copy()
       
        board_clone.push(move) #all the possible legal moves
        #print(board_clone.fen())

        if compare_FEN(board_clone.fen(), fen_after): #compare the possible configuration of the chess board with the real one
          #  print("The move is: ", board.san(move))     # san = standard algebric notation
            return move


if __name__ == "__main__":

    board = chess.Board() 
    
    fen_pos = ["rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1","rnbqkbnr/pppppppp/8/8/8/4P3/PPPP1PPP/RNBQKBNR b KQkq - 0 1","rnbqkbnr/pppp1ppp/4p3/8/8/4P3/PPPP1PPP/RNBQKBNR w KQkq - 0 2","rnbqkbnr/pppp1ppp/4p3/8/8/2N1P3/PPPP1PPP/R1BQKBNR b KQkq - 0 2","rnbq1bnr/ppppkppp/4p3/8/8/2N1P3/PPPP1PPP/R1BQKBNR w KQ - 0 3"] 


    for pos in range(len(fen_pos)-1):                 #range (start, end, step)   range(n)-> 0 - n-1 step 1
        move = Two_fen_to_pgn(fen_pos[pos], fen_pos[pos+1])
        print(board.san(move))
        board.push(move)
    
    
