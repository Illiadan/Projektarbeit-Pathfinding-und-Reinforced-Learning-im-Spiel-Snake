import os
from os import path

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim


class LinearQNet(nn.Module):
    def __init__(self, inputSize, hiddenSize, outputSize):
        super().__init__()
        self.linear1 = nn.Linear(inputSize, hiddenSize)
        self.linear2 = nn.Linear(hiddenSize, outputSize)

    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x

    def save(self, fileName="model.txt"):
        modelFolderPath = path.dirname(__file__)

        if not os.path.exists(modelFolderPath):
            os.makedirs(modelFolderPath)

        filePath = os.path.join(modelFolderPath, fileName)
        torch.save(self.state_dict(), filePath)


class QTrainer:
    def __init__(self, model, learningRate, gamma):
        self.learningRate = learningRate
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.learningRate)
        self.criterion = nn.MSELoss()

    def trainStep(self, state, action, reward, nextState, gameOver):
        #   input can be single value or list of tuples
        state = torch.tensor(state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)
        nextState = torch.tensor(nextState, dtype=torch.float)

        if len(state.shape) == 1:
            # (1, x)
            state = torch.unsqueeze(state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            nextState = torch.unsqueeze(nextState, 0)
            gameOver = (gameOver, )

        #   1:  predicted Q values with current state

        prediction = self.model(state)

        #   2:  newQ = r + y * max(next predicted Q value) -> only do this if not game over
        #   prediction.clone()
        #   predictions[argmax(action)] = newQ

        target = prediction.clone()
        for idx in range(len(gameOver)):
            newQ = reward[idx]
            if not gameOver[idx]:
                newQ = reward[idx] + self.gamma * torch.max(
                    self.model(nextState[idx]))

            target[idx][torch.argmax(action).item()] = newQ

        self.optimizer.zero_grad()
        loss = self.criterion(target, prediction)
        loss.backward()

        self.optimizer.step()
