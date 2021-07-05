all: mylib

mylib:
	mkdir -p build/
	g++ -std=c++17 -Ofast --shared fcore_lib.cpp -o build/fcore_lib.so -fPIC
