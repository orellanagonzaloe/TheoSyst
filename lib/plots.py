 #! /usr/bin/env python

import os
from array import array 
import math
import glob
import subprocess
import imp
import ctypes
import yaml


import ROOT
ROOT.gROOT.SetBatch(True)
from ROOT import *

samLatex = {
	'photonjet'      : '#gamma + jets',
	'ttgamma'        : 't#bar{t}#gamma',
	'wgamma'         : 'W#gamma',
	'zllgamma'       : 'Z(ll)#gamma',
	'znunugamma'     : 'Z(#nu#nu)#gamma',
	'vgammagamma'    : 'W#gamma#gamma/Z#gamma#gamma',
	'diphoton'       : '#gamma#gamma',
}


varLabels = {'Nominal' : 'Statistical', 'PDF_ME' : 'PDF ME', 'alphaS' : 'alphaS', 'scale_ME' : 'Scale ME','scale_ME_NP_muR' : 'Scale ME muR', 'scale_ME_NP_muF' : 'Scale ME muF', 'scale_ME_NP_muRmuF' : 'Scale ME muR+muF', 'altPDF1' : 'altPDF1', 'altPDF2' : 'altPDF2', 'NP_PDFalpha' : 'PDF+alpha', 'NP_PDFalpha2' : 'PDF ME', 'Total' : 'Total Syst'}

varLabelsHF = {'Nominal' : 'stat', 'PDF_ME' : 'PDF_ME', 'alphaS' : 'alphaS', 'scale_ME' : 'scale_ME','scale_ME_NP_muR' : 'scale_muR', 'scale_ME_NP_muF' : 'scale_muF', 'scale_ME_NP_muRmuF' : 'scale_muRmuF', 'altPDF1' : 'altPDF1', 'altPDF2' : 'altPDF2', 'NP_PDFalpha' : 'PDFalpha', 'NP_PDFalpha2' : 'PDFalpha', 'Total' : 'total'}



def safeDiv(x,y):
	if y == 0:
		return 0
	return x / y


def safeDiv2(x,y):
	if y <= 0:
		return 0
	return x / y



def setupPlot(cfg):

	regions = imp.load_source('', cfg['inputDir']+'regions.py').regions

	allInfo = {}

	for sam in cfg['plot_samples']:

		# print sam

		allInfo[sam] = {}

		for yr in cfg['plot_years']:

			# print yr

			allInfo[sam][yr] = {}

			with open('%s/syst_%s_%s_weightList.yaml' % (cfg['inputDir'], sam, yr), 'r') as file:
				cfgWeights = yaml.safe_load(file)


			allInfo[sam][yr]['varOrder'] = []
			allInfo[sam][yr]['varLabel'] = []
			allInfo[sam][yr]['varFiles'] = []

			for _type in cfg['varOrder']:
				
				for weight in cfgWeights:

					if cfgWeights[weight]['type'] == _type:

						file = '%s/syst_%s_%s/%s.root' % (cfg['inputDir'], sam, yr, weight)

						if len(glob.glob(file))>0:

							if _type == 'altPDF' and 'altPDF1' not in allInfo[sam][yr]['varLabel']:

								allInfo[sam][yr]['varOrder'].append('altPDF1')
								allInfo[sam][yr]['varLabel'].append('altPDF1')

							elif _type == 'altPDF':

								allInfo[sam][yr]['varOrder'].append('altPDF2')
								allInfo[sam][yr]['varLabel'].append('altPDF2')

							else:

								allInfo[sam][yr]['varOrder'].append(_type)
								allInfo[sam][yr]['varLabel'].append(varLabels[_type])
							
							allInfo[sam][yr]['varFiles'].append(file)

				if _type == 'Total':

					allInfo[sam][yr]['varOrder'].append(_type)
					allInfo[sam][yr]['varLabel'].append(varLabels[_type])
					allInfo[sam][yr]['varFiles'].append('%s/syst_%s_%s/all.root' % (cfg['inputDir'], sam, yr))

			for reg in regions:

				# print reg

				allInfo[sam][yr][reg] = {}

				yVals = array('f')
				xVals = array('f')
				xErr = array('f')
				yDn = array('f')
				yUp = array('f')

				for i,file in enumerate(allInfo[sam][yr]['varFiles']):
			
					inputfile = ROOT.TFile(file)
					tgae = inputfile.Get('%s_nevents' % reg)
						
					x = ctypes.c_double(0.) # x = ROOT.Double(0)
					y = ctypes.c_double(0.) # y = ROOT.Double(0)
					tgae.GetPoint(0, x, y)

					_y = y.value
					_yDn = tgae.GetErrorYlow(0)
					_yUp = tgae.GetErrorYhigh(0)
					
					xVals.append(ROOT.Double(i+0.5))
					xErr.append(ROOT.Double(0.5))
					yVals.append(_y)
					yDn.append(_yDn)
					yUp.append(_yUp)
					

					# for altPDF in the diagram plot we show the difference w.r.t. it's own central, but
					# in the table the errors are w.r.t. to the Nominal central, because that's
					# how it's computed in the Total (because of the Envelope)
					var = allInfo[sam][yr]['varOrder'][i]

					if 'altPDF' in var:

						_yDn = abs(_y - _yDn - yVals[0])
						_yUp = abs(_y + _yUp - yVals[0])
						_y = yVals[0]

					allInfo[sam][yr][reg][var] = (_y, _yDn, _yUp)

					allInfo[sam][yr][reg]['tgae'] = (xVals, yVals, xErr, yDn, yUp)


	return allInfo



def plotDiagrams(cfg, allInfo):

	regions = imp.load_source('', cfg['inputDir']+'regions.py').regions

	outputDir = '%s/%s' % (cfg['eosPathPlot'], cfg['tag'])

	if not os.path.exists(outputDir):
		os.makedirs(outputDir)


	for sam in cfg['plot_samples']:

		# print sam

		for yr in cfg['plot_years']:

			# print yr

			for reg in regions:

				# print reg

				xVals, yVals, xErr, yDn, yUp = allInfo[sam][yr][reg]['tgae']

				# canvas setup 

				can = ROOT.TCanvas()	

				ROOT.gPad.SetRightMargin(0.05)
				ROOT.gPad.SetTopMargin(0.05)

				ROOT.gStyle.SetOptStat(0)
				# ROOT.gStyle.SetOptTitle(0)

				can.cd()
				can.SetLeftMargin(0.2)

				cup   = ROOT.TPad('u', 'u', 0., 0.305, 0.99, 1)
				cdown = ROOT.TPad('d', 'd', 0., 0.01, 0.99, 0.295)
				cup.SetRightMargin(0.05)
				cup.SetBottomMargin(0.005)

				cup.SetTickx()
				cup.SetTicky()
				ROOT.gPad.Update()
				ROOT.gPad.RedrawAxis()
				cdown.SetTickx()
				cdown.SetTicky()
				cdown.SetRightMargin(0.05)
				cdown.SetLeftMargin(2.)
				cdown.SetBottomMargin(0.25)
				cdown.SetTopMargin(0.0054)
				cdown.SetFillColor(ROOT.kWhite)
				cup.Draw()
				cdown.Draw()

				# cup.SetTopMargin(0.005)

				# ROOT.gStyle.SetOptStat( 0 )
				# ROOT.gStyle.SetOptTitle(0)
				# ROOT.gPad.SetRightMargin(0.05)
				# ROOT.gPad.SetTopMargin(0.05)

				cup.cd()
				cup.SetGridx()

				
				# plots in upper canvas 


				# diagram

				tgae = ROOT.TGraphAsymmErrors(len(yVals), xVals, yVals, xErr, xErr, yDn, yUp)

				tgae.SetFillColorAlpha(ROOT.TColor.GetColor('#39a0ed'),0.9)
				tgae.SetFillStyle(1001)

				# dummy histogram to put bin axis/labels and plot setup

				tmpH1Up = ROOT.TH1D('tmpH1Up', 'tmpH1Up', len(yVals), 0, len(yVals))
				tmpH1Up.SetDirectory(0)

				for i, var in enumerate(allInfo[sam][yr]['varOrder']):
					tmpH1Up.GetXaxis().SetBinLabel(i+1,'')

				tmpH1Up.SetLineColor(ROOT.kWhite)
				tmpH1Up.SetTitle('%s_%s_%s' % (reg, sam, yr))
				tmpH1Up.GetYaxis().SetTitle( '# events' )
				
				maxErr = max(max(yUp), max(yDn))  
				yRangeDn = TMath.MinElement(len(allInfo[sam][yr]['varOrder']), tgae.GetY()) - max(yDn) - 0.05 * maxErr
				yRangeUp = TMath.MaxElement(len(allInfo[sam][yr]['varOrder']), tgae.GetY()) + max(yUp) + 0.05 * maxErr
				tmpH1Up.GetYaxis().SetRangeUser(yRangeDn, yRangeUp) 


				tmpH1Up.Draw()    
				tgae.Draw('z2 same')

				# lines upper

				line = TLine()
				line.SetLineColor(ROOT.kGray)
				line.SetLineStyle(7)
				line.SetY1(yVals[0])
				line.SetY2(yVals[0])
				line.SetX1(0)
				line.SetX2(len(yVals))

				# altPDFs (and hence Total) needs special lines

				_addition = 0
				for var in allInfo[sam][yr]['varOrder']:
					if 'altPDF' in var or var == 'Total':
						_addition += 1

				_lastX2 = len(yVals) - _addition


				for i, var in enumerate(allInfo[sam][yr]['varLabel']):

					if var == 'altPDF1':

						line.SetX2(line.GetX2() - 1)

						lineAtlPDF1 = TLine()
						lineAtlPDF1.SetY1(yVals[i])
						lineAtlPDF1.SetY2(yVals[i])
						lineAtlPDF1.SetX1(_lastX2)
						lineAtlPDF1.SetX2(_lastX2 + 1)
						lineAtlPDF1.SetLineColor(ROOT.kGray)
						lineAtlPDF1.SetLineStyle(7)

						lineAtlPDF1.Draw('same')

						_lastX2+=1

					if var == 'altPDF2':

						line.SetX2(line.GetX2() - 1)

						lineAtlPDF2 = TLine()
						lineAtlPDF2.SetY1(yVals[i])
						lineAtlPDF2.SetY2(yVals[i])
						lineAtlPDF2.SetX1(_lastX2)
						lineAtlPDF2.SetX2(_lastX2+1)
						lineAtlPDF2.SetLineColor(ROOT.kGray)
						lineAtlPDF2.SetLineStyle(7)

						lineAtlPDF2.Draw('same')

						_lastX2+=1

					if var == 'Total Syst':

						line.SetX2(line.GetX2() - 1)

						lineTotal = TLine()
						lineTotal.SetY1(yVals[0])
						lineTotal.SetY2(yVals[0])
						lineTotal.SetX1(_lastX2)
						lineTotal.SetX2(_lastX2+1)
						lineTotal.SetLineColor(ROOT.kGray)
						lineTotal.SetLineStyle(7)

						lineTotal.Draw('same')

						_lastX2+=1


				line.Draw('same')


				ROOT.gPad.Update()
				ROOT.gPad.RedrawAxis()

				cdown.cd()
				cdown.SetGridx()



				# plots lower canvas

				# diagrams 

				MG = ROOT.TMultiGraph()

				_ratioDn = array('f')
				_ratioUp = array('f')

				for yVal, yDn, yUp in zip(yVals, yDn, yUp):

					if yVal != 0:

						_ratioDn.append(-100*yDn/yVal)
						_ratioUp.append(100*yUp/yVal)

					else:

						_ratioDn.append(0)
						_ratioUp.append(0)

				ratioDn = ROOT.TGraphErrors(len(yVals), xVals, _ratioDn, xErr)
				ratioUp = ROOT.TGraphErrors(len(yVals), xVals, _ratioUp, xErr)

				ratioDn.SetLineColor(ROOT.TColor.GetColor('#ef2d56'))
				ratioDn.SetLineWidth(2)
				ratioUp.SetLineColor(ROOT.TColor.GetColor('#284b63'))
				ratioUp.SetLineWidth(2)

				MG.Add(ratioDn)
				MG.Add(ratioUp)

				# dummy histogram to put labels nad plot setup

				tmpH1Dn = ROOT.TH1D('tmpH1Dn', 'tmpH1Dn', len(yVals), 0, len(yVals))
				tmpH1Dn.SetDirectory(0)

				for i,var in enumerate(allInfo[sam][yr]['varLabel']):
					tmpH1Dn.GetXaxis().SetBinLabel(i+1, var)

				tmpH1Dn.SetLineColor(ROOT.kWhite)
				tmpH1Dn.SetTitle('')

				minErr = TMath.MinElement(len(allInfo[sam][yr]['varOrder']),ratioDn.GetY())
				maxErr = TMath.MaxElement(len(allInfo[sam][yr]['varOrder']),ratioUp.GetY())

				yRangeDn = minErr - 0.15 * max(abs(maxErr), abs(minErr))
				yRangeUp = maxErr + 0.15 * max(abs(maxErr), abs(minErr))

				tmpH1Dn.GetYaxis().SetRangeUser(yRangeDn, yRangeUp)
				tmpH1Dn.GetXaxis().SetLabelSize(0.10)
				tmpH1Dn.GetYaxis().SetLabelSize(0.10)
				tmpH1Dn.GetYaxis().SetTitle( '% error' )
				tmpH1Dn.GetYaxis().SetTitleSize(0.1)
				tmpH1Dn.GetYaxis().SetTitleOffset(0.5)


				line2 = TLine()
				line2.SetY1(0)
				line2.SetY2(0)
				line2.SetX1(0)
				line2.SetX2(len(yVals))
				line2.SetLineColor(ROOT.kGray)
				line2.SetLineStyle(7)


				tmpH1Dn.Draw() 
				MG.Draw('z')
				line2.Draw('same')


				can.Draw()


				can.Print('%s/syst_%s_%s_%s.pdf' % (outputDir, reg, sam, yr))
				can.Close()

	print '\nMerging pdf files in %s/all.pdf' % (outputDir)

	if os.path.isfile('%s/all.pdf' % outputDir):
		os.remove('%s/all.pdf' % outputDir)

	bashCommand = 'pdfunite %s/*.pdf %s/all.pdf' % (outputDir, outputDir)
	process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE, shell=True)
	output, error = process.communicate()

	print 'Done\n'


def latexTables(cfg, allInfo):

	regions = imp.load_source('', cfg['inputDir']+'regions.py').regions

	outputFile = '%s/%s/syst_table.tex' % (cfg['eosPathPlot'], cfg['tag'])

	print 'Latex table: %s' % outputFile

	tableOutput = open(outputFile, 'w')

	tableOutput.write('\\documentclass[a4paper,12pt,twoside,spanish]{article}\n')
	tableOutput.write('\\usepackage[legalpaper, landscape, margin=0.2in]{geometry}\n')
	tableOutput.write('\\usepackage{multirow}\n')
	tableOutput.write('\\usepackage{graphicx}\n')
	tableOutput.write('\\usepackage{caption}\n')
	tableOutput.write('\\begin{document}\n')
	tableOutput.write('\\centering\n')

	for yr in cfg['plot_years']:

		# tableOutput.write('\\begin{table}\\caption*{Avg Total Syst %s}\n' % yr)
		tableOutput.write('\\begin{table}\\caption*{Max Syst %s}\n' % yr)
		tableOutput.write('\\begin{tabular}{ r ' + '| c ' *len(regions.keys()) + '}\n')

		tableOutput.write('\\hline\n')

		line = ' '
		for reg in regions:

			line += ' & %s' % reg
		line+='\\\\\n'

		tableOutput.write(line)

		tableOutput.write('\\hline\n')

		for sam in cfg['plot_samples']:

			line = '$%s$' % samLatex[sam].replace('#','\\')

			for reg in regions:

				# Average of Up and Dn Total
				# avg = (allInfo[sam][yr][reg]['Total'][1] + allInfo[sam][yr][reg]['Total'][2])/2.
				# value = 100.*safeDiv(avg, allInfo[sam][yr][reg]['Total'][0])

				# Max between all Vars Up and Dn
				maxVar = 0
				for var in allInfo[sam][yr]['varOrder']: 

					dnErrPer = 100.*safeDiv(allInfo[sam][yr][reg][var][1],allInfo[sam][yr][reg][var][0])
					upErrPer = 100.*safeDiv(allInfo[sam][yr][reg][var][2],allInfo[sam][yr][reg][var][0])

					maxVar = max([maxVar, dnErrPer, upErrPer])

				value = maxVar

				line += ' & %.2f\\%%' % (value)

			line += '\\\\\n'

			tableOutput.write(line)

		tableOutput.write('\\hline\n')
		tableOutput.write('\\end{tabular}\n')
		tableOutput.write('\\end{table}\n')


	for sam in cfg['plot_samples']:

		for yr in cfg['plot_years']:

			tableOutput.write('\\begin{table}\\caption*{%s %s}\n' % (sam.replace('_',''), yr))
			tableOutput.write('\\resizebox{\\textwidth}{!}{\\begin{tabular}{l | c ' + '| c c ' *len(allInfo[sam][yr]['varOrder']) + '}\n')

			line = '\\multirow{2}{*}{Region} & \\multirow{2}{*}{Events} & '

			for f in allInfo[sam][yr]['varLabel']: 
				line += '\\multicolumn{2}{|c}{'+ f + '} & '

			line = line.replace('_','\\_')
			line = line[:-2] + '\\\\\n'
			tableOutput.write(line)

			tableOutput.write('\\cline{3-%i}' % (2*(len(allInfo[sam][yr]['varOrder'])+1)) )

			line = ' & & ' + ' $\\Delta^{-}$ & $\\Delta^{+}$ &' * len(allInfo[sam][yr]['varOrder'])
			line = line[:-2] + '\\\\\n'
			tableOutput.write(line)

			tableOutput.write('\\hline\n')

			regType = regions.keys()[0][0] # first letter in region name
			for reg in regions:

				if not reg.startswith(regType):
					regType = reg[0]
					tableOutput.write('\\hline\n')


				line = '%s & %.2f & ' % (reg, allInfo[sam][yr][reg]['Nominal'][0])
				for var in allInfo[sam][yr]['varOrder']: 

					dnErr = allInfo[sam][yr][reg][var][1]
					upErr = allInfo[sam][yr][reg][var][2]
					dnErrPer = 100. * safeDiv(allInfo[sam][yr][reg][var][1], allInfo[sam][yr][reg][var][0])
					upErrPer = 100. * safeDiv(allInfo[sam][yr][reg][var][2], allInfo[sam][yr][reg][var][0])

					tmpLine = '%.2f (%.2f \\%%) & %.2f (%.2f \\%%) & ' % (dnErr, dnErrPer, upErr, upErrPer)

					line += tmpLine 

				line = line[:-2] + '\\\\\n'
				tableOutput.write(line)

			tableOutput.write('\\end{tabular}}\n')
			tableOutput.write('\\end{table}\n')

	tableOutput.write('\\end{document}\n')
	tableOutput.close()

	print 'Done!\n'
	

def HFinput(cfg, allInfo):

	# input for hist fitter

	if 'fullR2' not in cfg['plot_years']:
		print 'HF input is only available for fullR2, please include it in the config file'
		return

	regions = imp.load_source('', cfg['inputDir']+'regions.py').regions

	outputFile = '%s/%s/config_input.py' % (cfg['eosPathPlot'], cfg['tag'])

	print 'Input for HF: %s' % outputFile

	HFconfig = open(outputFile, 'w')

	for sam in cfg['plot_samples']:

		for reg in regions:

			for var in allInfo[sam]['fullR2']['varOrder']:

				if var == 'Nominal': continue

				valNP = allInfo[sam]['fullR2'][reg][var][0]
				valNPUp = allInfo[sam]['fullR2'][reg][var][1]
				valNPDn = allInfo[sam]['fullR2'][reg][var][2]

				varHF = varLabelsHF[var]

				if valNP == 0:

					HFconfig.write('sigma_%s_%s_%s_up = 0. # 0 events in region \n' % (sam, reg, varHF))
					HFconfig.write('sigma_%s_%s_%s_dn = 0. # 0 events in region \n' % (sam, reg, varHF))

				else:

					HFconfig.write('sigma_%s_%s_%s_up = %f \n' % (sam, reg, varHF, valNPUp/valNP))
					HFconfig.write('sigma_%s_%s_%s_dn = %f \n' % (sam, reg, varHF, valNPDn/valNP))

	HFconfig.close()

	print 'Done!'


