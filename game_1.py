#Implementation of Two Player Tic-Tac-Toe game in Python.

''' We will make the board using dictionary 
    in which keys will be the location(i.e : top-left,mid-right,etc.)
    and initialliy it's values will be empty space and then after every move 
    we will change the value according to player's choice of move. '''
import random
import time
fc = 0
theBoard = {'7': ' ' , '8': ' ' , '9': ' ' ,
            '4': ' ' , '5': ' ' , '6': ' ' ,
            '1': ' ' , '2': ' ' , '3': ' ' }

board_keys = []

for key in theBoard:
    board_keys.append(key)

''' We will have to print the updated board after every move in the game and 
    thus we will make a function in which we'll define the printBoard function
    so that we can easily print the board everytime by calling this function. '''

def printBoard(board):
    print(board['7'] + '|' + board['8'] + '|' + board['9'])
    print('-+-+-')
    print(board['4'] + '|' + board['5'] + '|' + board['6'])
    print('-+-+-')
    print(board['1'] + '|' + board['2'] + '|' + board['3'])

def returnHumanTurn():
    r = random.randint(0,1)
    if r == 0:
        print("You are X")
        return 'X'
    print("You are O")
    return 'O'

def easyLevel(board, humanTurn):
    while True:
        r =  str(random.randint(1,9))
        if board[r]==' ':
            break
    print(f"The computer chose {r}")
    return r

#winning combinations
def winning(board, player):

    if(
    (board['1'] == player and board['2'] == player and board['3'] == player) or
    (board['4'] == player and board['5'] == player and board['6'] == player) or
    (board['7'] == player and board['8'] == player and board['9'] == player) or
    (board['1'] == player and board['4'] == player and board['7'] == player) or
    (board['2'] == player and board['5'] == player and board['8'] == player) or
    (board['3'] == player and board['6'] == player and board['9'] == player) or
    (board['1'] == player and board['5'] == player and board['9'] == player) or
    (board['3'] == player and board['5'] == player and board['7'] == player)):
        return True
    return False

def hardLevel(board, huPlayer):
    class Data:
        def __init__(self, score=0, index=0):
            self.score = score 
            self.index=index
    def emptyIndices(board):
        def check(x):
            if x!='X' and x!='O':
                return 1
            return 0
        return list(filter(check,board))
    def returnDic(board):
        dic = {}
        for i in range(len(board)):
            if board[i] ==i:
                dic[str(i+1)] =' '
            else:
                dic[str(i+1)] = board[i]
        return dic
    def returnList(board):
        arr=[0]*9
        for key in board:
            if  board[key]==' ':
                arr[int(key)-1] = int(key)-1
            else:
                arr[int(key)-1] = board[key]
        return arr

    def minimax(newBoard, player):
        global fc
        fc+=1
        availSpots = emptyIndices(newBoard)
        if winning(returnDic(newBoard), huPlayer):
            return Data(-10)
        elif winning(returnDic(newBoard), aiPlayer):
            return Data(10)
        elif len(availSpots) == 0:
            return Data(0)

        moves = []
        for i in range(len(availSpots)):
            move = Data()
            move.index = newBoard[availSpots[i]]
            newBoard[availSpots[i]] = player
            if player == aiPlayer:
                result = minimax(newBoard, huPlayer)
            else:
                result = minimax(newBoard, aiPlayer)
            move.score = result.score   

            newBoard[availSpots[i]] = move.index
            moves.append(move)

        bestMove = 0
        if player == aiPlayer:
            bestScore = -10000
            for i in range(len(moves)):
                if moves[i].score > bestScore:
                    bestScore = moves[i].score
                    bestMove = i
        else:
            bestScore = 10000 
            for i in range(len(moves)):
                if moves[i].score < bestScore:
                    bestScore = moves[i].score
                    bestMove = i
        return moves[bestMove]

    if huPlayer == 'X':
        aiPlayer ='O'
    else:
        aiPlayer = 'X'
    
    return str(minimax(returnList(board), aiPlayer).index+1)



def selectLevel():
    lvl = input("Choose the level 1 or 2\n")
    if lvl =='1':
        return easyLevel
    return hardLevel

# Now we'll write the main function which has all the gameplay functionality.
def game():
    count = 0
    level = selectLevel()
    humanTurn = returnHumanTurn()

    turn = 'X'

    while count < 9:
        printBoard(theBoard)
        print("It's your turn," + turn + ".Move to which place?")
        move = 'O'

        if humanTurn == turn:
            move = input()    
        else:
            time.sleep(1)
            move = level(theBoard.copy(), humanTurn)
        if theBoard[move] == ' ':
            theBoard[move] = turn
            count += 1
        else:
            print("That place is already filled.\nMove to which place?")
            continue

        # Now we will check if player X or O has won,for every move after 5 moves. 
        if count >= 5 and winning(theBoard, turn) == True:
            printBoard(theBoard)
            print("\nGame Over.\n")                
            print(" **** " +turn + " won. ****")                
            break
            

        # If neither X nor O wins and the board is full, we'll declare the result as 'tie'.
        if count == 9:
            printBoard(theBoard)
            print("\nGame Over.\n")                
            print("It's a Tie!!")

        # Now we have to change the player after every move.
        if turn =='X':
            turn = 'O'
        else:
            turn = 'X'        
    
    # Now we will ask if player wants to restart the game or not.
    restart = input("Do want to play Again?(y/n)")
    if restart == "y" or restart == "Y":  
        for key in board_keys:
            theBoard[key] = " "

        game()

if __name__ == "__main__":
    game()
