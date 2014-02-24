#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

import codecs
import sys
import time

import input
from input.keycombination import KeyCombination


sys.stdout = codecs.getwriter('utf8')(sys.stdout)


if __name__ == "__main__":
    input.start()
    
    while True:
        combi = KeyCombination(["R1","cross"])
        
        print input.isPressed(combi)
        time.sleep(.2)
