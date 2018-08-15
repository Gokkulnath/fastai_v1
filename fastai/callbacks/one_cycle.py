from ..imports.core import *
from ..callback import Callback, Stepper
from ..basic_train import Learner

class OneCycleScheduler(Callback):
    
    def __init__(self, learn:Learner, lr_max:float, epochs:int, moms:tuple=(0.95,0.85), div_factor:float=10., pct_end:float=0.1):
        self.learn = learn
        a = int(len(learn.data.train_dl) * epochs * (1 - pct_end) / 2)
        b = int(len(learn.data.train_dl) * epochs * pct_end)
        self.lr_scheds = [Stepper((lr_max/div_factor, lr_max), a),
                          Stepper((lr_max, lr_max/div_factor), a),
                          Stepper((lr_max/div_factor, lr_max/(div_factor*100)), b)]
        self.mom_scheds = [Stepper(moms, a), Stepper((moms[1], moms[0]), a), Stepper(moms[0], b)]
    
    def on_train_begin(self, **kwargs):
        self.opt = self.learn.opt
        self.opt.lr, self.opt.mom = self.lr_scheds[0].start, self.mom_scheds[0].start
        self.idx_s = 0
    
    def on_batch_end(self, **kwargs):
        self.opt.lr = self.lr_scheds[self.idx_s].step()
        self.opt.mom = self.mom_scheds[self.idx_s].step()
        if self.lr_scheds[self.idx_s].is_done:
            self.idx_s += 1
            if self.idx_s >= len(self.lr_scheds): return True