"""Functions relating to 'Menu.json' file are contained here.

Data from 'Menu.json' are taken from the stalls websites and modified.
"""


# Import required modules

from day_time import compare_time, get_current_day, get_current_time, return_day_tuple
from json_reader import read_file
from operating_times import check_stall_opened

# Initialise required variables

all_menu = read_file(file_name='Menu.json')
menus_display_str = 'Menus'
timings = 'Availability'


def get_every_menu(stall):
    """Returns a string with the menu of given string 'stall', nicely formatted.

    Function get_every_menu(stall) takes in 'stall' string. The function then retrieves the stall name, menu, timings,
    item and its price from 'all_menu' dictionary and sort them accordingly to the menus into a string. The string is
    then returned.
    """

    every_menu_str = stall

    for menu in all_menu[stall]:
        if menu != timings:
            every_menu_str += '\n' + menu
            for (item, price) in all_menu[stall][menu].items():
                every_menu_str += '\n' + item + ' ' + price
        else:
            every_menu_str += '\n' + timings
            for time_menu in all_menu[stall][menu]:
                every_menu_str += '\n' + time_menu
                for (day, time) in all_menu[stall][menu][time_menu].items():
                    every_menu_str += '\n' + day + ' ' + time
            every_menu_str += '\n' + menus_display_str
    return every_menu_str


def get_every_menus():
    """Returns a string with menus of all stalls, nicely formatted.

    Function get_every_menus() calls get_every_menu(stall) for every stall in 'all_menu'. The strings from
    get_every_menu(stall) is then combined and returned.
    """

    every_menus_str = menus_display_str

    for stall in all_menu:
        every_menus_str += '\n\n' + get_every_menu(stall=stall)
    return every_menus_str


def get_menu(stall, user_day=None, user_time=None):
    """Returns a string with the menu of given strings 'stall', 'user_day' and 'user_time' (user_day & user_time
    defaults to current day and time), nicely formatted.

    Function get_menu(stall, user_day, user_time) takes in strings 'stall', 'user_day' and 'user_time' (optional,
    uses current day and time otherwise). The function then retrieves the stall name, menu, item and its price
    according to day and time from 'all_menu'. Results are sorted into a string and returned.
    """

    menu_str = stall
    time_based = False

    if user_day is None:
        user_day = get_current_day()
    if user_time is None:
        user_time = get_current_time()

    if check_stall_opened(stall=stall, user_day=user_day, user_time=user_time):
        for branch in all_menu[stall]:
            if branch == timings:
                time_based = True
                for timed_menu in all_menu[stall][branch]:
                    for day in all_menu[stall][branch][timed_menu]:
                        if user_day in return_day_tuple(day_type=day):
                            if compare_time(user_time=user_time, time_range=all_menu[stall][branch][timed_menu][day]):
                                menu_str += '\n' + timed_menu
                                for (item, price) in all_menu[stall][timed_menu].items():
                                    menu_str += '\n' + item + ' ' + price
            elif not time_based:
                menu_str += '\n' + branch
                for (item, price) in all_menu[stall][branch].items():
                    menu_str += '\n' + item + ' ' + price
    else:
        menu_str += '\nSorry! Stall closed!'
    return menu_str


def get_menus():
    """Returns a string with the menu of all stalls given strings 'user_day' and 'user_time' (user_day & user_time
    defaults to current day and time), nicely formatted.

    Function get_menus() calls get_menu(stall, user_day, user_time) for every stall in 'all_menu'. The strings from
    get_menu(stall, user_day, user_time) is then combined and returned.
    """

    menus_str = menus_display_str

    for stall in all_menu:
        menus_str += '\n\n' + get_menu(stall=stall)
    return menus_str


def get_number_of_stalls():
    """Returns number of stalls.

    Function get_number_of_stalls() returns length of 'all_menu'.
    """

    return len(all_menu)


def get_stalls():
    """Returns a list of all stalls.

    Function get_stalls() gets all stalls from 'all_menu'.
    """

    return [stall for stall in all_menu]
