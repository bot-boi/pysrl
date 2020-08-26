#!/usr/bin/python3
# downloads map files from ScapeRune's website
import requests


url = 'https://www.scaperune.info/map/images/map/tiles/{}/{}/{}.png'
fname = 'images/maps/{}_{}_{}.png'
M = 32  # max is 31
xi = range(M)
yi = range(M)
zi = range(M)

for x in xi:
    for y in yi:
        for z in zi:
            x = 4  # zoom level?
            r = requests.get(url.format(x, y, z))
            if r.headers.get('content-type') == 'image/png':
                open(fname.format(x, y, z), 'wb').write(r.content)
                print('Saved ' + fname.format(x, y, z))
