import time
from dateutil import parser

str='2013-05-29T14:26:13.607756-05:00'
test1 = parser.parse(str)
print test1
#test2 = time.strptime('%Y-%m-%dT%H:%M:%S.%f')

#print test