import tkinter as tk
import tkinter.ttk as ttk
import os
import datetime as dt
import csv

def return_current_time():
    now = dt.datetime.now()
    current_time.config(text = now.strftime('%I:%M:%S %p'))
    current_time.after(1000, return_current_time)

def begin_task():
    global start_time
    start['state'] = 'disabled'
    stop['state'] = 'active'
    pause['state'] = 'active'
    start_time = dt.datetime.now()
    task_category_combobox['state'] = 'disabled'
    task_description_entry['state'] = 'disabled'
    name_entry['state'] = 'disabled'
    current_time.config(fg = 'green')


def end_task():
    global start_time
    global total_time_paused
    global csv_path
    stop['state'] = 'disabled'
    start['state'] = 'active'
    current_time.config(fg = 'red')
    stop_time = dt.datetime.now()
    stop_time = stop_time.replace(microsecond=0)
    start_time = start_time.replace(microsecond=0)
    print(start_time, stop_time)
    today = dt.datetime.today()
    time_taken = (stop_time - start_time) - total_time_paused
    start_time = dt.datetime.now()
    List = [name_entry.get(), today.strftime('%m/%d/%Y'), task_description_entry.get(), task_category_combobox.get(), str(time_taken)]
    total_time_paused = dt.timedelta(seconds=0)

    task_category_combobox['state'] = 'readonly'
    task_description_entry['state'] = 'normal'
    pause['state'] = 'disabled'
    name_entry['state'] = 'normal'


    with open(csv_path, 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(List)
        csvfile.close()

def pause_task():
    global total_time_paused
    global is_paused
    global start_pause_time

    if (is_paused):
        end_pause_time = dt.datetime.now()
        end_pause_time = end_pause_time.replace(microsecond=0)
        total_time_paused += end_pause_time - start_pause_time
        print(str(total_time_paused))
        pause.config(text='Pause Task', bg='blue')
        current_time.config(fg = 'green')
        is_paused = False

    elif not(is_paused):
        start_pause_time = dt.datetime.now()
        start_pause_time = start_pause_time.replace(microsecond=0)
        pause.config(text='Resume Task', bg='yellow')
        current_time.config(fg = 'yellow')
        is_paused = True

def Find_File_Path():
    global csv_path
    if(os.path.exists('/Volumes/Watts Atelier’s Public Folder/TaskInfo/tasks.csv')):
        csv_path = '/Volumes/Watts Atelier’s Public Folder/TaskInfo/tasks.csv'
    elif(os.path.exists('/Users/wattsatelier/Public/TaskInfo/tasks.csv')):
        csv_path ='/Users/wattsatelier/Public/TaskInfo/tasks.csv'
    else:
        print("Couldn't find the tasks file.")
        window.config(bg='red')




#Global Variables
start_time = dt.datetime.now()
start_pause_time = dt.datetime.now()
total_time_paused = dt.timedelta(seconds=0)
is_paused = False
csv_path = ''

window = tk.Tk()

window.title("Time Tracker")

timer_frame = tk.Frame(window, relief=tk.RAISED, borderwidth=1)
timer_frame.grid(row=1, column=1, pady=5, sticky='ew')
inputs_frame = tk.Frame(window)
inputs_frame.grid(row=2, column=1,padx=10, pady=5, sticky='w')

window.columnconfigure(1, weight=1, minsize=75)
inputs_frame.columnconfigure(0, weight=1)
inputs_frame.columnconfigure(1, weight=1)

window.minsize(width=250, height=70)
current_time_label = tk.Label(timer_frame, text='Current Time:', fg='white', font=('calibri', 20, 'bold'))
current_time_label.grid(row=0, column=1, sticky='w')

current_time = tk.Label(timer_frame, text='', fg="red", font=('calibri', 40, 'bold'))
current_time.grid(row=1, column=1, pady=5, sticky = 'w')

task_description = tk.Label(inputs_frame, text='Task Description:', fg='white')
task_description.grid(row=1, column=0)
task_description_entry = tk.Entry(inputs_frame)
task_description_entry.grid(row=1, column=1,sticky='we')
task_category = tk.Label(inputs_frame, text='Task Category:', fg='white')
task_category.grid(row=2, column=0, sticky='w')
task_category_combobox = ttk.Combobox(inputs_frame,
                                      values=[
                                        'Emails',
                                        'Meetings',
                                        'Editing',
                                        'Social Media',
                                        'Research',
                                        'Admin',
                                        'Writing',
                                        'Programming'
                                      ],
                                      state='readonly')
task_category_combobox.grid(row=2, column=1)

name_label = tk.Label(inputs_frame, text='Name:')
name_label.grid(row=0, column=0, sticky='e')
name_entry = tk.Entry(inputs_frame)
name_entry.grid(row=0, column=1, sticky='w')

start = tk.Button(inputs_frame, text='Start Task', width=6, command=begin_task)
stop = tk.Button(inputs_frame, text='End task', width=6, command=end_task)
pause = tk.Button(inputs_frame, text = 'Pause Task', width=6, command=pause_task)
start.grid(row=3, column=0, sticky='w')
pause.grid(row=4, column=0, sticky='w')
stop.grid(row=5, column=0, sticky='w')
return_current_time()
Find_File_Path()
stop['state'] = 'disabled'
pause['state'] = 'disabled'
window.mainloop()