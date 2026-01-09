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
    iterations = 0
    observations = []
    def __init__(self, iterations):
       self.iterations = iterations
        
    def feed_obs(self, red_obs, blue_obs):
        obs = (red_obs, blue_obs)
        self.observations.append(obs)

    def get_obs(self, iteration, agent):
        if agent == 'red':
            return self.observations[iteration][0]
        elif agent == 'blue':
            return self.observations[iteration][1]

path = '../Scenarios/Scenario1b.yaml'
scenario_gen = fr(path)

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
class Simulator():
    red_agent = B_lineAgent()
    blue_agent = BlueReactRemoveAgent()
    interface = Interface()

    def step_red(obs, verbose=True):
        action = red_agent.get_action(obs, action_space)
        results = env.step(action=action, agent='Red')
        return results

    def step_blue(obs, verbose=True):
        action = blue_agent.get_action(obs, blue_action_space)
        results = env.step(action=action, agent='Blue')
        return results

    def run():
        env = CybORG(scenario_gen) 

        results = env.reset(agent='Red')

        action_space = results.action_space
        blue_action_space = env.get_action_space('Blue')

        red_obs = results.observation
        
        steps = interface.choose_steps()

        obs = Observations(steps)
        for i in range(steps):
            results = step_red(red_obs)
            red_obs = results.observation

            blue_obs = env.get_observation('Blue')
            obs.feed_obs(red_obs, blue_obs)

            pprint(blue_obs)
            results = step_blue(blue_obs)
            blue_obs = results.observation

import tkinter as tk

class Interface():
    root = tk.Tk()
    running = False
    mode = -1
    def __init__():
        self.root.title("My window")

    def choose_mode():
        def set_mode(number):
            self.mode = number 
        if self.running == False:
            lbl_question = tk.Label(self.root, text="Choose simulation mode")
            lbl_question.pack()
            btn1 = tk.Button(self.root, "Mode 0", command=set_mode(0))
            btn1.pack()
            btn2 = tk.Button(self.root, "Mode 1", command=set_mode(1))
            btn2.pack()

    def choose_agent():
        if self.running == False && self.mode == 0:
            lbl_question = tk.Label(self.root, text="Choose agent")
            lbl_question.pack()
            btn1 = tk.Button(window, "Baseline", command=return "baseline")
            btn1.pack()
            btn2 = tk.Button(window, "Meander", command=return "meander")
            btn2.pack()
        else:
            lbl = tk.Label(self.root, text="WIP")
            lbl.pack()

    def choose_steps():
        if self.running == False:
            lbl_question = tk.Label(self.root, text="Choose step number:")
            lbl_question.pack()
            entry = tk.Entry(self.root, textvariable = steps_var)
            entry.pack()
            entry.bind("Return", lambda e: return step)
            return steps_var.get()
        
    def create_lbl(text):
        lbl = tk.Label(self.root, text=text)

    def draw():
        if choose_mode() == 0:
            if choose_agent() == "baseline":





def set_agent(number):
    agent = number

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
'''
submenu.add_command(label="1", command=)
submenu.add_command(label="2", command=)
submenu.add_command(label="3", command=)
'''

window.mainloop()
