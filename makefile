all: mylib

mylib:
	mkdir -p build/
	# -Wextra
	g++-10 -std=c++20 -g -I../optframe/src -fconcepts -fcoroutines -Wfatal-errors -Wall -pedantic -Ofast --shared fcore_lib.cpp -o build/fcore_lib.so -fPIC
	readelf -s build/fcore_lib.so | grep fcore

test:
	python3 demo_pyfcore.py
