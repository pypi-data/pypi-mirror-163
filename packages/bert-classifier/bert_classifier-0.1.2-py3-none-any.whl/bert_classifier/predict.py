import torch
from .bert import bert_encoder


MAX_LEN = 512

class Inference(object):
    def __init__(self, tokenizer, model, labels, max_len=MAX_LEN):
        self.tokenizer = tokenizer
        self.model = model
        self.labels = labels
        self.max_len = max_len

    def predict(self, inp):
        self.model.eval()
        enc = bert_encoder(inp, self.tokenizer, self.max_len)
        out = self.model(*enc)[-1].detach().cpu()
        idx = out.argmax().item()
        label = self.labels[idx]
        proba = out.softmax(-1)[idx].item()
        return label, proba

    def __call__(self, inp):
        return self.predict(inp)


def load_model(model_dir, device='cpu'):
    return torch.load(model_dir, map_location=device)
