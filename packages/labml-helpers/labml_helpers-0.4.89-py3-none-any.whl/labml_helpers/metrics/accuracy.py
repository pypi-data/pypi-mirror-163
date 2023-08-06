import dataclasses

import torch

from labml import tracker
from . import Metric


@dataclasses.dataclass
class AccuracyState:
    samples: int = 0
    correct: int = 0

    def reset(self):
        self.samples = 0
        self.correct = 0


class Accuracy(Metric):
    data: AccuracyState

    def __init__(self, ignore_index: int = -1):
        super().__init__()
        self.ignore_index = ignore_index

    def __call__(self, output: torch.Tensor, target: torch.Tensor):
        output = output.view(-1, output.shape[-1])
        target = target.view(-1)
        pred = output.argmax(dim=-1)
        mask = target == self.ignore_index
        pred.masked_fill_(mask, self.ignore_index)
        n_masked = mask.sum().item()
        self.data.correct += pred.eq(target).sum().item() - n_masked
        self.data.samples += len(target) - n_masked

    def create_state(self):
        return AccuracyState()

    def set_state(self, data: any):
        self.data = data

    def on_epoch_start(self):
        self.data.reset()

    def on_epoch_end(self):
        self.track()

    def track(self):
        if self.data.samples == 0:
            return
        tracker.add("accuracy.", self.data.correct / self.data.samples)


class AccuracyMovingAvg(Metric):
    def __init__(self, ignore_index: int = -1, queue_size: int = 5):
        super().__init__()
        self.ignore_index = ignore_index
        tracker.set_queue('accuracy.*', queue_size, is_print=True)

    def __call__(self, output: torch.Tensor, target: torch.Tensor):
        output = output.view(-1, output.shape[-1])
        target = target.view(-1)
        pred = output.argmax(dim=-1)
        mask = target == self.ignore_index
        pred.masked_fill_(mask, self.ignore_index)
        n_masked = mask.sum().item()
        if len(target) - n_masked > 0:
            tracker.add('accuracy.', (pred.eq(target).sum().item() - n_masked) / (len(target) - n_masked))

    def create_state(self):
        return None

    def set_state(self, data: any):
        pass

    def on_epoch_start(self):
        pass

    def on_epoch_end(self):
        pass


class BinaryAccuracy(Accuracy):
    def __call__(self, output: torch.Tensor, target: torch.Tensor):
        pred = output.view(-1) > 0
        target = target.view(-1)
        self.data.correct += pred.eq(target).sum().item()
        self.data.samples += len(target)


class AccuracyDirect(Accuracy):
    data: AccuracyState

    def __call__(self, output: torch.Tensor, target: torch.Tensor):
        output = output.view(-1)
        target = target.view(-1)
        self.data.correct += output.eq(target).sum().item()
        self.data.samples += len(target)
