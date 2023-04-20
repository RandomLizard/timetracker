import pandas as pd
import os
import matplotlib
import datetime as dt


class Report_Generator():

    task_file = None

    def __init__(self):

        self.find_file()

    def find_file(self):
        if os.path.exists('./tasktesting.csv'):
            self.task_file = pd.read_csv('./tasktesting.csv')
        elif os.path.exists('/Users/wattsatelier/Public/TaskInfo/tasks.csv'):
            self.task_file = pd.read_csv('/Users/wattsatelier/Public/TaskInfo/tasks.csv')
        elif os.path.exists('/Volumes/Watts Atelier’s Public Folder/TaskInfo/tasks.csv'):
            self.task_file = pd.read_csv('/Volumes/Watts Atelier’s Public Folder/TaskInfo/tasks.csv')

    