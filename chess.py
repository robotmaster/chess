
import cv2
import numpy as np


class Board:
    def __init__(self,height,width):
        self.height=height
        self.width=width
        self.scale=100
        self.pieces = []
        self.m_available=np.zeros((height,width))
        self.mapping={}
        self.color='w'
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
                background[top_left_y:bottom_right_y, bottom_right_x-10:bottom_right_x,:]=[0,211,255]
                background[top_left_y:top_left_y+10, top_left_x+10:bottom_right_x-10,:]=[0, 211, 255]
                background[bottom_right_y-10:bottom_right_y,top_left_x+10:bottom_right_x-10,:]=[0, 211, 255]
        cv2.imshow(fig, background)

    def addpiece(self,piece):  
        self.pieces.append(piece)
        n_piece=len(np.unique(self.m_available))
        self.mapping[n_piece]=piece
        self.m_available[piece.y: piece.y+piece.height,piece.x: piece.x+piece.width]=n_piece
        piece.number=n_piece
    def Place(self,x, y):
        X = int(x / self.scale)
        Y = int(y / self.scale)
        return (X, Y)


class Piece:
    def __init__(self, height, width, picture,x,y,pt,color,moved):
        self.height=height
        self.width=width
        self.picture=picture
        self.x=x
        self.y=y
        self.pt=pt
        self.color=color
        self.image=cv2.imread(self.picture)
        self.moved=moved
    def draw(self):
        cv2.imshow('img',self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


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





def isValid(piece,board,nextpoint_x,nextpoint_y):
    if piece.x==nextpoint_x and piece.y==nextpoint_y:
        return False
    if board.m_available[nextpoint_y,nextpoint_x]>0:
        if board.mapping[board.m_available[nextpoint_y,nextpoint_x]].color==         piece.color:
            return False
    if piece.pt=='rook':
        if nextpoint_x==piece.x:
            for p in range(piece.y+1,nextpoint_y):
                if board.m_available[p,piece.x]>0:
                    return False
            for p in range(nextpoint_y+1,piece.y):
                if board.m_available[p,piece.x]>0:
                    return False
            return True
        elif nextpoint_y==piece.y:
            for p in range(piece.x+1,nextpoint_x):
                if board.m_available[piece.y,p]>0:
                    return False
            for p in range(nextpoint_x+1,piece.x):
                if board.m_available[piece.y,p]>0:
                    return False
            return True
    if piece.pt=='queen':
        if nextpoint_x==piece.x:
            for p in range(piece.y+1,nextpoint_y):
                if board.m_available[p,piece.x]>0:
                    return False
            for p in range(nextpoint_y+1,piece.y):
                if board.m_available[p,piece.x]>0:
                    return False
            return True
        elif nextpoint_y==piece.y:
            for p in range(piece.x+1,nextpoint_x):
                if board.m_available[piece.y,p]>0:
                    return False
            for p in range(nextpoint_x+1,piece.x):
                if board.m_available[piece.y,p]>0:
                    return False
            return True
        elif abs(piece.x-nextpoint_x)-abs(piece.y-nextpoint_y)==0:
            if nextpoint_x-piece.x==nextpoint_y-piece.y:
                for p in range(piece.x+1,nextpoint_x):
                    if board.m_available[piece.y+(p-piece.x),p]>0:
                        return False
                for p in range(nextpoint_x+1,piece.x):
                    if board.m_available[nextpoint_y+(p-nextpoint_x),p]>0:
                        return False
            if nextpoint_x-piece.x==piece.y-nextpoint_y:
                for p in range(piece.x+1,nextpoint_x):
                    if board.m_available[piece.y+(piece.x-p),p]>0:
                        return False
                for p in range(nextpoint_x+1,piece.x):
                    if board.m_available[nextpoint_y+(nextpoint_x-p),p]>0:
                        return False
            return True
        #dont forget to add capturing
        else:
            return False
    if piece.pt=='king':
        if nextpoint_x==piece.x:
            if abs(piece.y-nextpoint_y)<2:
                return True
        elif nextpoint_y==piece.y:
            if abs(piece.x-nextpoint_x)<2:
                return True
            print(piece.mapping[11].y)
        elif abs(piece.x-nextpoint_x)-abs(piece.y-nextpoint_y)==0:
            if abs(piece.y-nextpoint_y)<2 and abs(piece.x-nextpoint_x)<2:
                return True
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
                        for p in range(nextpoint_x,piece.y):
                            if board.m_available[p,piece.x]>0:
                                return False
                        return True
                if piece.y<6:
                    if piece.y-nextpoint_y<2:
                        for p in range(nextpoint_x,piece.y):
                            if board.m_available[p,piece.x]>0:
                                return False
                        return True
                else:
                    return False
        elif board.m_available[nextpoint_y,nextpoint_x]>0:
            if nextpoint_x-piece.x==nextpoint_y-piece.y:
                if nextpoint_x-piece.x>0:
                    return False
                else:
                    return True
            if nextpoint_x-piece.x==piece.y-nextpoint_y:
                if nextpoint_x-piece.x<0:
                    return False
                else:
                    return True
                    
        #dont foget to add capturing
                
        else:
            return False
    if piece.pt=='b_pawn':
        if piece.x==nextpoint_x:
            if piece.y-nextpoint_y<0:
                if board.m_available[nextpoint_y,nextpoint_x]>0:
                    return False
                if piece.y==1:
                    if piece.y-nextpoint_y<3:
                        for p in range(nextpoint_x,piece.y):
                            if board.m_available[p,piece.x]>0:
                                return False
                        return True
                if piece.y>1:
                    if piece.y-nextpoint_y<2:
                        for p in range(nextpoint_x,piece.y):
                            if board.m_available[p,piece.x]>0:
                                return False
                        return True
        elif board.m_available[nextpoint_y,nextpoint_x]>0:
            if nextpoint_x-piece.x==nextpoint_y-piece.y:
                if nextpoint_x-piece.x<0:
                    return False
                else:
                    return True
            if nextpoint_x-piece.x==piece.y-nextpoint_y:
                if nextpoint_x-piece.x>0:
                    return False
                else:
                    return True
    
    if piece.pt=='bishop':
        if abs(piece.x-nextpoint_x)-abs(piece.y-nextpoint_y)==0:
            if nextpoint_x-piece.x==nextpoint_y-piece.y:
                for p in range(piece.x+1,nextpoint_x):
                    if board.m_available[piece.y+(p-piece.x),p]>0:
                        return False
                for p in range(nextpoint_x+1,piece.x):
                    if board.m_available[nextpoint_y+(p-nextpoint_x),p]>0:
                        return False
            if nextpoint_x-piece.x==piece.y-nextpoint_y:
                for p in range(piece.x+1,nextpoint_x):
                    if board.m_available[piece.y+(piece.x-p),p]>0:
                        return False
                for p in range(nextpoint_x+1,piece.x):
                    if board.m_available[nextpoint_y+(nextpoint_x-p),p]>0:
                        return False
                    
            return True
        #dont forget to add capturing
        else:
            return False
    if piece.pt=='ma':
        if abs(piece.x-nextpoint_x)==1:
            if abs(piece.y-nextpoint_y)==2:
                return True
        elif abs(piece.x-nextpoint_x)==2:
            if abs(piece.y-nextpoint_y)==1:
                return True
        else:
            return False

def Castle(nextpoint_x,nextpoint_y,piece):
    if piece.pt==king:
        if piece.moved=='m':
            return False
        elif board.color=='w':
            if nextpoint_x==2:
                if rook1.moved=='u':
                    if nextpoint_y==7:
                        return True

    else:
        return False


def Capturing(piece,board,nextpoint_x,nextpoint_y):
    if board.m_available[nextpoint_y,nextpoint_x]>0:
        if board.mapping[board.m_available[nextpoint_y,nextpoint_x]].color!=         piece.color:
            board.pieces.remove(board.mapping[board.m_available[nextpoint_y,nextpoint_x]])

def movepiece(board,piece,nextpoint_x,nextpoint_y):
    if isValid(piece,board,nextpoint_x,nextpoint_y):
        Capturing(piece,board,nextpoint_x,nextpoint_y)
        board.m_available[nextpoint_y,nextpoint_x]=board.m_available[piece.y,piece.x]
        board.m_available[piece.y,piece.x]=0
        piece.x=nextpoint_x
        piece.y=nextpoint_y
        return True
    elif Castle(board,piece):
        if nextpoint_x==2:
            if nextpoint_y==7:
                king.x=nextpoint_x
                king.y=nextpoint_y
    else:
        return False

global p_x, p_y
def onmouse(event,x,y,flags,params):

    if event == cv2.EVENT_LBUTTONDOWN:
        global p_x,p_y
        p_x, p_y=board.Place(x, y)
        piece_number = board.m_available[p_y, p_x]
        if piece_number > 0:
            piece = board.mapping[piece_number]

        ##current turn: board.turn

        ##step 1: choose a piece , the color has to match the turn color

            if piece.color==board.turn:
                board.currentpiece=piece

        ##step 2: after choosing a piece, if choose another piece with the same color, change piece


        ##step 3; if not, move if it's a valid move
        if board.currentpiece is not None and movepiece(board,board.currentpiece,p_x,p_y):

            if board.turn == 'w':
                board.turn = 'b'
            else:
                board.turn = 'w'

            if board.currentpiece.moved=='u':
                board.currentpiece.moved='m'
            board.currentpiece = None
        board.draw('chess')


cv2.namedWindow('chess')
cv2.setMouseCallback('chess', onmouse)
while(1):
    board.draw('chess')
    k = cv2.waitKey(0)& 0xFF
    if k == 27:         # esc to exit
        print ('Done')
        cv2.destroyAllWindows()
        break







