#!/bin/bash

cat BTSP-fcore-part1.py BTSP-fcore-part2.py BTSP-fcore-part3.py BTSP-fcore-part4.py BTSP-fcore-part5.py BTSP-fcore-part6.py BTSP-fcore-part8.py > BTSP-fcore.py 

# create NSGA-II example
cat BTSP-fcore.py  mainBTSP-fcore-nsgaii-part1.py mainBTSP-fcore-nsgaii-part2.py mainBTSP-fcore-nsgaii-part3.py > mainBTSP-fcore-nsgaii.py
