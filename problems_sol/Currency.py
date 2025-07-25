def currency(num):
    num_str = str(num)
    if '.' in num_str:
        int_part, dec_part = num_str.split('.')
        dec_part = '.' + dec_part
    else:
        int_part = num_str
        dec_part = ''
    n = len(int_part)
    if n <= 3:
        return int_part + dec_part
    res = int_part[-3:]
    int_part = int_part[:-3]
    while len(int_part) > 0:
        res = int_part[-2:] + ',' + res
        int_part = int_part[:-2]
    return res + dec_part

num = float(input("Enter num: "))
print("res: ", currency(num))
