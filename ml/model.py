import torch
import torch.nn as nn

class DodgeModel(nn.Module):
    def __init__(self, input_size=28, output_size=10):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_size, 64),
            nn.ReLU(),

            nn.Linear(64, 64),
            nn.ReLU(),

            nn.Linear(64, output_size)
        )

    def forward(self, x):
        return self.network(x)