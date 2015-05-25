#AUTHOR NAME: VISHAL MIRZA


from Tkinter import *
from tkMessageBox import *

#Function checkValidity checks if str is a valid position for the Piece. GG is the list of other pieces position. 

def checkValidity(str,GG):
    if(str[0]<0 or str[0]>7 or str[1]<0 or str[1]>13 or str==(0,0) or str==(1,0) or str==(2,0) or str==(0,1)
     or str==(1,1) or str==(0,2) or str==(5,0) or str==(6,0) or str==(7,0) or str==(6,1) or str==(7,1)
      or str==(7,2) or str==(0,11) or str==(0,12) or str==(1,12) or str==(0,13) or str==(1,13) or str==(2,13)
       or str==(7,11) or str==(6,12) or str==(7,12) or str==(5,13) or str==(6,13) or str==(7,13) ):
        return -1
    if str in GG:
        return 0
    return 1

#This checks if what possible moves Piece 'str' can take. XX is the list of its own color piece and YY is
# the list of opponent piece.
def possibleMoves(str,XX,YY):
    t=[]
    for i in range(-1,2):
        for j in range(-1,2):
            k=(str[0]+j,str[1]+i)
            if(checkValidity(k,XX)==1 and checkValidity(k,YY)==1 ):
                t.append(k)
            else:
                ii=0
                jj=0
                if(j==-1):
                    jj=-2
                if(j==1):
                    jj=2
                if(i==-1):
                    ii=-2
                if(i==1):
                    ii=2
                k=(str[0]+jj,str[1]+ii)
                if(checkValidity(k,XX)==1 and checkValidity(k,YY)==1):
                    t.append(k)
    return t

#This checks if Piece str can capture pieces from opponent pieces GG.
def CapturingMove(str,GG,HH):
    t=[]
    for i in range(-1,2):
        for j in range(-1,2):
            k=(str[0]+j,str[1]+i)
            if(not (checkValidity(k,GG)==1)):
                ii=0
                jj=0
                if(j==-1):
                    jj=-2
                if(j==1):
                    jj=2
                if(i==-1):
                    ii=-2
                if(i==1):
                    ii=2
                l=(str[0]+jj,str[1]+ii)
                if(checkValidity(l,GG)==1 and checkValidity(l,HH)):
                    t.append(l)
                    t.append(k)
                    return t

#This checks whether a player has moved to opponent castle. GG is the list of his own moves. 
def checkTerminalState(GG,color):
        win1=(3,13)
        win2=(4,13)
        win3=(3,0)
        win4=(4,0)
        if(color=='white'):
                if(win1 in GG or win2 in GG):
                        return 1
        if(color=='black'):
                if(win3 in GG or win4 in GG):
                        return 1

#This functions defines the evaluation function and calculates the value corresponding to the position
#of own pieces and opponet pieces. The function is developed based on following parameters.
#Player1 utility value depends on how near it is from the opponent castle, how far are the opponent
#pieces from his castle, number of pieces left for player1 and player2.
#F(x) directly proportional to 'near'           :distance from opponent castle
#F(x) inversly proportional to 'far'            :distance of opponent from her castle
#F(x) directly proportional to 'len(MyPiece)'   :Number of own pieces
#F(x) inversly proportional to 'len(OppPiece)'  :Number of Opponent pieces.
#constants are multiplied to keep the utility values small compared to INF, maximum utility value
def UtilityValue(MyPiece,OppPiece,Mycolor,OppColor):
    
        #near:Opponent Castle distance from My Pieces. 
        #far: My Castle distance from Oppnent Pieces.
        #Default is 1
        near=1
        far=1
        #MAXIMIZE VALUE OF white & MINIMIZE VALUE OF black
        if(Mycolor=='white' and OppColor=='black'):
            for i in MyPiece:
                near+= ((3.5 - float(i[0]))**2  +(13-float(i[1]))**2 )**0.5 
            val1=len(MyPiece)*(INF/(near*15))    #Nearest piece will have maximum value
            
            for j in OppPiece:
                far+=((3.5-float(j[0]))**2 + (float(j[1]))**2 )**0.5
            val2=INF/(far*100*len(OppPiece))

            return val1+val2

        #MAXIMIZE VALUE OF black & MINIMIZE VALUE OF white
        if(Mycolor=='black' and OppColor=='white'):
            for i in MyPiece:
                near+= ((3.5 - float(i[0]))**2  +(float(i[1]))**2 )**0.5 
            val1=len(MyPiece)*(INF/(near*15))    #Nearest piece will have maximum value
            
            for j in OppPiece:
                far+=((3.5-float(j[0]))**2 + (13-float(j[1]))**2 )**0.5
            val2=INF/(far*100*len(OppPiece))

            return val1+val2

        if(Mycolor=='black'):
            for i in MyPiece:
                near+= ((3.5 - float(i[0]))**2  +(float(i[1]))**2 )**0.5 
            val=INF/near    #Nearest piece will have maximum value
            return int(val)


#MaxValue is Max function of Alpha-beta algorithm

def MaxValue(XX,YY,count,ALPHA,BETA,color,ccolor):
    global NodeGen     #No of nodes generated
    global PrunInMax   #No of prunning which takes place in Max function
    D=[]               #D is the list which will have D[0]:utility value, D[1]:list of pieces position,
                       #D[2]:1 if capturing occured, 0 if not.

    if(checkTerminalState(XX,color)):       #Check whether max player has reached terminal state(castle captured).
        D.append(INF)
        D.append(XX)
        D.append(0)
        return D

    if(checkTerminalState(YY,ccolor)):      #Check whether min player has reached terminal state.
        D.append(-INF)
        D.append(YY)
        D.append(0)
        return D

    if(count==0):                           #Whether Tree Depth=0 is reached 
        h=UtilityValue(XX,YY,color,ccolor)
        D.append(h)
        D.append(XX)
        D.append(0)
        return D    
    v=-INF
    PieceP=()
    modList=XX[:]                           #Initial piece position
    for i in range(len(XX)):
        CapMove=CapturingMove(XX[i],YY,XX)     #First check whether capturing is possible or not
        if(CapMove):
            NodeGen+=1
            TT=XX[:]
            modList=XX[:]
            TT[i]=CapMove[0]
            D.append(INF)
            D.append(TT[:])
            D.append(CapMove[1])   #Captured
            return D
        PML=possibleMoves(XX[i],XX,YY)      #Possible action or moves that could be taken each piece
        #print PML
        for j in range(len(PML)):
            NodeGen=NodeGen+1               #Each possible move generates one node
            TT=XX[:]
            TT[i]=PML[j]

            k=MinValue(TT,YY,count-1,ALPHA,BETA,ccolor,color)[0]          
            if(k>v):
                v=k
                modList=TT[:]
            if(v>=BETA):
                PrunInMax+=1
                #print "Prunning"
                D.append(v)
                D.append(TT[:])    
                D.append(0)         #Not Captured
                return D
            if(ALPHA<v):
                ALPHA=v

    D.append(v)
    if modList==XX:
        D.append(TT)               #New list is appened which will be returned
    else:
        D.append(modList)
    D.append(0)         #Not Captured

    return D


def MinValue(XX,YY,count,ALPHA,BETA,ccolor,color):
    global NodeGen
    global PrunInMin
    D=[]

    if(checkTerminalState(YY,ccolor)):        #Check whether min player has reached terminal state(castle captured).
        D.append(-INF)
        D.append(YY)
        return D
    
    if(checkTerminalState(XX,color)):         #Check whether max player has reached terminal state.
        D.append(INF)
        D.append(XX)
        return D

    if(count==0):                              #Wether Tree Depth=0 is reached 
        h=UtilityValue(YY,XX,ccolor,color)
        D.append(h)
        D.append(YY)
        return D
    v=INF
    PieceP=()
    modList=YY[:]                              #Initial piece position

    for i in range(len(YY)):
        CapMove=CapturingMove(YY[i],XX,YY)        #First check whether capturing is possible or not
        
        if(CapMove):
            NodeGen+=1                          #Each possible move generates one node
            TT=YY[:]
            TT[i]=CapMove[0]
            D.append(-INF)
            D.append(TT[:])
            return D
        PML=possibleMoves(YY[i],YY,XX)
         
        for j in range(len(PML)):
            NodeGen=NodeGen+1                  #Incremement NodeGen For each Node generated
            TT=YY[:]
            
            TT[i]=PML[j]
            k=MaxValue(XX,TT,count-1,ALPHA,BETA,color,ccolor)[0]
            if(k<v):
                v=k             
                modList=TT[:]
            if(v<=ALPHA):
                #print "Prunning"
                PrunInMin+=1
                D.append(v)
                D.append(TT[:])
                return D
            if(BETA>v):
                BETA=v

    D.append(v)
    if modList==XX:
        D.append(TT)                       #New list is appened which will be returned
    else:
        D.append(modList)
    return D    



#Function calculates the best move that should be taken against human player. 
def ComputerTurn():
    global x
    global y
    global NodeGen
    global PrunInMin
    global PrunInMax
    global AIwin,AIcolor,Mycolor,MYwin

    #Checks whether anyone has won the game
    if(AIwin==1 or len(y)==0):
        msg=AIcolor+" WON"
        showwarning('Yes', msg)
        print AIcolor," won"
    if(MYwin==1 or len(x)==0):
        msg=MYcolor+" WON"
        showwarning('Yes', msg)
        print MYcolor," won"

    print "\nWait Computer Processing....."
    
    #Iteratively search until maximum depth of tree for an optimum move (the move with highest utility value)
    for i in range(MaxDepth+1):
        NodeGen=1
        T=MaxValue(x,y,i,-INF,INF,AIcolor,MYcolor)
        if(T[0]==INF or T[0]==-INF):
            break
    print "\nDepth Searched:",i
    print "Total Nodes Generated:",NodeGen
    print "Number of Prunning in Max: ",PrunInMax
    print "Number of Prunning in Min: ",PrunInMin

    #print 'INITIAL-> ',AIcolor,':',x
    
    if(len(x)==len(T[1])):
        for i in range(len(x)):
            if x[i]!=T[1][i]:
                SqID_plus_pieceId= cv.find_overlapping(x[i][0]*SqSize+SqSize/2,x[i][1]*SqSize+SqSize/2,x[i][0]*SqSize+SqSize/2,x[i][1]*SqSize+SqSize/2) 
                cv.delete(SqID_plus_pieceId[1])
                make_pieces(T[1][i],piece_offset,AIcolor)
                break



    x=T[1]                                         #New State for Computer Pieces
    CapPiece=T[2]                                  #Captured Piece by Computer, NULL if no capture
    
    #print '\nFINAL  -> ',AIcolor,':',x

    if(CapPiece):
        print '-------------------------',MYcolor, "Piece:",CapPiece," Captured------------------------"
        y.remove(CapPiece)
        SqID_plus_pieceId= cv.find_overlapping(CapPiece[0]*SqSize+SqSize/2,CapPiece[1]*SqSize+SqSize/2,CapPiece[0]*SqSize+SqSize/2,CapPiece[1]*SqSize+SqSize/2) 
        cv.delete(SqID_plus_pieceId[1])
    
    if(AIwin==1 or len(y)==0):
        msg=AIcolor+" WON"
        showwarning('Yes', msg)
        print AIcolor," won"
        
    if(checkTerminalState(x,AIcolor)):
        AIwin=1
        msg=AIcolor+" WON"
        showwarning('Yes', msg)
        print AIcolor," won"


#Function called when Human clicks on a piece
def HumanTurn1(event):
    global Flag2
    global PI,SqID,PieceID
    global x
    global y,AIcolor,Mycolor

    #Checks whether any other piece was previously clicked or not
    if Flag2:
        cv.itemconfig(SqID, outline="black", width=1)
    PI=(event.x/SqSize,event.y/SqSize)#input()#tuple(map(int,raw_input().split(',')))
    SqID,PieceID= cv.find_overlapping(event.x,event.y,event.x,event.y)
    #CHECK PF for Possible moves

    #CHECK WHETHER HUMAN HAS TAKEN VALID MOVE
    if PI in y:
        print PI
        cv.itemconfig(SqID, outline="blue", width=3)
        Flag2=1
        
    else:
        print "Wrong Entry"


#Called after human has clicked on a piece and then click on the square to be moved.
def HumanTurn2(event):
    global Flag2,SqID,PieceID,MYwin,AIwin

    #Checks whether anyone has won the game
    if(AIwin==1 or len(y)==0):
        msg=AIcolor+" WON"
        showwarning('Yes', msg)
        print AIcolor," won"
    if(MYwin==1 or len(x)==0):
        msg=MYcolor+" WON"
        showwarning('Yes', msg)
        print MYcolor," won"

    #Checks whether a piece to be moved was previously clicked or not    
    if Flag2:
        inndex=y.index(PI)
        PML=possibleMoves(PI,y,x)

        #print "Select Destination: X',Y' and Press Enter"

        PF=(event.x/SqSize,event.y/SqSize)
        #print "Capturing Move Need to be taken: ",CapMove

        #HERE WE CHECK IF HUMAN IS PERFORMING CAPTURING MOVE IF IT IS POSSIBLE
        for i in range(len(y)):
            CapMove=CapturingMove(y[i],x,y)     #First check whether capturing is possible or not
            
            if(CapMove):
                break

        if CapMove and PF in PML:
            CapX=0
            CapY=0
            if abs(PF[0]-PI[0])==2 and abs(PF[1]-PI[1])==2:
                CapX=(PI[0]+PF[0])/2
                CapY=(PI[1]+PF[1])/2
            if abs(PF[0]-PI[0])==2 and abs(PF[1]-PI[1])==0:
                CapX=(PI[0]+PF[0])/2
                CapY=PF[1]
            if abs(PF[0]-PI[0])==0 and abs(PF[1]-PI[1])==2:
                CapX=PF[0]
                CapY=(PI[1]+PF[1])/2

            #print 'CAPX:',CapX
            #print 'CAPY:',CapY

            if(CapX or CapY):
                temp=(CapX,CapY)
                if temp in x:
                    print '-------------------------',AIcolor, "Piece:",temp," Captured------------------------"
                    x.remove(temp)
                    SqID_plus_pieceId= cv.find_overlapping(CapX*SqSize+SqSize/2,CapY*SqSize+SqSize/2,CapX*SqSize+SqSize/2,CapY*SqSize+SqSize/2)      
                    cv.delete(SqID_plus_pieceId[1])
                    cv.delete(PieceID)

                    y[inndex]=PF
                    make_pieces(PF,piece_offset,MYcolor)
                    if(checkTerminalState(y,MYcolor)):
                        MYwin=1
                    ComputerTurn()
                    #Flag=2
                    return
                    
                    
            print "Capturing Move Need to be taken: "
          

        #No capturing done by human, so check for a valid plain move
        if not CapMove and PF in PML:
            cv.delete(PieceID)
            y[inndex]=PF
            make_pieces(PF,piece_offset,MYcolor)
            if(checkTerminalState(y,MYcolor)):
                MYwin=1
            ComputerTurn()
            
        else:
            print "You cannot move their"
            print 'Enter Again'

    if(len(x)==0):
        return 1



    




def make_squares(cv,start, stop, color,SqSize):
    for j in range(0,14):
        for i in range(start, stop, 1):
            cv.create_rectangle(i*SqSize, j*SqSize,(i+1)*SqSize, (j+1)*SqSize, fill=color,tag="Square")
            if j==0 or j==13:
                if i<=2 or i>=5:
                    cv.create_rectangle(i*SqSize, j*SqSize,(i+1)*SqSize, (j+1)*SqSize, fill="black",tag="Square")
            if j==1 or j==12:
                if i<=1 or i>=6:
                    cv.create_rectangle(i*SqSize, j*SqSize,(i+1)*SqSize, (j+1)*SqSize, fill="black",tag="Square")
            if j==2 or j==11:
                if i<=0 or i>=7:
                    cv.create_rectangle(i*SqSize, j*SqSize,(i+1)*SqSize, (j+1)*SqSize, fill="black",tag="Square")


def make_pieces(XX,piece_offset,color,):
    i=XX[0]
    j=XX[1]
    t=cv.create_oval(i*SqSize+piece_offset,j*SqSize+piece_offset,(i+1)*SqSize-piece_offset,\
        (j+1)*SqSize-piece_offset,fill=color,tag="Piece")
    #print "With tag ID:",cv.find_withtag("(1, 1)")
    return t
                            

def PieceClicked(event):
    #for i in AIpieceID:
        #cv.coords(i, 200)
        #print "C: ",cv.itemconfig(i, fill="blue") # change color
    a=event.x
    b=event.y
    print "clicked at", a/SqSize, b/SqSize
    
    
#Called once the color is chosen, they are assined to respective player(Human, computer)
def ColorClicked():
    global AIcolor,MYcolor

    if(v.get()==1):                
        Flag3=1
        print "Your Color:     ",'black'
        MYcolor='black'                    #Human Color
        AIcolor='white'                    #Computer Color 
        print "Computer Color: ",'white'
        SetLayout()

    if(v.get()==2):
        Flag3=1
        print "Your Color:     ",'white'
        MYcolor='white'                       #Human Color
        AIcolor='black'                      #Computer Color 
        print "Computer Color: ",'black'
        SetLayout()
  

#This function develops the GUI for Computer and human pieces
def SetLayout():
    
    global x,y,AIcolor,MYcolor
    if(AIcolor=='white'):
        FirstMove=1
        x=[w1,w2,w3,w4,w5,w6]
        y=[b1,b2,b3,b4,b5,b6]

    if(AIcolor=='black'):
        x=[b1,b2,b3,b4,b5,b6]
        y=[w1,w2,w3,w4,w5,w6]
    
    #Difficulty Level is defined based on the depth of tree developed by alpha-beta search
        #NO NEED TO CHECK WHETHER T[0] IS EQUAL TO -INF

    make_squares(cv,0,8,"LightBlue",SqSize)

    for i in x:
        AIids.append(make_pieces(i,piece_offset,AIcolor))
    for i in y:
       Myids.append(make_pieces(i,piece_offset,MYcolor))

    if(v.get()==1):
        ComputerTurn()
        HumanTurn1



#Assign the difficulty level equal to the maximum depth till which the tree can be created.
def SelectDifficulty():
    global MaxDepth
    if v2.get()==1:
        MaxDepth=1
    if v2.get()==2:
        MaxDepth=2
    if v2.get()==3:
        MaxDepth=3
    if v2.get()==4:
        MaxDepth=4




#Define variable: INF denotes the maximum utility value. w1-w6 and b1-b6 are initial piece locations.

INF=10000
w1=(3,5)
w2=(4,5)
w3=(2,4)
w4=(3,4)
w5=(4,4)
w6=(5,4)
b1=(3,8)
b2=(4,8)
b3=(2,9)
b4=(3,9)
b5=(4,9)
b6=(5,9)

T=[0]

AIwin=0          #is Set to 1 if Computer Wins
MYwin=0          #Set to 1 if Human Wins
NodeGen=1        #Number of Nodes Generated
PrunInMax=0      #Number of Prunning in Max function
PrunInMin=0      #Number of Prunning in Min function
FirstMove=0
MYcolor=''
AIcolor=''
Flag2=0          #Flag variable to check whether human has selected a piece by clicking the mouse on the piece.
MaxDepth=2       #Default value of Maximum Depth till which the player can go.

SqSize=40                   # Square Size on the GUI
PIECE_DIAMETER=38           # Piece Diameter on the GUI
piece_offset=(SqSize-PIECE_DIAMETER)
MainGUI=Tk()
v=IntVar()                  #This variable stores the color choice of user
v2=IntVar()                 #This variable stores the difficulty level choice of the user

MainGUI.title("Camelot")
h=SqSize*14                 #Height of the Gameboard
w=SqSize*8                  #Width of the Gameboard
cv=Canvas(MainGUI, height=h, width=w)            
cv.grid(row=4, column=0)

x=[]
y=[]
inp1=''

Flag3=0                    #Checks whether two clicks are done on radiobutton for color
AIids=[]                   #Stores piece ids on the canvas
Myids=[]
SqID=()                    #stores clicked square id
PieceID=()                 #stores cliced piece id
PI=()                      #stores Human player clicked piece id


#Creating Radiobuttons to input difficulty level choice of the user
lbb=Label(MainGUI,text="Select Difficulty Level(1-4):Low---->High ",justify=LEFT,padx=20)
rbb1=Radiobutton(MainGUI,text="Level 1",padx=10,variable=v2,value=1,command=SelectDifficulty)
rbb2=Radiobutton(MainGUI,text="Level 2",padx=10,variable=v2,value=2,command=SelectDifficulty)
rbb3=Radiobutton(MainGUI,text="Level 3",padx=10,variable=v2,value=3,command=SelectDifficulty)
rbb4=Radiobutton(MainGUI,text="Level 4",padx=10,variable=v2,value=4,command=SelectDifficulty)
lbb.grid(row=0, column=1,columnspan=4)
rbb1.grid(row=1, column=1,columnspan=1)
rbb2.grid(row=1, column=2,columnspan=1)
rbb3.grid(row=1, column=3,columnspan=1)
rbb4.grid(row=1, column=4,columnspan=1)

#Creating Radiobuttons to input color choice of user
lb=Label(MainGUI,text="Choose a color",justify=LEFT,padx=10)
rb1=Radiobutton(MainGUI,text="Black",padx=10,variable=v,value=1,command=ColorClicked)
rb2=Radiobutton(MainGUI,text="White",padx=10,variable=v,value=2,command=ColorClicked)
lb.grid(row=2, column=1,columnspan=4  )
rb1.grid(row=3, column=2,columnspan=1 )
rb2.grid(row=3, column=3,columnspan=1)


#When Pieces are clicked HumnaTurn1 is called and when Squares are clicked to move pieces HumanTurn2 is called
cv.tag_bind("Piece","<1>" ,HumanTurn1)
cv.tag_bind("Square","<1>",HumanTurn2)


MainGUI.mainloop()

    