from Tkinter import *


class FeedBackPanel(Frame):
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)

        self.config(bd=1, relief=RAISED, padx=2, pady=2)
        self.default_bg = self.cget('bg')
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)

        title_lbl = Label(self, text="Values", bd=2, relief=FLAT, fg="slate gray")
        title_lbl.grid(row=0, columnspan=4)

        ent_opt_dis = {'fg': 'gainsboro', 'state': DISABLED, 'justify': CENTER, 'width': 8}
        ent_opt_ena = {'fg': 'gainsboro', 'state': NORMAL, 'justify': CENTER, 'width': 8}

        # PID values of target panel
        Label(self, text="Target: ", fg="dim gray").grid(row=2, column=0, sticky=E)
        Label(self, text="Sense: ", fg="dim gray").grid(row=3, column=0, sticky=E)
        Label(self, text="Error: ", fg="dim gray").grid(row=4, column=0, sticky=E)
        Label(self, text="PID: ", fg="dim gray").grid(row=5, column=0, sticky=E)

        self.target_txt = StringVar()
        self.sense_txt = StringVar()
        self.pid_txt = StringVar()
        self.error_txt = StringVar()

        self.target_ent = Entry(self, textvariable=self.target_txt, **ent_opt_dis)
        self.target_ent.grid(row=2, column=1, sticky=W)
        self.sense_ent = Entry(self, textvariable=self.sense_txt, **ent_opt_dis)
        self.sense_ent.grid(row=3, column=1, sticky=W)
        self.error_ent = Entry(self, textvariable=self.error_txt, **ent_opt_dis)
        self.error_ent.grid(row=4, column=1, sticky=W)
        self.pid_ent = Entry(self, textvariable=self.pid_txt, **ent_opt_ena)
        self.pid_ent.grid(row=5, column=1, sticky=W)

        self.target_txt.set("...")
        self.sense_txt.set("...")
        self.pid_txt.set("...")
        self.error_txt.set("...")

        # Indicators
        Label(self, text="Door: ", fg="dim gray").grid(row=2, column=2, sticky=E)
        Label(self, text="State: ", fg="dim gray").grid(row=3, column=2, sticky=E)
        Label(self, text="Heater: ", fg="dim gray").grid(row=4, column=2, sticky=E)
        Label(self, text="Fan: ", fg="dim gray").grid(row=5, column=2, sticky=E)

        self.door_txt = StringVar()
        self.state_txt = StringVar()
        self.heater_txt = StringVar()
        self.fan_txt = StringVar()

        self.door_ent = Entry(self, textvariable=self.door_txt, **ent_opt_ena)
        self.door_ent.grid(row=2, column=3, sticky=W)
        self.state_ent = Entry(self, textvariable=self.state_txt, **ent_opt_ena)
        self.state_ent.grid(row=3, column=3, sticky=W)
        self.heater_ent = Entry(self, textvariable=self.heater_txt, **ent_opt_ena)
        self.heater_ent.grid(row=4, column=3, sticky=W)
        self.fan_ent = Entry(self, textvariable=self.fan_txt, **ent_opt_ena)
        self.fan_ent.grid(row=5, column=3, sticky=W)

        self.door_txt.set("...")
        self.state_txt.set("...")
        self.heater_txt.set("...")
        self.fan_txt.set("...")

        # PID K values
        self.kp_txt = StringVar()
        self.ki_txt = StringVar()
        self.kd_txt = StringVar()
        Label(self, textvariable=self.kp_txt, fg="gainsboro", state=DISABLED, justify=CENTER) \
            .grid(row=6, column=0)
        Label(self, textvariable=self.ki_txt, fg="gainsboro", state=DISABLED, justify=CENTER) \
            .grid(row=6, column=1, columnspan=2)
        Label(self, textvariable=self.kd_txt, fg="gainsboro", state=DISABLED, justify=CENTER) \
            .grid(row=6, column=3)

        self.kp_txt.set("Kp: ...")
        self.ki_txt.set("Ki: ...")
        self.kd_txt.set("Kd: ...")

    """
    Entry values
    """
    # PID
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

    def set_error_value(self, value):
        self.error_txt.set("{0:.2f}".format(value))

    # K values
    def set_kp_value(self, value):
        self.kp_txt.set("Kp: "+str(value))

    def set_ki_value(self, value):
        self.ki_txt.set("Ki: "+str(value))

    def set_kd_value(self, value):
        self.kd_txt.set("Kd: "+str(value))

    # Indicators
    def set_door_state(self, state):
        if state == 'O':
            self.door_txt.set('Open')
            self.door_ent.configure(fg="gainsboro")
            self.door_ent.configure(bg="orange red")
        elif state == 'C':
            self.door_txt.set('Closed')
            self.door_ent.configure(fg="dim gray")
            self.door_ent.configure(bg="lawn green")
        else:
            self.door_txt.set('...')
            self.door_ent.configure(bg=None)

    def set_state_state(self, state):
        pass

    def set_heater_state(self, state):
        if state == 'ON':
            self.heater_txt.set('On')
            self.heater_ent.configure(fg="gainsboro")
            self.heater_ent.configure(bg="orange red")
        elif state == 'OFF':
            self.heater_txt.set('Off')
            self.heater_ent.configure(fg="dim gray")
            self.heater_ent.configure(bg=self.default_bg)
        else:
            self.heater_txt.set('...')
            self.heater_ent.configure(fg="dim gray")
            self.heater_ent.configure(bg=self.default_bg)

    def set_fan_state(self, state):
        if state == 'ON':
            self.fan_txt.set('On')
            self.fan_ent.configure(fg="gainsboro")
            self.fan_ent.configure(bg="royal blue")
        elif state == 'OFF':
            self.fan_txt.set('Off')
            self.fan_ent.configure(fg="dim gray")
            self.fan_ent.configure(bg=self.default_bg)
        else:
            self.fan_txt.set('...')
            self.fan_ent.configure(fg="dim gray")
            self.fan_ent.configure(bg=self.default_bg)


