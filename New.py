from Tkinter import *
from tkMessageBox import *
import string

class CamelotInterface:
	SQUARESIZE=40
	HEIGHT=14
	WIDTH=8
	def __init__(self,userPieceColor):

		self.userPieceColor=userPieceColor
		self.currentRound='white'

		self.master=Tk()
		self.master.title("Camelot")
		#self.makeDisplay()
		self.whitePieces={}
		self.blackPieces={}

		self.userPieces=self.whitePieces if userPieceColor=='white' else self.blackPieces
		self.AIPieces=self.whitePieces if userPieceColor=='black' else self.blackPieces
		white_castle_list = [(0,3),(0,4)]
        black_castle_list = [(13,3),(13,4)]
        self.user_castles = self.white_castles if userPieceColor == 'white' else self.black_castles
        self.AI_castles = self.white_castles if userPieceColor == 'black' else self.black_castles

        black_list = [
                      (0,0),(0,0),(0,1),(0,2),(0,5),(0,6),(0,7)
                      ,(1,0),(1,1),(1,6),(1,7)
                      ,(2,0),(2,7)
                      ,(11,0),(11,7)
                      ,(12,0),(12,1),(12,6),(12,7)
                      ,(13,0),(13,1),(13,2),(13,5),(13,6),(13,7)
                      ]
        self.blackBlocks = set(black_list)
		#print set(blackList)

        #self.white_castles = set(white_castle_list)
        #self.black_castles = set(black_castle_list)

        self.makeDisplay()
		
	

	def makeDisplay(self):
		total_height=self.HEIGHT*self.SQUARESIZE
		total_width=self.WIDTH*self.SQUARESIZE
		self.c=Canvas(self.master,height=total_height,width=total_width)
		#self.make_camelot_squares(0,8,"LightBlue","squares")
        for y in range(0,self.HEIGHT):
            for x in range(0, self.WIDTH):
                self.color=color
                if y==0 or y==13:
                    if x<=2 or x>=5:
                        self.color="black"
                if y==1 or y==12:
                    if x<=1 or x>=6:
                        self.color="black"
                if y==2 or y==11:
                    if x<=0 or x>=7:
                        self.color="black"
                                
                self.c.create_rectangle(x*self.SQUARESIZE, y*self.SQUARESIZE,\
                 (x+1)*self.SQUARESIZE, (y+1)*self.SQUARESIZE, fill="LightBlue", tag="squares")


	#def make_camelot_square(self,start,stop,color,tag)
		

if __name__ == '__main__':
	Choose_color='white'
	CI=CamelotInterface(Choose_color)
	CI.master.mainloop()