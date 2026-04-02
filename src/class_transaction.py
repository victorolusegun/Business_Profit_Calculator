class Transaction:
    def __init__(self, date, time, ref_id, description, amount, balance):
        self.date = date
        self.time = time
        self.ref_id = ref_id
        self.description = description
        self.amount = amount
        self.balance = balance
