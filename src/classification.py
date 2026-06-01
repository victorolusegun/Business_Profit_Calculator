class ClassTransaction:
    def __init__(self, date, time, ref_id, amount, balance, tx_type):
        self.date = date
        self.time = time
        self.ref_id = ref_id
        self.amount = amount
        self.balance = balance
        self.tx_type = tx_type
        # self.rnd_amt = rnd_amt

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