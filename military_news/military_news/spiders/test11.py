import re
s = 'aa\r  bb\n  cc'
tmp = re.sub(r'[\r\n]', '', s)
print(tmp)
