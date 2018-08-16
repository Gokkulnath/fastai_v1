from .imports.core import *
from ipykernel.kernelapp import IPKernelApp

FileLike = Union[str, Path]
AnnealingFt = Union[Callable[[float,float,float],float],Callable[[float,float,float,float],float]]

def in_notebook(): return IPKernelApp.initialized()

def is_tuple(x) -> bool:    return isinstance(x, tuple)
def is_iterable(x) -> bool: return isinstance(x, Iterable)

def listify(p=None, q=None) -> Collection:
    "Makes p a list that looks like q"
    if p is None: p=[]
    elif is_iterable(p): p=[p]
    n = q if type(q)==int else 1 if q is None else len(q)
    if len(p)==1: p = p * n
    return p

if in_notebook():  tqdm, trange = tqdm_notebook, tnrange

class SmoothenValue():
    "To compute the moving average of values"

    def __init__(self, beta:float):
        self.beta,self.n,self.mov_avg = beta,0,0

    def __repr__(self) -> str:
        return f'SmoothenValue: current {self.smooth}, n={self.n}'
    
    def add_value(self, val:float):
        self.n += 1
        self.mov_avg = self.beta * self.mov_avg + (1 - self.beta) * val
        self.smooth = self.mov_avg / (1 - self.beta ** self.n)

def annealing_no(start:float, end:float, pct:float) -> float:     return start
def annealing_linear(start:float, end:float, pct:float) -> float: return start + pct * (end-start)
def annealing_exp(start:float, end:float, pct:float) -> float:    return start * (end/start) ** pct
def annealing_cos(start:float, end:float, pct:float) -> float:
    cos_out = np.cos(np.pi * pct) + 1
    return end + (start-end)/2 * cos_out
    
def do_annealing_poly(start:float, end:float, pct:float, degree:float) -> float:
    return end + (start-end) * (1-pct)**degree
def annealing_poly(degree:float) -> Callable: return partial(do_annealing_poly, degree=degree)