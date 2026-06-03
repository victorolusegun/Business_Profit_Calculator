from datetime import datetime

def filter_transactions(table):
    dataframe = []
    for page in table:
        line_list = page.split('\n')
        for line in line_list:
            single_line = line.split()
            try:
                rule1 = single_line[0]
            except IndexError:
                continue
            format = '%Y/%m/%d'
            try:
                v_rule1 = datetime.strptime(rule1, format)
            except ValueError:
                continue
            if v_rule1 and len(single_line) == 5:
                dataframe.append(single_line)
    return dataframe