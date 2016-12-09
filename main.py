import matplotlib.pyplot as plt
from Tkinter import *
from pid import PID
from Manager import Manager


def main():
    root = Tk()
    Manager(root)
    root.mainloop()

def test_pid(p=0.2, i=0.0, d= 0.0):
    pid = PID.PID(p, i, d)

    setpoint_list = []
    time_list = []
    for i in range (1,50):
        time_list.append(i)
        if i < 9:
            setpoint_list.append(0)
        else:
            setpoint_list.append(1)

    pid.set_point = 0.0
    pid.dt = 0.01
    feedback = 0

    feedback_list = []

    plt.plot(time_list, setpoint_list)
    plt.xlim((-1, 51))
    plt.xlabel('time (s)')
    plt.ylabel('PID (PV)')
    plt.title('TEST PID')
    plt.ylim((-1, 2))
    plt.grid(True)
    plt.ion()

    for i in range(1, 30):
        pid.set_point = setpoint_list[i]
        output = pid.do_work(feedback)
        # Simulate new feedback
        if pid.set_point > 0:
            feedback += (output - (1/i))

        feedback_list.append(feedback)

        plt.ylim((min(feedback_list) - 0.5, max(feedback_list) + 0.5))
        plt.scatter(i, feedback)
        plt.pause(0.02)

    while True:
        plt.pause(0.05)

if __name__ == "__main__":
    main()
    # test_pid(1.1, 0.5, 0.001)



