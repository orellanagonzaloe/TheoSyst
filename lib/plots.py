 #! /usr/bin/env python

import os
from array import array 
import math
import glob
import subprocess
import imp
import ctypes

import ROOT
ROOT.gROOT.SetBatch(True)
from ROOT import *

d_samples = {
	'photonjet'      : '#gamma + jets',
	'ttgamma'        : 't#bar{t}#gamma',
	'wgamma'         : 'W#gamma',
	'zllgamma'       : 'Z(ll)#gamma',
	'znunugamma'     : 'Z(#nu#nu)#gamma',
	'vgammagamma'    : 'W#gamma#gamma/Z#gamma#gamma',
	'diphoton'       : '#gamma#gamma',
}

label_dict = {'Sherpa_ME_PDF13000.root':'alt_PDF1', 'Sherpa_ME_PDF25300.root':'alt_PDF2', 'Sherpa_ME_PDF261000_alphaS_NNPDF_NNLO.root':'alphaS', 'Sherpa_ME_PDF261000_scale.root':'Scale', 'Sherpa_ME_PDF261000_var.root':'PDF_ME', 'Sherpa_PDF261000_Nominal.root':'Statistical', 'aMcAtNlo_PDF260000_Nominal_type2.root' : 'Statistical', 'aMcAtNlo_ME_PDF260000_scale_type2.root' : 'Scale' , 'aMcAtNlo_ME_PDF260000_var_type2.root' : 'PDF_ME', 'all.root' : 'Total Syst', 'Sherpa_PDF261000_Normalisation.root':'Normalisation'}

d_colors = {
	'alt_PDF1'    : '#f7fab5',
	'alt_PDF2'         : '#f8f59b',
	'Statistical'          : '#a4cee6',
	'PDF_ME'          : '#348ABD',
	'Scale'       : '#348ABD',
	'alphaS'          : '#BCBC93',
	'Total Syst'          : '#36BDBD',
}

def setup_output(cfg):

	d_results = {}

	regions = imp.load_source('', cfg['inputDir']+'regions.py').regions

	for sam in cfg['plot_samples']:

		d_results[sam] = {}

		for yr in cfg['plot_years']:

			d_results[sam][yr] = {}

			files = glob.glob(cfg['inputDir']+'syst_'+sam+'_'+yr+'/*.root')

			index = [i for i,f in enumerate(files) if 'Nominal' in f][0]
			f_tmp = files[index]
			files.pop(index)
			files.insert(0, f_tmp)

			y_nom = array('f')

			variations = []

			for i,f in enumerate(files):
				
				var_syst = label_dict[f.split('/')[-1]]

				variations.append(var_syst)

				d_results[sam][yr][var_syst] = {}
				
				inputfile = ROOT.TFile(f)

				x = array('f')
				dx = array('f')
				y = array('f')
				dy_dn = array('f')
				dy_up = array('f')
				
				for j, reg in enumerate(regions):

					tgae_tmp = inputfile.Get(reg+'_nevents')
					
					x_tmp = ctypes.c_double(0.)
					y_tmp = ctypes.c_double(0.)

					tgae_tmp.GetPoint(0, x_tmp, y_tmp)
					y_dn_tmp = tgae_tmp.GetErrorYlow(0)
					y_up_tmp = tgae_tmp.GetErrorYhigh(0)

					if i == 0:
						y_nom.append(y_tmp.value)

					if 'alt_PDF' in var_syst:
						y_dn_tmp = abs(y_tmp.value - y_dn_tmp - y_nom[j])
						y_up_tmp = abs(y_tmp.value + y_up_tmp - y_nom[j])
					
					d_results[sam][yr][var_syst][reg] = (y_tmp.value, y_dn_tmp, y_up_tmp)

					x.append(ROOT.Double(j+0.5))
					dx.append(ROOT.Double(0.5))
					y.append(0.)
					dy_dn.append(100.*safeDiv(y_dn_tmp, y_nom[j]))
					dy_up.append(100.*safeDiv(y_up_tmp, y_nom[j]))

				d_results[sam][yr][var_syst]['TGAE'] = ROOT.TGraphAsymmErrors(len(files), x, y, dx, dx, dy_dn, dy_up)

			d_results[sam][yr]['variations'] = variations

	plots(cfg, d_results, 'wgamma', 'fullR2')


def plots(cfg, d_results, sam, yr):

	canvas = ROOT.TCanvas()

	regions = imp.load_source('', cfg['inputDir']+'regions.py').regions

	h_tmp_1 = ROOT.TH1D('h_tmp_1', 'h_tmp_1', len(regions), 0, len(regions))

	for i,r in enumerate(regions):
		h_tmp_1.GetXaxis().SetBinLabel(i+1,r)
	h_tmp_1.SetLineColor(ROOT.kWhite)
	h_tmp_1.GetYaxis().SetRangeUser(-60., 80.) 
	h_tmp_1.GetYaxis().SetTitle( '% Uncertainty' )
	h_tmp_1.Draw('same')    

	MG = ROOT.TMultiGraph()
	gStyle.SetPalette(ROOT.kRainBow)

	var = d_results[sam][yr]['variations']
	index = [i for i,f in enumerate(var) if 'Scale' in f]
	if len(index)>0:
		f_tmp = var[index[0]]
		var.pop(index[0])
		var.insert(0, f_tmp)
	index = [i for i,f in enumerate(var) if 'Total Syst' in f]
	if len(index)>0:
		f_tmp = var[index[0]]
		var.pop(index[0])
		var.insert(0, f_tmp)

	for v in d_results[sam][yr]['variations']:

		d_results[sam][yr][v]['TGAE'].SetFillColorAlpha(ROOT.TColor.GetColor(d_colors[v]), 0.7)
		d_results[sam][yr][v]['TGAE'].SetLineColor(ROOT.kBlack)
		MG.Add(d_results[sam][yr][v]['TGAE'])


	MG.Draw('25 pfc')


	line = TLine()
	line.SetY1(0.)
	line.SetY2(0.)
	line.SetX1(0.)
	line.SetX2(len(regions))
	line.SetLineColor(ROOT.kGray)
	line.SetLineStyle(7)

	line.Draw('same')

	if not os.path.exists(cfg['eosPathPlot'] + cfg['tag']):
		os.makedirs(cfg['eosPathPlot'] + cfg['tag'])

	canvas.Print(cfg['eosPathPlot'] + cfg['tag'] + '/test.pdf')



def plots_tmp(cfg):

	# UNDER CONSTRUCTION!!!!


	regions = imp.load_source('', cfg['inputDir']+'regions.py').regions

	if not os.path.exists(cfg['eosPathPlot']):
		os.makedirs(cfg['eosPathPlot'])

	dict_all = {}
	lst_vars = {}

	for sam in cfg['plot_samples']:

		# print sam

		dict_all[sam] = {}

		for yr in cfg['plot_years']:

			# print yr

			dict_all[sam][yr] = {}

			for reg in regions:

				# print reg

				dict_all[sam][yr][reg] = {}

				lst_vars[sam] = glob.glob(cfg['inputDir']+'syst_'+sam+'_'+yr+'/*.root')

				# if 'output/syst/syst_'+sam+'_'+yr+'/all.root' in lst_vars[sam]:
				# 	lst_vars[sam].remove('output/syst/syst_'+sam+'_'+yr+'/all.root')

				nom_ele = [s for s in lst_vars[sam] if 'Nominal' in s]
				pdf_me_ele = [s for s in lst_vars[sam] if 'PDF_ME' in label_dict[s.split('/')[-1]]]
				altpdf1_ele = [s for s in lst_vars[sam] if 'Sherpa_ME_PDF25300' in s]
				altpdf2_ele = [s for s in lst_vars[sam] if 'Sherpa_ME_PDF13000' in s]
				all_ele = [s for s in lst_vars[sam] if 'all' in s]

				lst_vars[sam].insert(0, lst_vars[sam].pop(lst_vars[sam].index(nom_ele[0])))
				if len(pdf_me_ele)>0:
					lst_vars[sam].append(lst_vars[sam].pop(lst_vars[sam].index(pdf_me_ele[0])))
				if len(altpdf1_ele)>0:
					lst_vars[sam].append(lst_vars[sam].pop(lst_vars[sam].index(altpdf1_ele[0])))
				if len(altpdf1_ele)>0:
					lst_vars[sam].append(lst_vars[sam].pop(lst_vars[sam].index(altpdf1_ele[0])))
				if len(altpdf2_ele)>0:
					lst_vars[sam].append(lst_vars[sam].pop(lst_vars[sam].index(altpdf2_ele[0])))
				if len(all_ele)>0:
					lst_vars[sam].append(lst_vars[sam].pop(lst_vars[sam].index(all_ele[0])))


				nom = array('f')
				xvar = array('f')
				xerr = array('f')
				ydn = array('f')
				yup = array('f')
				labels = []

				r_dn = array('f')
				r_up = array('f')

				y_nom = 0.
				for i,f in enumerate(lst_vars[sam]):
			
					inputfile = ROOT.TFile(f)
					tgae_tmp = inputfile.Get(reg+'_nevents')
						
					x = ctypes.c_double(0.) # x = ROOT.Double(0)
					y = ctypes.c_double(0.) # y = ROOT.Double(0)
					tgae_tmp.GetPoint(0,x,y)
					y = y.value
					dy_dn = tgae_tmp.GetErrorYlow(0)
					dy_up = tgae_tmp.GetErrorYhigh(0)

					if i == 0: y_nom = y
					
					xvar.append(ROOT.Double(i+0.5))
					xerr.append(ROOT.Double(0.5))
					nom.append(y)
					ydn.append(dy_dn)
					yup.append(dy_up)
					
					if y!=0:
						r_dn.append(-100*dy_dn/y)
						r_up.append(100*dy_up/y)
					else:
						r_dn.append(0)
						r_up.append(0)

					label = label_dict[f.split('/')[-1]]

					if 'alt_PDF' in label:
						dy_dn = abs(y - dy_dn - y_nom)
						dy_up = abs(y + dy_up - y_nom)
						y = y_nom

					dict_all[sam][yr][reg][label] = (y, dy_dn, dy_up)
				

				max_error = max( max(yup), max(ydn) )  

				tgae = ROOT.TGraphAsymmErrors(len(nom),xvar,nom,xerr,xerr,ydn,yup)


				h_tmp_1 = ROOT.TH1D('h_tmp_1','h_tmp_1',len(lst_vars[sam]),0,len(lst_vars[sam]))
				h_tmp_2 = ROOT.TH1D('h_tmp_2','h_tmp_2',len(lst_vars[sam]),0,len(lst_vars[sam]))

				ratio_dn = ROOT.TGraphErrors(len(nom),xvar,r_dn,xerr)
				ratio_up = ROOT.TGraphErrors(len(nom),xvar,r_up,xerr)
				MG = ROOT.TMultiGraph()

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

				line = TLine()
				line.SetY1(nom[0])
				line.SetY2(nom[0])
				line.SetX1(0)
				line.SetX2(len(nom)-3)
				if sam == 'ttgamma':
					line.SetX2(len(nom))
				line.SetLineColor(ROOT.kGray)
				line.SetLineStyle(7)


				if sam != 'ttgamma':

					line_atlpdf1 = TLine()
					line_atlpdf1.SetY1(nom[-3])
					line_atlpdf1.SetY2(nom[-3])
					line_atlpdf1.SetX1(len(nom)-3)
					line_atlpdf1.SetX2(len(nom)-2)
					line_atlpdf1.SetLineColor(ROOT.kGray)
					line_atlpdf1.SetLineStyle(7)

					line_atlpdf2 = TLine()
					line_atlpdf2.SetY1(nom[-2])
					line_atlpdf2.SetY2(nom[-2])
					line_atlpdf2.SetX1(len(nom)-2)
					line_atlpdf2.SetX2(len(nom)-1)
					line_atlpdf2.SetLineColor(ROOT.kGray)
					line_atlpdf2.SetLineStyle(7)

					line_total = TLine()
					line_total.SetY1(nom[0])
					line_total.SetY2(nom[0])
					line_total.SetX1(len(nom)-1)
					line_total.SetX2(len(nom))
					line_total.SetLineColor(ROOT.kGray)
					line_total.SetLineStyle(7)



				for i,f in enumerate(lst_vars[sam]):
					h_tmp_1.GetXaxis().SetBinLabel(i+1,'')

				h_tmp_1.SetLineColor(ROOT.kWhite)
				h_tmp_1.SetTitle(reg+' '+sam+' '+yr)
				
				h_tmp_1.GetYaxis().SetRangeUser(TMath.MinElement(len(lst_vars[sam]),tgae.GetY())-max(ydn)-0.05*max_error,TMath.MaxElement(len(lst_vars[sam]),tgae.GetY())+max(yup)+0.05*max_error) 
				h_tmp_1.GetYaxis().SetTitle( '# events' )
				h_tmp_1.Draw()    

				tgae.SetFillColorAlpha(ROOT.TColor.GetColor('#39a0ed'),0.9)
				tgae.SetFillStyle(1001)

				tgae.Draw('z2 same')
				line.Draw('same')

				if sam != 'ttgamma':
					line_atlpdf1.Draw('same')
					line_atlpdf2.Draw('same')
					line_total.Draw('same')

				ROOT.gPad.Update()
				ROOT.gPad.RedrawAxis()


				cdown.cd()
				cdown.SetGridx()

				line2 = TLine()
				line2.SetY1(0)
				line2.SetY2(0)
				line2.SetX1(0)
				line2.SetX2(len(nom))
				line2.SetLineColor(ROOT.kGray)
				line2.SetLineStyle(7)


				for i,f in enumerate(lst_vars[sam]):
					label = label_dict[f.split('/')[-1]]
					h_tmp_2.GetXaxis().SetBinLabel(i+1,label)

				h_tmp_2.SetLineColor(ROOT.kWhite)
				h_tmp_2.SetTitle('')


				range_up = TMath.MaxElement(len(lst_vars[sam]),ratio_up.GetY())
				range_dn = TMath.MinElement(len(lst_vars[sam]),ratio_dn.GetY())

				h_tmp_2.GetYaxis().SetRangeUser( range_dn-0.15*max(abs(range_up),abs(range_dn)) , range_up+0.15*max(abs(range_up),abs(range_dn)) )
				h_tmp_2.GetXaxis().SetLabelSize(0.10)
				h_tmp_2.GetYaxis().SetLabelSize(0.10)
				h_tmp_2.GetYaxis().SetTitle( '% error' )
				h_tmp_2.GetYaxis().SetTitleSize(0.1)
				h_tmp_2.GetYaxis().SetTitleOffset(0.5)
				h_tmp_2.Draw() 


				MG.Add(ratio_dn)
				ratio_dn.SetLineColor(ROOT.TColor.GetColor('#ef2d56'))
				ratio_dn.SetLineWidth(2)
				MG.Add(ratio_up)
				ratio_up.SetLineColor(ROOT.TColor.GetColor('#284b63'))
				ratio_up.SetLineWidth(2)

				MG.Draw('z')
				line2.Draw('same')


				can.Draw()


				can.Print(cfg['eosPathPlot'] + cfg['tag'] + '/syst_'+reg+'_'+sam+'_'+yr+'.pdf')
				can.Close()

	print 'Merging pdf files in %s' % (cfg['eosPathPlot'] + cfg['tag'] + '/all.pdf')

	if os.path.isfile(cfg['eosPathPlot'] + cfg['tag'] + '/all.pdf'):
		os.remove(cfg['eosPathPlot'] + cfg['tag'] + '/all.pdf')

	bashCommand = 'pdfunite %s%s/*.pdf %s%s/all.pdf' % (cfg['eosPathPlot'], cfg['tag'], cfg['eosPathPlot'], cfg['tag'])
	process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE, shell=True)
	output, error = process.communicate()

	print 'Done\n'

	print 'Creating tex in %s' % (cfg['eosPathPlot'] + cfg['tag'] + '/syst_table.tex')

	# print dict_all
	table_output = open (cfg['eosPathPlot'] + cfg['tag'] + '/syst_table.tex','w')

	table_output.write('\\documentclass[a4paper,12pt,twoside,spanish]{article}\n')
	table_output.write('\\usepackage[legalpaper, landscape, margin=0.2in]{geometry}\n')
	table_output.write('\\usepackage{multirow}\n')
	table_output.write('\\usepackage{graphicx}\n')
	table_output.write('\\usepackage{caption}\n')
	table_output.write('\\begin{document}\n')
	table_output.write('\\centering\n')

	table_output.write('\\begin{table}\\caption*{Avg fullR2 Total Syst}\n')
	table_output.write('\\begin{tabular}{ r ' + '| c ' *len(regions.keys()) + '}\n')

	table_output.write('\\hline\n')

	line = ' '
	for reg in regions:

		line += ' & %s' % reg
	line+='\\\\\n'

	table_output.write(line)

	table_output.write('\\hline\n')

	for sam in cfg['plot_samples']:

		line = '$%s$' % d_samples[sam].replace('#','\\')

		for reg in regions:

			avg = (dict_all[sam]['fullR2'][reg]['Total Syst'][1] + dict_all[sam]['fullR2'][reg]['Total Syst'][2])/2.

			line += ' & %.2f\\%%' % (100.*safeDiv(avg,dict_all[sam]['fullR2'][reg]['Total Syst'][0]))

		line += '\\\\\n'

		table_output.write(line)

	table_output.write('\\hline\n')
	table_output.write('\\end{tabular}\n')
	table_output.write('\\end{table}\n')


	for sam in cfg['plot_samples']:
		for yr in cfg['plot_years']:
			table_output.write('\\begin{table}\\caption*{%s %s}\n' % (sam.replace('_',''), yr))
			table_output.write('\\resizebox{\\textwidth}{!}{\\begin{tabular}{l | c ' + '| c c ' *len(lst_vars[sam]) + '}\n')

			vars_tmp = '\\multirow{2}{*}{Region} & \\multirow{2}{*}{Events} & '

			for f in lst_vars[sam]: 
				vars_tmp += '\\multicolumn{2}{|c}{'+ label_dict[f.split('/')[-1]] + '} & '

			vars_tmp = vars_tmp.replace('_','\\_')
			vars_tmp = vars_tmp[:-2] + '\\\\\n'
			table_output.write(vars_tmp)

			table_output.write('\\cline{3-%i}' % (2*(len(lst_vars[sam])+1)) )

			vars2_tmp = ' & & ' + ' $\\Delta^{-}$ & $\\Delta^{+}$ &' * len(lst_vars[sam])
			vars2_tmp = vars2_tmp[:-2] + '\\\\\n'
			table_output.write(vars2_tmp)

			table_output.write('\\hline\n')

			reg_tmp = regions.keys()[0][0]
			for reg in regions:

				if not reg.startswith(reg_tmp):
					reg_tmp = reg[0]
					table_output.write('\\hline\n')

				label = label_dict[lst_vars[sam][0].split('/')[-1]]
				line = '%s & %.2f & ' % (reg, dict_all[sam][yr][reg][label][0])
				for f in lst_vars[sam]: 

					label = label_dict[f.split('/')[-1]]

					syst_tmp = '%.2f (%.2f \\%%) & %.2f (%.2f \\%%) & ' % (dict_all[sam][yr][reg][label][1], 100.*safeDiv(dict_all[sam][yr][reg][label][1],dict_all[sam][yr][reg][label][0]), dict_all[sam][yr][reg][label][2],100.*safeDiv(dict_all[sam][yr][reg][label][2],dict_all[sam][yr][reg][label][0]))

					line+=syst_tmp 

				line = line[:-2] + '\\\\\n'
				table_output.write(line)

			table_output.write('\\end{tabular}}\n')
			table_output.write('\\end{table}\n')

	table_output.write('\\end{document}\n')
	table_output.close()
	


	# input for hist fitter
	print 'Creating input for HF in %s' % (cfg['eosPathPlot'] + cfg['tag'] + '/config_input.py')
	config_input = open(cfg['eosPathPlot'] + cfg['tag'] + '/config_input.py','w')
	for sam in cfg['plot_samples']:
		for reg in regions:
			if dict_all[sam]['fullR2'][reg]['Total Syst'][0] == 0:
				config_input.write('sigma_%s_%s_up = 0. # 0 events in region \n' % (sam, reg))
				config_input.write('sigma_%s_%s_dn = 0. # 0 events in region \n' % (sam, reg))
			else:
				config_input.write('sigma_%s_%s_up = %f \n' % (sam, reg, dict_all[sam]['fullR2'][reg]['Total Syst'][2]/dict_all[sam]['fullR2'][reg]['Total Syst'][0]))
				config_input.write('sigma_%s_%s_dn = %f \n' % (sam, reg, dict_all[sam]['fullR2'][reg]['Total Syst'][1]/dict_all[sam]['fullR2'][reg]['Total Syst'][0]))
	config_input.close()


	print 'Done!'




def safeDiv(x,y):
	if y == 0:
		return 0
	return x / y


def safeDiv2(x,y):
	if y <= 0:
		return 0
	return x / y







def theo_syst_plots2(inputdir, tag, mod_reg):


	inputfile = ROOT.TFile(inputdir+'/syst_wgamma_20152016/all.root')
	tgae_all = inputfile.Get('CRQ_dphi_jetmet')
	print 'tgae_all'
	tgae_all.Print()
	inputfile = ROOT.TFile(inputdir+'/syst_wgamma_20152016/Sherpa_ME_PDF261000_scale.root')
	tgae_scale = inputfile.Get('CRQ_dphi_jetmet')
	print 'tgae_scale'
	tgae_scale.Print()
	inputfile = ROOT.TFile(inputdir+'/syst_wgamma_20152016/Sherpa_ME_PDF261000_alphaS_NNPDF_NNLO.root')
	tgae_alpha = inputfile.Get('CRQ_dphi_jetmet')
	print 'tgae_alpha'
	tgae_alpha.Print()
	inputfile = ROOT.TFile(inputdir+'/syst_wgamma_20152016/Sherpa_ME_PDF261000_var.root')
	tgae_pdfvar = inputfile.Get('CRQ_dphi_jetmet')
	print 'tgae_pdfvar'
	tgae_pdfvar.Print()
	inputfile = ROOT.TFile(inputdir+'/syst_wgamma_20152016/Sherpa_ME_PDF13000.root')
	tgae_pdf1 = inputfile.Get('CRQ_dphi_jetmet')
	print 'tgae_pdf1'
	tgae_pdf1.Print()
	inputfile = ROOT.TFile(inputdir+'/syst_wgamma_20152016/Sherpa_ME_PDF25300.root')
	tgae_pdf2 = inputfile.Get('CRQ_dphi_jetmet')
	print 'tgae_pdf2'
	tgae_pdf2.Print()
	inputfile = ROOT.TFile(inputdir+'/syst_wgamma_20152016/Sherpa_PDF261000_Nominal.root')
	tgae_nom = inputfile.Get('CRQ_dphi_jetmet')
	print 'tgae_nom'
	tgae_nom.Print()


	x, y, exl, exh, eyl, eyh = array('f'), array('f'), array('f'), array('f'), array('f'), array('f')
	for i in xrange(tgae_nom.GetN()):
		x_nom = ROOT.Double(0)
		y_nom = ROOT.Double(0)
		tgae_nom.GetPoint(i,x_nom,y_nom)
		x.append(x_nom)
		y.append(ROOT.Double(0))
		exl.append(tgae_nom.GetErrorX(i))
		exh.append(tgae_nom.GetErrorX(i))
		eyl.append(safeDiv2(100.*tgae_all.GetErrorYlow(i),y_nom))
		eyh.append(safeDiv2(100.*tgae_all.GetErrorYhigh(i),y_nom))


	tgae_ratio = ROOT.TGraphAsymmErrors(tgae_nom.GetN(), x, y, exl, exh, eyl, eyh)
	




	can = ROOT.TCanvas()
	legend = ROOT.TLegend(0.75,0.65,0.9,0.9)
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


	cup.cd()
	# cup.SetLogy()

	MG = ROOT.TMultiGraph()
	tgae_scale.SetFillColorAlpha(kAzure, 0.5)
	tgae_scale.SetLineColor(kAzure)
	legend.AddEntry( tgae_scale , 'scale' , 'f' )
	MG.Add(tgae_scale)
	tgae_pdf2.SetFillColorAlpha(kSpring, 0.5)
	tgae_pdf2.SetLineColor(kSpring)
	legend.AddEntry( tgae_pdf2 , 'pdf2' , 'f' )
	MG.Add(tgae_pdf2)
	tgae_alpha.SetFillColorAlpha(kOrange, 0.5)
	tgae_alpha.SetLineColor(kOrange)
	legend.AddEntry( tgae_alpha , 'alpha' , 'f' )
	MG.Add(tgae_alpha)
	tgae_pdfvar.SetFillColorAlpha(kRed, 0.5)
	tgae_pdfvar.SetLineColor(kRed)
	legend.AddEntry( tgae_pdfvar , 'pdfvar' , 'f' )
	MG.Add(tgae_pdfvar)
	tgae_pdf1.SetFillColorAlpha(kTeal, 0.5)
	tgae_pdf1.SetLineColor(kTeal)
	legend.AddEntry( tgae_pdf1 , 'pdf1' , 'f' )
	MG.Add(tgae_pdf1)
	tgae_all.SetFillColor(1)
	tgae_all.SetFillStyle(3004)
	legend.AddEntry( tgae_all , 'all' , 'f' )
	MG.Add(tgae_all)

	MG.Draw('a3 same')

	

	legend.SetTextSize(0.04)
	legend.SetBorderSize(0)
	legend.Draw('same')


	ROOT.gPad.Update()
	ROOT.gPad.RedrawAxis()

	cdown.cd()

	tgae_ratio.SetFillColorAlpha(kRed, 0.5)
	tgae_ratio.Draw('a3 same')




	can.Print(com.eos_path_plots+'syst/'+tag+'/syst_test.pdf')
