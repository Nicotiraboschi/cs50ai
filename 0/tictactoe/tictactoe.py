"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count_x = 0
    count_0 = 0
    
    for row in board:
        for s in row:
            if s == EMPTY:
                continue
            elif s == X:
                count_x += 1
            else:
                count_0 += 1
    if count_x == count_0:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    i = -1
    actions = set()
    for row in board:
        i += 1
        j = -1
        for s in row:
            j += 1
            if s == EMPTY:
                actions.add((i, j))
                continue
            elif s == X:
                continue
            else:
                continue
    
    return actions

# MAIN


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = [row[:] for row in board]
    i = action[0]
    j = action[1]
    if new_board[i][j] != EMPTY:
        raise Exception("not possible")
    if i < 0 or i > 2 or j < 0 or j > 2:
        raise Exception("not possible")
    player_to_move = player(board)
    new_board[i][j] = player_to_move
    return new_board
        
# MAIN


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    squares = []

    for row in board:
        for square in row:
            squares.append(square)
            
    def check_for_row(p):
        if p != 0 and p != 3 and p != 6:
            return None
        value = EMPTY
        n = p
        if squares[n] != EMPTY:
            value = squares[n]
            n += 1
            if squares[n] == value:
                n += 1
                if squares[n] == value:
                    return (value)
        return None
    
    def check_for_columns(p):
        if p != 0 and p != 1 and p != 2:
            return None
        n = p
        value = EMPTY
        if squares[n] != EMPTY:
            value = squares[n]
            n += 3
            if squares[n] == value:
                n += 3
                if squares[n] == value:
                    return (value)
        return None
    
    def check_for_diag_from_left():
        n = 0
        value = EMPTY
        if squares[n] != EMPTY:
            value = squares[n]
            n = 4
            if squares[n] == value:
                n = 8
                if squares[n] == value:
                    return (value) 
        return None
    
    def check_for_diag_from_right():
        n = 2
        value = EMPTY
        if squares[n] != EMPTY:
            value = squares[n]
            n = 4
            if squares[n] == value:
                n = 6
                if squares[n] == value:
                    return (value) 
        return None
    
    result = None
    result = check_for_row(0)
    result = check_for_row(1)
    check_for_row(2)
    
    result = check_for_diag_from_left()
    if result != None:
        return result
    result = check_for_diag_from_right()
    if result != None:
        return result
    for i in [0, 3, 6]:
        result = check_for_row(i)
        if result != None:
            return result
    for i in [0, 1, 2]:
        result = check_for_columns(i)
        if result != None:
            return result
    # return check_all_squares()
    return None

# MAIN


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    squares = []

    for row in board:
        for square in row:
            squares.append(square)

    def check_for_row(p):
        if p != 0 and p != 3 and p != 6:
            return None
        value = EMPTY
        n = p
        if squares[n] != EMPTY:
            value = squares[n]
            n += 1
            if squares[n] == value:
                n += 1
                if squares[n] == value:
                    return (True)
        return None
    
    def check_for_columns(p):
        if p != 0 and p != 1 and p != 2:
            return None
        n = p
        value = EMPTY
        if squares[n] != EMPTY:
            value = squares[n]
            n += 3
            if squares[n] == value:
                n += 3
                if squares[n] == value:
                    return (True)
        return None
    
    def check_for_diag_from_left():
        n = 0
        value = EMPTY
        if squares[n] != EMPTY:
            value = squares[n]
            n = 4
            if squares[n] == value:
                n = 8
                if squares[n] == value:
                    return (True) 
        return None
    
    def check_for_diag_from_right():
        n = 2
        value = EMPTY
        if squares[n] != EMPTY:
            value = squares[n]
            n = 4
            if squares[n] == value:
                n = 6
                if squares[n] == value:
                    return (True) 
        return None
    
    result = None
    result = check_for_row(0)
    result = check_for_row(1)
    check_for_row(2)
    
    def check_all_squares():
        for row in board:
            for square in row:
                if square == EMPTY:
                    return False
        return True

    result = check_for_diag_from_left()
    if result != None:
        return result
    result = check_for_diag_from_right()
    if result != None:
        return result
    for i in [0, 3, 6]:
        result = check_for_row(i)
        if result != None:
            return result
    for i in [0, 1, 2]:
        result = check_for_columns(i)
        if result != None:
            return result
    return check_all_squares()
            
    # keep a value n. check list[n]. if not empty, sign the value. check the value for value[n+1]. if == value, check n++2. if == value, wins. 
          
    # raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    res = winner(board)
    if res == X:
        return 1
    elif res == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    
    if winner(board):
        return None
    # MAIN
    
    if len(actions(board)) == 9:
        return (0, 0)
    
    if len(actions(board)) == 8:
        if board[1][1] == None:
            return (1, 1)
        else:
            return (0, 0)
        
    def check_rows(board):
        o_value = None
        x_value = None
        for row in board:
            if row[0] == row[1] and row[0] != None and row[2] == None:
                player_to_move = row[0]
                if player_to_move == X:
                    x_value = (board.index(row), 2)
                else:
                    o_value = (board.index(row), 2)
            if row[0] == row[2] and row[0] != None and row[1] == None:
                player_to_move = row[0]
                if player_to_move == X:
                    x_value = (board.index(row), 1)
                else:
                    o_value = (board.index(row), 1)
                    
            if row[1] == row[2] and row[1] != None and row[0] == None:
                player_to_move = row[1]
                if player_to_move == X:
                    x_value = (board.index(row), 0)
                else:
                    o_value = (board.index(row), 0)
        player_to_move = player(board)
        if player_to_move == X:
            if x_value:
                return x_value
            else:
                if o_value:
                    return o_value
        if player_to_move == O:
            if o_value:
                return o_value
            else:
                if x_value:
                    return x_value
        return None
            
    def check_columns(board):
        o_value = None
        x_value = None
        if board[0][0] == board[1][0] and board[0][0] != None and board[2][0] == None:
            player_to_move = board[0][0]
            if player_to_move == X:
                x_value = (2, 0)
            else:
                o_value = (2, 0)
        if board[0][1] == board[1][1] and board[0][1] != None and board[2][1] == None:
            player_to_move = board[0][1]
            if player_to_move == X:
                x_value = (2, 1)
            else:
                o_value = (2, 1)
                
        if board[0][2] == board[1][2] and board[0][2] != None and board[2][2] == None:
            player_to_move = board[0][2]
            if player_to_move == X:
                x_value = (2, 2)
            else:
                o_value = (2, 2)
        
        if board[0][0] == board[2][0] and board[0][0] != None and board[1][0] == None:
            player_to_move = board[0][0]
            if player_to_move == X:
                x_value = (1, 0)
            else:
                o_value = (1, 0)
        if board[0][1] == board[2][1] and board[0][1] != None and board[1][1] == None:
            player_to_move = board[0][1]
            if player_to_move == X:
                x_value = (1, 1)
            else:
                o_value = (1, 1)
                
        if board[0][2] == board[2][2] and board[0][2] != None and board[1][2] == None:
            player_to_move = board[0][2]
            if player_to_move == X:
                x_value = (1, 2)
            else:
                o_value = (1, 2)
        
        if board[1][0] == board[2][0] and board[1][0] != None and board[0][0] == None:
            player_to_move = board[1][0]
            if player_to_move == X:
                x_value = (0, 0)
            else:
                o_value = (0, 0)
        if board[1][1] == board[2][1] and board[1][1] != None and board[0][1] == None:
            player_to_move = board[1][1]
            if player_to_move == X:
                x_value = (0, 1)
            else:
                o_value = (0, 1)
        
        if board[1][2] == board[2][2] and board[1][2] != None and board[0][2] == None:
            player_to_move = board[1][2]
            if player_to_move == X:
                x_value = (0, 2)
            else:
                o_value = (0, 2)
        player_to_move = player(board)
        if player_to_move == X:
            if x_value:
                return x_value
            else:
                if o_value:
                    return o_value
        if player_to_move == O:
            if o_value:
                return o_value
            else:
                if x_value:
                    return x_value
        return None
        
    def check_diag_left(board):
        o_value = None
        x_value = None
        if board[0][0] == board[1][1] and board[0][0] != None and board[2][2] == None:
            player_to_move = board[0][0]
            if player_to_move == X:
                x_value = (2, 2)
            else:
                o_value = (2, 2)
        if board[0][0] == board[2][2] and board[0][0] != None and board[1][1] == None:
            player_to_move = board[0][0]
            if player_to_move == X:
                x_value = (1, 1)
            else:
                o_value = (1, 1)
        if board[1][1] == board[2][2] and board[1][1] != None and board[0][0] == None:
            player_to_move = board[1][1]
            if player_to_move == X:
                x_value = (0, 0)
            else:
                o_value = (0, 0)
        player_to_move = player(board)
        if player_to_move == X:
            if x_value:
                return x_value
            else:
                if o_value:
                    return o_value
        
        if player_to_move == O:
            if o_value:
                return o_value
            else:
                if x_value:
                    return x_value
        return None
    
    def check_diag_right(board):
        o_value = None
        x_value = None
        if board[0][2] == board[1][1] and board[0][2] != None and board[2][0] == None:
            player_to_move = board[0][2]
            if player_to_move == X:
                x_value = (2, 0)
            else:
                o_value = (2, 0)
        if board[0][2] == board[2][0] and board[0][2] != None and board[1][1] == None:
            player_to_move = board[0][2]
            if player_to_move == X:
                x_value = (1, 1)
            else:
                o_value = (1, 1)
        if board[1][1] == board[2][0] and board[1][1] != None and board[0][2] == None:
            player_to_move = board[1][1]
            if player_to_move == X:
                x_value = (0, 2)
            else:
                o_value = (0, 2)
        player_to_move = player(board)
        if player_to_move == X:
            if x_value:
                return x_value
            else:
                if o_value:
                    return o_value
        if player_to_move == O:
            if o_value:
                return o_value
            else:
                if x_value:
                    return x_value
        return None
    
    if check_rows(board):
        return check_rows(board)
    if check_columns(board):
        return check_columns(board)
    if check_diag_left(board):
        return check_diag_left(board)
    if check_diag_right(board):
        return check_diag_right(board)
         
    # MAIN  
                   
    possible_actions = actions(board)
    lists = {}
    for i in range(1, len(possible_actions) + 1):
        lists[i] = []
        
    def loop(new_board):
        possible_moves = actions(new_board)
        for possible_move in possible_moves:
            res = result(new_board, possible_move)
            terminated = terminal(res)               
            obj = {"state": res, "move_parent": possible_move, "eval": []}
            if terminated:
                value = utility(res)
                obj["eval"].append(value)
                lists[len(possible_moves)].append(obj)
                continue
            else:
                lists[len(possible_moves)].append(obj)
                loop(res)
            
    loop(board)
    
    def get_parent_board(child_board, action):
        new_board = child_board
        new_board[action[0]][action[1]] = EMPTY
        
        return new_board
        
    # check the range
    i = 0
    
    def get_value(list, player_who_moves): 
               
        if player_who_moves == X:
            return max(list)
        else:
            return min(list)
        
    while len(lists.keys()) > 1:
        i += 1
        for object in lists[i]:
            if len(object["eval"]):
                to_move = player(object["state"])
                object["eval"] = [get_value(object["eval"], to_move)]

            new_board = get_parent_board(object["state"], object["move_parent"])
            player_to_move = player(object["state"])
            ev = get_value(object["eval"], player_to_move)
            for ob in lists[i+1]:
                if ob["state"] == new_board:
                    ob["eval"].append(ev)
        del lists[i]    
    
    if player(board) == O: 
        val = max(lists[len(possible_actions)][0]["eval"])
    else:
        val = min(lists[len(possible_actions)][0]["eval"])
    max_min = {"move": lists[len(possible_actions)][0]["move_parent"], "value": val}
    
    for ob in lists[len(possible_actions)]:
        to_move = player(ob["state"])
        ob["eval"] = get_value(ob["eval"], to_move)
        ev = ob["eval"]
        if to_move == O and ev >= max_min["value"]:
            max_min["move"] = ob["move_parent"]
            max_min["value"] = ev
        elif to_move == X and ev <= max_min["value"]:  
            max_min["move"] = ob["move_parent"]
            max_min["value"] = ev
    return tuple(max_min["move"])