from dataclasses import dataclass
from typing import List

@dataclass
class CalculatorState:
    """Calculator state with a stack of values."""

    stack: List[float] = None
    
    def __post_init__(self):
        """Initialize the stack if not provided."""
        self.stack = self.stack or []