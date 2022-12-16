import heapq as hq
import io
from tkinter import *
import time
# from psutil import process_partitions,process_usage,virtual_memory,cpu_percent
import psutil
import random
from tabulate import tabulate
import threading
import os
import signal


import ctypes
libgcc_s = ctypes.CDLL('libgcc_s.so.1')
window = Tk()
window.geometry("900x600")
window.configure(bg='#5CDB95')
window.title("CPU RAM Process USAGE")


def conversor_bytes_to_gb(byte):
    one_gigabyte = 1073741824  # Bytes
    giga = byte/one_gigabyte
    giga = "{0:.1f}" .format(giga)
    return giga


def show_ram_info():
    ram_usage = psutil.virtual_memory()
    ram_usage = dict(ram_usage._asdict())
    # print(ram_usage)
    for key in ram_usage:
        if key != 'percent':
            ram_usage[key] = conversor_bytes_to_gb(ram_usage[key])

    #print ('{}-GB-/-() GB({}%)'.format(ram_usage["used"],ram_usage["total"],ram_usage["percent"]))
    ram_label.config(
        text='{}GB/ {} GB({:.2f}%)' .format(ram_usage["used"], ram_usage["total"], ((float(ram_usage["used"])*100/float(ram_usage["total"])))))
    ram_label.after(200, show_ram_info)


def show_cpu_info():
    cpu_use = psutil.cpu_percent(interval=1)
    # print('{} %'.format(cpu_use))
    cpu_label.config(text='{} %'.format(cpu_use))
    cpu_label.after(200, show_cpu_info)


def show_battery_percent():
    battery = psutil.sensors_battery().percent
    battery_label.config(text='{:.2f} %'.format(battery))
    battery_label.after(1000, show_battery_percent)


# Title program
# battery percent
battery_title_label = Label(window, text='Battery: ', relief='solid',
                            font="arial 24 bold", fg='#EDF5E1', bg='#5CDB95')
battery_title_label.place(x=1240, y=155)
battery_label = Label(window, fg="#EDF5E1", font="Arial 20 bold",
                      width=20, bg='#5CDB95', relief='solid')
battery_label.place(x=1450, y=155)

title_program = Label(window, text='PC TASK Manager',
                      font="arial 30 bold", fg='#EDF5E1', bg='#5CDB95', relief='solid')
title_program.place(x=750, y=20)
# cpu title
cpu_title_label = Label(window, text='CPU Usage: ', relief='solid',
                        font="arial 24 bold", fg='#EDF5E1', bg='#5CDB95')
cpu_title_label.place(x=20, y=155)
# label to show percent of cpu
cpu_label = Label(window, fg="#EDF5E1", font="Arial 20 bold", relief='solid',
                  width=20, bg='#5CDB95')
cpu_label.place(x=230, y=155)
# ram title
ram_title_label = Label(window, text='RAM Usage: ', relief='solid',
                        font="arial 24 bold", fg="#EDF5E1", bg='#5CDB95')
ram_title_label.place(x=20, y=255)
# Label to show percent of RAM
ram_label = Label(window, fg="#EDF5E1", font="Arial 20 bold", relief='solid',
                  width=20, bg='#5CDB95')
ram_label.place(x=230, y=255)
# process title
process_title_label = Label(window, text='Process Usage: ', relief='solid',
                            font="arial 24 bold", fg='#EDF5E1', bg='#5CDB95')
process_title_label.place(x=550, y=360)
# Text area for process information
textArea = Label(window, bg="#05386B", fg="#EDF5E1", width=106, relief='solid',
                 height=23, padx=10, font=("consolas", 14))
textArea.place(x=15, y=410)
textAreabuttons = Label(window, bg="#05386B", fg="#EDF5E1", width=15,
                        height=23, padx=10, font=("consolas", 14))
textAreabuttons.place(x=1195, y=410)
textArea_blocklist = Label(window, bg="#05386B", fg="#EDF5E1", width=30,
                           height=23, padx=10, font=("consolas", 14))
textArea_blocklist.place(x=1550, y=410)
blocklist_title_label = Label(
    window, text='BlockList', font="arial 24 bold", fg='#EDF5E1', bg='#05386B')
blocklist_title_label.place(x=1650, y=410)

# label to show percent of cpu

# get the pids from last which mostly are user processes


def process_info(p, memory_info, i):
    process_info = {}

    process_info['Sl.No'] = i
    process_info['pid'] = str(p.pid)
    process_info['Name'] = p.name()
    process_info['Status'] = p.status()
    process_info['Num Threads'] = p.num_threads()
    process_info['CPU'] = f'{p.cpu_percent() / psutil.cpu_count():.2f}' + "%"
    process_info['Random'] = random.randint(0, 10)
    # process_info['CPU'] = f'{cpu_percent:.2f}' + "%"
    process_info['Memory(MB)'] = f'{p.memory_info().rss / 1e6:.3f}'

    # except FileNotFoundError:
    #     pass
    return process_info


def refresh_click():

    extracting_process_info(-1)


def end_task(m):

    extracting_process_info(m)


def add_to_blocklist(m):

    extracting_process_info(m+10)


blocklist = []
testingg = Label(window, bg="#05386B", fg="#EDF5E1", width=1,
                 height=1, padx=10, font=("consolas", 14))
testingg.place(x=1550, y=410)


def blocklist_block():

    for pid in psutil.pids()[-200:]:
        try:
            p = psutil.Process(pid)
            if (p.name() in blocklist):
                p.kill()
                break
        except psutil.NoSuchProcess:
            pass
    testingg.config(text="_")
    testingg.after(200, blocklist_block)
# def open_app(name):
#     os.open('/usr/bin/google-chrome-stable',os.O_RDWR)
# app_open_btn = Button(window, text='appopen', bd='1',bg='#EDF5E1',
#                      height=1, width=5, highlightthickness=0, command=lambda:open_app('chrome'))
# app_open_btn.place(x=130, y=450)


def extracting_process_info(m):
    proc = []
    for pid in psutil.pids()[-200:]:
        try:
            p = psutil.Process(pid)
            if (p.name() in blocklist):
                pass
            else:
                p.cpu_percent()
                proc.append(p)

        except psutil.NoSuchProcess:
            pass

        # sort by cpu_percent
    top = {}
    # time.sleep(1)
    for p in proc:
        # trigger cpu_percent() the second time for measurement
        # top[p] = p.cpu_percent() / psutil.cpu_count
        try:
            top[p] = p.memory_info().rss / 1e6
        except psutil.NoSuchProcess:
            pass
    top_list = sorted(top.items(), key=lambda x: x[1])
    # top_list=list(top.items())
    top10 = top_list[-10:]
    top10.reverse()
    return_all = []
    i = 0
    for p, memory_info in top10:
        try:

            return_all.append(process_info(p, memory_info, i))
            i = i+1
        except Exception as e:
            pass
    info = return_all
    _list = [i.values() for i in info]
    infoTabulated = tabulate(
        _list, headers=info[0].keys(), tablefmt="grid", missingval="-")
    textArea.config(text=infoTabulated)
    if (m != -1 and m <= 9):
        for i in info:
            values = list(i.values())
            if (m == values[0]):

                p1 = psutil.Process(int(values[1]))
                p1.kill()
                print(values[2])

    elif (m != -1 and m > 9):
        for i in info:
            values = list(i.values())
            if (m-10 == values[0]):

                p1 = psutil.Process(int(values[1]))
                p1.kill()
                blocklist.append(values[2])
                print(values[2])
    m = -1
    abc = ''
    for elements in blocklist:
        abc += elements
        abc += '\n'
    textArea_blocklist.config(text=abc)
    textArea.after(2000, lambda: extracting_process_info(-1))


# def loop():
#     while(0==0):
#         time.sleep(1)
#         extracting_process_info(-1)
def clear_blocklist():
    blocklist.clear()
    refresh_click()


refresh_btn = Button(window, text='Refresh', bd='1', bg='#EDF5E1',
                     height=1, width=5, highlightthickness=0, command=refresh_click)
refresh_btn.place(x=850, y=360)

clear_blocklist_btn = Button(window, text='Clear', bd='1', bg='#EDF5E1',
                             height=1, width=5, highlightthickness=0, command=clear_blocklist)
clear_blocklist_btn.place(x=1830, y=450)
# i = 0
# for p, cpu_percent in top10:
#     process_info(p, i)
#     i = i+1
# def end_process(i):


def creating_buttons():
    btn = Button(window, text='End Task', bd='1', bg='#EDF5E1', activebackground='#EDF5E1',
                 height=1, width=5, highlightthickness=0, command=lambda: end_task(0))
    btn.place(x=1205, y=480)
    btn = Button(window, text='End Task', bd='1', bg='#EDF5E1', activebackground='#EDF5E1',
                 height=1, width=5, highlightthickness=0, command=lambda: end_task(1))
    btn.place(x=1205, y=480+46)
    btn = Button(window, text='End Task', bd='1', bg='#EDF5E1', activebackground='#EDF5E1',
                 height=1, width=5, highlightthickness=0, command=lambda: end_task(2))
    btn.place(x=1205, y=480+92)
    btn = Button(window, text='End Task', bd='1', bg='#EDF5E1', activebackground='#EDF5E1',
                 height=1, width=5, highlightthickness=0, command=lambda: end_task(3))
    btn.place(x=1205, y=480+138)
    btn = Button(window, text='End Task', bd='1', bg='#EDF5E1', activebackground='#EDF5E1',
                 height=1, width=5, highlightthickness=0, command=lambda: end_task(4))
    btn.place(x=1205, y=480+184)
    btn = Button(window, text='End Task', bd='1', bg='#EDF5E1', activebackground='#EDF5E1',
                 height=1, width=5, highlightthickness=0, command=lambda: end_task(5))
    btn.place(x=1205, y=480+46*5)
    btn = Button(window, text='End Task', bd='1', bg='#EDF5E1', activebackground='#EDF5E1',
                 height=1, width=5, highlightthickness=0, command=lambda: end_task(6))
    btn.place(x=1205, y=480+46*6)
    btn = Button(window, text='End Task', bd='1', bg='#EDF5E1', activebackground='#EDF5E1',
                 height=1, width=5, highlightthickness=0, command=lambda: end_task(7))
    btn.place(x=1205, y=480+46*7)
    btn = Button(window, text='End Task', bd='1', bg='#EDF5E1', activebackground='#EDF5E1',
                 height=1, width=5, highlightthickness=0, command=lambda: end_task(8))
    btn.place(x=1205, y=480+46*8)
    btn = Button(window, text='End Task', bd='1', bg='#EDF5E1', activebackground='#EDF5E1',
                 height=1, width=5, highlightthickness=0, command=lambda: end_task(9))
    btn.place(x=1205, y=480+46*9)


def creating_buttons_blockist():
    btn = Button(window, text='Add to blocklist', bd='1', bg='#EDF5E1', activebackground='#EDF5E1',
                 height=1, width=9, highlightthickness=0, command=lambda: add_to_blocklist(0))
    btn.place(x=1275, y=480)
    btn = Button(window, text='Add to blocklist', bd='1', bg='#EDF5E1', activebackground='#EDF5E1',
                 height=1, width=9, highlightthickness=0, command=lambda: add_to_blocklist(1))
    btn.place(x=1275, y=480+46)
    btn = Button(window, text='Add to blocklist', bd='1', bg='#EDF5E1', activebackground='#EDF5E1',
                 height=1, width=9, highlightthickness=0, command=lambda: add_to_blocklist(2))
    btn.place(x=1275, y=480+92)
    btn = Button(window, text='Add to blocklist', bd='1', bg='#EDF5E1', activebackground='#EDF5E1',
                 height=1, width=9, highlightthickness=0, command=lambda: add_to_blocklist(3))
    btn.place(x=1275, y=480+138)
    btn = Button(window, text='Add to blocklist', bd='1', bg='#EDF5E1', activebackground='#EDF5E1',
                 height=1, width=9, highlightthickness=0, command=lambda: add_to_blocklist(4))
    btn.place(x=1275, y=480+184)
    btn = Button(window, text='Add to blocklist', bd='1', bg='#EDF5E1', activebackground='#EDF5E1',
                 height=1, width=9, highlightthickness=0, command=lambda: add_to_blocklist(5))
    btn.place(x=1275, y=480+46*5)
    btn = Button(window, text='Add to blocklist', bd='1', bg='#EDF5E1', activebackground='#EDF5E1',
                 height=1, width=9, highlightthickness=0, command=lambda: add_to_blocklist(6))
    btn.place(x=1275, y=480+46*6)
    btn = Button(window, text='Add to blocklist', bd='1', bg='#EDF5E1', activebackground='#EDF5E1',
                 height=1, width=9, highlightthickness=0, command=lambda: add_to_blocklist(7))
    btn.place(x=1275, y=480+46*7)
    btn = Button(window, text='Add to blocklist', bd='1', bg='#EDF5E1', activebackground='#EDF5E1',
                 height=1, width=9, highlightthickness=0, command=lambda: add_to_blocklist(8))
    btn.place(x=1275, y=480+46*8)
    btn = Button(window, text='Add to blocklist', bd='1', bg='#EDF5E1', activebackground='#EDF5E1',
                 height=1, width=9, highlightthickness=0, command=lambda: add_to_blocklist(9))
    btn.place(x=1275, y=480+46*9)


if __name__ == '__main__':
    show_cpu_info()
    show_ram_info()
    show_battery_percent()
    # info = extracting_process_info()
    # _list = [i.values() for i in info]
    # infoTabulated = tabulate(
    #     _list, headers=info[0].keys(), tablefmt="grid", missingval="-")
    # textArea.insert(END, infoTabulated)
    # textArea.after(200, show_cpu_info)
    extracting_process_info(-1)
    creating_buttons()
    creating_buttons_blockist()
    blocklist_block()
    window.mainloop()
