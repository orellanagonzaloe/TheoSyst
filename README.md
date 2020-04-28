Theoretical systematics
=========================

Tool to obtain theoretical systematics for different regions

## Creating input for the tool

Creating rooftiles with 1D histograms for each region and systematic variation, also distributions. e.g.:
    
    python main.py --createHists --sample photonjet_nnlo --year 20152016 --outputFile output/syst_v102_0_1/syst_photonjet_20152016.root --regions regions/regions_theo_v1.py

## Running the systematics-tools

To run the systematics-tools (use only SCL6)

	python main.py --computeSyst --inputSystFile output/syst_v102_0_1/syst_photonjet_20152016.root --outputDir output/syst_v102_0_1/syst_photonjet_20152016 --config output/syst_v102_0_1/syst_photonjet_20152016_config.yaml


## Plots

	python main.py --plots --inputDir output/syst_v102_0_1/ --tag syst_v102_0_1

## Setting up the tool

ONLY USE SCL6!
Setup for the first time (in any directory you want):

	git clone ssh://git@gitlab.cern.ch:7999/atlas-physics/pmg/tools/systematics-tools.git
	cd systematics-tools
	source systematics-tools-bootstrap.sh
	cp setupSystematicsTool.sh ~/.

For subsequent loggins:

	source setupSystematicsTool.sh 

Also you just can simply run (recomended):

	setupATLAS
	asetup 21.6.10,AthGeneration
	source ${LCG_RELEASE_BASE}/LCG_88/MCGenerators/rivet/${RIVETVER}/${LCG_PLATFORM}/rivetenv.sh
	export RIVET_ANALYSIS_PATH=$RIVET_ANALYSIS_PATH:${LCG_RELEASE_BASE}/LCG_88/MCGenerators/rivet/${RIVETVER}/${LCG_PLATFORM}/share/Rivet
	source data/setupLHAPDF.sh
	export SYSTTOOLSPATH=$PWD
	export PATH=$PATH:$PWD/local/bin/:/afs/cern.ch/sw/XML/TL2016/bin/x86_64-linux
	export PATH=$PWD/local/bin:$PATH
	export PYTHONPATH=$PYTHONPATH:$PWD/local/bin/
	if [ -e /usr/lib64/atlas/libsatlas.so ]; then
	   workaroundLib="`pwd`/extraLibs"
	   if [ ! -e $workaroundLib ]; then
	     mkdir -p $workaroundLib
	     ln -s /usr/lib64/atlas/libsatlas.so $workaroundLib/libptf77blas.so.3
	     ln -s /usr/lib64/atlas/libsatlas.so $workaroundLib/libptcblas.so.3
	     ln -s /usr/lib64/atlas/libsatlas.so $workaroundLib/libatlas.so.3
	     ln -s /usr/lib64/atlas/libsatlas.so $workaroundLib/liblapack.so.3 
	   # do the same for any other atlas lib that is missing and needed
	   fi
	   export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$workaroundLib"
	fi

