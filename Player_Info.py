import tkinter as tk
import threading, zipfile
import sqlite3
from tkinter import ttk
from tkinter import messagebox
from Game_Window import Game
from queue import Queue
from threading import Thread
from urllib.request import urlopen
import webbrowser
from multiprocessing import Process


class AsyncZip(threading.Thread):  # Python: a kind of Thread

    def __init__(self, infile, outfile):
        threading.Thread.__init__(self)
        self.infile = infile  # unzipped source
        self.outfile = outfile  # zipped target

    def run(self):  # Python: executed when start() called on the object
        # outfile contains a zip of infile and monitor reports completion
        f = zipfile.ZipFile(self.outfile, 'w', zipfile.ZIP_DEFLATED)
        f.write(self.infile)
        f.close()
        print('Finished background zip of: ', self.infile)


class MyException(Exception):  # inherit from Exception

    error_description = "Please Enter the value in the fields."

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Db:
    def connect(self):
        conn = sqlite3.connect('player.db')  # connect to db (create if absent)
        c = conn.cursor()  # pointer to beginning
        return conn, c

    # Select all the names of the player to get into the list
    def get_player_name(self, c):
        names = []
        player_name = c.execute('SELECT * FROM player')
        for row in player_name:
            names.append(row[1])
        return names

    # Add New Names in the Database if it does not exist
    def add_name(self, name, conn, c):
        try:
            c.execute('INSERT INTO player(name) VALUES (\'' + name + '\')')
            conn.commit()
        except sqlite3.IntegrityError:
            print("Already added in Table")


class Player_Info(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()

        self.createWidgets()

    def get_url(self,a_queue, a_url):
        # Pre: a_queue is Queue object and a_url is legitimate URL
        # Post: Content of a_url is at the back of a_queue
        a_queue.put(urlopen(a_url).read())

    #Save the Player Score Status File in html and Zip Format with the use of Background Thread
    def save_sc(self,win,loose,tie,player_name):
        html_score = "<html><head><title>Score History</title></head><body><h1>" + player_name + " Score History</h1>" \
                                                                                                                  "<table><tr><td>Status</td><td>Value</td></tr>" \
                                                                                                                  "<tr><td>Wins</td><td>" + str(
            win) + "</td></tr>" \
                   "<tr><td>Lost</td><td>" + str(loose) + "</td></tr>" \
                                                          "<tr><td>Tie</td><td>" + str(tie) + "</td></tr></table>" \
                                                                                              "</body></html>"
        f = open(player_name + "_score.html", "w")  # relative access
        f.write(html_score)
        f.close()
        url_relative = self.player_name_combo.get() + "_score"
        background_thread = AsyncZip(url_relative + ".html", url_relative + '.zip')
        background_thread.start()
        webbrowser.open_new(url_relative)

    def createWidgets(self):
        obj = Db()
        conn, c = obj.connect()

        self.player_lbl = tk.Label(self, text="Player Name")
        self.player_lbl.grid(row=0, column=0, padx=(10, 10), pady=(10, 10))

        self.player_name_combo = tk.ttk.Combobox(self, value=obj.get_player_name(c))
        self.player_name_combo.grid(row=0, column=1, columnspan=2, padx=(10, 10), pady=(10, 10), sticky="we")

        self.choice_lbl = tk.Label(self, text="Your Choice")
        self.choice_lbl.grid(row=1, column=0, padx=(10, 10), pady=(10, 10))

        self.choice_combo = tk.ttk.Combobox(self, value=('Cross', 'Circle'), takefocus=0)
        self.choice_combo.grid(row=1, column=1, columnspan=2, padx=(10, 10), pady=(10, 10), sticky="we")

        self.view_status_btn = tk.Button(self, text="View Status", command=lambda root=root: self.view_status(c))
        self.view_status_btn.grid(row=2, column=0, padx=(10, 10), pady=(10, 10))

        self.enter_game_btn = tk.Button(self, text="Play Game !", command=lambda root=root: self.open_game(root))
        self.enter_game_btn.grid(row=2, column=1, padx=(10, 10), pady=(10, 10))

        self.extract_score_btn = tk.Button(self, text="Get All Score", command=lambda root=root: self.get_score(c))
        self.extract_score_btn.grid(row=2, column=2, padx=(10, 10), pady=(10, 10))

        self.view_browser_btn = tk.Button(self, text="How to Play Tic Tac Toe", command=lambda root=root: self.view_browser())
        self.view_browser_btn.grid(row=3, column=0, columnspan=3, padx=(10, 10), pady=(10, 10))

    # Show the Player Status counting the values of Wins, Loose and Tie from the database by selecting the
    # rows related to the player and incrementing the variables
    def view_status(self, c):
        c.execute('SELECT id FROM player where Name=\'' + self.player_name_combo.get() + '\'')
        player_id = c.fetchone()
        if (player_id is not None):
            rows = c.execute('select game_status from wins where player_id=' + str(player_id[0]))
            win = 0
            loose = 0
            tie = 0
            for r in rows:
                if (r[0] == 1):
                    win += 1
                elif (r[0] == 2):
                    loose += 1
                elif (r[0] == 3):
                    tie += 1
            tk.messagebox.showinfo('Status', "Win: " + str(win) + "\nLost: " + str(loose) + "\nTie: " + str(tie))
        else:
            tk.messagebox.showinfo('Status', "No Games Played Yet or Player Does not Exist")

    # Shows Exception if one of the Control is Empty.
    def get_value_control(self, ctrl):
        val = ctrl.get()
        if (val != ""):
            return val
        else:
            raise MyException(val)

    def open_game(self, root):
        try:
            obj = Db()
            conn, c = obj.connect()

            name = self.get_value_control(self.player_name_combo)
            option = self.get_value_control(self.choice_combo)
            obj.add_name(name, conn, c)
            conn.close()
            root.quit()
            root.destroy()
            root_new = tk.Tk()
            root_new.title("Play Tic Tac Toe")
            app = Game(player_name=name, choice=option, master=root_new)
            app.mainloop()
        except MyException:
            tk.messagebox.showerror('Error', MyException.error_description)

    # Get Player Score on HTML File as well as compressed in Zip Format with a new Process
    def get_score(self, c):
        c.execute('SELECT id FROM player where Name=\'' + self.player_name_combo.get() + '\'')
        player_id = c.fetchone()
        if (player_id is not None):
            rows = c.execute('select game_status from wins where player_id=' + str(player_id[0]))
            win = 0
            loose = 0
            tie = 0
            for r in rows:
                if (r[0] == 1):
                    win += 1
                elif (r[0] == 2):
                    loose += 1
                elif (r[0] == 3):
                    tie += 1

            a_process = Process(target=self.save_sc, args=(win,loose,tie,self.player_name_combo.get(),))
            a_process.start()
            a_process.join()  # execute next statement when a_process completed

        else:
            tk.messagebox.showinfo('Status', "No Games Played Yet or Player Does not Exist")

    #Display Link on How to Play Tic Tac Toe and Wikipedia Link on Tic Tac Toe
    def view_browser(self):
        the_urls = ["http://www.wikihow.com/Play-Tic-Tac-Toe", "https://en.wikipedia.org/wiki/Tic-tac-toe"]
        # The content of the first URL in the_urls is on the monitor
        the_queue = Queue()
        for url in the_urls:
            thread = Thread(target=self.get_url, args=(the_queue, url))
            thread.start()
            webbrowser.open_new(url)

root = tk.Tk()
root.title("Tic Tac Toe")

app = Player_Info(master=root)

app.mainloop()
