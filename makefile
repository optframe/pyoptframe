all: mylib

mylib:
	mkdir -p build/
	# -Wextra
	g++ -std=c++17 -g -Isrc/optframe-src/include -fconcepts -Wall -pedantic -Ofast --shared pyoptframe/fcore_lib.cpp -o build/fcore_lib.so -fPIC
	#readelf -s build/fcore_lib.so | grep fcore

test:
	# (cd demo/ && python3 demo_pyfcore.py)
	(cd tests/ && python3 test_engine_kp.py)
	

install:
	#pip install  --global-option=build_ext --global-option="-I/home/imcoelho/git-reps/optframe/src" .
	pip install .

clean:
	rm -f build/*