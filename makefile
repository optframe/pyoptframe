CC=clang++
CC_GCC=g++
CC_CLANG=clang++
#CC=clang++
CPPSTD=-std=c++20 # -fconcepts-diagnostics-depth=2  # -Wfatal-errors
#CPPSTD=--std=c++17 -fconcepts -Wfatal-errors

##########################################
#         SUBMODULE LOCATION
#
OPTFRAME_SRC=./thirdparty/optframe-external
#
# LOCAL file (only hot dev in same project...)
#
#OPTFRAME_SRC=./thirdparty/optframe-local
#
#@echo "IMPORTANT: Remember to point src/optframe-src to optframe project /include directory"
#@echo "EXAMPLE: ln -s  my/full/optframe/include  ./thirdparty/optframe-local"	
##########################################


all: optframe_lib demo_local

optframe_lib:
	# mkdir -p build/
	# -Wextra
	#
	@echo "BUILD WITH ${CC_GCC} (PART 1/2)"
	$(CC_GCC) $(CPPSTD) -g -I${OPTFRAME_SRC}/include -Wall -pedantic -Ofast --shared optframe/optframe_lib.cpp -o optframe/optframe_lib.so -fPIC
	#
	@echo "BUILD WITH ${CC_CLANG} (PART 2/2)"
	$(CC_CLANG) $(CPPSTD) -g -I${OPTFRAME_SRC}/include -Wall -pedantic -Ofast --shared optframe/optframe_lib.cpp -o optframe/optframe_lib.so -fPIC
	#
	#readelf -s build/optframe_lib.so | grep fcore

publish_test:
	rm -f dist/*
	python -m build
	rm -f dist/*.whl
	twine check dist/*
	twine upload -r testpypi dist/* --verbose
	


demo_local: optframe/optframe_lib.so
	python3 demo/demo_kp.py 

demo_local_tiny: optframe/optframe_lib.so
	echo "TEST Demo KP Tiny SA"
	python3 demo/demo_kp_tiny_sa.py 
	echo "TEST Demo KP Tiny"
	python3 demo/demo_kp_tiny.py 
	# echo "DEMO 02: KP"
	# (cd demo/02_QuickstartKP_SA/ && ./join.sh)
	# python3 demo/02_QuickstartKP_SA/mainKP-fcore-ex.py

.PHONY: docs

docs:
	cd docs && make clean && make html

test_local: load_thirdparty optframe_lib
	echo ""
	echo "Running DEV Demos as tests..."
	echo ""
	(cd demo/02_QuickstartKP_SA/ && ./join.sh && python3 dev-mainKP-fcore-ex.py > /dev/null)
	(cd demo/03_QuickstartTSP_VNS_BRKGA/ && ./join.sh && python3 dev-mainTSP-fcore-brkga.py > /dev/null)
	(cd demo/03_QuickstartTSP_VNS_BRKGA/ && ./join.sh && python3 dev-mainTSP-fcore-ils.py > /dev/null)

test: test_local test_package

test_package: install
	# (cd demo/ && python3 demo_pyfcore.py)
	(cd tests/ && python3 test_pkg_engine_kp.py)
	echo ""
	echo "Running PACKAGE Demos as tests..."
	echo ""
	(cd demo/02_QuickstartKP_SA/ && ./join.sh && python3 mainKP-fcore-ex.py > /dev/null)
	(cd demo/03_QuickstartTSP_VNS_BRKGA/ && ./join.sh && python3 mainTSP-fcore-brkga.py > /dev/null)
	(cd demo/03_QuickstartTSP_VNS_BRKGA/ && ./join.sh && python3 mainTSP-fcore-ils.py > /dev/null)
	
	

install:
	#pip install  --global-option=build_ext --global-option="-I${OPTFRAME_SRC}/include" .
	rm -rf ./optframe-git/
	rm -f dist/*
	python3 -m build
	# python3 -m pip install --no-cache-dir -e .
	python3 -m pip install --no-cache-dir .

clean:
	rm -f optframe/*.so

load_thirdparty:
	git submodule update --init --recursive 
	git pull --recurse-submodules
