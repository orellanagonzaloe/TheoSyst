#! /usr/bin/env python

import os
import argparse
import yaml
import glob
import sys
from array import array

import ROOT
ROOT.gROOT.SetBatch(True)
from ROOT import *


did_dict = {
	'photonjet': '364544',
	'ttgamma': '407320',
	'wgamma': '364525',
	'zllgamma': '364504',
	'znunugamma': '364519',
	'vgammagamma' : '364554',
	'diphoton' : '364554', # '364350', temporary fix: not included in Database yet
	}


def systematics(config):

	import systematicsTool as st
	import readDatabase as rdb

	inDir = os.path.dirname(config['inputSystFile'])
	inFile = config['inputSystFile'].split('/')[-1]

	weightList = rdb.getWeights(did_dict[inFile.split('_')[1]])[0]

	with open(inDir+inFile.replace('.root', '_weightList.yaml'), 'w+') as f:
		data = yaml.dump(weightList, f)

	# print weightList

	schema = '!INDIR/!INFILE.root:!WEIGHTNAME/Syst_!WEIGHTNAME_!AONAME'
	
	os.system('mkdir -p %s' % config['outputDir'])

	result = st.combineAllVariations(weightList, inDir, config['outputDir'], schema=schema, inFile=inFile)

	if config['doSystToolPlots']:
		plots = st.makeSystematicsPlotsWithROOT(result, config['outputDir'])


	for r in config['regions']:

		print '\n%s' % r

		for file in sorted(result):

			f = TFile(file)

			x = Double(0)
			y = Double(0)

			f.Get(r+'_nevents').GetPoint(0,x,y)

			dn = f.Get(r+'_nevents').GetErrorYlow(0)
			up = f.Get(r+'_nevents').GetErrorYhigh(0)
			pdn = 0.
			pup = 0.
			if y!=0:
				pdn = 100.*dn/y
				pup = 100.*up/y
			print ('Var %s:\t-%f (%f%%)\t+%f (%f%%)\t(cent: %f)') % (result[file].replace('[','').replace(']',''), dn, pdn, up, pup, y)




	# f2 = ROOT.TFile('output/syst_v102_0_1/syst_photonjet_20152016.root')

	# w_list = ['Weight', 'MEWeight', 'WeightNormalisation', 'NTrials', 'MUR0p5_MUF0p5_PDF261000',
 #  'MUR0p5_MUF1_PDF261000', 'MUR1_MUF0p5_PDF261000', 'MUR1_MUF1_PDF261000', 'MUR1_MUF2_PDF261000',
 #  'MUR2_MUF1_PDF261000', 'MUR2_MUF2_PDF261000', 'MUR1_MUF1_PDF261001', 'MUR1_MUF1_PDF261002',
 #  'MUR1_MUF1_PDF261003', 'MUR1_MUF1_PDF261004', 'MUR1_MUF1_PDF261005', 'MUR1_MUF1_PDF261006',
 #  'MUR1_MUF1_PDF261007', 'MUR1_MUF1_PDF261008', 'MUR1_MUF1_PDF261009', 'MUR1_MUF1_PDF261010',
 #  'MUR1_MUF1_PDF261011', 'MUR1_MUF1_PDF261012', 'MUR1_MUF1_PDF261013', 'MUR1_MUF1_PDF261014',
 #  'MUR1_MUF1_PDF261015', 'MUR1_MUF1_PDF261016', 'MUR1_MUF1_PDF261017', 'MUR1_MUF1_PDF261018',
 #  'MUR1_MUF1_PDF261019', 'MUR1_MUF1_PDF261020', 'MUR1_MUF1_PDF261021', 'MUR1_MUF1_PDF261022',
 #  'MUR1_MUF1_PDF261023', 'MUR1_MUF1_PDF261024', 'MUR1_MUF1_PDF261025', 'MUR1_MUF1_PDF261026',
 #  'MUR1_MUF1_PDF261027', 'MUR1_MUF1_PDF261028', 'MUR1_MUF1_PDF261029', 'MUR1_MUF1_PDF261030',
 #  'MUR1_MUF1_PDF261031', 'MUR1_MUF1_PDF261032', 'MUR1_MUF1_PDF261033', 'MUR1_MUF1_PDF261034',
 #  'MUR1_MUF1_PDF261035', 'MUR1_MUF1_PDF261036', 'MUR1_MUF1_PDF261037', 'MUR1_MUF1_PDF261038',
 #  'MUR1_MUF1_PDF261039', 'MUR1_MUF1_PDF261040', 'MUR1_MUF1_PDF261041', 'MUR1_MUF1_PDF261042',
 #  'MUR1_MUF1_PDF261043', 'MUR1_MUF1_PDF261044', 'MUR1_MUF1_PDF261045', 'MUR1_MUF1_PDF261046',
 #  'MUR1_MUF1_PDF261047', 'MUR1_MUF1_PDF261048', 'MUR1_MUF1_PDF261049', 'MUR1_MUF1_PDF261050',
 #  'MUR1_MUF1_PDF261051', 'MUR1_MUF1_PDF261052', 'MUR1_MUF1_PDF261053', 'MUR1_MUF1_PDF261054',
 #  'MUR1_MUF1_PDF261055', 'MUR1_MUF1_PDF261056', 'MUR1_MUF1_PDF261057', 'MUR1_MUF1_PDF261058',
 #  'MUR1_MUF1_PDF261059', 'MUR1_MUF1_PDF261060', 'MUR1_MUF1_PDF261061', 'MUR1_MUF1_PDF261062',
 #  'MUR1_MUF1_PDF261063', 'MUR1_MUF1_PDF261064', 'MUR1_MUF1_PDF261065', 'MUR1_MUF1_PDF261066',
 #  'MUR1_MUF1_PDF261067', 'MUR1_MUF1_PDF261068', 'MUR1_MUF1_PDF261069', 'MUR1_MUF1_PDF261070',
 #  'MUR1_MUF1_PDF261071', 'MUR1_MUF1_PDF261072', 'MUR1_MUF1_PDF261073', 'MUR1_MUF1_PDF261074',
 #  'MUR1_MUF1_PDF261075', 'MUR1_MUF1_PDF261076', 'MUR1_MUF1_PDF261077', 'MUR1_MUF1_PDF261078',
 #  'MUR1_MUF1_PDF261079', 'MUR1_MUF1_PDF261080', 'MUR1_MUF1_PDF261081', 'MUR1_MUF1_PDF261082',
 #  'MUR1_MUF1_PDF261083', 'MUR1_MUF1_PDF261084', 'MUR1_MUF1_PDF261085', 'MUR1_MUF1_PDF261086',
 #  'MUR1_MUF1_PDF261087', 'MUR1_MUF1_PDF261088', 'MUR1_MUF1_PDF261089', 'MUR1_MUF1_PDF261090',
 #  'MUR1_MUF1_PDF261091', 'MUR1_MUF1_PDF261092', 'MUR1_MUF1_PDF261093', 'MUR1_MUF1_PDF261094',
 #  'MUR1_MUF1_PDF261095', 'MUR1_MUF1_PDF261096', 'MUR1_MUF1_PDF261097', 'MUR1_MUF1_PDF261098',
 #  'MUR1_MUF1_PDF261099', 'MUR1_MUF1_PDF261100', 'MUR1_MUF1_PDF269000', 'MUR1_MUF1_PDF270000',
 #  'MUR1_MUF1_PDF25300', 'MUR1_MUF1_PDF13000']

 #  	for w in w_list:

 #  		h_tmp = f2.Get('%s/Syst_%s_VRM_nevents' % (w, w))
 #  		ev = h_tmp.GetBinContent(1)

 #  		print '%s: %f' % (w, ev)
