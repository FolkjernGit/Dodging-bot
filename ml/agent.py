import torch
import random
import torch.nn as nn
import torch.optim as optim

class Agent:
    def __init__(self, model):
        self.model = model
        
        self.epsilon = 1.0 
        
        self.gamma = 0.99 
        
        self.optimizer = optim.Adam(
            
        self.model.parameters(),
        lr=0.001
        )

        self.loss_function = nn.MSELoss()
        
        
    def choose_action(self, observation, training=True):

        if random.random() < self.epsilon:
            return random.randint(0, 3)

        with torch.no_grad():
            observation = torch.tensor(
                observation,
                dtype=torch.float32
            )

            q_values = self.model(observation)

            return torch.argmax(q_values).item()
    
    def train_step(self, batch):
        states, actions, rewards, next_states, dones = batch

        states = torch.tensor(
            states,
            dtype=torch.float32
        )

        actions = torch.tensor(
            actions,
            dtype=torch.long
        )

        rewards = torch.tensor(
            rewards,
            dtype=torch.float32
        )

        next_states = torch.tensor(
            next_states,
            dtype=torch.float32
        )

        dones = torch.tensor(
            dones,
            dtype=torch.float32
        )


        # current Q values
        current_q = self.model(states)


        # get the Q value of the action we took
        current_q = current_q.gather(
            1,
            actions.unsqueeze(1)
        ).squeeze(1)


        # next Q values
        with torch.no_grad():
            next_q = self.model(next_states).max(1)[0]


        # target calculation
        target_q = rewards + (
            self.gamma * next_q * (1 - dones)
        )


        # calculate error
        loss = self.loss_function(
            current_q,
            target_q
        )


        # update network
        self.optimizer.zero_grad()

        loss.backward()

        self.optimizer.step()


        return loss.item()