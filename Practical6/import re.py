import re
s = 'my 2 favourite numbers are 27 and 69'
number1 = re.findall(r'[0-9]+',s)
print(number1)