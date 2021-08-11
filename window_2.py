from tkinter import Label, Toplevel, simpledialog, messagebox, PhotoImage, Button, Canvas

from menu import get_menu
from day_time import convert_time, convert_date, check_public_holiday
from operating_times import get_operating_time

map_stalls_list = ('Bakery Cuisine', 'Boost Juice', 'Each-A-Cup', 'Fun World Cafe', 'Long John Silver\'s')
title = 'NTU'

user_day = user_time = None


def input_time_la(day, time):
    global user_day, user_time
    user_day = day
    user_time = time


def back(root, me):
    me.withdraw()
    root.deiconify()
    pass


def specific_time(counter, GUI):
    mini_window = Toplevel()
    # background_image = PhotoImage(file='image\\Bakery Cuisine Background.png')  # not dynamic
    # another_label2 = Label(mini_window, text=get_operating_time(map_stalls_list[i]), font=('Arial', 30),
    #                       fg='white', bg='black', image=background_image, compound='center')
    another_label2 = Label(mini_window, text=get_operating_time(map_stalls_list[counter]), font=('Arial', 30),
                           fg='white', bg='black', compound='center')
    # another_label2.image = background_image
    # another_label2.pack(side='left', fill='y')
    another_label2.grid(row=0, column=0, sticky='nsew')
    another_background_image = PhotoImage(file='image\\Menu Background.png')
    another_label3 = Label(mini_window, font=('Arial', 30), bg='black', fg='white')
    another_label3.configure(text=get_menu(map_stalls_list[counter], user_day=user_day, user_time=user_time),
                             image=another_background_image, compound='center')
    another_label3.image = another_background_image
    # waiting time
    frames = [PhotoImage(file='image\\hour_glass\\frame(' + str(i+1) + ').png') for i in range(96)]
    waiting_time_button = Button(another_label2, compound='bottom', text="waiting time",
                                 bg="black", fg="cyan",
                                 font=('Arial', 15),
                                 command=waiting_time, borderwidth=0)

    def update(ind):
        frame = frames[ind]
        ind += 1
        if ind > 95:
            ind = 0
        waiting_time_button.configure(image=frame)
        waiting_time_button.image = frame
        mini_window.after(50, update, ind)


    waiting_time_image = PhotoImage(file='image\\hourglass.gif')
    waiting_time_button = Button(another_label2, image=waiting_time_image, compound='bottom', text="waiting time",
                                 bg="black", fg="cyan",
                                 font=('Arial', 15),
                                 command=waiting_time, borderwidth=0)
    waiting_time_button.image = waiting_time_image
    waiting_time_button.place(relx=0.5, rely=0.15, anchor='center')
    mini_window.after(0, update, 0)


    back_button_image = PhotoImage(file="image\\back button.png")
    # back_button = Button(mini_window,command=lambda root=GUI, me=mini_window: back(GUI, mini_window),image = back_button_image)
    back_button = Button(another_label3, command=lambda root=GUI, me=mini_window: back(GUI, mini_window),
                         image=back_button_image)
    back_button.image = back_button_image
    # back_button.place(relx=0.6785, rely=0.7480)
    back_button.place(relx=0.5, rely=0.7480, anchor='center')
    another_label3.grid(row=0, column=1, sticky='nsew')
    # another_label3.pack(side='right', fill='y')
    centre_window(mini_window)


def waiting_time():
    while True:
        people_int = simpledialog.askinteger(title=title, prompt="Enter Number of People in Queue", minvalue=0)
        if people_int is not None:
            messagebox.showinfo(title=title, message="Waiting time is about " + str(people_int * 4) + " minutes.")
        break


def centre_window(asd, height=0):
    asd.withdraw()
    asd.update_idletasks()  # Update "requested size" from geometry manager
    x = (asd.winfo_screenwidth() - asd.winfo_reqwidth()) / 2
    y = (asd.winfo_screenheight() - asd.winfo_reqheight() - height) / 2
    asd.geometry("+%d+%d" % (x, y))
    # This seems to draw the GUI frame immediately, so only call deiconify()
    # after setting correct GUI position
    asd.deiconify()
