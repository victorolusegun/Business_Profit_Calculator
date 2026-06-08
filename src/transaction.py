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
        
    def rounding(self):
        return round(self.amount, -2)
    
class Class_Transaction(Transaction):
    def __init__(self, date, time, ref_id, amount, balance, tx_type):
        super().__init__(date, time, ref_id, amount, balance)
        self.tx_type = tx_type
    
    def agent_charge(self):
        if self.tx_type == 'Withdrawal':
            x = 5000
            if self.amount < x + 1000:
                charge = 100
            elif self.amount >= x + 1000:
                remainder = round(self.amount / x)
                charge = remainder * 100
        elif self.tx_type == 'Transfer':
            x = 10000
            if self.amount <= x:
                charge = 100
            elif self.amount > x:
                remainder = round(self.amount / x)
                charge = remainder * 100
        elif self.tx_type == 'Airtime':
            charge = 0
        elif self.tx_type == 'Others':
            charge = 50
        return charge
    
    def service_charge(self):
        if self.tx_type == 'Withdrawal':
            if self.amount >= 20000:
                service_cost = 100
            else:
                service_cost = (round(self.amount, -2) * 0.5) / 100
        elif self.tx_type == 'Transfer':
            service_cost = 20
            if self.amount >= 10000:
                service_cost += 50
        else:
            service_cost = 0
        return round(service_cost, 2)