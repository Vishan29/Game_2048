#Code to create a 2048 game using python tkinter....

#importing tkinter libraries
from tkinter import *
from tkinter import messagebox
import random

#board class
class Board:
    bg_color={
        '2': '#eee4da',
        '4': '#ede0c8',
        '8': '#edc850',
        '16': '#edc53f',
        '32': '#f67c5f',
        '64': '#f65e3b',
        '128': '#edcf72',
        '256': '#edcc61',
        '512': '#f2b179',
        '1024': '#f59563',
        '2048': '#edc22e',
    }

    color={
         '2': '#776e65',
        '4': '#f9f6f2',
        '8': '#f9f6f2',
        '16': '#f9f6f2',
        '32': '#f9f6f2',
        '64': '#f9f6f2',
        '128': '#f9f6f2',
        '256': '#f9f6f2',
        '512': '#776e65',
        '1024': '#f9f6f2',
        '2048': '#f9f6f2',
    }

    def __init__(self):
        self.n=4
        self.window=Tk()
        self.window.title('2048 Game')
        photo = PhotoImage(file = "img_2048.png")
        self.window.iconphoto(False,photo)
        self.gameArea=Frame(self.window,bg= 'azure3')
        self.board=[]
        self.gridCell=[[0]*4 for i in range(4)]
        self.compress=False
        self.merge=False
        self.moved=False
        self.score=0
        for i in range(4):
            rows=[]
            for j in range(4):
                l=Label(self.gameArea,text='',bg='azure4',
                font=('arial',22,'bold'),width=4,height=2)
                l.grid(row=i,column=j,padx=7,pady=7)
                rows.append(l);
            self.board.append(rows)
        self.gameArea.grid()
    def reverse(self):
        for ind in range(4):
            i=0
            j=3
            while(i<j):
                self.gridCell[ind][i],self.gridCell[ind][j]=self.gridCell[ind][j],self.gridCell[ind][i]
                i+=1
                j-=1
    def transpose(self):
        self.gridCell=[list(t)for t in zip(*self.gridCell)]
    def compressGrid(self):
        self.compress=False
        temp=[[0] *4 for i in range(4)]
        for i in range(4):
            cnt=0
            for j in range(4):
                if self.gridCell[i][j]!=0:
                    temp[i][cnt]=self.gridCell[i][j]
                    if cnt!=j:
                        self.compress=True
                    cnt+=1
        self.gridCell=temp
    def mergeGrid(self):
        self.merge=False
        for i in range(4):
            for j in range(4 - 1):
                if self.gridCell[i][j] == self.gridCell[i][j + 1] and self.gridCell[i][j] != 0:
                    self.gridCell[i][j] *= 2
                    self.gridCell[i][j + 1] = 0
                    self.score += self.gridCell[i][j]
                    self.merge = True
    def random_cell(self):
        cells=[]
        for i in range(4):
            for j in range(4):
                if self.gridCell[i][j] == 0:
                    cells.append((i, j))
        curr=random.choice(cells)
        i=curr[0]
        j=curr[1]
        self.gridCell[i][j]=2
    
    def can_merge(self):
        for i in range(4):
            for j in range(3):
                if self.gridCell[i][j] == self.gridCell[i][j+1]:
                    return True
        
        for i in range(3):
            for j in range(4):
                if self.gridCell[i+1][j] == self.gridCell[i][j]:
                    return True
        return False
        
    def paintGrid(self):
        for i in range(4):
            for j in range(4):
                if self.gridCell[i][j]==0:
                    self.board[i][j].config(text='',bg='azure4')
                else:
                    self.board[i][j].config(text=str(self.gridCell[i][j]),
                    bg=self.bg_color.get(str(self.gridCell[i][j])),
                    fg=self.color.get(str(self.gridCell[i][j])))

class Game:
    def __init__(self,Panel):
        self.Panel=Panel
        self.end=False
        self.Win=False
    def start(self):
        self.Panel.random_cell()
        self.Panel.random_cell()
        self.Panel.paintGrid()
        self.Panel.window.bind('<Key>', self.link_keys)
        self.Panel.window.mainloop()
    
    def link_keys(self,event):
        if self.end or self.Win:
            return
        self.Panel.compress = False
        self.Panel.merge = False
        self.Panel.moved = False
        presed_key=event.keysym
        if presed_key=='Up':
            self.Panel.transpose()
            self.Panel.compressGrid()
            self.Panel.mergeGrid()
            self.Panel.moved = self.Panel.compress or self.Panel.merge
            self.Panel.compressGrid()
            self.Panel.transpose()
        elif presed_key=='Down':
            self.Panel.transpose()
            self.Panel.reverse()
            self.Panel.compressGrid()
            self.Panel.mergeGrid()
            self.Panel.moved = self.Panel.compress or self.Panel.merge
            self.Panel.compressGrid()
            self.Panel.reverse()
            self.Panel.transpose()
        elif presed_key=='Left':
            self.Panel.compressGrid()
            self.Panel.mergeGrid()
            self.Panel.moved = self.Panel.compress or self.Panel.merge
            self.Panel.compressGrid()
        elif presed_key=='Right':
            self.Panel.reverse()
            self.Panel.compressGrid()
            self.Panel.mergeGrid()
            self.Panel.moved = self.Panel.compress or self.Panel.merge
            self.Panel.compressGrid()
            self.Panel.reverse()
        else:
            pass
        self.Panel.paintGrid()
        print(self.Panel.score)
        flag=0
        for i in range(4):
            for j in range(4):
                if(self.Panel.gridCell[i][j]==2048):
                    flag=1
                    break
        if(flag==1): #found 2048
            self.Win=True
            messagebox.showinfo('2048', message='You Win!!')
            print("Win")
            return
        for i in range(4):
            for j in range(4):
                if self.Panel.gridCell[i][j]==0:
                    flag=1
                    break
        if not (flag or self.Panel.can_merge()):
            self.end=True
            messagebox.showinfo('2048','Game Over!!!')
            print("Over")
        if self.Panel.moved:
            self.Panel.random_cell()
        
        self.Panel.paintGrid()
    
Panel = Board() #creating panel
Game_2048 = Game(Panel) #creating game using panel
Game_2048.start() #to start the game