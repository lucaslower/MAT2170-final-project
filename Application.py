"""
Application() class.
Handles GUI setup of data visualization, using tkinter.
"""

import tkinter as tk


class Application(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.quitButton = tk.Button(self, text='Quit', command=self.quit)
        self.quitButton.grid()
