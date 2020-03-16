
Theoretical systematics
=========================

## Theoretical systematics

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
	export PATH=$PATH:$PWD/local/bin/:/afs/cern.ch/sw/XML/TL2016/bin/x86_64-linux
	export PYTHONPATH=$PYTHONPATH:$PWD/local/bin/
	export SYSTTOOLSPATH=$PWD


Creating rooftiles with 1D histograms for each region and systematic variation, also distributions. e.g.:
    
    python theo_syst.py --sample zllgamma --year 20152016 --regions regions/regions.py --outputfile output/syst_test/syst_zllgamma_20152016.root

For one slice/did:

    python theo_syst.py --sample zllgamma --year 20152016 --regions regions/regions.py --outputfile output/syst_test/syst_zllgamma_364504_20152016.root --did 364504
    
To run the systematics tool with that output (use scl6 only here):

	python theo_syst.py --systematics --inputfile output/syst_test/syst_zllgamma_20152016.root --outputdir output/syst_test/syst_zllgamma_20152016 2>&1 | tee output/syst_test/syst_zllgamma_20152016.out

Plotting previous output and table of content:

	python theo_syst.py --plot_theo_syst --inputdir output/syst_test --tag plots_19_09_24