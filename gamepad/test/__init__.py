#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

import codecs
import sys
import time

import controls
from controls.keycombination import KeyCombination


sys.stdout = codecs.getwriter('utf8')(sys.stdout)


if __name__ == "__main__":
    controls.start()
    
    while True:
        combi = KeyCombination(["R1","cross"])
        
        print controls.isPressed(combi)
        time.sleep(1)
