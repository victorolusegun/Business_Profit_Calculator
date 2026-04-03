from datetime import datetime

def filter_transactions(table):
    file_path = r"C:\Users\hp\Desktop\Restart\POS Profit Calculator\data\processed\output.csv"
    with open(file_path, 'a') as pro:
        for page in table:
            line_list = page.split('\n')
            for line in line_list:
                single_line = line.split()
                rule1 = single_line[0]
                format = '%Y/%m/%d'
                try:
                    v_rule1 = datetime.strptime(rule1, format)
                except ValueError:
                    continue
                if v_rule1 and len(single_line) == 5:
                    pro.write(','.join(single_line) + '\n')