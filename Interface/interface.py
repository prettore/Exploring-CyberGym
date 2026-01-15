#   user chooses simulation type
#   AI vs Rule Based / Rule based vs Rule based / AI vs AI
#   (considering the AI is already trained)
#   user chooses agents
#   RED: Meander agent / Baseline agent
#   BLUE: React Remove / React Restore
#   Number of iterations:
#
from termcolor import colored
import sys
sys.path.append('/home/gabriel/Projects/CybORG-Sims/cage-challenge-2/CybORG/')
from pprint import pprint
tsize = 80

from CybORG import CybORG
from CybORG.Agents.SimpleAgents.B_line import *
from CybORG.Agents.SimpleAgents.Meander import *
from CybORG.Agents.SimpleAgents.BlueReactAgent import *
from CybORG.Agents.SimpleAgents.GreenAgent import *
#from CybORG.Shared.Actions.AbstractActions import Analyse
from CybORG.Simulator.Scenarios import FileReaderScenarioGenerator as fr

class Observations():
    observations = []
    step_number = 0
    current_step = 0

    def __init__(self, steps):
       self.step_number = steps
        
    def feed_obs(self, red_obs, blue_obs):
        obs = (red_obs, blue_obs)
        self.observations.append(obs)

    def get_obs(self, agent):
        if agent == 'red':
            return self.observations[self.current_step][0]
        elif agent == 'blue':
            return self.observations[self.current_step][1]


'''
print('Modos')
print("0 - R vs R")
mode = int(input('Escolha o modo: '))

print('Agentes Vermelhos')
print('0 - Baseline')
print('1 - Meander')
num = int(input('Escolha o Agente V: '))
def select_red_agent():
    if num == 0:
        agent = B_lineAgent()
    elif num == 1:
        agent = RedMeanderAgent()
    return agent

red_agent = select_red_agent()

blue_agent = None
print('Agentes Azuis')
print('0 - React Remove')
print('1 - React Restore')
num = int(input('Escolha o Agente A: '))
def select_blue_agent():
    if num == 0:
        agent = BlueReactRemoveAgent()
    elif num == 1:
        agent = BlueReactRestoreAgent()
    return agent
'''

import tkinter as tk

class Interface():
    def __init__(self):
        self.root = tk.Tk()
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=20)
        self.root.title("My window")

        self.simulator = Simulator()
        self.steps = 0
        
    def clean_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def main_menu(self):
        tk.Label(self.frame, text="Choose simulation mode").pack()
        btn1 = tk.Button(self.frame, text="Rule vs Rule", command=lambda: self.mode1()).pack()
        btn2 = tk.Button(self.frame, text="Rule vs AI", command=lambda: self.mode2()).pack()

    def mode1(self):
        def set_agent(name):
            if name == 'baseline':
                self.agent = B_lineAgent()
            elif name == 'meander':
                self.agent = RedMeanderAgent()
            self.choose_steps(1)

        self.clean_frame()
        self.main_menu()
        tk.Label(self.frame, text="Choose agent").pack()
        tk.Button(self.frame, text="Baseline", command=lambda: set_agent('baseline')).pack()
        tk.Button(self.frame, text="Meander", command=lambda: set_agent('meander')).pack()

    def mode2(self):
        self.clean_frame()
        self.main_menu()
        tk.Label(self.frame, text="WIP").pack()

    def choose_steps(self, prev_mode):
        self.clean_frame()
        self.main_menu()
        if prev_mode == 1:
            self.mode1()
        elif prev_mode == 2:
            self.mode2()

        tk.Label(self.frame, text="Choose step number:").pack()

        entry = tk.Entry(self.frame)
        entry.pack()

        def clicked():
            self.steps = int(entry.get())
            self.observations = Observations(self.steps)
            self.simulator.run(self.agent, self.steps, self.observations)
            self.display_obs()

        tk.Button(self.frame, text="Go", command=clicked).pack()
        
    def display_obs(self):
        self.clean_frame()
        red_obs = self.observations.get_obs('red')

        pprint(red_obs)
        offset = 0
        
        row = 1
        column = 0
        
        def dict_loop(dic, row, column):
            for k, v in dic.items():
                tk.Label(self.frame, text=k).grid(row=row,column=column)
                if type(v) == dict:
                    dict_loop(v, row, column+1)
                elif type(v) == list:
                    list_loop(v, row, column+1) 
                else:
                    tk.Label(self.frame, text=v).grid(row=row,column=column+1)
                row += 1

        def list_loop(l, row, column):
            for v in l:

                if type(v) == dict:
                    dict_loop(v, row, column)
                else:
                    tk.Label(self.frame, text=k).grid(row=row+1,column=column+1)
                    
        dict_loop(red_obs, row, column)

        '''
        for k1, v1 in red_obs.items():
            offset += 1
            tk.Label(self.frame, text=k1).grid(row=offset,column=0)

            if type(v1) == dict:
                for k2, v2 in v1.items():
                    offset += 1
                    tk.Label(self.frame, text=k2).grid(row=offset-1, column=1)
                    if type(v2) == dict:
                        for k3, v3 in v2.items():
                            offset += 1
                            tk.Label(self.frame, text=k3).grid(row=offset, column=2)
                            if type(v3) == dict:
                                for k4, v4 in v3.items():
                                    offset += 1
                                    tk.Label(self.frame, text=k4).grid(row=offset+1, column=3)
                                    if type(v4) == dict:
                                        for k5, v5 in v4.items():
                                            offset += 1
                                            tk.Label(self.frame, text=k5).grid(row=offset+2, column=4)

                                    else:
                                        tk.Label(self.frame, text=v4).grid(row=offset, column=4)

                            else:
                                tk.Label(self.frame, text=v3).grid(row=offset, column=3)
                    else:
                        tk.Label(self.frame, text=v2).grid(row=offset, column=2)
            else:
                tk.Label(self.frame, text=v1).grid(row=offset+1, column=1)
                    
        '''
        def next():
            if self.observations.current_step < self.steps - 1:
                self.observations.current_step += 1
                self.display_obs()
        def previous():
            if self.observations.current_step > 0:
                self.observations.current_step -= 1
                self.display_obs()

        tk.Button(self.frame, text=">", command=next).grid(row=0,column=1)
        tk.Button(self.frame, text="<", command=previous).grid(row=0,column=0)
        
    def mainloop(self):
        self.root.mainloop()


class Simulator():
    def __init__(self):
        path = '../Scenarios/Scenario1b.yaml'
        scenario_gen = fr(path)
        self.env = CybORG(scenario_gen) 
        self.mode = None
        self.blue_agent = BlueReactRemoveAgent()

    def step_red(self, obs, action_space, verbose=True):
        action = self.red_agent.get_action(obs, action_space)
        results = self.env.step(action=action, agent='Red')
        return results

    def step_blue(self, obs, action_space, verbose=True):
        action = self.blue_agent.get_action(obs, action_space)
        results = self.env.step(action=action, agent='Blue')
        return results

    def run(self, agent, steps, obs):

        self.red_agent = agent
        self.steps = steps

        results = self.env.reset(agent='Red')

        red_action_space = results.action_space
        blue_action_space = self.env.get_action_space('Blue')

        red_obs = results.observation

        for i in range(steps):
            results = self.step_red(red_obs, red_action_space)
            red_obs = results.observation

            blue_obs = self.env.get_observation('Blue')
            obs.feed_obs(red_obs, blue_obs)

            results = self.step_blue(blue_obs, blue_action_space)
            blue_obs = results.observation

if __name__=="__main__":
    interface = Interface()
    interface.main_menu()
    interface.mainloop()
'''
if mode == 0:
    label2 = tk.Label(window, text="Escolha os agentes")
    label2.pack()
    label3 = tk.Label(window, text="Red")
    label3.pack()
    button2 = tk.Button(window, text="Baseline", command=set_agent(0))
    button2.pack()
    button3 = tk.Button(window, text="Baseline", command=set_agent(1))
    button3.pack()


menu = tk.Menu(window)
window.config(menu=menu)

submenu = tk.Menu(menu)
menu.add_cascade(label="Arquivo", menu=submenu)
submenu.add_command(label="Sair", command=window.quit)

menu2 = tk.Menu(window)
window.config(menu=menu2)

submenu = tk.Menu(menu)
menu.add_cascade(label="View", menu=submenu)

submenu.add_command(label="1", command=)
submenu.add_command(label="2", command=)
submenu.add_command(label="3", command=)

window.mainloop()
'''