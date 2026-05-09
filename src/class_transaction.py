class Transaction:
    def __init__(self, date, time, ref_id, amount, balance):
        self.date = date
        self.time = time
        self.ref_id = ref_id
        self.amount = amount
        self.balance = balance

    def classification(self):
        if self.ref_id[-5:] == '12201':
            return 'Withdrawal'
        elif self.ref_id[-5:] == '16101':
            return 'Airtime'
        elif self.ref_id[-5:] == '04101':
            return 'Transfer'
        else:
            return 'Others'