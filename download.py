import re
import requests

pattern = re.compile("\n")
f = open("urls.txt")
lines = f.readlines()
f.close()
lines = list(map(lambda x: pattern.sub("", x), lines))
for index, line in enumerate(lines):
    req = requests.get(line, timeout=60)
    with open("images/{}.jpg".format(index),'wb') as f:
        f.write(req.content)
