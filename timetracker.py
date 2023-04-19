import tkinter as tk
import tkinter.ttk as ttk
import os
import datetime as dt
import csv

class TimeManager():

    task_start_time = dt.time(0,0,0,0)
    task_end_time = dt.time(0,0,0,0)

    start_pause_time = dt.time(0,0,0,0)
    end_pause_time = dt.time(0,0,0,0)
    total_time_paused = dt.time(0,0,0,0)
    is_paused = False

    csv_path = ''


    def __init__(self, ClockLabel, NameEntry, TaskDescEntry, TaskCategoryBox, StartButton, PauseButton, StopButton, Window):
        #Widgets
        self.ClockLabel = ClockLabel
        self.NameEntry = NameEntry
        self.TaskDescEntry = TaskDescEntry
        self.TaskCategoryBox = TaskCategoryBox
        self.StartButton = StartButton
        self.PauseButton = PauseButton
        self.StopButton = StopButton
        self.Window = Window

        self.return_current_time()
        self.Find_File_Path()

        self.StopButton['state'] = 'disabled'
        self.PauseButton['state'] = 'disabled'



    def return_current_time(self):
        now = dt.datetime.now()
        self.ClockLabel.config(text = now.strftime('%I:%M:%S %p'))
        self.ClockLabel.after(1000, self.return_current_time)

    def begin_task(self):

        #configure widgets for state (started task)
        self.StartButton['state'] = 'disabled'
        self.StopButton['state'] = 'active'
        self.PauseButton['state'] = 'active'
        self.TaskCategoryBox['state'] = 'disabled'
        self.TaskDescEntry['state'] = 'disabled'
        name_entry['state'] = 'disabled'
        current_time.config(fg = 'green')

        #sets the start time to when the user clicked the start task button
        self.task_start_time = dt.datetime.now()


    def end_task(self):

        #configure widgets for state (ended task) TODO: Split state configurations into their own method
        self.StopButton['state'] = 'disabled'
        self.StartButton['state'] = 'active'
        self.ClockLabel.config(fg = 'red')
        self.TaskCategoryBox['state'] = 'readonly'
        self.TaskDescEntry['state'] = 'normal'
        self.PauseButton['state'] = 'disabled'
        self.NameEntry['state'] = 'normal'

        self.task_end_time = dt.datetime.now()
        today = dt.datetime.today()
        
        self.task_end_time = self.task_end_time.replace(microsecond=0)
        self.task_start_time = self.task_start_time.replace(microsecond=0)
        time_taken = (self.task_end_time - self.task_start_time) - self.total_time_paused
        self.total_time_paused = dt.timedelta(seconds=0)

        List = [self.NameEntry.get(), today.strftime('%m/%d/%Y'), self.TaskDescEntry.get(), self.TaskCategoryBox.get(), str(time_taken)]

        #TODO: make writing to the CSV file it's own method.
        with open(csv_path, 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(List)
            csvfile.close()

    def pause_task(self):

        if (self.is_paused):
            self.PauseButton.config(text='Pause Task', bg='blue')
            self.ClockLabel.config(fg = 'green')
        
            self.end_pause_time = dt.datetime.now()
            self.end_pause_time = self.end_pause_time.replace(microsecond=0)
            self.total_time_paused += self.end_pause_time - self.start_pause_time

            is_paused = False

        elif not(is_paused):
            pause.config(text='Resume Task', bg='yellow')
            current_time.config(fg = 'yellow')

            self.start_pause_time = dt.datetime.now()
            self.start_pause_time = start_pause_time.replace(microsecond=0)

            is_paused = True

    def Find_File_Path(self):
        if(os.path.exists('/Volumes/Watts Atelier’s Public Folder/TaskInfo/tasks.csv')):
            self.csv_path = '/Volumes/Watts Atelier’s Public Folder/TaskInfo/tasks.csv'
        elif(os.path.exists('/Users/wattsatelier/Public/TaskInfo/tasks.csv')):
            self.csv_path ='/Users/wattsatelier/Public/TaskInfo/tasks.csv'
        elif(os.path.exists('./taskstesting.csv')):
            self.csv_path = './taskstesting.csv'
        else:
            print("Couldn't find the tasks file.")
            self.Window.config(bg='red')



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

start = tk.Button(inputs_frame, text='Start Task', width=6)
stop = tk.Button(inputs_frame, text='End task', width=6)
pause = tk.Button(inputs_frame, text = 'Pause Task', width=6)
start.grid(row=3, column=0, sticky='w')
pause.grid(row=4, column=0, sticky='w')
stop.grid(row=5, column=0, sticky='w')

my_time_manager = TimeManager(
    current_time, 
    name_entry,
    task_description_entry, 
    task_category_combobox, 
    start, 
    pause, 
    stop, 
    window
    )

start.bind(my_time_manager.begin_task())
stop.bind(my_time_manager.end_task())
pause.bind(my_time_manager.pause_task())

window.mainloop()