# @Author: J.Y.
# @Date:   2019-09-23T09:58:34+09:00
# @Last modified by:   J.Y.
# @Last modified time: 2019-09-23T10:18:50+09:00
# @License: J.Y. JeeYz
# @Copyright: J.Y. JeeYz


from urllib.request import urlopen
data = "language=python&framework=django"
f = urlopen("http://127.0.0.1:8000", bytes(data, encoding='utf-8'))
print(f.read(500).decode('utf-8'))







## endl
