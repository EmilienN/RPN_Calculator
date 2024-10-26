from dataclasses import dataclass
from typing import List

@dataclass
class CalculatorState:
    stack: List[float] = None
    
    def __post_init__(self):
        self.stack = self.stack or []