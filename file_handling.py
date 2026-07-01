import os
import hashlib

print(os.getcwd())

os.chdir('/Users/prashant/Downloads')
print(f'Current Working Directory is : {os.getcwd()}')

name = 'Prashant'
data = hashlib.md5(name.encode())
print(data.hexdigest())


