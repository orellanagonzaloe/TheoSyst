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

	weightList = rdb.getWeights(did_dict[config['sample']])[0]

	# Add Scale and PDFalpha NP by hand

	if config['sample'] != 'ttgamma':

		weightList['NP_muR'] = {}
		weightList['NP_muR']['combination'] = 'envelope'
		weightList['NP_muR']['nominal'] = 'MUR1_MUF1_PDF261000'
		weightList['NP_muR']['nominal_pdf'] = '261000'
		weightList['NP_muR']['type'] = 'scale_ME_NP_muR'
		weightList['NP_muR']['weights'] = ['MUR0.5_MUF1_PDF261000', 'MUR2_MUF1_PDF261000']
		weightList['NP_muF'] = {}
		weightList['NP_muF']['combination'] = 'envelope'
		weightList['NP_muF']['nominal'] = 'MUR1_MUF1_PDF261000'
		weightList['NP_muF']['nominal_pdf'] = '261000'
		weightList['NP_muF']['type'] = 'scale_ME_NP_muF'
		weightList['NP_muF']['weights'] = ['MUR1_MUF0.5_PDF261000', 'MUR1_MUF2_PDF261000']
		weightList['NP_muRmuF'] = {}
		weightList['NP_muRmuF']['combination'] = 'envelope'
		weightList['NP_muRmuF']['nominal'] = 'MUR1_MUF1_PDF261000'
		weightList['NP_muRmuF']['nominal_pdf'] = '261000'
		weightList['NP_muRmuF']['type'] = 'scale_ME_NP_muRmuF'
		weightList['NP_muRmuF']['weights'] = ['MUR0.5_MUF0.5_PDF261000', 'MUR2_MUF2_PDF261000']

	else:

		weightList['NP_muR'] = {}
		weightList['NP_muR']['combination'] = 'envelope'
		weightList['NP_muR']['nominal'] = ' muR=0.10000E+01 muF=0.10000E+01 '
		weightList['NP_muR']['nominal_pdf'] = '260000'
		weightList['NP_muR']['type'] = 'scale_ME_NP_muR'
		weightList['NP_muR']['weights'] = [' muR=0.50000E+00 muF=0.10000E+01 ', ' muR=0.20000E+01 muF=0.10000E+01 ']
		weightList['NP_muF'] = {}
		weightList['NP_muF']['combination'] = 'envelope'
		weightList['NP_muF']['nominal'] = ' muR=0.10000E+01 muF=0.10000E+01 '
		weightList['NP_muF']['nominal_pdf'] = '260000'
		weightList['NP_muF']['type'] = 'scale_ME_NP_muF'
		weightList['NP_muF']['weights'] = [' muR=0.10000E+01 muF=0.50000E+00 ', ' muR=0.10000E+01 muF=0.20000E+01 ']
		weightList['NP_muRmuF'] = {}
		weightList['NP_muRmuF']['combination'] = 'envelope'
		weightList['NP_muRmuF']['nominal'] = ' muR=0.10000E+01 muF=0.10000E+01 '
		weightList['NP_muRmuF']['nominal_pdf'] = '260000'
		weightList['NP_muRmuF']['type'] = 'scale_ME_NP_muRmuF'
		weightList['NP_muRmuF']['weights'] = [' muR=0.50000E+00 muF=0.50000E+00 ', ' muR=0.20000E+01 muF=0.20000E+01 ']



	# print weightList

	schema = '!INDIR/!INFILE.root:!WEIGHTNAME/Syst_!WEIGHTNAME_!AONAME'
	
	os.system('mkdir -p %s' % config['outputDir'])


	result = st.combineAllVariations(weightList, inDir, config['outputDir'], schema=schema, inFile=inFile, returnOnlyVariationsInComination=False)

	# add PDFalpha manually 
	weightList['NP_PDFalpha'] = {}

	if config['sample'] != 'ttgamma':

		weightList['NP_PDFalpha']['type'] = 'NP_PDFalpha'

	else:

		weightList['NP_PDFalpha']['type'] = 'NP_PDFalpha2'


	with open(inDir+'/'+inFile.replace('.root', '_weightList.yaml'), 'w+') as f:
		data = yaml.dump(weightList, f)


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



	print result


	if config['doSystToolPlots']:

		eosPathPlot = '%s%s/plotsTool/%s_%s' % (config['eosPathPlot'], config['tag'], config['sample'], config['year'])

		_regexFilter = None # variations included
		_regexVeto = '.{0,}__1.{0,}' # variations NOT included

		if not os.path.exists(eosPathPlot):
			os.makedirs(eosPathPlot)

		varToDelete = ['all.root', 'Sherpa_ME_PDF261000_scale.root', 'Sherpa_ME_PDF261000_alphaS_NNPDF_NNLO.root', 'Sherpa_ME_PDF13000.root', 'Sherpa_ME_PDF25300.root', 'Sherpa_ME_PDF261000_var.root', 'aMcAtNlo_ME_PDF260000_scale_type2.root', 'aMcAtNlo_PDF260000_Nominal_type2.root', 'aMcAtNlo_ME_PDF260000_var_type2.root'] # Nominal can't be deleted


		for var in varToDelete:

			for file in result:

				if var in file:

					del result[file]

		plots = st.makeSystematicsPlotsWithROOT(result, eosPathPlot, regexFilter=_regexFilter, regexVeto=_regexVeto)


