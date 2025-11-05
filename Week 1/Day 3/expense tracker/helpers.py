from dataclasses import dataclass



@dataclass
class Expense:
    description: str
    amount: int | float
    category: str
    date: str
    is_recurring: bool


