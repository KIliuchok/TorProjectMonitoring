import os
import time

from db_operations import *

### Updating the Relay/Bridges Data for all time

file1 = "networksize.csv"
file2 = "versions.csv"
file3 = "platforms.csv"
file4 = "relays-ipv6.csv"
file5 = "bridges-ipv6.csv"

files = ["networksize.csv",
"versions.csv",
"platforms.csv",
"relays-ipv6.csv",
"bridges-ipv6.csv"]

urls = ["wget https://metrics.torproject.org/networksize.csv",
"wget https://metrics.torproject.org/versions.csv",
"wget https://metrics.torproject.org/platforms.csv",
"wget https://metrics.torproject.org/relays-ipv6.csv",
"wget https://metrics.torproject.org/bridges-ipv6.csv"]

for item in urls:
    os.system(item)

update_relay_and_bridges(file1, file2, file3, file4, file5)


for file in files:
    remove_string = "rm " + file
    os.system(remove_string)
