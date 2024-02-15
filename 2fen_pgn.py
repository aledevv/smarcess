import chess
import chess.svg


if __name__ == "__main__":

    board = chess.Board() #gli oggetti con la lettera grande

    fen_tmp = 'rnbqkbnr/pppppppp/8/8/8/3P4/PPP1PPPP/RNBQKBNR b KQkq - 0 1'

    legal_moves_lst = [ board.san(move)
                        for move in board.legal_moves
                      ]
    
    print(legal_moves_lst)


    for move in board.legal_moves:
        board_clone = board.copy()
        print("before: ", board_clone.fen())
        board_clone.push(move)
        print("after: ", board_clone.fen())
        if board_clone.fen() == fen_tmp:
            print("The move is: ", board.san(move))     # san = standard algebric notation

            break

boardFen = chess.Board("rnbqkbnr/pppppppp/8/8/8/3P4/PPP1PPPP/RNBQKBNR b KQkq - 0 1")

chess.svg.board (
    boardFen
)