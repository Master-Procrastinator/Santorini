import torch as T
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from Game import *

def state_mappings():
    mappings = {
        (0,None) : 0,
        (1,None) : 1,
        (2,None) : 2,
        (3,None) : 3,
        (4,None) : 4,
        (0,'A') : 5,
        (1,'A') : 6,
        (2,'A') : 7,
        (3,'A') : 8,
        (0,'B') : 9,
        (1,'B') : 10,
        (2,'B') : 11,
        (3,'B') : 12,
    }
    return mappings

def convertTo1D(board, mappings):
    data = []
    for squares in board.board:
        for square in squares:
            if square.worker == None:
                data.append(mappings.get((square.building_level, None)))
            elif square.worker.name == "A1" or square.worker.name == "A2":
                data.append(mappings.get((square.building_level, "A")))
            else:
                data.append(mappings.get((square.building_level, "B")))
    return data
            

class ValueFunc(nn.Module):
    def __init__(self):
        super(ValueFunc, self).__init__()
        self.fc1 = nn.Linear(25,128)
        self.fc2 = nn.Linear(128,64)
        self.dropout = nn.Dropout(0.2)
        self.fc3 = nn.Linear(64,1)
        self.optimizer = optim.Adam(self.parameters(),lr=0.01)
        self.loss = nn.MSELoss()
        self.device = T.device('cpu')
        self.to(self.device)

    def forward(self,x):
        x = T.Tensor(x).to(self.device)
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

class Agent():
    def __init__(self):
        self.nn = ValueFunc()
        self.name = "A"
        self.workers = [Worker([], str(self.name)+"1"), Worker([], str(self.name)+"2")]
        self.values = []
    

    def action(self, board):
        states = board.all_possible_next_states(self.name)
        values = []
        for state in states:
            converted_state = convertTo1D(state, state_mappings())
            values.append(self.nn.forward(converted_state))
        highest_value = np.argmax(values)
        self.values.append(highest_value)
        return states[highest_value]
    
    
    

           
        