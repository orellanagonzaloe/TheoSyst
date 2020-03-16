#! /usr/bin/env python

import os,sys
import re
import argparse
import glob
import imp

import ROOT
ROOT.gROOT.SetBatch(True)
from ROOT import *

import lib.xsutils as xsu
import lib.common as com
import lib.samples as sam


# l_draw = ['all_weights', 'reg_weights', 'nevents', 'ph_pt', 'ph_eta', 'met_et', 'dphi_jetmet', 'ht']
# l_draw = ['all_weights', 'nevents', 'ph_pt', 'ph_eta', 'met_et', 'dphi_jetmet', 'ht']
l_draw = ['nevents']

def main():

	if args.plot_theo_syst:

		import lib.plot as plt

		plt.theo_syst_plots(inputdir, args.tag, reg)
		# plt.theo_syst_plots2(inputdir, args.tag, reg)

		return

	if args.systematics:

		systematics(args.inputfile, args.outputdir, do_plots=False)

		return

	if args.inputfile is not None:
		(weight_names, h_syst) = loop(file = args.inputfile)
	else:
		(weight_names, h_syst) = loop(sample = args.sample)
	
	output_file(outputfile, weight_names, h_syst)





def loop(sample=None, file=None, ZeroCounts=True): 

	ref_file_tmp = [file]
	loop_samples = [file]

	sample_type = '.mini.'
	if truth:
		sample_type = '.truth.'

	if sample is not None:
		ref_file_tmp = glob.glob(sample_path + version + '/' + sam.samples_dict[args.sample][0] + sample_type + com.tag_dict[year] + '*root/*root*')
		if args.did is not None:
			loop_samples = [s for s in sam.samples_dict[sample] if args.did in s]
		else:
			loop_samples = sam.samples_dict[sample]


	# definition of histograms to fill, this is needed to be done before the entire for loop...
	h_syst = {}


	h_wname_tmp = TH1D()
	f_name_tmp = TFile(ref_file_tmp[0])
	h_wname_tmp = f_name_tmp.Get('lhe3_name')
	h_wname_tmp.SetDirectory(0)
	f_name_tmp.Close()

	weight_names = []
	for i in range(1,h_wname_tmp.GetNbinsX()+1):

		name = h_wname_tmp.GetXaxis().GetBinLabel(i)

		if name=='':
			continue

		weight_names.append(h_wname_tmp.GetXaxis().GetBinLabel(i))

	for w in weight_names:

		h_syst[w] = {}

		hname_syst = 'Syst_%s_weights' % safeWeightName(w)

		h_syst[w]['all_weights'] = TH1D( hname_syst, hname_syst, 300, -150., 150.)
		h_syst[w]['all_weights'].Sumw2()
		

		for r in reg.regions:

			hname_syst = 'Syst_%s_%s_weights' % (safeWeightName(w), r)

			h_syst[w][r+'_weights'] = TH1D( hname_syst, hname_syst, 300, -150., 150.)
			h_syst[w][r+'_weights'].Sumw2()


			hname_syst = 'Syst_%s_%s_nevents' % (safeWeightName(w), r)

			h_syst[w][r+'_nevents'] = TH1D( hname_syst, hname_syst, 1, 0., 1.)
			h_syst[w][r+'_nevents'].Sumw2()


			hname_syst = 'Syst_%s_%s_ph_pt' % (safeWeightName(w), r)

			h_syst[w][r+'_ph_pt'] = TH1D( hname_syst, hname_syst, 14, 145., 1545.)
			h_syst[w][r+'_ph_pt'].Sumw2()


			hname_syst = 'Syst_%s_%s_ph_eta' % (safeWeightName(w), r)

			h_syst[w][r+'_ph_eta'] = TH1D( hname_syst, hname_syst, 30, -3., 3.)
			h_syst[w][r+'_ph_eta'].Sumw2()


			hname_syst = 'Syst_%s_%s_met_et' % (safeWeightName(w), r)

			h_syst[w][r+'_met_et'] = TH1D( hname_syst, hname_syst, 10, 0., 1000.)
			h_syst[w][r+'_met_et'].Sumw2()


			hname_syst = 'Syst_%s_%s_dphi_jetmet' % (safeWeightName(w), r)

			h_syst[w][r+'_dphi_jetmet'] = TH1D( hname_syst, hname_syst, 17, 0., 3.4)
			h_syst[w][r+'_dphi_jetmet'].Sumw2()


			hname_syst = 'Syst_%s_%s_ht' % (safeWeightName(w), r)

			h_syst[w][r+'_ht'] = TH1D( hname_syst, hname_syst, 30, 0., 6000.)
			h_syst[w][r+'_ht'].Sumw2()



	# for loop in samples
	canvas = TCanvas()
	for n,s in enumerate(loop_samples):

		all_files = [s]
		if sample is not None:
			all_files = glob.glob(sample_path + version + '/' + s + sample_type + com.tag_dict[year] + '*root/*root*')
		
		print ('File (%i/%i): %s')%(n+1, len(loop_samples), all_files[0])

		weight_mc = {}


		h_lhe3_sumw = TH1D()
		h_lhe3_name = TH1D()
		h_events = TH1D()

		f = TFile(all_files[0])
		h_lhe3_sumw = f.Get('lhe3_sumw')
		h_lhe3_sumw.Reset()
		h_lhe3_sumw.SetDirectory(0)
		h_events = f.Get('events')
		h_events.SetDirectory(0)
		h_lhe3_name = f.Get('lhe3_name')
		h_lhe3_name.SetDirectory(0)
		f.Close()


		chain = TChain('mini')

		for file in all_files:

			f_tmp = TFile(file)

			tmp = f_tmp.Get('lhe3_sumw')
			h_lhe3_sumw.Add(tmp)
			f_tmp.Close()

			chain.Add(file)
	
		for i in range(1,h_lhe3_name.GetNbinsX()+1):

			w_name = h_lhe3_name.GetXaxis().GetBinLabel(i)

			if w_name == '':
				continue

			w_name_sumw = h_lhe3_sumw.GetXaxis().GetBinLabel(i+1) # i+1 is used because there is a weight 'LHE3SumWeightsAlg' that passes the PMNT filter of the CBK, indexed with i=0... (fixed now in PMNT, can be changed after v75_2_theosyst)

			if w_name_sumw != w_name.replace(' ','').replace('.',''):
				print '\033[1;93mWARNING\033[0m: Weight name from CBK (\'%s\') differs from PMGWeightTool name (\'%s\')' % (w_name_sumw, w_name)

			# sumw = h_lhe3_sumw.GetBinContent(i+1) # same as before
			sumw = h_events.GetBinContent(3) # now for each variation the normalization is with the nominal sumw (not with the corresponding sumw of each variation) (2020-02-10)

			weight_mc[w_name] = (i-1,sumw)

		did = args.did
		if sample is not None:	
			did = s.split('/')[-1].split('.')[1] 
		xs = xsu.get_xs_from_did(int(did))

		for i,w in enumerate(weight_mc):

			print ('Weight (%i/%i): %s')%(i+1,len(weight_mc),w)

			lumi_w = ( com.lumi_dict[year] * xs ) / weight_mc[w][1]

			# weights histogram

			hname_syst = 'Syst_%s_weights' % safeWeightName(w)

			varexp = 'weight_lhe3[%i]>>+%s' % (weight_mc[w][0], hname_syst)
			selection = '%s' % str(lumi_w)

			if 'all_weights' in l_draw:
				chain.Draw(varexp,selection)

			for r in reg.regions:

				# weights histogram in each region

				hname_syst = 'Syst_%s_%s_weights' % (safeWeightName(w), r)

				varexp = 'weight_lhe3[%i]>>+%s' % (weight_mc[w][0], hname_syst)

				selection = '(%s)*(%s)' % (str(lumi_w), reg.regions[r])

				if 'reg_weights' in l_draw:
					chain.Draw(varexp,selection)

				# Number of events in each region

				hname_syst = 'Syst_%s_%s_nevents' % (safeWeightName(w), r)

				varexp = '0.5>>+%s' % hname_syst

				selection = '(%s*weight_lhe3[%i]*weight_sf*weight_pu)*(%s)' % ( str(lumi_w), weight_mc[w][0], reg.regions[r] )

				if 'nevents' in l_draw:
					chain.Draw(varexp,selection)

				# distributions in each region

				for d in ['ph_pt[0]', 'ph_eta[0]', 'met_et', 'dphi_jetmet', 'ht']:

					hname_syst = 'Syst_%s_%s_%s' % (safeWeightName(w), r, d.replace('[0]',''))

					varexp = '%s>>+%s' % (d, hname_syst)

					clean_cond = [cond.replace(' ','') for cond in reg.regions[r].split('&&') if not d in cond]
					cond = '&&'.join(clean_cond)

					selection = '(%s*weight_lhe3[%i]*weight_sf*weight_pu)*(%s)' % ( str(lumi_w), weight_mc[w][0], cond )

					if d.replace('[0]','') in l_draw:
						chain.Draw(varexp,selection)


	if ZeroCounts and 'nevents' in l_draw:

		for w in weight_names:
			for r in reg.regions:

				if h_syst[w][r+'_nevents'].GetEntries() == 0:
					print ('Histogram %s has 0 entries...') % (h_syst[w][r+'_nevents'].GetName())

	return (weight_names, h_syst)


def output_file(name, weight_names, h_syst):

	if not os.path.exists(os.path.dirname(name)):
		os.makedirs(os.path.dirname(name))

	output = TFile( name , 'RECREATE' )

	for w in sorted(weight_names):

		output.mkdir(safeWeightName(w))
		output.cd(safeWeightName(w))

		hname_syst = 'Syst_%s_weights' % safeWeightName(w)
		h_syst[w]['all_weights'].Write( hname_syst )

		for r in reg.regions:

			hname_syst = 'Syst_%s_%s_weights' % (safeWeightName(w), r)
			h_syst[w][r+'_weights'].Write( hname_syst )

			hname_syst = 'Syst_%s_%s_nevents' % (safeWeightName(w), r)
			h_syst[w][r+'_nevents'].Write( hname_syst )

			hname_syst = 'Syst_%s_%s_ph_pt' % (safeWeightName(w), r)
			h_syst[w][r+'_ph_pt'].Write( hname_syst )

			hname_syst = 'Syst_%s_%s_ph_eta' % (safeWeightName(w), r)
			h_syst[w][r+'_ph_eta'].Write( hname_syst )

			hname_syst = 'Syst_%s_%s_met_et' % (safeWeightName(w), r)
			h_syst[w][r+'_met_et'].Write( hname_syst )

			hname_syst = 'Syst_%s_%s_dphi_jetmet' % (safeWeightName(w), r)
			h_syst[w][r+'_dphi_jetmet'].Write( hname_syst )

			hname_syst = 'Syst_%s_%s_ht' % (safeWeightName(w), r)
			h_syst[w][r+'_ht'].Write( hname_syst )

		output.cd()

	output.Close()

	print ('%s file created') % (name)



def safeWeightName(weight):

	if weight.startswith(' '):
		weight = weight[1:]
	if weight.endswith(' '):
		weight = weight[:-1]

	weight = weight.replace(' ','_')
	weight = weight.replace('+','')
	for decimalPoint in re.findall('[0-9].[0-9]',weight):
		weight=weight.replace(decimalPoint,decimalPoint.replace('.','p'))

	return weight


def systematics(inputfile, outputdir, do_plots=False):

	import systematicsTool as st
	import readDatabase as rdb

	inDir = '/'.join(inputfile.split('/')[:-1])
	inFile = inputfile.split('/')[-1]

	weightList = rdb.getWeights(com.did_dict[inFile.split('_')[1]])[0]
	print weightList

	schema = '!INDIR/!INFILE.root:!WEIGHTNAME/Syst_!WEIGHTNAME_!AONAME'
	
	os.system('mkdir -p %s' % outputdir)

	result = st.combineAllVariations(weightList, inDir, outputdir, schema=schema, inFile=inFile)

	if do_plots:
		plots = st.makeSystematicsPlotsWithROOT(result, outputdir)


	nom_file = glob.glob(outputdir + '/*_Nominal.root')

	if len(nom_file)>0:
		f = TFile(nom_file[0])
		for r in reg.regions:

			x = Double(0)
			y = Double(0)

			f.Get(r+'_nevents').GetPoint(0,x,y)

			print ('%s:\t\t%f') % (r, y)
			print ('Var Nominal:\t-%f\t+%f') % (f.Get(r+'_nevents').GetErrorYlow(0), f.Get(r+'_nevents').GetErrorYhigh(0))

			for file in sorted(result):

				if result[file] == '[Nominal]':
					continue

				f2 = TFile(file)

				dn = f2.Get(r+'_nevents').GetErrorYlow(0)
				up = f2.Get(r+'_nevents').GetErrorYhigh(0)
				pdn = 0.
				pup = 0.
				if y!=0:
					pdn = 100.*dn/y
					pup = 100.*up/y
				print ('Var %s:\t-%f (%f%%)\t+%f (%f%%)') % (result[file].replace('[','').replace(']',''), dn, pdn, up, pup)

			print ''




def check_args(args):

	# improve this!

	if not args.systematics and args.inputfile is not None and args.did is None:
		print 'Please especify DSID of file (--did XXXXXX)'
		return -1
	if args.sample is not None and args.inputfile is not None:
		print 'Input can only be a sample name or a file'
		return -1
	if args.systematics and (args.inputfile is None or args.outputdir is None):
		print 'Please set an inputfile and outputdir'
		return -1



parser = argparse.ArgumentParser()

parser.add_argument('--sample', dest='sample', type=str, default=None)
parser.add_argument('--year', dest='year', type=str)
parser.add_argument('--version', dest='version', type=str, default='v75_2_theosyst')

parser.add_argument('--regions', dest='regions', type=str, default='regions/regions.py')

parser.add_argument('--systematics', action='store_true')
parser.add_argument('--inputfile', dest='inputfile', type=str, default=None)
parser.add_argument('--inputdir', dest='inputdir', type=str, default=None)
parser.add_argument('--outputdir', dest='outputdir', type=str, default='output/syst/test')
parser.add_argument('--outputfile', dest='outputfile', type=str, default='output/syst/test.root')

parser.add_argument('--truth', action='store_true')

parser.add_argument('--sample_path', dest='sample_path', type=str, default = '/eos/user/g/goorella/data/mini2/')

parser.add_argument('--did', dest='did', type=str, default=None)

parser.add_argument('--plot_theo_syst', action='store_true')
parser.add_argument('--tag', dest='tag', type=str, default='tag')

args = parser.parse_args()
check_args(args)

reg = imp.load_source('', args.regions)

year = args.year
version = args.version

truth = args.truth


inputdir = args.inputdir
outputdir = args.outputdir
outputfile = args.outputfile

sample_path = args.sample_path

if __name__ == '__main__':
	main()
#  

