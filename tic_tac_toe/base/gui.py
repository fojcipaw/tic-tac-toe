'''
Created on 15 kwi 2022

@author: fojcjpaw
'''
from tkinter import *
from tkinter import messagebox

class GUI:
    def __init__(self, board):
        self.board = board
        self.t=Tk()
        self.t.title("TIC TAC TOE")
        self.t.configure(bg="white")  #Making the background of the window as white
        
        #Grid buttons
        b1=Button(self.t,text="",height=4,width=8,bg="black",activebackground="white",fg="white",font="Times 15 bold",command=lambda: self.__btn_click(0,0))
        b2=Button(self.t,text="",height=4,width=8,bg="black",activebackground="white",fg="white",font="Times 15 bold",command=lambda: self.__btn_click(0,1))
        b3=Button(self.t,text="",height=4,width=8,bg="black",activebackground="white",fg="white",font="Times 15 bold",command=lambda: self.__btn_click(0,2))
        b4=Button(self.t,text="",height=4,width=8,bg="black",activebackground="white",fg="white",font="Times 15 bold",command=lambda: self.__btn_click(1,0))
        b5=Button(self.t,text="",height=4,width=8,bg="black",activebackground="white",fg="white",font="Times 15 bold",command=lambda: self.__btn_click(1,1))
        b6=Button(self.t,text="",height=4,width=8,bg="black",activebackground="white",fg="white",font="Times 15 bold",command=lambda: self.__btn_click(1,2))
        b7=Button(self.t,text="",height=4,width=8,bg="black",activebackground="white",fg="white",font="Times 15 bold",command=lambda: self.__btn_click(2,0))
        b8=Button(self.t,text="",height=4,width=8,bg="black",activebackground="white",fg="white",font="Times 15 bold",command=lambda: self.__btn_click(2,1))
        b9=Button(self.t,text="",height=4,width=8,bg="black",activebackground="white",fg="white",font="Times 15 bold",command=lambda: self.__btn_click(2,2))
    
        b1.grid(row=0,column=0)
        b2.grid(row=0,column=1)
        b3.grid(row=0,column=2)
    
        b4.grid(row=1,column=0)
        b5.grid(row=1,column=1)
        b6.grid(row=1,column=2)
    
        b7.grid(row=2,column=0)
        b8.grid(row=2,column=1)
        b9.grid(row=2,column=2)
        
        self.gui_board=((b1,b2,b3),
                    (b4,b5,b6),
                    (b7,b8,b9))
        
        self.is_clicked = IntVar(self.t,0)
        self.action = None

    def __reset(self):
        self.board.reset()
        for col in range(0,3):
            for row in range(0,3):
                self.gui_board[row][col]["text"]=""
                self.gui_board[row][col]["bg"]="black"
    
    def __btn_click(self,row,col):
        if (row,col) in self.board.available_moves():
            self.action = (row,col)
        else:
            self.action = None
            messagebox.showerror("Error", "incorrect apply_action!")
        self.is_clicked.set(1)
    
    def update_field(self, packs):
        for p in packs:
            row = p[0]
            col = p[1]
            value = p[2]
            self.gui_board[row][col]["fg"]="blue"
            self.gui_board[row][col]["text"]=f'{value:.2f}'
        
    def finish(self, winner_mark):
        #mark green the winner line
        the_winning_line = self.board.get_winning_line()
        is_new_game_needed = False
        if the_winning_line != None:
            for row,col in the_winning_line:                
                self.gui_board[row][col]["bg"]="green"
            msg = messagebox.askquestion ("Game over","The winner is: " + winner_mark +
                                          ", do you want to play again?",icon = 'info')
            if msg == 'yes':
                self.__reset()
                is_new_game_needed = True
            else:
                self.is_clicked.set(1)
                self.t.destroy()
        else:
            msg = messagebox.askquestion ("Game over","Draw :-), do you want to play again?",icon = 'info')
            if msg == 'yes':
                self.__reset()
                is_new_game_needed = True
            else:
                self.is_clicked.set(1)
                self.t.destroy()
        return is_new_game_needed

    def apply_action(self, action, mark):
        row = action[0]
        col = action[1]
        self.gui_board[row][col]["fg"]="white"
        if  self.gui_board[row][col]["text"] and mark == "O":
            self.gui_board[row][col]["text"]=mark + "(" + str(self.gui_board[row][col]["text"]) + ")"
        else:
            self.gui_board[row][col]["text"]=mark

    def get_action(self):
        return self.action
    
    def loop(self):
        self.t.mainloop()
    
    def update(self):
        self.t.update_idletasks()
        self.t.update()
    
    def wait(self):
        self.t.wait_variable(self.is_clicked)