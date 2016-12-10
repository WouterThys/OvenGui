from Tkinter import *
import time


class MessagePanel(Frame):
    def __init__(self, master, *args, **kwargs):
        #Frame.__init__(self, master, width=50, height=100, *args, **kwargs)
        Frame.__init__(self, master, height=20, *args, **kwargs)

        self.config(bd=1, relief=RAISED, padx=2, pady=10)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)

        #
        title_lbl = Label(self, text="Feedback", bd=2, relief=FLAT, fg="slate gray")
        title_lbl.grid(row=0, columnspan=4)

        input_frame = Frame(self, borderwidth=3, relief=SUNKEN)
        input_frame.grid(row=1, column=0, columnspan=4)

        # Names
        time_lbl = Label(input_frame, text="Time", fg="dim gray")
        time_lbl.grid(row=1, column=0)
        time_lbl = Label(input_frame, text="Sender", fg="dim gray")
        time_lbl.grid(row=1, column=1)
        time_lbl = Label(input_frame, text="Command", fg="dim gray")
        time_lbl.grid(row=1, column=2)
        time_lbl = Label(input_frame, text="Message", fg="dim gray")
        time_lbl.grid(row=1, column=3, columnspan=2)
        # Text widgets
        self.time_txt = Text(input_frame, bg='lavender', state=DISABLED, font=("consolas", 12), undo=True, wrap='word', width=10, height=8)
        self.time_txt.grid(row=2, column=0, pady=2)
        self.time_txt.bind("<Button-4>", self.on_mouse_wheel)
        self.time_txt.bind("<Button-5>", self.on_mouse_wheel)
        self.sender_txt = Text(input_frame, bg='lavender', state=DISABLED, font=("consolas", 12), undo=True, wrap='word', width=10, height=8)
        self.sender_txt.grid(row=2, column=1, pady=2)
        self.sender_txt.bind("<Button-4>", self.on_mouse_wheel)
        self.sender_txt.bind("<Button-5>", self.on_mouse_wheel)
        self.command_txt = Text(input_frame, bg='lavender', state=DISABLED, font=("consolas", 12), undo=True, wrap='word', width=10, height=8)
        self.command_txt.grid(row=2, column=2, pady=2)
        self.command_txt.bind("<Button-4>", self.on_mouse_wheel)
        self.command_txt.bind("<Button-5>", self.on_mouse_wheel)
        self.message_txt = Text(input_frame, bg='lavender', state=DISABLED, font=("consolas", 12), undo=True, wrap='word', width=30, height=8)
        self.message_txt.grid(row=2, column=3, columnspan=2, pady=2, sticky='nsew')
        self.message_txt.bind("<Button-4>", self.on_mouse_wheel)
        self.message_txt.bind("<Button-5>", self.on_mouse_wheel)
        # Scoll bar
        self.scroll = Scrollbar(input_frame, orient='vertical', command=self.on_vertical_scroll)
        self.scroll.grid(row=2, column=5, sticky='nsew')
        self.time_txt.configure(yscrollcommand=self.scroll.set)
        self.sender_txt.configure(yscrollcommand=self.scroll.set)
        self.command_txt.configure(yscrollcommand=self.scroll.set)
        self.message_txt.configure(yscrollcommand=self.scroll.set)

    def __del__(self):
        self.time_txt.unbind("<Button-4>")
        self.time_txt.unbind("<Button-5>")
        self.sender_txt.unbind("<Button-4>")
        self.sender_txt.unbind("<Button-5>")
        self.command_txt.unbind("<Button-4>")
        self.command_txt.unbind("<Button-5>")
        self.message_txt.unbind("<Button-4>")
        self.message_txt.unbind("<Button-5>")

    def on_vertical_scroll(self, *args):
        self.time_txt.yview(*args)
        self.sender_txt.yview(*args)
        self.command_txt.yview(*args)
        self.message_txt.yview(*args)

    def on_mouse_wheel(self, event):
        if event.num == 5 or event.delta == -120:
            self.time_txt.yview_scroll((event.delta), "units")
            self.sender_txt.yview_scroll((event.delta), "units")
            self.command_txt.yview_scroll((event.delta), "units")
            self.message_txt.yview_scroll((event.delta), "units")
        if event.num == 4 or event.delta == 120:
            self.time_txt.yview_scroll((event.delta/120), "units")
            self.sender_txt.yview_scroll((event.delta/120), "units")
            self.command_txt.yview_scroll((event.delta/120), "units")
            self.message_txt.yview_scroll((event.delta/120), "units")
        return "break"

    def add_new_line(self, the_time, the_sender, the_command, the_message):
        t = time.strftime("%H:%M:%S", time.localtime(the_time))
        self.time_txt.configure(state=NORMAL)
        self.time_txt.insert(END, t+"\n", "a")
        self.time_txt.configure(state=DISABLED)
        self.sender_txt.configure(state=NORMAL)
        self.sender_txt.insert(END, the_sender+"\n", "a")
        self.sender_txt.configure(state=DISABLED)
        self.command_txt.configure(state=NORMAL)
        self.command_txt.insert(END, the_command+"\n", "a")
        self.command_txt.configure(state=DISABLED)
        self.message_txt.configure(state=NORMAL)
        self.message_txt.insert(END, the_message+"\n", "a")
        self.message_txt.configure(state=DISABLED)

        self.time_txt.see('end')
        self.sender_txt.see('end')
        self.command_txt.see('end')
        self.message_txt.see('end')