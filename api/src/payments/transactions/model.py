
import json

class Transaction:

    def __init__(self, id: str, from_account_id: str, to_account_id: str, amount: float):
        self.id = id
        self.from_account_id = from_account_id
        self.to_account_id = to_account_id
        self.amount = amount

    def toJSON(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4)
