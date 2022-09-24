#CC=g++
CC=clang++-12
CPPSTD=-std=c++20 -Wfatal-errors
#CPPSTD=--std=c++17 -fconcepts -Wfatal-errors

all: mylib

mylib:
	mkdir -p build/
	# -Wextra
	$(CC) $(CPPSTD) -g -Isrc/optframe-src/include -Wall -pedantic -Ofast --shared optframe/fcore_lib.cpp -o build/fcore_lib.so -fPIC
	#readelf -s build/fcore_lib.so | grep fcore

demo_draft:
	# (cd demo && valgrind --leak-check=full python3 draft_pyfcore.py)
	(cd demo && python3 draft_pyfcore.py)

test:
	# (cd demo/ && python3 demo_pyfcore.py)
	(cd tests/ && python3 test_engine_kp.py)
	

install:
	#pip install  --global-option=build_ext --global-option="-I/home/imcoelho/git-reps/optframe/src" .
	pip install .

clean:
	rm -f build/*