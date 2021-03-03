#! /usr/bin/env python

import os
import argparse
import imp
import yaml


def check_args(args):

	# under construction

	# if not args.systematics and args.inputfile is not None and args.did is None:
	# 	print 'Please especify DSID of file (--did XXXXXX)'
	# 	return -1
	# if args.sample is not None and args.inputfile is not None:
	# 	print 'Input can only be a sample name or a file'
	# 	return -1
	# if args.systematics and (args.inputfile is None or args.outputdir is None):
	# 	print 'Please set an inputfile and outputdir'
	# 	return -1

	return



###--- args ---###

parser = argparse.ArgumentParser()

parser.add_argument('--createHists', action='store_true')
parser.add_argument('--computeSyst', action='store_true')
parser.add_argument('--plots', action='store_true')

parser.add_argument('--sample', dest='sample', type=str, default=None)
parser.add_argument('--year', dest='year', type=str)

parser.add_argument('--regions', dest='regions', type=str, default='regions/regions.py')
parser.add_argument('--config', dest='config', type=str, default=None)

parser.add_argument('--inputDir', dest='inputDir', type=str, default=None)
parser.add_argument('--inputFile', dest='inputFile', type=str, default=None)
parser.add_argument('--inputSystFile', dest='inputSystFile', type=str, default=None)
parser.add_argument('--outputDir', dest='outputDir', type=str, default='output/syst/test')
parser.add_argument('--outputFile', dest='outputFile', type=str, default='output/syst/test.root')

parser.add_argument('--truth', dest='truth', type=str, default='.mini.')

parser.add_argument('--did', dest='did', type=str, default=None)

parser.add_argument('--tag', dest='tag', type=str, default='test_tag')

args = parser.parse_args()
check_args(args)


if args.outputDir[-1] != '/':
	args.outputDir += '/'
if args.inputDir is not None and args.inputDir[-1] != '/':
	args.inputDir += '/'


###--- config ---###

with open('config.yaml', 'r') as f:
	cfg = yaml.safe_load(f)

createHists = args.createHists
computeSyst = args.computeSyst
plots = args.plots

cfg['sample'] = args.sample
cfg['year'] = args.year

regions = imp.load_source('', args.regions).regions
config = args.config

cfg['inputDir'] = args.inputDir
cfg['inputFile'] = args.inputFile
cfg['outputFile'] = args.outputFile
	
cfg['sampleType'] = args.truth

cfg['did'] = args.did

cfg['tag'] = args.tag

config = args.config
if config is not None:

	with open(config, 'r') as f:
		cfg2 = yaml.safe_load(f)

	cfg2['inputSystFile'] = args.inputSystFile
	cfg2['outputDir'] = args.outputDir


###--- main ---###

if plots:

	import lib.plots as plt

	allInfo = plt.setupPlot(cfg)
	plt.plotDiagrams(cfg, allInfo)
	plt.latexTables(cfg, allInfo)
	plt.HFinput(cfg, allInfo)

	# plt.setup_output(cfg)
	# plt.plots_tmp(cfg)


elif computeSyst:

	import lib.systematics as sst

	sst.systematics(cfg2)

elif createHists:

	import lib.mini_draw as md
	
	md.initLoop(cfg, regions)


