import requests
import pdb
import random
import sys
from bs4 import BeautifulSoup

if len(sys.argv) != 2:
    print(sys.argv)
    print("Please enter a single url")
    sys.exit(1)

soup = BeautifulSoup(requests.get(sys.argv[1]).text, 'html.parser')
pdb.set_trace()
