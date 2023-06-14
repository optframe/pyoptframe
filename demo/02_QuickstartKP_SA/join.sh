#!/bin/bash

cat KP-fcore-ex-part0.py     KP-fcore-ex-part1.py KP-fcore-ex-part2.py  KP-fcore-ex-part3.py  KP-fcore-ex-part4.py KP-fcore-ex-part5.py KP-fcore-ex-part6.py > KP-fcore-ex.py 
cat KP-fcore-ex-part0-dev.py KP-fcore-ex-part1.py KP-fcore-ex-part2.py  KP-fcore-ex-part3.py  KP-fcore-ex-part4.py KP-fcore-ex-part5.py KP-fcore-ex-part6.py > dev-KP-fcore-ex.py 

cat KP-fcore-ex.py     mainKP-fcore-ex-part1.py mainKP-fcore-ex-part2.py  mainKP-fcore-ex-part3.py mainKP-fcore-ex-part4.py mainKP-fcore-ex-part5.py > mainKP-fcore-ex.py
cat dev-KP-fcore-ex.py mainKP-fcore-ex-part1.py mainKP-fcore-ex-part2.py  mainKP-fcore-ex-part3.py mainKP-fcore-ex-part4.py mainKP-fcore-ex-part5.py > dev-mainKP-fcore-ex.py

