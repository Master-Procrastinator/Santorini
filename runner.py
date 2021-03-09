from Game import *


def main(agent):
    win = None
    board = Board(agent, HumanPlayer("B"))
    board = board.PlayerA.place_workers(board)
    board = board.PlayerB.place_workers(board)
    #board.intialize_workers([[1,1],[1,3]],[[3,1],[3,3]])
    currentPlayer = board.PlayerA
    while win == None:
        win = board.start_turn_check_win(currentPlayer)
        if win != None:
            break
        else:
            board.print_board()
            print("----------------------------------------------------------------\n")
            board = currentPlayer.action(board)
            win = board.end_turn_check_win(currentPlayer)
            if win != None:
                board.print_board()
                break

        if currentPlayer == board.PlayerA:
            currentPlayer = board.PlayerB
        else:
            currentPlayer = board.PlayerA
    return win





if __name__=='__main__':
    main()