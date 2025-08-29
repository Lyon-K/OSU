class Player:
    """Base player class"""
    def __init__(self, symbol):
        self.symbol = symbol

    def get_symbol(self):
        return self.symbol
    
    def get_move(self, board):
        raise NotImplementedError()



class HumanPlayer(Player):
    """Human subclass with text input in command line"""
    def __init__(self, symbol):
        Player.__init__(self, symbol)
        self.total_nodes_seen = 0

    def clone(self):
        return HumanPlayer(self.symbol)
        
    def get_move(self, board):
        col = int(input("Enter col:"))
        row = int(input("Enter row:"))
        return  (col, row)


class AlphaBetaPlayer(Player):
    """Class for Alphabeta AI: implement functions minimax, eval_board, get_successors, get_move
    eval_type: int
        0 for H0, 1 for H1, 2 for H2
    prune: bool
        1 for alpha-beta, 0 otherwise
    max_depth: one move makes the depth of a position to 1, search should not exceed depth
    total_nodes_seen: used to keep track of the number of nodes the algorithm has seearched through
    symbol: X for player 1 and O for player 2
    """
    def __init__(self, symbol, eval_type, prune, max_depth):
        Player.__init__(self, symbol)
        self.eval_type = eval_type
        self.prune = prune
        self.max_depth = int(max_depth) 
        self.max_depth_seen = 0
        self.total_nodes_seen = 0
        if symbol == 'X':
            self.oppSym = 'O'
        else:
            self.oppSym = 'X'


    def terminal_state(self, board):
        # If either player can make a move, it's not a terminal state
        for c in range(board.cols):
            for r in range(board.rows):
                if board.is_legal_move(c, r, "X") or board.is_legal_move(c, r, "O"):
                    return False 
        return True 


    def terminal_value(self, board):
        # Regardless of X or O, a win is float('inf')
        state = board.count_score(self.symbol) - board.count_score(self.oppSym)
        if state == 0:
            return 0
        elif state > 0:
            return float('inf')
        else:
            return -float('inf')


    def flip_symbol(self, symbol):
        # Short function to flip a symbol
        if symbol == "X":
            return "O"
        else:
            return "X"


    def alphabeta(self, board):
        # Write minimax function here using eval_board and get_successors
        # type:(board) -> (int, int)
        sucessors = self.get_successors(board, self.symbol)
        highest_eval_board = sucessors[0]
        highest_eval_value = -float('inf')
        alpha = -float('inf')
        beta = float('inf')
        for sucessor in sucessors:
            successor_eval_value = self.minimax(sucessor, self.max_depth, alpha, beta)
            # print(f'TEMP: alphabeta: successor_eval_value: {successor_eval_value}')
            if(successor_eval_value > highest_eval_value):
                highest_eval_board = sucessor
                highest_eval_value = successor_eval_value
                # print('TEMP: ALPHABETA: New successor board')
                # sucessor.display()
            alpha = max(alpha, successor_eval_value)
            if self.prune == '1' and beta <= alpha:
                break
        col, row = highest_eval_board.move
        return col, row


    def minimax(self, board, depth, alpha = -float('inf'), beta = float('inf'), is_alpha = False):
        # print(f'TEMP: MINIMAX: depth: {depth}')
        # print(f'TEMP: MINIMAX: player: ' + 'alpha' if is_alpha else 'beta')
        # print(f'TEMP: MINIMAX: alpha: {alpha}')
        # print(f'TEMP: MINIMAX: beta: {beta}')
        # board.display()
        successors = self.get_successors(board, self.symbol if is_alpha else self.oppSym)
        if depth == 0 or len(successors) == 0:
            self.total_nodes_seen += 1
            # print(f'TEMP: MINIMAX: self.eval_board(board): {self.eval_board(board)}')
            return self.eval_board(board)
        
        for successor in successors:
            self.total_nodes_seen += 1
            successor_eval = self.minimax(successor,  depth - 1, alpha, beta, not is_alpha)
            if is_alpha:
                alpha =  max(successor_eval, alpha)
            else:
                beta =  min(successor_eval, beta)
            if self.prune == '1' and beta <= alpha:
                break
        return alpha if is_alpha else beta


    def eval_board(self, board):
        # Write eval function here
        # type:(board) -> (float)
        if not board.has_legal_moves_remaining(self.symbol) and not board.has_legal_moves_remaining(self.oppSym):
            score = board.count_score(self.symbol) - board.count_score(self.oppSym)
            if score > 0:
                return float('inf')
            elif score < 0:
                return -float('inf')
            else:
                return 0
        value = 0
        for x in range (board.get_num_cols()):
            for y in range (board.get_num_rows()):
                if self.eval_type == '0':
                    value += self.heuristic_0(board, x, y)
                elif self.eval_type == '1':
                    value += self.heuristic_1(board, x, y)
                elif self.eval_type == '2':
                    value += self.heuristic_2(board, x, y)
        return value


    def heuristic_0(self, board, x, y):
        if board.is_cell_empty(x,y):
            return 0
        return 1 if board.grid[x][y] == self.symbol else -1


    def heuristic_1(self, board, x, y):
        if board.is_cell_empty(x,y):
            if board.is_legal_move(x,y,self.symbol):
                return 1
            if board.is_legal_move(x,y,self.oppSym):
                return -1
        return 0


    def heuristic_2(self, board, x, y):
        if x in [0, 3] and y in [0, 3]:
            return 1000 if board.is_legal_move(x,y,self.symbol) else -1000
        if board.is_cell_empty(x,y):
            if board.is_legal_move(x,y,self.symbol):
                return 1
            if board.is_legal_move(x,y,self.oppSym):
                return -1
        return 0


    def get_successors(self, board, player_symbol):
        # Write function that takes the current state and generates all successors obtained by legal moves
        # type:(board, player_symbol) -> (list)
        successors = []
        for i in range(board.get_num_cols()):
            for j in range(board.get_num_rows()):
                if board.is_cell_empty(i, j) and board.is_legal_move(i,j,player_symbol):
                    new_board = board.cloneOBoard()
                    new_board.play_move(i,j,player_symbol)
                    new_board.move = (i,j)
                    successors.append(new_board)
        # print(f'Successors( {self.symbol} ): {[successor.move for successor in successors]}')
        return successors


    def get_move(self, board):
        # Write function that returns a move (column, row) here using minimax
        # type:(board) -> (int, int)
        return self.alphabeta(board)
