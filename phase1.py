from Tkinter import *
from tkMessageBox import *
import string

class CheckersInterface:
    DEBUG=1
    DEBUG_BIG_THINGS=0
    #The Tuneable Constants
    DELAY=0 #885=1 sec.
    SQUARESIZE=40
    PIECE_DIAMETER=30
    
    def __init__(self, master=None):

        self.piece_offset=(self.SQUARESIZE-self.PIECE_DIAMETER)#calulation saver

        self.master=Tk()
        self.master.title("Camelot")

        self.make_display()

        self.begin_new_game()


    def make_display(self):
        h=self.SQUARESIZE*14 #calculation saver
        w=self.SQUARESIZE*8 #calculation saver
        self.c=Canvas(self.master, height=h, width=w)
        self.message=Label(self.master, text="Choose Color", bd=2, relief=RAISED,font=("", "10", ""))

        self.make_checker_squares(0,7,"bisque")
        self.make_checker_squares(1,8,"green","squares")

        
        history_scroll=Scrollbar(self.master)
        #self.history_display=Listbox(self.master, yscrollcommand=history_scroll.set)
        #history_scroll.config(command=self.history_display.yview)
       # self.history_display.bind("<Double-Button-1>", self.go_to_move)
        
        self.message.grid(row=0, column=0, columnspan=3, pady=5)
        #self.history_display.grid(row=1, column=1, sticky=N+S)
        history_scroll.grid(row=1, column=2, sticky=N+S)
        
        self.c.grid(row=1, column=0)
        

    def begin_new_game(self):
        """This is the function that begins a new game.  It will be run whenever
        a new game is needed.  It clears various variables, creates the pieces
        using make_pieces, binds the pieces and squares, binds the exit, and
        sets self.moving to the player who starts.  It then calls self.MoveLoop.
            This function requires self.message."""
        if self.DELAY:
            self.message.config(text="Creating new game...", fg="purple")
        
        #variable clearing
        self.c.itemconfig("squares", width=1, outline="black")
        self.pieces= {"black":[], "white":[]} #first list is black's pieces, then white's pieces.
        self.piece=None
        self.piece_square=None
        self.square=()

        self.c.delete("pieces")
        self.c.delete("win_text")
        self.history=[]

        #flag setting
        self.got_move=0
        self.got_piece=0

        
        self.make_pieces("black", self.DELAY)
        self.make_pieces("white", self.DELAY)

        print self.pieces
        
        self.c.tag_bind("pieces", "<1>", self.get_piece_click)
        self.c.tag_bind("squares", "<1>", self.get_square_click)

        self.moving= "white" #reversed since setup_move will switch it.
        
        if self.DEBUG_BIG_THINGS:
            print self.pieces

        
        #self.MoveLoop()
            
    def get_piece_click(self, event):
        print "HELLO1"
        """This function is called when a piece is clicked on.  It sets
        self.got_piece, and assigns the id of the piece clicked on to
        self.piece"""

        try:
            self.piece_square, self.piece=self.c.find_overlapping(event.x, event.y, event.x, event.y)
            print "Piece ID:",self.piece, "    Square ID:",self.piece_square
        except ValueError:
            return
        self.got_piece=1
        
        if self.check_piece(): 
            self.c.itemconfig(self.piece_square, outline="blue", width=3)
            

    def check_piece(self):
        """CHECKS THE COLOR OF PIECE"""

        if self.c.itemcget(self.piece, "fill") == self.moving:
            return 1
        showwarning('Yes', 'Invalid Move')
        return 0
        
    def get_square_click(self, event):
        print "Hello2"
        """This function is called when a square is clicked on.  It only acts if self.got_piece has been
        set before.  When it acts, it sets self.got_move, and assigns the id of the square clicked on to
        self.square."""

        if self.got_piece:
            self.square=self.c.find_overlapping(event.x, event.y, event.x, event.y)
            if self.DEBUG:
                print "got square:", self.square
            self.got_move=1



    def make_checker_squares(self, start, stop, color,tags=""):
        for y in range(0,14):
            for x in range(start, stop, 2):
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
                 (x+1)*self.SQUARESIZE, (y+1)*self.SQUARESIZE, fill=self.color, tag="squares")
            if start==0:
                start=1; stop=8
            else:
                if start==1:
                    start=0; stop=7

    def make_pieces(self, color, delay):
        """This function will make, and place in standard starting position, all the pieces for a specified
        color.  The color can be either "black" or "white".  If it is 0, they are placed on the top half of the board, if it is 1, on the bottom.
            The pieces are appended to the list variable corosponding to the color given, and they are given
            the tag "pieces".  The delay argument sets a delay(duh!), the unit
            is about 885 per sec.            
            The variables requiwhite by this function are:
                self.pieces(a dictionary of two lists, one for each side), self.c(a Canvas),
                self.SQUARESIZE, self.piece_offset"""
        #self.pieces= {"black":[], "white":[]} #first list is black's pieces, then white's pieces.

        side=self.pieces[color]
        if color=="white":
            start=2; stop=6
            start2=4; stop2=6
        if color=="black":
            start=3; stop=5
            start2=7; stop2=9
        for y in range(start2, stop2):
            for x in range(start, stop):
              #  for unused in range(delay):
              #      self.master.update()
                side.append(self.c.create_oval(x*self.SQUARESIZE+self.piece_offset,\
                                               y*self.SQUARESIZE+self.piece_offset,\
                                               (x+1)*self.SQUARESIZE-self.piece_offset,\
                                               (y+1)*self.SQUARESIZE-self.piece_offset,\
                                               fill=color, tag="pieces"))

            if start==2 and stop==6:
                start=3; stop=5
            else:
                if start==3 and stop==5:
                    start=2; stop=6

        
    
    def remove_piece(self, event=None):
        print "Hee"
        """This is a function which will remove the piece which is
        clicked on."""
        piece=self.c.find_overlapping(event.x, event.y, event.x, event.y)
        print piece
        if len(piece) == 2 and self.c.type(piece[1]) == "oval":
            piece=piece[1]
            self.c.delete(piece)
            try:
                self.pieces["white"].remove(piece)
            except:
                self.pieces["black"].remove(piece)
        else:
            if self.DEBUG:
                print "Not a piece!"

if __name__=='__main__':        
    CI=CheckersInterface()
    CI.master.mainloop()


