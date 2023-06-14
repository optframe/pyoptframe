#!/bin/bash

cat BTSP-fcore-part0-dev.py ../03_QuickstartTSP_VNS_BRKGA/TSP-fcore-part1.py BTSP-fcore-part2.py BTSP-fcore-part3.py BTSP-fcore-part4.py ../03_QuickstartTSP_VNS_BRKGA/TSP-fcore-part5.py ../03_QuickstartTSP_VNS_BRKGA/TSP-fcore-part6.py BTSP-fcore-part8.py > BTSP-fcore.py 

# create NSGA-II example
cat BTSP-fcore.py  mainBTSP-fcore-nsgaii-part1.py mainBTSP-fcore-nsgaii-part2.py mainBTSP-fcore-nsgaii-part3.py > mainBTSP-fcore-nsgaii.py
