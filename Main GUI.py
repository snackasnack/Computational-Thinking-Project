"""GUI

All the GUI related items are here.
"""

# Import required modules
from tkcalendar import Calendar

from day_time import get_current_date, get_current_time, get_current_time_in_seconds, get_day, get_current_day
from menu import get_number_of_stalls, get_stalls
from operating_times import check_stall_opened
from tkinter import Canvas, Label, PhotoImage, Tk, Toplevel, StringVar, OptionMenu, Button
from window_2 import specific_time, input_time_la
from winsound import PlaySound, SND_ASYNC, SND_FILENAME


def centre_window(window):
    """Centres main window given 'window' Tk

    Function centre_window(window) centres the given 'window' Tk by taking into account main window geometry and
    screen geometry. winfo_screenwidth(), winfo_screenheight(), winfo_width(), winfo_height() are used. The main
    window is hidden using withdraw() then displayed again using deiconify().
    """

    window.withdraw()
    window.update_idletasks()
    x = (window.winfo_screenwidth() - max(window.winfo_width(), window.winfo_reqwidth())) / 2
    y = (window.winfo_screenheight() - max(window.winfo_height(), window.winfo_reqheight())) / 2
    window.geometry('+%d+%d' % (x, y))
    window.deiconify()


def click(event, window, item_id):
    """Hides first window, shows 2nd window on click, given which label is clicked, given 'window' Tk and 'item_id' int.

    Function click(event, window, item_id) takes in 'window' Tk and 'item_id' int, hides the first window and shows
    the 2nd window.
    """

    specific_time(counter=item_id, GUI=window)
    window.withdraw()


class MainWindow:
    """MainWindow Class

    MainWindow Class contains all GUI.
    """

    # Initialise required variables

    user_time = get_current_time()
    title = 'NTU'
    geometry = '1024x660'
    image_str = 'image\\'
    image_format = '.png'
    font = 'MSGothic 25 bold'
    anchor = 'center'
    frame = 'frame'
    colour = '#000000'
    grey = ' (Grey)'
    frame_position_list = ((0.562, 0.357), (0.715, 0.645), (0.702, 0.148), (0.561, 0.551), (0.7095, 0.3705))
    map_canvas = None
    background_canvas = None
    poster_canvas = None
    user_day = get_current_day()
    user_time = get_current_time()

    stall_label_list = []
    pin_label_list = []
    pin_image_list = []

    def __init__(self, window):
        """Initialise main window given 'window' Tk.

        Function __init__(self, window) takes in 'window' Tk and initialises the main window and calls
        create_elements().
        """
        self.background_canvas = Canvas(window, highlightthickness=0, borderwidth=0)
        self.map_canvas = Canvas(window, highlightthickness=100, borderwidth=100)
        self.poster_canvas = Canvas(window, highlightthickness=0, borderwidth=0)
        self.create_elements(window=window)
        # Main GUI
        window.configure(highlightthickness=0, borderwidth=0)
        window.title(self.title)
        # window.resizable(0, 0)
        window.geometry(newGeometry=self.geometry)
        centre_window(window)
        window.mainloop()

    def input_specific_time(self, window):
        def print_sel():
            self.user_time = hour_variable.get() + ':' + minute_variable.get()
            self.user_day = get_day(calendar.selection_get())
            # print(type(calendar.selection_get()))
            print(self.user_time + '\n' + self.user_day)
            input_time_la(day=self.user_day, time=self.user_time)
            top.destroy()

        def reset():
            self.user_time = get_current_time()
            self.user_day = get_current_day()
            input_time_la(day=self.user_day, time=self.user_time)
            top.destroy()

        # Calendar
        top = Toplevel()
        calendar = Calendar(top, font='Arial 14', selectmode='day', locale='en_SG', cursor='hand1')
        calendar.pack(fill='both', expand=True)
        # Hours
        top_canvas = Canvas(top)
        hours_list = ['{:02d}'.format(i) for i in range(24)]
        hour_variable = StringVar(top_canvas)
        hour_variable.set('00')
        hour_option = OptionMenu(top_canvas, hour_variable, *hours_list)
        hour_option.config(font=('Arial', 20))
        hour_option.grid(row=0, column=0)
        # Colon
        colon_label = Label(top_canvas, text=':', font=('Arial', 20))
        colon_label.grid(row=0, column=1)
        # Minutes
        minutes_list = ['{:02d}'.format(i) for i in range(60)]
        minute_variable = StringVar(top_canvas)
        minute_variable.set('00')
        minute_option = OptionMenu(top_canvas, minute_variable, *minutes_list)
        minute_option.config(font=('Arial', 20))
        minute_option.grid(row=0, column=2)
        top_canvas.pack()
        # OK Button
        ok_button = Button(top, text='OK', command=print_sel)
        ok_button.pack(fill='both')
        # Reset Button
        reset_button = Button(top, text='Reset', command=reset)
        reset_button.pack(fill='both')
        centre_window(window=top)

    def create_elements(self, window):
        """Create all the elements in the GUI given 'window' Tk.

        Function create_elements(self, window) takes in 'window' Tk creates and configures background_canvas,
        map_canvas, map_label, ntu_logo, clock(calling update_time_label(clock_id)) and calls create_hover_labels().
        """
        self.stall_label_list = [Label(window, highlightthickness=5, borderwidth=5, background='cyan') for i in
                                 get_stalls()]

        # Background
        background_image = PhotoImage(file=self.image_str + 'The Hive - Copy' + self.image_format)
        self.background_canvas.create_image(800, 650, image=background_image, anchor=self.anchor)
        window.image = background_image
        self.background_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        # NTU Map
        self.map_canvas.place(relx=0.68, rely=0.57, anchor=self.anchor)
        map_image = PhotoImage(file=self.image_str + 'NTU Map' + self.image_format)
        map_label = Label(self.map_canvas, image=map_image, highlightthickness=0, borderwidth=0)
        map_label.image = map_image
        map_label.pack()
        # Poster on the left
        self.poster_canvas.place(relx=0.20, rely=0.57, anchor=self.anchor)
        poster_image = PhotoImage(file=self.image_str + 'Poster' + self.image_format)
        poster_label = Label(self.poster_canvas, image=poster_image, highlightthickness=0, borderwidth=0)
        poster_label.image = poster_image
        poster_label.pack()
        # NTU Logo
        ntu_logo = PhotoImage(file=self.image_str + 'NTU Logo' + self.image_format)
        self.background_canvas.create_image((130, 50), image=ntu_logo)
        self.background_canvas.image = ntu_logo
        # Clock
        clock_id = self.background_canvas.create_text((554, 50), font=self.font, anchor=self.anchor,
                                                      justify=self.anchor, fill=self.colour)
        window.bind('<Configure>', lambda event, item_id=clock_id: self.move(event, window=window, item_id=item_id))
        self.update_time_label(clock_id=clock_id)
        # Hover Labels
        self.create_hover_labels(window=window)
        # REAL BUTTON
        clock_image = PhotoImage(file=self.image_str + 'Clock' + self.image_format)
        time_button = Button(self.poster_canvas, image=clock_image, font='30', width=373 / 2, height=543 / 3,
                             command=lambda root=window: self.input_specific_time(window=root))
        time_button.image = clock_image
        time_button.place(relx=0.25, rely=0.51, anchor=self.anchor)

    def create_hover_labels(self, window):
        """Creates all hover labels and its images and bind them to the label, given 'window' Tk.

        Function create_hover_labels(self, window) takes in 'window' Tk and creates and configures pin_label_list
        labels and pin_image_list images.
        """
        for i in range(get_number_of_stalls()):
            # Pin Images
            self.pin_image_list.append(PhotoImage(file=self.image_str + self.frame + str(i + 1) + self.image_format))
            # Pin Labels
            self.pin_label_list.append(
                Label(self.map_canvas, image=self.pin_image_list[i], highlightthickness=0, borderwidth=0))
            self.pin_label_list[i].place(relx=self.frame_position_list[i][0], rely=self.frame_position_list[i][1],
                                         anchor=self.anchor)
            self.pin_label_list[i].bind('<Button-1>', lambda event, root=window, item_id=i: click(event, window=root,
                                                                                                  item_id=item_id))
            self.pin_label_list[i].bind('<Enter>', lambda event, root=window, item_id=i: self.hover(event, window=root,
                                                                                                    item_id=item_id))
            self.pin_label_list[i].bind('<Leave>', self.leave)

    def hover(self, event, window, item_id):
        """When hovered, shows image of the stall (Grey if closed, Coloured if opened), given 'window' Tk and
        'item_id' int.

        Function hover(self, event, window, item_id) takes in 'window' Tk, 'item_id' int and gets the image of the
        stall and displays it. winfo_width(), winfo_reqwidth(), winfo_height(), winfo_reqheight() are used to
        configure the position of the label. Grey image is shown if stall is closed, coloured image otherwise.
        """
        # Checks if stall is opened or closed and uses images accordingly
        if check_stall_opened(stall=get_stalls()[item_id], user_day=self.user_day, user_time=self.user_time):
            label_image = PhotoImage(file=self.image_str + get_stalls()[item_id] + self.image_format)
        else:
            label_image = PhotoImage(file=self.image_str + get_stalls()[item_id] + self.grey + self.image_format)
        # Stall Label
        self.stall_label_list[item_id].configure(image=label_image)
        self.stall_label_list[item_id].image = label_image
        '''self.stall_label_list[item_id].place(
            x=self.pin_label_list[item_id].winfo_x() + (window.winfo_width() - self.map_canvas.winfo_width()
                                                        - (self.stall_label_list[
                                                               item_id].winfo_reqwidth() -
                                                           self.pin_label_list[
                                                               item_id].winfo_width())) / 2,
            y=self.pin_label_list[item_id].winfo_y() + (window.winfo_height() - self.map_canvas.winfo_height()) / 2
              + self.pin_label_list[item_id].winfo_height())'''
        x=self.pin_label_list[item_id].winfo_x() * 0.85 + (window.winfo_width() - self.map_canvas.winfo_width() - (self.stall_label_list[item_id].winfo_reqwidth() - self.pin_label_list[item_id].winfo_width())) * 0.68,
        y=self.pin_label_list[item_id].winfo_y() + (window.winfo_height() - self.map_canvas.winfo_height()) * 0.57
        self.stall_label_list[item_id].place(x=x, y=y)
        # 0.68, 0.57

    def leave(self, event):
        """When mouse leaves label, remove the image.

        Function leave(self, event) removes the image when the mouse leaves label.
        """
        for j in range(get_number_of_stalls()):
            self.stall_label_list[j].image = None
            self.stall_label_list[j].place_forget()

    def move(self, event, window, item_id):
        """When the windows resize, item of int 'item_id' is moved accordingly given 'window' Tk.

        Function move(self, event, window, item_id) positions the clock to the top right corner, given 'window' Tk
        and int 'item_id' of the clock when window resize.
        """
        self.background_canvas.coords(item_id, window.winfo_width() - 100, 50)

    def update_time_label(self, clock_id):
        """Updates time accordingly, given 'clock_id' int.

        Function update_time_label(self, clock_id) positions the clock to the top right corner, given int 'clock_id'
        of the clock.
        """
        self.background_canvas.itemconfig(tagOrId=clock_id,
                                          text=get_current_date() + '\n' + get_current_time_in_seconds())
        self.background_canvas.after(200, lambda item_id=clock_id: self.update_time_label(clock_id=clock_id))


GUI = Tk()
# PlaySound(sound='audio\\Coffee Shop.wav', flags=SND_FILENAME | SND_ASYNC)
main_window = MainWindow(GUI)
GUI.mainloop()
