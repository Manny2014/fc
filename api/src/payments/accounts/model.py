class Account:
    def __init__(self, id, balance):
        self.id = id
        self.balance = balance

    def has_money(self):
        return self.balance > 0

    def has_more_than(self, balance):
        return self.balance >= balance
