SIZE = 5
PLAYER_MAX = 1
PLAYER_MIN = -1
EMPTY = 0
class Board:
    def __init__(self):
        self.board = list()
        self.nums_max = 0
        self.nums_min = 0
    
    def createBoard(self, state, player):
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


    def makeMove(self, move, player):
        if self.board[move[0]] == 0:
            return False
        if self.board[move[1]] != 0:
            return False
        ## Chuyen trang thai ban co
        self.board[move[1]] = self.board[move[0]]
        self.board[move[0]] = 0
        
        # Ganh
        lst = list()
        if move[1] % 2 == 0:
            lst = [(move[1] - 6, move[1] + 6), (move[1] - 5, move[1] + 5), (move[1] - 4, move[1] + 4), (move[1] - 1, move[1] + 1)]
        else:
            lst = [(move[1] - 5, move[1] + 5), (move[1] - 1, move[1] + 1)]
        for x in lst:
            if Board.isAdjacentAndValid(x[0], move[1]) and Board.isAdjacentAndValid(x[1], move[1]) :
                if not self.board[x[0]] in [self.board[move[1]], 0] and not self.board[x[1]] in [self.board[move[1]], 0]: #quan co 2 ben khac quan co o giua
                    self.board[x[0]] = self.board[move[1]]
                    self.board[x[1]] = self.board[move[1]]
                    if self.board[move[1]] == PLAYER_MAX:
                        self.nums_max += 2
                        self.nums_min -= 2
                    else:
                        self.nums_max -= 2
                        self.nums_min += 2
        
        ## Vay
        for i in range(SIZE*SIZE):
            if self.board[i] != self.board[move[1]] and self.board[i] != 0:
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
                    self.board[i] = self.board[move[1]]
                    if player == 1:
                        self.nums_max += 1
                        self.nums_min -= 1
                    elif player == -1:
                        self.nums_max -= 1
                        self.nums_min += 1
                else:
                    total_khi = self.calculate_for_teammate(team_list, mark_list)
                    if total_khi == 0:
                        self.board[i] = self.board[move[1]]
                        for t in team_list:
                            self.board[t] = self.board[move[1]]
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
        



def board_print(board):
    for i in [4, 3, 2, 1, 0]:
        print(i, ":", end=" ")
        for j in range(5):
            print(board[i][j], end=" ")
        print()
    print("   ", 0, 1, 2, 3, 4)
    print("")

def board_print_from_array(board):
    for i in [0, 1, 2, 3, 4]:
        print('{}  {}  {}  {}  {}'.format(convert(board[i*5]), convert(board[i*5 + 1]) ,convert(board[i*5 + 2]), convert(board[i*5 + 3]), convert(board[i*5 + 4])))


def convert(x):
    return 'b' if (x == 1) else 'r' if (x == -1) else '.'


board = Board()
board.createBoard([[-1,0,-1,1,-1],
                    [0,1,0,1,-1],
                    [-1,0,-1,-1,0],
                    [1,1,-1,-1,1],
                    [1,0,0,0,0]], PLAYER_MAX)
board_print_from_array(board.board)
print('{} / {}\n'.format(board.nums_max, board.nums_min))
print('\n')
board.makeMove([6,11], PLAYER_MAX)
print('\n')
board_print_from_array(board.board)
print('{} / {}'.format(board.nums_max, board.nums_min))