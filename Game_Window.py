import tkinter as tk
import tkinter.messagebox
import Algo
import sqlite3

class Game(tk.Frame):
    name = ""
    player_choice=""
    def __init__(self, player_name,choice, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.name = player_name
        self.player_choice=choice
        self.createWidgets()

    def createWidgets(self):
        self.theBoard = [' '] * 10
        self.turn="player"

        self.blank_image = tk.PhotoImage(file="Resources/fff.gif")
        if(self.player_choice=="Cross"):
            self.choice_image = tk.PhotoImage(file="Resources/cross.gif")
            self.playerLetter, self.computerLetter = Algo.inputPlayerLetter('X')
        else:
            self.choice_image=tk.PhotoImage(file="Resources/zero.gif")
            self.playerLetter, self.computerLetter = Algo.inputPlayerLetter('O')

        self.player_lbl = tk.Label(self, text="Welcome, " + self.name)
        self.player_lbl.grid(row=0,column=0,columnspan=3)

        self.b1 = tk.Button(self,text="",relief="groove",image=self.blank_image,height=60,width=65, command=lambda: self.btn_click(self.b1,1))
        self.b1.grid(row=1,column=0,padx=(10, 10),pady=(10, 10))

        self.b2 = tk.Button(self,text="",relief="groove",image=self.blank_image,height=60,width=65,command=lambda: self.btn_click(self.b2,2))
        self.b2.grid(row=1,column=1,padx=(10, 10),pady=(10, 10))

        self.b3 = tk.Button(self,text="",relief="groove",image=self.blank_image,height=60,width=65,command=lambda: self.btn_click(self.b3,3))
        self.b3.grid(row=1,column=2,padx=(10, 10),pady=(10, 10))

        self.b4 = tk.Button(self,text="",relief="groove",image=self.blank_image,height=60,width=65,command=lambda: self.btn_click(self.b4,4))
        self.b4.grid(row=2,column=0,padx=(10, 10),pady=(10, 10))

        self.b5 = tk.Button(self,text="",relief="groove",image=self.blank_image,height=60,width=65,command=lambda: self.btn_click(self.b5,5))
        self.b5.grid(row=2,column=1,padx=(10, 10),pady=(10, 10))

        self.b6 = tk.Button(self,text="",relief="groove",image=self.blank_image,height=60,width=65,command=lambda: self.btn_click(self.b6,6))
        self.b6.grid(row=2,column=2,padx=(10, 10),pady=(10, 10))

        self.b7 = tk.Button(self,text="",relief="groove",image=self.blank_image,height=60,width=65,command=lambda: self.btn_click(self.b7,7))
        self.b7.grid(row=3,column=0,padx=(10, 10),pady=(10, 10))

        self.b8 = tk.Button(self,text="",relief="groove",image=self.blank_image,height=60,width=65,command=lambda: self.btn_click(self.b8,8))
        self.b8.grid(row=3,column=1,padx=(10, 10),pady=(10, 10))

        self.b9 = tk.Button(self,text="",relief="groove",image=self.blank_image,height=60,width=65,command=lambda: self.btn_click(self.b9,9))
        self.b9.grid(row=3,column=2,padx=(10, 10),pady=(10, 10))

    def btn_click(self,btn,val):
        btn.config(image=self.choice_image,state="disabled")
        move=val
        tie=""
        Algo.makeMove(self.theBoard, self.playerLetter, move)
        if Algo.isWinner(self.theBoard, self.playerLetter):
                conn = sqlite3.connect('player.db')  # connect to db (create if absent)
                c = conn.cursor()  # pointer to beginning

                # Save the Player Status with the Id in the table about the status of game
                # if the game is win it will save with game_status value as 1

                c.execute('SELECT id FROM player where Name=\'' + self.name + '\'')
                player_id = c.fetchone()
                c.execute('insert into wins(player_id,game_status) values('+str(player_id[0])+',1)')
                conn.commit()
                conn.close()
                result = tkinter.messagebox.askquestion("Information", "Hooray "+self.name+"! You have won the game!\nDo you want to play again?")
                if (result == 'yes'):
                    self.master.quit()
                    self.master.destroy()
                    root_new = tk.Tk()
                    root_new.title("Play Tic Tac Toe")
                    app = Game(player_name=self.name, choice=self.player_choice, master=root_new)
                    app.mainloop()
                else:
                    self.master.quit()
                    self.master.destroy()

        else:
                 if Algo.isBoardFull(self.theBoard):
                     tie="true"
                 else:
                     move = Algo.getComputerMove(self.theBoard, self.computerLetter)
                     Algo.makeMove(self.theBoard, self.computerLetter, move)
                     #print(move)
                     if(move==1):
                         if(self.computerLetter=='X'):
                            image_new=tk.PhotoImage(file="Resources/cross.gif")
                            self.b1.config(image=image_new,state="disabled")
                            self.b1.image=image_new
                         else:
                            image_new=tk.PhotoImage(file="Resources/zero.gif")
                            self.b1.config(image=image_new,state="disabled")
                            self.b1.image=image_new
                     if(move==2):
                             if(self.computerLetter=='X'):
                                image_new=tk.PhotoImage(file="Resources/cross.gif")
                                self.b2.config(image=image_new,state="disabled")
                                self.b2.image=image_new
                             else:
                                image_new=tk.PhotoImage(file="Resources/zero.gif")
                                self.b2.config(image=image_new,state="disabled")
                                self.b2.image=image_new
                     if(move==3):
                             if(self.computerLetter=='X'):
                                image_new=tk.PhotoImage(file="Resources/cross.gif")
                                self.b3.config(image=image_new,state="disabled")
                                self.b3.image=image_new
                             else:
                                image_new=tk.PhotoImage(file="Resources/zero.gif")
                                self.b3.config(image=image_new,state="disabled")
                                self.b3.image=image_new
                     if(move==4):
                             if(self.computerLetter=='X'):
                                image_new=tk.PhotoImage(file="Resources/cross.gif")
                                self.b4.config(image=image_new,state="disabled")
                                self.b4.image=image_new
                             else:
                                image_new=tk.PhotoImage(file="Resources/zero.gif")
                                self.b4.config(image=image_new,state="disabled")
                                self.b4.image=image_new
                     if(move==5):
                             if(self.computerLetter=='X'):
                                image_new=tk.PhotoImage(file="Resources/cross.gif")
                                self.b5.config(image=image_new,state="disabled")
                                self.b5.image=image_new
                             else:
                                image_new=tk.PhotoImage(file="Resources/zero.gif")
                                self.b5.config(image=image_new,state="disabled")
                                self.b5.image=image_new
                     if(move==6):
                             if(self.computerLetter=='X'):
                                image_new=tk.PhotoImage(file="Resources/cross.gif")
                                self.b6.config(image=image_new,state="disabled")
                                self.b6.image=image_new
                             else:
                                image_new=tk.PhotoImage(file="Resources/zero.gif")
                                self.b6.config(image=image_new,state="disabled")
                                self.b6.image=image_new
                     if(move==7):
                             if(self.computerLetter=='X'):
                                image_new=tk.PhotoImage(file="Resources/cross.gif")
                                self.b7.config(image=image_new,state="disabled")
                                self.b7.image=image_new
                             else:
                                image_new=tk.PhotoImage(file="Resources/zero.gif")
                                self.b7.config(image=image_new,state="disabled")
                                self.b7.image=image_new
                     if(move==8):
                             if(self.computerLetter=='X'):
                                image_new=tk.PhotoImage(file="Resources/cross.gif")
                                self.b8.config(image=image_new,state="disabled")
                                self.b8.image=image_new
                             else:
                                image_new=tk.PhotoImage(file="Resources/zero.gif")
                                self.b8.config(image=image_new,state="disabled")
                                self.b8.image=image_new
                     if(move==9):
                             if(self.computerLetter=='X'):
                                image_new=tk.PhotoImage(file="Resources/cross.gif")
                                self.b9.config(image=image_new,state="disabled")
                                self.b9.image=image_new
                             else:
                                image_new=tk.PhotoImage(file="Resources/zero.gif")
                                self.b9.config(image=image_new,state="disabled")
                                self.b9.image=image_new

                 if Algo.isWinner(self.theBoard, self.computerLetter):

                     # Save the Player Status with the Id in the table about the status of game
                     # if the player looses game it will save with game_status value as 2

                     conn = sqlite3.connect('player.db')  # connect to db (create if absent)
                     c = conn.cursor()  # pointer to beginning
                     c.execute('SELECT id FROM player where Name=\'' + self.name + '\'')
                     player_id = c.fetchone()

                     c.execute('insert into wins(player_id,game_status) values(' + str(player_id[0]) + ',2)')
                     conn.commit()
                     conn.close()

                     result = tkinter.messagebox.askquestion("Information",
                                                             "The computer has beaten you :-( \nDo you want to play again?")
                     if (result == 'yes'):
                         self.master.quit()
                         self.master.destroy()
                         root_new = tk.Tk()
                         root_new.title("Play Tic Tac Toe")
                         app = Game(player_name=self.name, choice=self.player_choice, master=root_new)
                         app.mainloop()
                     else:
                         self.master.quit()
                         self.master.destroy()

                 else:
                    if Algo.isBoardFull(self.theBoard):
                        tie="true"

                 if(tie=="true"):
                     # Save the Player Status with the Id in the table about the status of game
                     # if the game is tie it will save with game_status value as 3

                     conn = sqlite3.connect('player.db')  # connect to db (create if absent)
                     c = conn.cursor()  # pointer to beginning
                     c.execute('SELECT id FROM player where Name=\'' + self.name + '\'')
                     player_id = c.fetchone()

                     c.execute('insert into wins(player_id,game_status) values(' + str(player_id[0]) + ',3)')
                     conn.commit()
                     conn.close()
                     result=tkinter.messagebox.askquestion("Information", "The game is a tie!\nDo you want to play again?")
                     if(result=='yes'):
                         self.master.quit()
                         self.master.destroy()
                         root_new = tk.Tk()
                         root_new.title("Play Tic Tac Toe")
                         app = Game(player_name=self.name, choice=self.player_choice, master=root_new)
                         app.mainloop()
                     else:
                         self.master.quit()
                         self.master.destroy()



