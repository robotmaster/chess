
import cv2
import numpy as np
from inputbox import *
## does not work on mac os 10 or later without tkinter/tk/tcl 8.6.5
##change the boardfliiped in castle and pawns to determine if boardflipped, use boardflipped. it will return false when white is at the bottom and returns true when black is at the bottom

class Board:
    def __init__(self,height,width):
        self.height=height
        self.width=width
        self.scale=100
        self.pieces=[]
        self.m_available=np.zeros((height,width))
        self.mapping={}
        self.turn='w'
        self.currentpiece=None
    def draw(self,fig):
        background=np.zeros((self.height*self.scale,self.width*self.scale,3),np.uint8)
        #background[:]=self.color
        for i in range(8):
            for j in range(8):
                top_left_x=j*self.scale
                top_left_y=i*self.scale
                bottom_right_x=(j+1)*self.scale
                bottom_right_y=(i+1)*self.scale
                if (i+j)%2==0:
                    background[top_left_y:bottom_right_y,top_left_x:bottom_right_x,:]=255
                else:
                    background[top_left_y:bottom_right_y,top_left_x:bottom_right_x,:]=0
        for p in self.pieces:
            top_left_x=int((p.x+0.1)*self.scale)
            top_left_y=int((p.y+0.1)*self.scale)
            bottom_right_x=int((p.x+p.width-0.1)*self.scale)
            bottom_right_y=int((p.y+p.height-0.1)*self.scale)
            newimg=cv2.resize(p.image,(bottom_right_x-top_left_x,bottom_right_y-top_left_y))
            background[top_left_y:bottom_right_y,top_left_x:bottom_right_x,:]=newimg
            if p==self.currentpiece:
                background[top_left_y:bottom_right_y,top_left_x:top_left_x+10,:]=[0,211,255]
                background[top_left_y:bottom_right_y,bottom_right_x-10:bottom_right_x,:]=[0,211,255]
                background[top_left_y:top_left_y+10,top_left_x+10:bottom_right_x-10,:]=[0,211,255]
                background[bottom_right_y-10:bottom_right_y,top_left_x+10:bottom_right_x-10,:]=[0,211,255]
        cv2.imshow(fig,background)

    def addpiece(self,piece):
        self.pieces.append(piece)
        n_piece=np.max(self.m_available)
        self.mapping[n_piece+1]=piece
        self.m_available[piece.y: piece.y+piece.height,piece.x: piece.x+piece.width]=n_piece+1
        piece.number=n_piece
    def Place(self,x,y):
        X=int(x / self.scale)
        Y=int(y / self.scale)
        return (X,Y)


class Piece:
    def __init__(self,height,width,picture,x,y,pt,color,moved):
        self.height=height
        self.width=width
        self.picture=picture
        self.x=x
        self.y=y
        self.pt=pt
        self.color=color
        self.image=cv2.imread(self.picture)
        self.moved=moved
        self.enpassant=False
    def draw(self):
        cv2.imshow('img',self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
global boardflipped
boardflipped = False

board=Board(8,8)

b_king=Piece(1,1,'b_king_chess.jpg',4,0,'king','b','u')
board.addpiece(b_king)

queen=Piece(1,1,'queen_chess.jpg',3,7,'queen','w','u')
board.addpiece(queen)

b_queen=Piece(1,1,'b_queen_chess.jpg',3,0,'queen','b','u')
board.addpiece(b_queen)

king=Piece(1,1,'king_chess.jpg',4,7,'king','w','u')
board.addpiece(king)

b_bishop1=Piece(1,1,'b_bishop_chess.jpg',2,0,'bishop','b','u')
board.addpiece(b_bishop1)

b_bishop2=Piece(1,1,'b_bishop_chess.jpg',5,0,'bishop','b','u')
board.addpiece(b_bishop2)

bishop1=Piece(1,1,'bishop_chess.jpg',5,7,'bishop','w','u')
board.addpiece(bishop1)

bishop2=Piece(1,1,'bishop_chess.jpg',2,7,'bishop','w','u')
board.addpiece(bishop2)

ma1=Piece(1,1,'ma_chess.jpg',1,7,'ma','w','u')
board.addpiece(ma1)

ma2=Piece(1,1,'ma_chess.jpg',6,7,'ma','w','u')
board.addpiece(ma2)

rook1=Piece(1,1,'rook_chess.jpg',0,7,'rook','w','u')
board.addpiece(rook1)

rook2=Piece(1,1,'rook_chess.jpg',7,7,'rook','w','u')
board.addpiece(rook2)

b_ma1=Piece(1,1,'b_ma_chess.jpg',1,0,'ma','b','u')
board.addpiece(b_ma1)

b_ma2=Piece(1,1,'b_ma_chess.jpg',6,0,'ma','b','u')
board.addpiece(b_ma2)

b_rook1=Piece(1,1,'b_rook_chess.jpg',0,0,'rook','b','u')
board.addpiece(b_rook1)

b_rook2=Piece(1,1,'b_rook_chess.jpg',7,0,'rook','b','u')
board.addpiece(b_rook2)

b_pawn=[]
for i in range(8):
    b_pawn.append(Piece(1,1,'b_pawn_chess.jpg',i,1,'b_pawn','b','u'))
    board.addpiece(b_pawn[i])

pawn=[]
for i in range(8):
    pawn.append(Piece(1,1,'pawn_chess.jpg',i,6,'pawn','w','u'))
    board.addpiece(pawn[i])
boardshouldbeflipped=checkflipboard()
def FlipBoard(board):
    global boardflipped
    for p in board.pieces:
        x=7-p.x
        y=7-p.y
        p.x=x
        p.y=y
        board.m_available[y,x]=board.m_available[p.y,p.x]
        board.m_available[p.y,p.x]=0
    if boardflipped:
        boardflipped=False
    else:
        boardflipped=True
def IsCheck (board,color):
    if color=='b':
        for p in board.pieces:
            if p.color == 'w':
                if isValid(p,board,b_king.x,b_king.y,False,False):
                    return True

    if color=='w':
        for p in board.pieces:
            if p.color == 'b':
                if isValid(p,board,king.x,king.y,False,False):
                    return True
    return False
def isValid(piece,board,nextpoint_x,nextpoint_y,enpassant=False,needcheck=True):
    if piece.x==nextpoint_x and piece.y==nextpoint_y:
        return False
    if board.m_available[nextpoint_y,nextpoint_x]>0:
        if board.mapping[board.m_available[nextpoint_y,nextpoint_x]].color==piece.color:
            return False
    if piece.pt=='rook':
        if nextpoint_x==piece.x:
            for p in range(piece.y+1,nextpoint_y):
                if board.m_available[p,piece.x]>0:
                    return False
            for p in range(nextpoint_y+1,piece.y):
                if board.m_available[p,piece.x]>0:
                    return False

        elif nextpoint_y==piece.y:
            for p in range(piece.x+1,nextpoint_x):
                if board.m_available[piece.y,p]>0:
                    return False
            for p in range(nextpoint_x+1,piece.x):
                if board.m_available[piece.y,p]>0:
                    return False
        else:
            return False
    if piece.pt=='queen':
        if nextpoint_x==piece.x:
            for p in range(piece.y+1,nextpoint_y):
                if board.m_available[p,piece.x]>0:
                    return False
            for p in range(nextpoint_y+1,piece.y):
                if board.m_available[p,piece.x]>0:
                    return False

        elif nextpoint_y==piece.y:
            for p in range(piece.x+1,nextpoint_x):
                if board.m_available[piece.y,p]>0:
                    return False
            for p in range(nextpoint_x+1,piece.x):
                if board.m_available[piece.y,p]>0:
                    return False

        elif abs(piece.x-nextpoint_x)-abs(piece.y-nextpoint_y)==0:
            if nextpoint_x-piece.x==nextpoint_y-piece.y:
                for p in range(piece.x+1,nextpoint_x):
                    if board.m_available[piece.y+(p-piece.x),p]>0:
                        return False
                for p in range(nextpoint_x+1,piece.x):
                    if board.m_available[nextpoint_y+(p-nextpoint_x),p]>0:
                        return False
            elif nextpoint_x-piece.x==piece.y-nextpoint_y:
                for p in range(piece.x+1,nextpoint_x):
                    if board.m_available[piece.y+(piece.x-p),p]>0:
                        return False
                for p in range(nextpoint_x+1,piece.x):
                    if board.m_available[nextpoint_y+(nextpoint_x-p),p]>0:
                        return False
            else:
                return False
        #dont forget to add capturing
        else:
            return False
    if piece.pt=='king':
        if nextpoint_x==piece.x:
            if abs(piece.y-nextpoint_y)>=2:
                return False
        elif nextpoint_y==piece.y:
            if abs(piece.x-nextpoint_x)>=2:
                return False
        elif abs(piece.x-nextpoint_x)-abs(piece.y-nextpoint_y)==0:
            if abs(piece.y-nextpoint_y)>=2 or abs(piece.x-nextpoint_x)>=2:
                return False
        #dont forget to add capturing
        else:
            return False
    if piece.pt=='pawn':
        if piece.x==nextpoint_x:
            if piece.y-nextpoint_y>0:
                if board.m_available[nextpoint_y,nextpoint_x]>0:
                    return False
                if piece.y==6:
                    if piece.y-nextpoint_y<3:
                        for p in range(piece.y,nextpoint_y):
                            if board.m_available[p,piece.x]>0:
                                return False
                    else:
                        return False
                else:
                    if piece.y-nextpoint_y<2:
                        for p in range(piece.y,nextpoint_y):
                            if board.m_available[p,piece.x]>0:
                                return False
                    else:
                        return False
            else:
                return False
        elif board.m_available[nextpoint_y,nextpoint_x]>0:
            if nextpoint_y-piece.y!=-1 or abs(nextpoint_x-piece.x)!=1:
                return False

        elif board.m_available[nextpoint_y,nextpoint_x]==0:
            if board.m_available[piece.y,nextpoint_x]>0:
                apiece = board.m_available[piece.y,nextpoint_x]
                if board.mapping[apiece].enpassant==False:
                    return False
                elif abs(nextpoint_x-piece.x)>1:
                    return False
            else:
                return False
        #dont forget to add capturing

    if piece.pt=='b_pawn':
        if boardflipped:
            if piece.x == nextpoint_x:
                if piece.y - nextpoint_y > 0:
                    if board.m_available[nextpoint_y, nextpoint_x] > 0:
                        return False
                    if piece.y == 6:
                        if piece.y - nextpoint_y < 3:
                            for p in range(piece.y, nextpoint_y):
                                if board.m_available[p, piece.x] > 0:
                                    return False
                        else:
                            return False
                    else:
                        if piece.y - nextpoint_y < 2:
                            for p in range(piece.y, nextpoint_y):
                                if board.m_available[p, piece.x] > 0:
                                    return False
                        else:
                            return False
                else:
                    return False
            elif board.m_available[nextpoint_y, nextpoint_x] > 0:
                if nextpoint_y - piece.y != -1 or abs(nextpoint_x - piece.x) != 1:
                    return False

            elif board.m_available[nextpoint_y, nextpoint_x] == 0:
                if board.m_available[piece.y, nextpoint_x] > 0:
                    apiece = board.m_available[piece.y, nextpoint_x]
                    if board.mapping[apiece].enpassant == False:
                        return False
                    elif abs(nextpoint_x - piece.x) > 1:
                        return False
                else:
                    return False
        else:
            if piece.x==nextpoint_x:
                if piece.y-nextpoint_y<0:
                    if board.m_available[nextpoint_y,nextpoint_x]>0:
                        return False
                    if piece.y==1:
                        if nextpoint_y-piece.y<3:
                            for p in range(nextpoint_y,piece.y):
                                if board.m_available[p,piece.x]>0:
                                    return False
                        else:
                            return False
                    if piece.y>1:
                        if nextpoint_y-piece.y<2:
                            for p in range(nextpoint_y,piece.y):
                                if board.m_available[p,piece.x]>0:
                                    return False
                        else:
                            return False
                else:
                    return False

            elif board.m_available[nextpoint_y,nextpoint_x]>0:
                if nextpoint_y-piece.y!=1 or abs(nextpoint_x-piece.x)!=1:
                    return False
            elif board.m_available[nextpoint_y,nextpoint_x]==0:
                if board.m_available[piece.y,nextpoint_x]>0:
                    bpiece = board.m_available[piece.y,nextpoint_x]
                    if board.mapping[bpiece].enpassant==False:
                        return False
                    elif abs(nextpoint_x-piece.x)>1:
                        return False
                else:
                    return False

    if piece.pt=='bishop':
        if abs(piece.x-nextpoint_x)-abs(piece.y-nextpoint_y)==0:
            if nextpoint_x-piece.x==nextpoint_y-piece.y:
                for p in range(piece.x+1,nextpoint_x):
                    if board.m_available[piece.y+(p-piece.x),p]>0:
                        return False
                for p in range(nextpoint_x+1,piece.x):
                    if board.m_available[nextpoint_y+(p-nextpoint_x),p]>0:
                        return False
            elif nextpoint_x-piece.x==piece.y-nextpoint_y:
                for p in range(piece.x+1,nextpoint_x):
                    if board.m_available[piece.y+(piece.x-p),p]>0:
                        return False
                for p in range(nextpoint_x+1,piece.x):
                    if board.m_available[nextpoint_y+(nextpoint_x-p),p]>0:
                        return False

            else:
                return False
        #dont forget to add capturing
        else:
            return False
    if piece.pt=='ma':
        if abs(piece.x-nextpoint_x)==1:
            if abs(piece.y-nextpoint_y)!=2:
                return False
        elif abs(piece.x-nextpoint_x)==2:
            if abs(piece.y-nextpoint_y)!=1:
                return False
        else:
            return False
    ##hypothetically move
    if needcheck:
        if board.m_available[nextpoint_y, nextpoint_x]>0:
            nextpiece=board.mapping[board.m_available[nextpoint_y, nextpoint_x]]
        cur_x=piece.x
        cur_y=piece.y
        capturedPiece = Capturing(piece,board,nextpoint_x,nextpoint_y,enpassant)
        board.m_available[nextpoint_y, nextpoint_x] = board.m_available[piece.y, piece.x]
        board.m_available[piece.y, piece.x]=0
        piece.x = nextpoint_x
        piece.y = nextpoint_y
        checkResult= IsCheck(board, piece.color)
        ##do some clean up before returning
        board.m_available[cur_y, cur_x] = board.m_available[nextpoint_y, nextpoint_x]
        if capturedPiece is not None:
            board.pieces.append(board.mapping[capturedPiece])
            board.m_available[nextpoint_y, nextpoint_x]=capturedPiece
        else:
            board.m_available[nextpoint_y, nextpoint_x]=0

        piece.x=cur_x
        piece.y=cur_y
        return not checkResult
    else:
        return True
def checkmate(board,color):


def isValidCastle(board,nextpoint_x,piece):
    if piece.pt!='king':
        return False
    if piece.moved=='m':
        return False
    if board.turn=='w':
        if nextpoint_x==2:
            #check if rook has already moved
            if rook1.moved=='m':
                return False
            #check if there's any piece between the king and the rook
            for p in range(2,4):
                if board.m_available[7,p]>0:
                    return False
            #check if there's a check on any position between king and it's castled postion
            for x_position in range(2,5):
                for p in board.pieces:
                    if p.color=='b':
                        if isValid(p,board,x_position,7):
                            return False
        if nextpoint_x==6:
            if rook2.moved=='m':
                return False
            for p in range(5,7):
                if board.m_available[7,p]>0:
                    return False
            for x_position in range(4,7):
                for p in board.pieces:
                    if p.color=='b':
                        if isValid(p,board,x_position,7):
                            return False
    if board.turn=='b':
        if nextpoint_x==2:
            if b_rook1.moved=='m':
                return False
            for p in range(2,4):
                if board.m_available[0,p]>0:
                    return False
            for x_position in (2,4):
                for p in board.pieces:
                    if p.color=='w':
                        if isValid(p,board,x_position,0):
                            return False
        if nextpoint_x==6:
            if b_rook2.moved=='m':
                return False
            for p in range(5,6):
                if board.m_available[0,p]>0:
                    return False
            for x_position in (4,6):
                for p in board.pieces:
                    if p.color=='w':
                        if isValid(p,board,x_position,0):
                            return False
    if abs(nextpoint_x-piece.x)==2:
        return True
    else:
        return False

global isCastleMove

def Capturing(piece,board,nextpoint_x,nextpoint_y,enpassantmove):
    if enpassantmove==False:
        if board.m_available[nextpoint_y,nextpoint_x]>0:
            if board.mapping[board.m_available[nextpoint_y,nextpoint_x]].color!=piece.color:
                nextpiece=board.m_available[nextpoint_y,nextpoint_x]
                board.pieces.remove(board.mapping[nextpiece])
                return nextpiece
        return None
    else:
        if board.m_available[piece.y,nextpoint_x]>0:
            if board.mapping[board.m_available[piece.y,nextpoint_x]].color!=piece.color:
                nextpiece=board.m_available[piece.y,nextpoint_x]
                board.pieces.remove(board.mapping[nextpiece])
                board.m_available[piece.y,nextpoint_x]=0 ##remove the taken pawn


def movepiece(board,piece,nextpoint_x,nextpoint_y,):
    global isCastleMove
    isCastleMove=False
    if isValidCastle(board,nextpoint_x,piece):
        isCastleMove=True
    if isValid(piece,board,nextpoint_x,nextpoint_y,) or isValidCastle(board,nextpoint_x,piece):
        enpassantmove=False
        if piece.pt=='pawn':
            if piece.y-nextpoint_y==2:
                piece.enpassant=True
        if piece.pt=='b_pawn':
            if nextpoint_y-piece.y==2:
                piece.enpassant=True
        if piece.pt in ['pawn','b_pawn'] and board.m_available[nextpoint_y,nextpoint_x]==0:
            enpassantmove=True
        Capturing(piece,board,nextpoint_x,nextpoint_y,enpassantmove)
        board.m_available[nextpoint_y,nextpoint_x]=board.m_available[piece.y,piece.x]
        board.m_available[piece.y,piece.x]=0
        piece.x=nextpoint_x
        piece.y=nextpoint_y
        piece.moved='m'
        if isCastleMove: #if castle move,need to move rook
            if piece.x==2:
                if piece.color=='w':
                    board.m_available[7,3]=board.m_available[rook1.y,rook1.x]
                    board.m_available[rook1.y,rook1.x]=0
                    rook1.x=3
                    rook1.y=7
                    rook1.moved='m'
            if piece.x==6:
                if piece.color=='w':
                    board.m_available[7,5]=board.m_available[rook2.y,rook2.x]
                    board.m_available[rook2.y,rook2.x]=0
                    rook2.x=5
                    rook2.y=7
                    rook2.moved='m'
            if piece.x==2:
                if piece.color=='b':
                    board.m_available[0,3]=board.m_available[b_rook1.y,b_rook1.x]
                    board.m_available[b_rook1.y,b_rook1.x]=0
                    b_rook1.x=3
                    b_rook1.y=0
                    b_rook1.moved='m'
            if piece.x==6:
                if piece.color=='b':
                    board.m_available[0,5]=board.m_available[b_rook2.y,b_rook2.x]
                    board.m_available[b_rook2.y,b_rook2.x]=0
                    b_rook2.x=5
                    b_rook2.y=0
                    b_rook2.moved='m'

        ##promotion
        if piece.pt=='pawn' and piece.y==0: ##white pawn reaches to the promotion position
            newpiece=getInput()
            if newpiece==None:
                cv2.destroyAllWindows()
                quit()
            board.pieces.remove(board.mapping[board.m_available[piece.y, piece.x]])##remove promoted pawn
            if newpiece=='queen':
                board.addpiece(Piece(1, 1, 'queen_chess.jpg',piece.x,piece.y,'queen','w','m'))
            if newpiece=='rook':
                board.addpiece(Piece(1, 1, 'rook_chess.jpg',piece.x,piece.y,'rook','w','m'))
            if newpiece=='knight':
                board.addpiece(Piece(1, 1, 'ma_chess.jpg',piece.x,piece.y,'ma','w','m'))
            if newpiece=='bishop':
                board.addpiece(Piece(1, 1,'bishop_chess.jpg',piece.x, piece.y,'bishop','w','m'))
        if piece.pt=='b_pawn' and piece.y==7: ##black pawn reaches to the promotion position
            newpiece=getInput()
            board.pieces.remove(board.mapping[board.m_available[piece.y, piece.x]])##remove promoted pawn
            if newpiece=='queen':
                board.addpiece(Piece(1, 1, 'b_queen_chess.jpg',piece.x,piece.y,'queen','b','m'))
            if newpiece=='rook':
                board.addpiece(Piece(1, 1, 'b_rook_chess.jpg',piece.x,piece.y,'rook','b','m'))
            if newpiece=='knight':
                board.addpiece(Piece(1, 1, 'b_ma_chess.jpg',piece.x,piece.y,'ma','b','m'))
            if newpiece=='bishop':
                board.addpiece(Piece(1, 1,'b_bishop_chess.jpg',piece.x, piece.y,'bishop','b','m'))



        return True

    else:
        return False

global p_x,p_y
def onmouse(event,x,y,flags,params):
    global isCastleMove
    if event==cv2.EVENT_LBUTTONDOWN:
        global p_x,p_y
        p_x,p_y=board.Place(x,y)
        piece_number=board.m_available[p_y,p_x]
        if piece_number > 0:
            piece=board.mapping[piece_number]

        ##current turn: board.turn

        ##step 1: choose a piece ,the color has to match the turn color

            if piece.color==board.turn:
                board.currentpiece=piece

        ##step 2: after choosing a piece,if choose another piece with the same color,change piece


        ##step 3; if not,move if it's a valid move
        if board.currentpiece is not None and movepiece(board,board.currentpiece,p_x,p_y):
            if boardshouldbeflipped=='yes':
                FlipBoard(board)
            if board.turn=='w':
                for i in range(8):
                    b_pawn[i].enpassant=False
                board.turn='b'
            else:
                for i in range(8):
                    pawn[i].enpassant=False
                board.turn='w'

            board.currentpiece=None
        board.draw('chess')


cv2.namedWindow('chess')
cv2.setMouseCallback('chess',onmouse)
while(1):
    board.draw('chess')
    k=cv2.waitKey(0)& 0xFF
    if k==27:         # esc to exit
        print ('Done')
        cv2.destroyAllWindows()
        break