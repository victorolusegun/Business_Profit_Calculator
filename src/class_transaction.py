class Transaction:
    def __init__(self, date, time, ref_id, amount, balance):
        self.date = date
        self.time = time
        self.ref_id = ref_id
        self.amount = amount
        self.balance = balance

    def classification(self):
        if self.amount < 0:
            return 'Transfer'
        elif 0 < self.amount <= 500:
            return 'Bill Payment'
        else:
            return 'Withdrawal'