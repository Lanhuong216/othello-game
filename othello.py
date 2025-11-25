import argparse
import copy
import signal
import sys
import timeit
import importlib
from board import Board, move_string, print_moves

player = {-1: "Black", 1: "White"}


def game(white_engine, black_engine, game_time=300.0, verbose=False):
    """Run a single game. Raise RuntimeError in the event of time expiration.
    Raise LookupError in the case of a bad move. The tournament engine must
    handle these exceptions."""
    board = Board()
    time_left = {-1: game_time, 1: game_time}
    engine = {-1: black_engine, 1: white_engine}

    if verbose:
        print("INITIAL BOARD\n--\n")
        board.display(time_left)

    for move_num in range(60):
        moves = []
        for color in [-1, 1]:
            start_time = timeit.default_timer()
            move = get_move(board, engine[color], color, move_num, time_left)
            end_time = timeit.default_timer()

            time_left[color] -= round(end_time - start_time, 1)

            if time_left[color] < 0:
                raise RuntimeError(color)

            if move is not None:
                board.execute_move(move, color)
                moves.append(move)

                if verbose:
                    print("--\n")
                    print(f"Round {move_num + 1}: {player[color]} plays in {move_string(move)}\n")
                    board.display(time_left)

        if not moves:
            break

    print("FINAL BOARD\n--\n")
    board.display(time_left)

    return board

def dupgame(white_engine, black_engine, game_time=300.0):
    """Run a single game. Raise RuntimeError in the event of time expiration.
    Raise LookupError in the case of a bad move. The tournament engine must
    handle these exceptions."""
    board = Board()
    time_left = {-1: game_time, 1: game_time}
    engine = {-1: black_engine, 1: white_engine}


    for move_num in range(60):
        moves = []
        for color in [-1, 1]:
            start_time = timeit.default_timer()
            move = get_move(board, engine[color], color, move_num, time_left)
            end_time = timeit.default_timer()

            time_left[color] -= round(end_time - start_time, 1)

            if time_left[color] < 0:
                raise RuntimeError(color)

            if move is not None:
                board.execute_move(move, color)
                moves.append(move)


        if not moves:
            break

    return board


def winner(board):
    black_count = board.count(-1)
    white_count = board.count(1)
    if black_count > white_count:
        return -1, black_count, white_count
    elif white_count > black_count:
        return 1, black_count, white_count
    else:
        return 0, black_count, white_count


def get_move(board, engine, color, move_num, time_left, **kwargs):
    legal_moves = board.get_legal_moves(color)
    if not legal_moves:
        return None
    elif len(legal_moves) == 1:
        return legal_moves[0]
    else:
        move = engine.get_move(copy.deepcopy(board), color, move_num, time_left[color], time_left[-color])
        if move not in legal_moves:
            raise LookupError(color)
        return move


def signal_handler(signal_received, frame):
    print('\n\n- You quit the game!')
    sys.exit()


def main(white_engine, black_engine, game_time, verbose):
    try:
        board = game(white_engine, black_engine, game_time, verbose)
        stats = winner(board)
        bscore, wscore = str(stats[1]), str(stats[2])

        if stats[0] == -1:
            print(f"- {player[-1]} wins the game! ({bscore}-{wscore})")
            return -1, int(bscore), int(wscore)
        elif stats[0] == 1:
            print(f"- {player[1]} wins the game! ({wscore}-{bscore})")
            return 1, int(bscore), int(wscore)
        else:
            print(f"- {player[-1]} and {player[1]} are tied! ({bscore}-{wscore})")
            return 0, int(bscore), int(wscore)

    except RuntimeError as e:
        color = e.args[0]
        if color == -1:
            print(f"\n- {player[-1]} ran out of time!")
            print(f"{player[1]} wins the game! (64-0)")
            return 1, 0, 64
        else:
            print(f"\n- {player[1]} ran out of time!")
            print(f"{player[-1]} wins the game! (64-0)")
            return -1, 64, 0

    except LookupError as e:
        color = e.args[0]
        if color == -1:
            print(f"\n- {player[-1]} made an illegal move!")
            print(f"{player[1]} wins the game! (64-0)")
            return 1, 0, 64
        else:
            print(f"\n- {player[1]} made an illegal move!")
            print(f"{player[-1]} wins the game! (64-0)")
            return -1, 64, 0
        
def dupmain(white_engine, black_engine, game_time, verbose, index):
    try:
        board = dupgame(white_engine, black_engine, game_time)
        stats = winner(board)
        bscore, wscore = str(stats[1]), str(stats[2])

        if stats[0] == -1:
            print(f"Test {index} - {player[-1]} wins the game! ({bscore}-{wscore})")
            return -1, int(bscore), int(wscore)
        elif stats[0] == 1:
            print(f"Test {index} - {player[1]} wins the game! ({wscore}-{bscore})")
            return 1, int(bscore), int(wscore)
        else:
            print(f"Test {index} - {player[-1]} and {player[1]} are tied! ({bscore}-{wscore})")
            return 0, int(bscore), int(wscore)

    except RuntimeError as e:
        color = e.args[0]
        if color == -1:
            print(f"\nTest {index} - {player[-1]} ran out of time!")
            print(f"{player[1]} wins the game! (64-0)")
            return 1, 0, 64
        else:
            print(f"\nTest {index} - {player[1]} ran out of time!")
            print(f"{player[-1]} wins the game! (64-0)")
            return -1, 64, 0

    except LookupError as e:
        color = e.args[0]
        if color == -1:
            print(f"\nTest {index} - {player[-1]} made an illegal move!")
            print(f"{player[1]} wins the game! (64-0)")
            return 1, 0, 64
        else:
            print(f"\nTest {index} - {player[1]} made an illegal move!")
            print(f"{player[-1]} wins the game! (64-0)")
            return -1, 64, 0


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)

    parser = argparse.ArgumentParser(description="Play the Othello game with different engines.")
    parser.add_argument("black_engine", type=str, nargs=1, help="black engine (human, minimax, alpha, random)")
    parser.add_argument("white_engine", type=str, nargs=1, help="white engine (human, minimax, alpha, random)")
    parser.add_argument("-aB", action="store_true", help="turn on alpha-beta pruning for the black player")
    parser.add_argument("-aW", action="store_true", help="turn on alpha-beta pruning for the white player")
    parser.add_argument("-t", type=int, default=300, help="adjust time limit")
    parser.add_argument("-v", action="store_true", help="display the board on each turn")
    parser.add_argument("-lB", type=int, default=4, help="adjust level of minimax")
    parser.add_argument("-lW", type=int, default=4, help="adjust level of minimax")
    parser.add_argument("-dup", type=int, help="loop to run program")
    parser.add_argument("--host", type=str, default="localhost", help="Server host for network mode (client only)")
    parser.add_argument("--port", type=int, default=12345, help="Port for network mode")
    args = parser.parse_args()

    black_engine = args.black_engine[0]
    white_engine = args.white_engine[0]
    player[-1] = f"{black_engine} (black)"
    player[1] = f"{white_engine} (white)"

    try:
        engines_b = importlib.import_module(f"engines.{black_engine}")
        engines_w = importlib.import_module(f"engines.{white_engine}")
        
        # Network receivers need connection manager to be initialized first
        # So we initialize network_server/network_client before network_receiver
        
        # Step 1: Initialize network_server or network_client first (they create connection)
        engine_b = None
        engine_w = None
        
        if black_engine in ["network_server", "network_client"]:
            if black_engine == "network_server":
                engine_b = engines_b.engine(host='0.0.0.0', port=args.port)
            else:
                engine_b = engines_b.engine(host=args.host, port=args.port)
        elif white_engine in ["network_server", "network_client"]:
            # Initialize white engine first if it's network_server/client
            if white_engine == "network_server":
                engine_w = engines_w.engine(host='0.0.0.0', port=args.port)
            else:
                engine_w = engines_w.engine(host=args.host, port=args.port)
        
        # Step 2: Initialize the remaining engine (could be network_receiver or other)
        if engine_b is None:
            engine_b = engines_b.engine()
        
        if engine_w is None:
            engine_w = engines_w.engine()
        engines_list = {"greedy", "human", "random"}
        if args.aB and black_engine not in engines_list:
            engine_b.alpha_beta = True
        if args.aW and white_engine not in engines_list:
            engine_w.alpha_beta = True
            
        if args.lB and black_engine not in engines_list:
            engine_b.ply_maxmin = engine_b.ply_alpha = args.lB
            
        if args.lW and white_engine not in engines_list:
            engine_w.ply_maxmin = engine_w.ply_alpha = args.lW
            
            
        
        v = args.v or white_engine == "human" or black_engine == "human"
        if args.dup:
            print(f"{player[-1]} vs. {player[1]}\n")
            start_time = timeit.default_timer()
            for index in range(args.dup):
                dupmain(engine_w, engine_b, game_time=args.t, verbose=v, index=index+1)
            end_time = timeit.default_timer()
            time_left = round(end_time - start_time, 1)
            print(f"It took {time_left}s")
        else:
            print(f"{player[-1]} vs. {player[1]}\n")
            main(engine_w, engine_b, game_time=args.t, verbose=v)

    except ImportError as e:
        print(f"Unknown engine -- {str(e).split()[-1]}")
        sys.exit()
