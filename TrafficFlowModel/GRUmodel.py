from torch.nn import Module, GRU, Linear

class GRUMODEL(Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(GRUMODEL, self).__init__()
        self.gru = GRU(input_size, hidden_size, batch_first = True)
        self.fc = Linear(hidden_size, output_size)

    def forward(self, x):
        out, _ = self.gru(x)
        out = self.fc(out[:, -1, :])

        return out