#!/bin/bash

cat VRP-fcore-part1.py VRP-fcore-part2.py VRP-fcore-part3.py VRP-fcore-part4.py VRP-fcore-part5.py VRP-fcore-part6.py VRP-fcore-part7.py > VRP-fcore.py 

# create ILS/VNS example
cat VRP-fcore.py  mainVRP-fcore-part1.py mainVRP-fcore-part2.py mainVRP-fcore-part3.py > mainVRP-fcore.py
