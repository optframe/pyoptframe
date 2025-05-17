CPPSTD=--std=c++20

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


all: load_thirdparty optframe_lib demo_local

OPTFRAME_C_LIB=thirdparty/optframe-external/src/OptFrameLib/OptFrameLib.cpp

optframe_lib: optframe/optframe_lib.so
	@echo "make optframe_lib: OptFrame C Library is built!"

optframe/optframe_lib.so:
	@echo "make optframe/optframe_lib.so: BUILD WITH ${CXX}"
	$(CXX) $(CPPSTD) -g -I${OPTFRAME_SRC}/include   -Wall -pedantic -Ofast --shared optframe/optframe_lib.cpp $(OPTFRAME_C_LIB)  -o optframe/optframe_lib.so -fPIC
	# readelf -s optframe/optframe_lib.so | grep fcore
	ls -la optframe/optframe_lib.so

optframe_lib_cmake:
	@echo "make optframe_lib_cmake: BUILD WITH CL (default)"
	cmake -S. -Bbuild -GNinja
	ninja -Cbuild
	mv optframe/liboptframe_lib.so optframe/optframe_lib.so

	
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

test_local: optframe_lib
	@echo "make test_local"
	@echo ""
	@echo "Running DEV Demos as tests..."
	@echo ""
	(cd demo/02_QuickstartKP_SA/ && ./join.sh && python3 dev-mainKP-fcore-ex.py > /dev/null)
	(cd demo/03_QuickstartTSP_VNS_BRKGA/ && ./join.sh && python3 dev-mainTSP-fcore-brkga.py > /dev/null)
	(cd demo/03_QuickstartTSP_VNS_BRKGA/ && ./join.sh && python3 dev-mainTSP-fcore-ils.py > /dev/null)
	@echo "Finished 'make test_local'"

test: optframe_lib test_local test_package

test_package: clean install
	# (cd demo/ && python3 demo_pyfcore.py)
	(cd tests/ && python3 test_pkg_engine_kp.py)
	echo ""
	echo "Running PACKAGE Demos as tests..."
	echo ""
	(cd demo/02_QuickstartKP_SA/ && ./join.sh && python3 mainKP-fcore-ex.py > /dev/null)
	(cd demo/03_QuickstartTSP_VNS_BRKGA/ && ./join.sh && python3 mainTSP-fcore-brkga.py > /dev/null)
	(cd demo/03_QuickstartTSP_VNS_BRKGA/ && ./join.sh && python3 mainTSP-fcore-ils.py > /dev/null)
	echo "Finished 'make test_package'"
	
	

install: clean
	echo "***** BUILDING AND INSTALLING ***** "
	python3 -m pip install build twine
	(cd docs && python3 -m pip install -r requirements.txt)
	python3 -m build
	python3 -m pip install --no-cache-dir .

clean:
	echo "***** CLEANING ***** "
	rm -f  optframe/*.so
	rm -rf optframe/__pycache__
	rm -f  dist/*
	rm -rf ./optframe-git/
	rm -rf ./optframe.egg-info
	rm -rf venv/
	rm -rf build/

load_thirdparty:
	git submodule update --init --recursive 
	git pull --recurse-submodules
	pip install numpy # for demos
