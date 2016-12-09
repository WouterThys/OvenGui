from Tkinter import *


class FeedBackPanel(Frame):
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)

        self.config(bd=1, relief=RAISED, padx=2, pady=2)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)

        title_lbl = Label(self, text="Feedback", bd=2, relief=FLAT, fg="slate gray")
        title_lbl.grid(row=0, columnspan=3)

        Label(self, text="Target: ", fg="dim gray").grid(row=2, column=0, sticky=E)
        Label(self, text="Sense: ", fg="dim gray").grid(row=3, column=0, sticky=E)
        Label(self, text="PID: ", fg="dim gray").grid(row=4, column=0, sticky=E)

        self.target_txt = StringVar()
        self.sense_txt = StringVar()
        self.pid_txt = StringVar()
        Entry(self, textvariable=self.target_txt, fg="gainsboro", state=DISABLED, justify=CENTER)\
            .grid(row=2, column=1, columnspan=2, sticky=W)
        Entry(self, textvariable=self.sense_txt, fg="gainsboro", state=DISABLED, justify=CENTER) \
            .grid(row=3, column=1, columnspan=2, sticky=W)
        self.pid_ent = Entry(self, textvariable=self.pid_txt, fg="gainsboro", justify=CENTER)
        self.pid_ent.grid(row=4, column=1, columnspan=2, sticky=W)

        self.target_txt.set("...")
        self.sense_txt.set("...")
        self.pid_txt.set("...")

        self.kp_txt = StringVar()
        self.ki_txt = StringVar()
        self.kd_txt = StringVar()
        Label(self, textvariable=self.kp_txt, fg="gainsboro", state=DISABLED, justify=CENTER) \
            .grid(row=5, column=0)
        Label(self, textvariable=self.ki_txt, fg="gainsboro", state=DISABLED, justify=CENTER) \
            .grid(row=5, column=1)
        Label(self, textvariable=self.kd_txt, fg="gainsboro", state=DISABLED, justify=CENTER) \
            .grid(row=5, column=2)

        self.kp_txt.set("Kp: ...")
        self.ki_txt.set("Ki: ...")
        self.kd_txt.set("Kd: ...")

    """
    Button click events
    """

    """
    Entry values
    """
    def set_target_value(self, value):
        self.target_txt.set("{0:.2f}".format(value))

    def set_sense_value(self, value):
        self.sense_txt.set("{0:.2f}".format(value))

    def set_pid_value(self, value):
        self.pid_txt.set("{0:.2f}".format(value))
        if value > 0:
            self.pid_ent.configure(bg='orange red')
        elif value == 0:
            self.pid_ent.configure(bg="lawn green")
        else:
            self.pid_ent.configure(bg="royal blue")

    def set_kp_value(self, value):
        self.kp_txt.set("Kp: "+str(value))

    def set_ki_value(self, value):
        self.ki_txt.set("Ki: "+str(value))

    def set_kd_value(self, value):
        self.kd_txt.set("Kd: "+str(value))

