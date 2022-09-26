#CC=g++
CC=clang++-12
CPPSTD=-std=c++20 -Wfatal-errors
#CPPSTD=--std=c++17 -fconcepts -Wfatal-errors

all: optframe_lib demo

optframe_lib:
	# mkdir -p build/
	# -Wextra
	@echo "IMPORTANT: Remember to point src/optframe-src to optframe project /include directory"
	@echo "EXAMPLE: ln -s  my/full/optframe/include  src/optframe-src"
	$(CC) $(CPPSTD) -g -Isrc/optframe-src/include -Wall -pedantic -Ofast --shared optframe/optframe_lib.cpp -o optframe/optframe_lib.so -fPIC
	#readelf -s build/optframe_lib.so | grep fcore

demo: optframe/optframe_lib.so
	# valgrind --leak-check=full python3 demo/demo_pyfcore.py 
	python3 demo/demo_pyfcore.py 
	

test:   #install
	# (cd demo/ && python3 demo_pyfcore.py)
	(cd tests/ && python3 test_engine_kp.py)
	

install:
	#pip install  --global-option=build_ext --global-option="-I/home/imcoelho/git-reps/optframe/src" .
	pip install .

clean:
	rm -f optframe/*.so