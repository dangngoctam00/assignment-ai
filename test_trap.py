import math
import random
import time

SIZE = 5
PLAYER_MAX = 1
PLAYER_MIN = -1
EMPTY = 0
TIMELIMIT = 0.07
INF = math.inf




class Board:
    def __init__(self, state = []):
        self.nums_max = 0
        self.nums_min = 0   
        self.board = list()
        if len(state) > 0:
            self.createBoard(state)        
       

    def createBoard(self, state):
        self.nums_max = 0
        self.nums_min = 0
        self.board = list()
        for i in range(SIZE):
            for j in range(SIZE):
                cur_player = state[i][j]
                if cur_player == PLAYER_MAX:
                    self.board.append(1)
                    self.nums_max += 1
                elif cur_player == PLAYER_MIN:
                    self.board.append(-1)
                    self.nums_min += 1       
                else:
                    self.board.append(0)   


    def static_evaluation(self):
        if self.nums_max == 0:
            return -INF
        if self.nums_min == 0:
            return INF
        return self.nums_max - self.nums_min

    def get_all_available_move(self, player, opponent):
        opponent_start = opponent[0]
        opponent_end = opponent[1]
        if opponent_start != opponent_end and PreviousBoard.board.nums_max == self.nums_max \
                 and PreviousBoard.board.nums_min == self.nums_min:

            available_move = list()
            trap_list = list()
            isTrap = False
            for i in range(SIZE*SIZE):
                if self.board[i] == player:
                    adjacency_list = None
                    if i % 2 == 0:
                        adjacency_list = [i + 6, i - 6, i + 5, i - 5, i + 4, i - 4, i + 1, i - 1]
                    else:
                        adjacency_list = [i + 5, i - 5, i + 1, i - 1]
                    
                    for adjacency_node in adjacency_list:
                        if self.isValidTargetPosition(i, adjacency_node):
                            if adjacency_node == opponent_start:
                                symmetric_pair_list = None
                                if adjacency_node % 2 == 0:
                                    symmetric_pair_list = [(adjacency_node - 6, adjacency_node + 6), (adjacency_node - 5, adjacency_node + 5), (adjacency_node - 4, adjacency_node + 4), (adjacency_node - 1, adjacency_node + 1)]
                                else:
                                    symmetric_pair_list = [(adjacency_node - 5, adjacency_node + 5), (adjacency_node - 1, adjacency_node + 1)]
                                for symmetric_pair in symmetric_pair_list:
                                    if Board.isAdjacentAndValid(adjacency_node, symmetric_pair[0]) and Board.isAdjacentAndValid(adjacency_node, symmetric_pair[1]):
                                        if not self.board[symmetric_pair[0]] in [self.board[i], 0] and not self.board[symmetric_pair[1]] in [self.board[i], 0]:
                                            if PreviousBoard.board.board[symmetric_pair[0]] == 0 or PreviousBoard.board.board[symmetric_pair[1]] == 0 or PreviousBoard.board.board[adjacency_node] != 0:
                                                isTrap = True
                                                trap_list.append((i, adjacency_node))
                                                break                                       
                            
                            available_move.append((i, adjacency_node))
            print("abc")
            if isTrap:
                trap_list = list(filter(lambda move: move[1] == opponent_start, trap_list))
                print("trap_list: ", trap_list)
                return trap_list
            return available_move
        else:
            available_move = list()
            for i in range(SIZE*SIZE):
                if self.board[i] == player:
                    lst = list()
                    if i%2 == 0:
                        lst = [i-6, i-5, i-4, i-1, i+1, i+4, i+5, i+6]
                    else:
                        lst = [i-5, i-1, i+1, i+5]
                    for x in lst:
                        if self.isValidTargetPosition(i, x):
                            available_move.append((i, x))
            return available_move

    
    def makeMove(self, move, player):
        # print('move: ', move)
        start = move[0]
        end = move[1]
        if self.board[start] == 0 and self.board[end] != 0:
            return False        
        
        # change state of board
        self.board[end] = self.board[start]
        self.board[start] = 0
        
        # Ganh
        lst = list()
        if end % 2 == 0:
            lst = [(end - 6, end + 6), (end - 5, end + 5), (end - 4, end + 4), (end - 1, end + 1)]
        else:
            lst = [(end - 5, end + 5), (end - 1, end + 1)]
        for x in lst:
            if Board.isAdjacentAndValid(x[0], end) and Board.isAdjacentAndValid(x[1], end) :
                if not self.board[x[0]] in [self.board[end], 0] and not self.board[x[1]] in [self.board[end], 0]: #quan co 2 ben khac quan co o giua
                    self.board[x[0]] = self.board[end]
                    self.board[x[1]] = self.board[end]
                    if self.board[end] == PLAYER_MAX:
                        self.nums_max += 2
                        self.nums_min -= 2
                    else:
                        self.nums_max -= 2
                        self.nums_min += 2
        
        ## Vay
        for i in range(SIZE*SIZE):
            if self.board[i] != self.board[end] and self.board[i] != 0:
                lst = list()                
                teammates = 0
                if i%2 == 0:
                    lst = [i-6, i-5, i-4, i-1, i+1, i+4, i+5, i+6]
                else:
                    lst = [i-5, i-1, i+1, i+5]
                movable = list()
                for x in lst:
                    if Board.isAdjacentAndValid(x, i):
                        movable.append(x)
                khi = 0 #khi cua 1 quan co
                team_list = list()
                mark_list = [0]*25
                mark_list[i] = 1
                for x in movable:                   
                    if self.board[x] != 0:
                        if self.board[x] == self.board[i]:
                            teammates += 1
                            team_list.append(x)
                            mark_list[x] = 1                        
                        continue
                    else:                         
                        khi += 1               
                if khi != 0:
                    continue
                if teammates == 0 and khi == 0:
                    self.board[i] = self.board[end]
                    if player == 1:
                        self.nums_max += 1
                        self.nums_min -= 1
                    elif player == -1:
                        self.nums_max -= 1
                        self.nums_min += 1
                else:
                    total_khi = self.calculate_for_teammate(team_list, mark_list)
                    if total_khi == 0:
                        self.board[i] = self.board[end]
                        for t in team_list:
                            self.board[t] = self.board[end]
                        if player == PLAYER_MAX:
                            self.nums_max = self.nums_max + len(team_list) + 1
                            self.nums_min = self.nums_min - len(team_list) - 1
                        elif player == PLAYER_MIN:
                            self.nums_max = self.nums_max - len(team_list) - 1
                            self.nums_min = self.nums_min + len(team_list) + 1        
        return True    

    def calculate_for_teammate(self, team_list ,mark_list):
        for i in team_list:
            if i % 2 == 0:
                lst = [i-6, i-5, i-4, i-1, i+1, i+4, i+5, i+6]
            else:
                lst = [i-5, i-1, i+1, i+5]
            moveable = list()
            khi = 0
            team_list_new = list()
            for x in lst:
                if Board.isAdjacentAndValid(x, i) and mark_list[x] == 0:
                    moveable.append(x)                
            for x in moveable:
                if self.board[x] == 0:
                    khi += 1
                    return khi
                if self.board[x] == self.board[i]:
                    team_list_new.append(x)
            mark_list[i] = 1
        if len(team_list_new) != 0:
            return self.calculate_for_teammate(team_list_new, mark_list)
        return khi  

    @staticmethod
    def isAdjacentAndValid(a, b):
        return True if a >= 0 and a <= 24 and b >= 0 and b <= 24 and a % 5 - b % 5 in [-1, 0, 1] else False 
    
    def isValidTargetPosition(self ,start, end):
        return True if end >= 0 and end <= 24 and start % 5 - end % 5 in [-1, 0, 1] and self.board[end] == 0 else False 

    
    def copyBoard(self):
        new_board = Board()
        new_board.board = self.board.copy()
        new_board.nums_max = self.nums_max
        new_board.nums_min = self.nums_min
        return new_board
            

class PreviousBoard:
    board = Board([[1,1,1,1,1], 
                        [1,0,0,0,1], 
                        [1,0,0,0,-1], 
                        [-1,0,0,0,-1], 
                        [-1,-1,-1,-1,-1]])    

    
def makeMoveForPreviousBoard(state, move, player):
    PreviousBoard.board = Board()
    PreviousBoard.board.createBoard(state)    
    PreviousBoard.board.makeMove(move, player)



def move(board, player):
    ai = AI()
    custom_board = Board()
    custom_board.createBoard(board)
    opponent = opponent_move(custom_board)
    move = ai.minimax_search(custom_board, player, opponent)
    board_print(board)
    if not move:
        return move
    makeMoveForPreviousBoard(board, move, player)
    board_print_from_array(PreviousBoard.board.board)
    # print("Move: ", move)
    move = ((int(move[0]/5), move[0]%5), (int(move[1]/5), move[1]%5))
    return move



def opponent_move(board):
    start = -1
    end = -1
    for i in range(SIZE*SIZE):
        if board.board[i] != PreviousBoard.board.board[i]:
            if PreviousBoard.board.board[i] != 0 and board.board[i] == 0:
                start = i
            if PreviousBoard.board.board[i] == 0 and board.board[i] != 0:
                end = i
    # print('start: {} -> end: {}'.format(vi_tri_dau, vi_tri_sau))
    return (start, end)


class AI:
    def __init__(self):
        self.timeStart = time.time()
        self.timeExceeded = False

    def minimax_search(self, board, player, opponent):
        alpha = -INF
        beta = INF
        depth = 1
        best_move = list()
        moveable_list = board.get_all_available_move(player, opponent)
        if len(moveable_list) == 0:
            return None
        if len(moveable_list) == 1:
            return moveable_list[0]
        

        while not self.timeOut():
            for move in moveable_list:
                new_board = board.copyBoard()
                new_board.makeMove(move, player)
                value = self.min_alpha_beta(depth - 1, alpha, beta, new_board, player, move)
                if value >= alpha:
                    alpha = value
                    best_move.append((move, alpha))
                if self.timeOut():
                    break
            depth += 1
        best_move = list(filter(lambda x: x[1] == alpha, best_move)) 
        best_move = list(map(lambda x: x[0], best_move))
        if len(best_move) == 1:
            return best_move[0]
        else:
            return best_move[random.randint(0, len(best_move) - 1)]



    def max_alpha_beta(self, depth, alpha, beta, board: Board, player, opponent):
        if (depth == 0 or self.timeOut()):
            return board.static_evaluation()
        moveable_list = board.get_all_available_move(player, opponent)   # (start, end)
        if len(moveable_list) == 0:            
            return -INF           
        max_value = -INF
        for move in moveable_list:
            new_board = board.copyBoard()
            new_board.makeMove(move, player)
            # print('Max:\n')
            # board_print_from_array(new_board.board)
            max_value = max(max_value, self.min_alpha_beta(depth - 1, alpha, beta, new_board, AI.changePlayer(player), move))         
            # if value == None:
            #     return (value, value)
            # print('Value: ', value, '\n')           
            if max_value >= beta:
                return max_value 

            alpha = max(alpha, max_value)          
            if self.timeOut():
                break
        return max_value

  
            

    def min_alpha_beta(self, depth, alpha, beta, board: Board, player, opponent):
        if depth == 0 or self.timeOut():            
            return board.static_evaluation()
        moveable_list = board.get_all_available_move(player, opponent)   # (start, end)
        if len(moveable_list) == 0:
            return INF      
        min_value = INF
        for move in moveable_list:
            new_board = board.copyBoard()
            new_board.makeMove(move, player)
            # print('Min: \n')
            min_value = min(min_value, self.max_alpha_beta(depth - 1, alpha, beta, new_board, AI.changePlayer(player), move))
            # if value == None:
            #     return (value, value)
            # board_print_from_array(new_board.board)
            # print('Value: ', value, '\n')            
            
            if min_value <= alpha:
                return min_value  
            
            beta = min(min_value, beta)

            if self.timeOut():
                break  

        return min_value
    def timeOut(self):
        if time.time() - self.timeStart >= TIMELIMIT:
            self.timeExceeded = True
            return True
        return False

    @staticmethod
    def changePlayer(player):
        return PLAYER_MAX if player == -1 else PLAYER_MIN





def board_print_from_array(board):
    for i in [0, 1, 2, 3, 4]:
        print('{}  {}  {}  {}  {}'.format(convert(board[i*5]), convert(board[i*5 + 1]) ,convert(board[i*5 + 2]), convert(board[i*5 + 3]), convert(board[i*5 + 4])))


def convert(x):
    return 'b' if (x == 1) else 'r' if (x == -1) else '.'





def process_after_move(move, board, player):
    custom_board = Board()
    custom_board.createBoard(board)
    start = int(move[0][0]*5 + move[0][1])
    end = int(move[1][0]*5 + move[1][1])
    if custom_board.board[start] == 0 and custom_board.board[end] != 0:
        return None        
    
    # change state of board
    custom_board.board[end] = custom_board.board[start]
    custom_board.board[start] = 0
    
    # Ganh
    lst = list()
    if end % 2 == 0:
        lst = [(end - 6, end + 6), (end - 5, end + 5), (end - 4, end + 4), (end - 1, end + 1)]
    else:
        lst = [(end - 5, end + 5), (end - 1, end + 1)]
    for x in lst:
        if Board.isAdjacentAndValid(x[0], end) and Board.isAdjacentAndValid(x[1], end) :
            if not custom_board.board[x[0]] in [custom_board.board[end], 0] and not custom_board.board[x[1]] in [custom_board.board[end], 0]: #quan co 2 ben khac quan co o giua
                custom_board.board[x[0]] = custom_board.board[end]
                custom_board.board[x[1]] = custom_board.board[end]
                if custom_board.board[end] == PLAYER_MAX:
                    custom_board.nums_max += 2
                    custom_board.nums_min -= 2
                else:
                    custom_board.nums_max -= 2
                    custom_board.nums_min += 2
    
    ## Vay
    for i in range(SIZE*SIZE):
        if custom_board.board[i] != custom_board.board[end] and custom_board.board[i] != 0:
            lst = list()                
            teammates = 0
            if i%2 == 0:
                lst = [i-6, i-5, i-4, i-1, i+1, i+4, i+5, i+6]
            else:
                lst = [i-5, i-1, i+1, i+5]
            movable = list()
            for x in lst:
                if Board.isAdjacentAndValid(x, i):
                    movable.append(x)
            khi = 0 #khi cua 1 quan co
            team_list = list()
            mark_list = [0]*25
            for x in movable:                   
                if custom_board.board[x] != 0:
                    if custom_board.board[x] == custom_board.board[i]:
                        teammates += 1
                        team_list.append(x)
                        mark_list[x] = 1                        
                    continue
                else:                         
                    khi += 1               
            if khi != 0:
                continue
            if teammates == 0 and khi == 0:
                custom_board.board[i] = custom_board.board[end]
                if player == 1:
                    custom_board.nums_max += 1
                    custom_board.nums_min -= 1
                elif player == -1:
                    custom_board.nums_max -= 1
                    custom_board.nums_min += 1
            else:
                total_khi = custom_board.calculate_for_teammate(team_list, mark_list)
                if total_khi == 0:
                    custom_board.board[i] = custom_board.board[end]
                    for t in team_list:
                        custom_board.board[t] = custom_board.board[end]
                    if player == PLAYER_MAX:
                        custom_board.nums_max = custom_board.nums_max + len(team_list) + 1
                        custom_board.nums_min = custom_board.nums_min - len(team_list) - 1
                    elif player == PLAYER_MIN:
                        custom_board.nums_max = custom_board.nums_max - len(team_list) - 1
                        custom_board.nums_min = custom_board.nums_min + len(team_list) + 1        
    
    n_board = [[0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]]
    for i in range(5):
        for j in range(5):
            n_board[i][j] = custom_board.board[i*5+j]

    return n_board



def board_print(board, move=[], num=0):

    print("====== The current board(", num, ")is (after move): ======")
    if move:
        print("move = ", move)
    for i in [4, 3, 2, 1, 0]:
        print(i, ":", end=" ")
        for j in range(5):
            print(convert(board[i][j]), end=" ")
        print()
    print("   ", 0, 1, 2, 3, 4)
    print("")


def play(board):    
    curr_player = 1 # MAX
    state = board    

    board_num = 0
        
    board_print(state)
    
    while True:
        print("It is ", curr_player, "'s turn")

        start = time.time()
        move_value = move(state, curr_player)
        # move = [(4, 2), (3, 2)]
        elapse = time.time() - start

        # print(move)

        if not move_value:
            break

        print("The move is : ", move_value, end=" ")
        print(" (in %.2f ms)" % (elapse*1000), end=" ")
        # if elapse > 3.0:
        #     print(" ** took more than three second!!", end=" ")
        #     break
        print()
        # check_move
        state = process_after_move(move_value, state, curr_player)

        board_num += 1
        board_print(state, num=board_num)

        if curr_player == 1:
            curr_player = -1
        else:
            curr_player = 1

    print("Game Over")
    if curr_player == -1:
        print("The Winner is:", 'PLAYER_MAX - blue')
    else:
        print("The Winner is:", 'PLAYER_MIN - red')

board = [[1,1,1,1,1],
        [1,0,0,0,1],
        [-1,0,0,0,1],
        [-1,0,0,0,-1],
        [-1,-1,-1,-1,-1]]
# play(board)

PreviousBoard.board.createBoard([[1,0,0,0,0],
[1,  1,  0,  -1,  0],
[1,  1,  1,  1,  -1],
[1,  1,  0,  1,  1],
[0,  0,  1,  1,  1]])

board_print_from_array(PreviousBoard.board.board)

print( move([[1,0,-1,0,0],
[1,  1,  0,  0,  0],
[1,  1,  1,  1,  -1],
[1,  1,  0,  1,  1],
[0,  0,  1,  1,  1]], 1))
