#!/bin/bash

cat TSP-fcore-part0.py     TSP-fcore-part1.py TSP-fcore-part2.py TSP-fcore-part3.py TSP-fcore-part4.py TSP-fcore-part5.py TSP-fcore-part6.py TSP-fcore-part7.py > TSP-fcore.py 
cat TSP-fcore-part0-dev.py TSP-fcore-part1.py TSP-fcore-part2.py TSP-fcore-part3.py TSP-fcore-part4.py TSP-fcore-part5.py TSP-fcore-part6.py TSP-fcore-part7.py > dev-TSP-fcore.py 

# create ILS/VNS example
cat TSP-fcore.py      mainTSP-fcore-ils-part1.py mainTSP-fcore-ils-part2.py mainTSP-fcore-ils-part3.py > mainTSP-fcore-ils.py
cat dev-TSP-fcore.py  mainTSP-fcore-ils-part1.py mainTSP-fcore-ils-part2.py mainTSP-fcore-ils-part3.py > dev-mainTSP-fcore-ils.py

# create BRKGA example
cat TSP-fcore.py      mainTSP-fcore-brkga-part1.py mainTSP-fcore-brkga-part2.py mainTSP-fcore-brkga-part3.py  mainTSP-fcore-brkga-part4.py > mainTSP-fcore-brkga.py
cat dev-TSP-fcore.py  mainTSP-fcore-brkga-part1.py mainTSP-fcore-brkga-part2.py mainTSP-fcore-brkga-part3.py  mainTSP-fcore-brkga-part4.py > dev-mainTSP-fcore-brkga.py
