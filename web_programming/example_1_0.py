# @Author: J.Y.
# @Date:   2019-09-18T20:00:40+09:00
# @Last modified by:   J.Y.
# @Last modified time: 2019-09-18T20:10:20+09:00
# @License: J.Y. JeeYz
# @Copyright: J.Y. JeeYz

from urllib.request import urlopen
f = urlopen("http://www.example.com")
print(f.read(500).decode('utf-8'))




## endl
