#! /usr/bin/env python

import os
import argparse
import re
import yaml
import glob
import sys
from array import array

import ROOT
ROOT.gROOT.SetBatch(True)
from ROOT import *

import lib.samples as sam
import lib.xsutils as xsu
import lib.multidraw as mtd


lumi_dict = {
	'2015':  3219.56,
	'2016': 32965.30,
	'20152016': 36184.86,
	'2017': 44307.40,
	'2018': 59937.20,
	}

tag_dict = {
	'2015': 'mc16a',
	'2016': 'mc16a',
	'20152016': 'mc16a',
	'2017': 'mc16d',
	'2018': 'mc16e',
	}

def initLoop(cfg, regions): 

	ref_file_tmp = glob.glob(cfg['eosPath'] + cfg['version'] + '/' + sam.samples_dict[cfg['sample']][0] + cfg['sampleType'] + tag_dict[cfg['year']] + '*root/*root*')[0]

	if cfg['inputFile'] is not None:

		ref_file_tmp = cfg['inputFile']

	# definition of histograms to fill, this is needed to be done before the entire for loop...
	h_syst = {}

	h_wname_tmp = TH1D()
	f_name_tmp = TFile(ref_file_tmp)
	h_wname_tmp = f_name_tmp.Get('lhe3_name')
	h_wname_tmp.SetDirectory(0)
	f_name_tmp.Close()

	weight_names = []
	for i in range(1,h_wname_tmp.GetNbinsX()+1):

		name = h_wname_tmp.GetXaxis().GetBinLabel(i)

		if name=='': continue

		weight_names.append(h_wname_tmp.GetXaxis().GetBinLabel(i))

	for w in weight_names:

		h_syst[w] = {}

		hname_syst = 'Syst_%s_weights' % safeWeightName(w)

		h_syst[w]['all_weights'] = TH1D( hname_syst, hname_syst, 300, -150., 150.)
		h_syst[w]['all_weights'].Sumw2()
		
		for r in regions:

			hname_syst = 'Syst_%s_%s_weights' % (safeWeightName(w), r)

			h_syst[w][r+'_weights'] = TH1D( hname_syst, hname_syst, 300, -150., 150.)
			h_syst[w][r+'_weights'].Sumw2()


			hname_syst = 'Syst_%s_%s_nevents' % (safeWeightName(w), r)

			h_syst[w][r+'_nevents'] = TH1D( hname_syst, hname_syst, 1, 0., 1.)
			h_syst[w][r+'_nevents'].Sumw2()

			for var in cfg['varSyst']:

				hname_syst = 'Syst_%s_%s_%s' % (safeWeightName(w), r, clean_var(var))

				h_syst[w]['%s_%s' % (r, var)] = TH1D(hname_syst, hname_syst, cfg['varSyst'][var][0], cfg['varSyst'][var][1], cfg['varSyst'][var][2])
				h_syst[w]['%s_%s' % (r, var)].Sumw2()


	print weight_names

	loop(cfg, regions, h_syst, weight_names)


def loop(cfg, regions, h_syst, weight_names): 

	loop_samples = sam.samples_dict[cfg['sample']]

	if cfg['inputFile'] is not None:
		loop_samples = cfg['inputFile']


	canvas = ROOT.TCanvas()
	for n,s in enumerate(loop_samples):

		if cfg['did'] is not None and cfg['did'] not in s: continue

		all_files = glob.glob(cfg['eosPath'] + cfg['version'] + '/' + s + cfg['sampleType'] + tag_dict[cfg['year']] + '*root/*root*')

		if cfg['inputFile'] is not None:
			all_files = [s]
		
		print ('File (%i/%i): %s') % (n+1, len(loop_samples), s)


		weight_mc = {}

		h_lhe3_sumw = TH1D()
		h_lhe3_name = TH1D()
		h_events = TH1D()

		f = TFile(all_files[0])
		h_lhe3_sumw = f.Get('lhe3_sumw')
		h_lhe3_sumw.Reset()
		h_lhe3_sumw.SetDirectory(0)
		h_events = f.Get('events')
		h_events.Reset()
		h_events.SetDirectory(0)
		h_lhe3_name = f.Get('lhe3_name')
		h_lhe3_name.SetDirectory(0)
		f.Close()


		chain = TChain('mini')

		for file in all_files:

			f_tmp = TFile(file)

			tmp = f_tmp.Get('lhe3_sumw')
			h_lhe3_sumw.Add(tmp)
			tmp = f_tmp.Get('events')
			h_events.Add(tmp)

			f_tmp.Close()

			chain.Add(file)

		sumw = h_events.GetBinContent(3)
		for i in range(1,h_lhe3_name.GetNbinsX()+1):

			w_name = h_lhe3_name.GetXaxis().GetBinLabel(i)

			if w_name == '': continue

			w_name_sumw = h_lhe3_sumw.GetXaxis().GetBinLabel(i)

			if w_name_sumw != w_name.replace(' ','').replace('.',''):
				print '\033[1;93mWARNING\033[0m: Weight name from CBK (\'%s\') differs from PMGWeightTool name (\'%s\')' % (w_name_sumw, w_name)

			# sumw = h_lhe3_sumw.GetBinContent(i)
			sumw = h_events.GetBinContent(3) # now for each variation the normalization is with the nominal sumw (not with the corresponding sumw of each variation) (2020-02-10)

			weight_mc[w_name] = (i-1, sumw)

		did = cfg['did']
		if cfg['sample'] is not None:	
			did = s.split('/')[-1].split('.')[1] 
		xs = xsu.get_xs_from_did(int(did))

		draw_list  = []

		for i,w in enumerate(weight_mc):

			# print ('Weight (%i/%i): %s') % (i+1, len(weight_mc), w)

			lumi_w = ( lumi_dict[cfg['year']] * xs ) / weight_mc[w][1]

			# all weights histogram

			hname_syst = 'Syst_%s_weights' % safeWeightName(w)
			varexp = 'weight_lhe3[%i]>>+%s' % (weight_mc[w][0], hname_syst)
			selection = '%s' % str(lumi_w)

			draw_list.append((hname_syst, 'weight_lhe3[%i]'%weight_mc[w][0], selection))

			for r in regions:

				# weights histogram in each region

				hname_syst = 'Syst_%s_%s_weights' % (safeWeightName(w), r)
				varexp = 'weight_lhe3[%i]>>+%s' % (weight_mc[w][0], hname_syst)
				selection = '(%s)*(%s&&fabs(weight_lhe3[%i])<100)' % (str(lumi_w), regions[r], weight_mc[w][0])

				draw_list.append((hname_syst, 'weight_lhe3[%i]'%weight_mc[w][0], selection))

				# Number of events in each region

				hname_syst = 'Syst_%s_%s_nevents' % (safeWeightName(w), r)
				varexp = '0.5>>+%s' % hname_syst
				selection = '(%s*weight_lhe3[%i]*weight_sf*weight_pu)*(%s&&fabs(weight_lhe3[%i])<100)' % (str(lumi_w), weight_mc[w][0], regions[r], weight_mc[w][0])

				draw_list.append((hname_syst, str(0.5), selection))

				# distributions in each region

				for var in cfg['varSyst']:

					hname_syst = 'Syst_%s_%s_%s' % (safeWeightName(w), r, clean_var(var))
					varexp = '%s>>+%s' % (var, hname_syst)
					clean_cond = [cond.replace(' ','') for cond in regions[r].split('&&') if not var in cond]
					cond = '&&'.join(clean_cond)
					selection = '(%s*weight_lhe3[%i]*weight_sf*weight_pu)*(%s&&fabs(weight_lhe3[%i])<100)' % ( str(lumi_w), weight_mc[w][0], cond, weight_mc[w][0])

					draw_list.append((hname_syst, var, selection))


		chain.MultiDraw(*draw_list)



	if cfg['checkZeroCounts']:

		for w in weight_names:
			for r in regions:

				if h_syst[w][r+'_nevents'].GetEntries() == 0:
					print ('Histogram %s has 0 entries...') % (h_syst[w][r+'_nevents'].GetName())

	output_file(cfg, regions, weight_names, h_syst)



def output_file(cfg, regions, weight_names, h_syst):

	outputdir = os.path.dirname(cfg['outputFile'])
	outputfile = cfg['outputFile']

	if not os.path.exists(outputdir):
		os.makedirs(outputdir)

	output = TFile(outputfile, 'RECREATE')


	for w in sorted(weight_names):

		output.mkdir(safeWeightName(w))
		output.cd(safeWeightName(w))

		hname_syst = 'Syst_%s_weights' % safeWeightName(w)
		h_syst[w]['all_weights'].Write(hname_syst)

		for r in sorted(regions):

			hname_syst = 'Syst_%s_%s_weights' % (safeWeightName(w), r)
			h_syst[w][r+'_weights'].Write(hname_syst)

			hname_syst = 'Syst_%s_%s_nevents' % (safeWeightName(w), r)
			h_syst[w][r+'_nevents'].Write(hname_syst)

			for var in cfg['varSyst']:

				hname_syst = 'Syst_%s_%s_%s' % (safeWeightName(w), r, clean_var(var))
				h_syst[w]['%s_%s' % (r, var)].Write(hname_syst)

		output.cd()

	output.Close()

	print ('\n%s file created') % (outputfile)

	cfg['regions'] = regions
	cfg['weights'] = weight_names


	with open(outputfile.replace('.root', '_config.yaml'), 'w+') as f:
		data = yaml.dump(cfg, f)
	print ('%s file created') % (outputfile.replace('.root', '_config.yaml'))


def safeWeightName(weight):

	weight = weight.replace('+','')
	weight = weight.replace(' nominal ','')
	weight = weight.replace(' set = ','_')
	weight = weight.replace(' = ','_')
	weight = weight.replace('=','')
	weight = weight.replace(',','')
	weight = weight.replace('.','')
	weight = weight.replace(':','')
	weight = weight.replace(' ','_')
	weight = weight.replace('#','num')
	weight = weight.replace('\n','_')
	weight = weight.replace('/','over')
	
	# they changed again safe naming convention :/

	# if weight.startswith(' '):
	# 	weight = weight[1:]
	# if weight.endswith(' '):
	# 	weight = weight[:-1]

	# weight = weight.replace(' ','_')
	# weight = weight.replace('+','')

	# for decimalPoint in re.findall('[0-9].[0-9]',weight):
	# 	weight=weight.replace(decimalPoint,decimalPoint.replace('.','p'))

	return weight

def clean_var(var):
	return var.replace(':', '_').replace('[','').replace(']', '').replace('(', '').replace(')','').replace('/','')
