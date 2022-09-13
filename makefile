all: mylib

mylib:
	mkdir -p build/
	# -Wextra
	g++-10 -std=c++20 -g -I../optframe/src -fconcepts -fcoroutines -Wfatal-errors -Wall -pedantic -Ofast --shared cpplib/fcore_lib.cpp -o build/fcore_lib.so -fPIC
	readelf -s build/fcore_lib.so | grep fcore

test:
	(cd pyoptframe/ && python3 demo_pyfcore.py)

make_pip:
	#pip install  --global-option=build_ext --global-option="-I/home/imcoelho/git-reps/optframe/src" .
	pip install .
