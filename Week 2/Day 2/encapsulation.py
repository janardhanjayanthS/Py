from enum import Enum


class AccountType(Enum):
    SA = "savings account"
    CA = "current account"
    FDA = "fixed deposit account"
    RDA = "recurring deposit account"


class BankAccount:
    def __init__(self, name: str) -> None:
        """
        Initializes a bank account
        Args:
            name: account holders name
        Attributes:
            name: account holders name
            __balance: (private) account's balance
            _account_type: type of account
        """
        self.name: str = name
        self.__balance: float = 0
        self._account_type: AccountType | None = None

    def set_account_type(self, account_type: AccountType) -> None:
        """
        sets an account type to current instance
        Args:
            account_type: (enum) type of account
        """
        if self._account_type is None:
            self._account_type = account_type
        else:
            print(f"Account type already exists: {self._account_type.value}")

    def _get_balance(self) -> float:
        """
        Returns accounts balacnce
        """
        return self.__balance

    def _set_balance(self, amount: float) -> None:
        """
        updates balance from child classes
        Args:
            amount: amount to set
        """
        self.__balance = amount

    def display(self) -> None:
        """
        Displays information about bank account
        """
        result = f"Account holder's name: {self.name} \nAccount balance: {self._get_balance()} \n"
        if self._account_type is None:
            print("Account type is not set")
        else:
            result += f"Account type: {self._account_type.value}"
        print("*" * 10)
        print(result)
        print("*" * 10)

    def deposit(self, amount: float) -> None:
        """
        Deposits amount to the bank account
        Args:
            amount: amount to be deposited
        """
        if amount > 0:
            self.__balance += amount
            print(f"Deposited: ${amount}")
            print(f"current balance: ${self._get_balance()}")
        else:
            print("Amount cannot be negative or 0")

    def withdraw(self, amount: float) -> None:
        """
        Withdraws amount from bank account
        Args:
            amount: amount to be withdrawn
        """
        if amount > self.__balance:
            print(f"Insufficient funds, your balance is ${self._get_balance()}")
        else:
            self.__balance -= amount
            print(f"Withdrew ${amount}")
            print(f"current balance: ${self.__balance}")


class SavingsAccount(BankAccount):
    def __init__(self, name: str) -> None:
        """
        Initializes Savings account
        Args:
            name: account holders name
        Attributes:
            _account_type: type of account, set to savings account
            __interest_rate: rate of interest per annum
        """
        super().__init__(name)
        self._account_type = AccountType.SA
        self.__interest_rate: float = 0.03

    def apply_interst(self) -> None:
        """
        applys interst rate to account's balance
        """
        self._set_balance(self._get_balance() + (self._get_balance() * self.__interest_rate))
        print(f"Balance after applying interest rate: {self._get_balance()}")
        self.display()


if __name__ == "__main__":
    # acc1 = BankAccount(name="Jane Doe")
    # acc1.set_account_type(account_type=AccountType.FDA)
    # acc1.deposit(amount=900.99)
    # acc1.display()

    sa_acc = SavingsAccount(name="MnM")
    sa_acc.withdraw(amount=1000)
    sa_acc.deposit(amount=1000)
    sa_acc.withdraw(amount=55)
    sa_acc.apply_interst()
