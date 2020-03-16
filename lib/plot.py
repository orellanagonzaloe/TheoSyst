 #! /usr/bin/env python

import os
from array import array 
import math
import glob
import subprocess

import ROOT
ROOT.gROOT.SetBatch(True)
from ROOT import *

import lib.style as sty
import lib.common as com
import lib.grid_points as grd
import lib.regions as reg

def main(year, tag, unblind):

	for r in reg.regions:

		if not os.path.exists(com.eos_path_plots+'opt/'+tag+'/'+r):
			os.makedirs(com.eos_path_plots+'opt/'+tag+'/'+r)

		for var in com.variables:
			
			hists = fill_hists(var, r, year, unblind)

			plot(hists,var,r,tag,unblind, year)


def fill_hists(var, reg, year, unblind):

	hists = {}

	for i in com.samples:

		hists[i] = TH1D('', '', com.binning_dict[var][0], com.binning_dict[var][1], com.binning_dict[var][2] )
		hists[i].Sumw2()

		if 'data' in i and reg.startswith('SR') and not unblind:
			continue

		for yr in com.year_dict[year]:

			f = TFile('output/opt/'+i+'_'+yr+'.root')
			h_tmp = TH1D()
			if f.IsZombie():
				print ('\033[1;93mWARNING\033[0m: %s does not exist') % ('output/opt/'+i+'_'+yr+'.root')
				continue
			if not f.GetListOfKeys().Contains('h_dist_'+reg+'_'+com.clean_var(var)+'_'+yr):
				print ('\033[1;93mWARNING\033[0m: %s not in %s') % ('h_dist_'+reg+'_'+com.clean_var(var)+'_'+yr, 'output/opt/'+i+'_'+yr+'.root')
				continue
			h_tmp = f.Get('h_dist_'+reg+'_'+com.clean_var(var)+'_'+yr)
			h_tmp.SetDirectory(0)
			hists[i].Add(h_tmp)
			f.Close()

	return hists

def plot(hists, var, reg, tag, unblind, year):

	can = ROOT.TCanvas('', '', 800, 800)
	can.cd()
	can.SetLeftMargin(0.2)

	cup   = ROOT.TPad('u', 'u', 0., 0.305, 0.99, 1)
	cdown = ROOT.TPad('d', 'd', 0., 0.01, 0.99, 0.295)
	cup.SetRightMargin(0.05)
	cup.SetBottomMargin(0.005)

	cup.SetTickx()
	cup.SetTicky()
	cdown.SetTickx()
	cdown.SetTicky()
	cdown.SetRightMargin(0.05)
	cdown.SetLeftMargin(2.)
	cdown.SetBottomMargin(0.25)
	cdown.SetTopMargin(0.0054)
	cdown.SetFillColor(ROOT.kWhite)
	cup.Draw()
	cdown.Draw()



	cup.SetTopMargin(0.01)

	gStyle.SetOptStat( 0 )
	gStyle.SetOptTitle(0)
	gPad.SetRightMargin(0.05)
	gPad.SetTopMargin(0.05)

	cup.cd()
	cup.SetLogy()

	legend_bkg = TLegend(0.6,0.65,0.94,0.94)
	legend_bkg.SetTextSize(0.03)
	legend_bkg.SetBorderSize(0)
	legend_sig = TLegend(0.58,0.5,0.94,0.65)
	legend_sig.SetTextSize(0.03)
	legend_sig.SetBorderSize(0)

	hs = THStack()
	hist_sm = TH1D('','', com.binning_dict[var][0], com.binning_dict[var][1], com.binning_dict[var][2])
	h_max = []
	h_int = []
	samples_bkg = [i for i in com.samples if 'GGM_' not in i and 'MG_ph' not in i and 'data' not in i]
	samples_sig = [i for i in com.samples if 'GGM_' in i or 'MG_ph' in i]
	samples_dat = 'data' in com.samples and (not reg.startswith('SR') or reg.startswith('SR') and unblind )

	legend_bkg.SetNColumns(2);
	for i,h in enumerate(samples_bkg):
		h_max.append(hists[h].GetMaximum())
		h_int.append(hists[h].Integral(1, hists[h].GetNbinsX()), 'width')
		hists[h].GetBinWidth(1)
		hists[h].SetLineColor( kBlack )
		hists[h].SetLineWidth( 1 )
		hists[h].SetFillColor( ROOT.TColor.GetColor(sty.colors_dict[h]) )
		hists[h].SetMarkerColor( ROOT.TColor.GetColor(sty.colors_dict[h]) )
		hists[h].SetBinContent( hists[h].GetNbinsX() , hists[h].GetBinContent(hists[h].GetNbinsX()) + hists[h].GetBinContent(hists[h].GetNbinsX()+1) )
		legend_bkg.AddEntry( hists[h] , sty.labels_dict[h] , 'f' )

	h_sorted = [x for _,x in sorted(zip(h_int,samples_bkg))]

	for h in h_sorted:
		hs.Add(hists[h])
		hist_sm.Add(hists[h])

	for h in samples_sig:
		hists[h].SetLineColor( ROOT.TColor.GetColor(sty.sig_color(h)) )
		hists[h].SetLineStyle( 2 )
		hists[h].SetLineWidth( 3 )
		hists[h].SetMarkerColor( ROOT.TColor.GetColor(sty.sig_color(h)) )
		hists[h].SetBinContent( hists[h].GetNbinsX() , hists[h].GetBinContent(hists[h].GetNbinsX()) + hists[h].GetBinContent(hists[h].GetNbinsX()+1))
		legend_sig.AddEntry( hists[h] , sty.sig_label(h) , 'f' )

	if samples_dat:
		if var=='met_et' and reg.startswith('CR'):
			hists['data'].GetXaxis().SetRangeUser(0.,175.)
		hists['data'].SetMarkerStyle(20)
		hists['data'].SetMarkerSize(1.2)
		hists['data'].SetLineWidth(2)
		hists['data'].SetLineColor( ROOT.TColor.GetColor(sty.colors_dict['data']) )
		hists['data'].SetMarkerColor( ROOT.TColor.GetColor(sty.colors_dict['data']) )
		hists['data'].SetBinContent( hists['data'].GetNbinsX() , hists['data'].GetBinContent(hists['data'].GetNbinsX()) + hists['data'].GetBinContent(hists['data'].GetNbinsX()+1))
		legend_bkg.AddEntry( hists['data'] , sty.labels_dict['data'] , 'lp' )


	hs.Draw('hist')
	hs.GetXaxis().SetTitleOffset( 1.1 )
	hs.GetXaxis().SetRangeUser( sty.var_plots[var][1] , sty.var_plots[var][2] )
	hs.GetYaxis().SetTitleOffset( 0.9 )
	hs.GetYaxis().SetTitleSize(0.05)
	hs.GetYaxis().SetLabelSize(0.05)
	hs.GetYaxis().SetTitle( 'Events / '+str(int(hists[hists.keys()[0]].GetBinWidth(1)))+' GeV' )
	hs.SetMinimum(0.015)
	hs.SetMaximum(max(h_max)*100)
	hs.Draw('hist')

	for h in samples_sig:
		hists[h].Draw('hist same')

	if samples_dat:
		hists['data'].Draw('PE same')

	hist_sm2 = TH1D()
	hist_sm2 = hist_sm.Clone()
	legend_bkg.AddEntry( hist_sm , 'SM Total' , 'lf' )
	hist_sm.SetFillColor(ROOT.kGray+3)
	hist_sm.SetLineColor(ROOT.kGray+3)
	hist_sm.SetFillStyle(3354)
	hist_sm.SetLineWidth(2)
	hist_sm.SetMarkerSize(0)

	hist_sm2.SetLineWidth(2)
	hist_sm2.SetMarkerSize(0)
	hist_sm2.SetFillColor(0)
	hist_sm2.SetLineColor(ROOT.kGray+3)
	hist_sm.Draw('hist e2 ][ same')
	hist_sm2.Draw('hist ][ same')

	legend_bkg.Draw()
	legend_sig.Draw()

	reg_label = TLatex(0.18,0.9,reg)
	reg_label.SetNDC()
	reg_label.SetTextFont(42)
	reg_label.SetTextSize(0.035)
	reg_label.SetLineWidth(2)
	reg_label.Draw()

	year_label = TLatex(0.18,0.85,year)
	year_label.SetNDC()
	year_label.SetTextFont(42)
	year_label.SetTextSize(0.035)
	year_label.SetLineWidth(2)
	year_label.Draw()

	##########################################

	cdown.cd()
	h_sig = {}
	h_max_sig = []
	for h in samples_sig:
		h_sig[h] = TH1D()
		h_sig[h] = get_significance(hists[h], hist_sm, var)
		h_max_sig.append(h_sig[h].GetMaximum())
		h_sig[h].SetLineColor( ROOT.TColor.GetColor(sty.sig_color(h)) )
		h_sig[h].SetLineStyle( 2 )
		h_sig[h].SetLineWidth( 3 )
		h_sig[h].SetMarkerColor( ROOT.TColor.GetColor(sty.sig_color(h)) )
		h_sig[h].GetXaxis().SetTitle( sty.var_plots[var][0] )
		h_sig[h].GetXaxis().SetRangeUser( sty.var_plots[var][1] , sty.var_plots[var][2] )
		h_sig[h].GetXaxis().SetLabelSize(0.12)
		h_sig[h].GetXaxis().SetTitleSize(0.1)
		h_sig[h].GetXaxis().SetTitleOffset(1.1)
		h_sig[h].GetXaxis().SetTickLength(0.06)
		# h_sig[h].GetXaxis().SetLabelOffset(0.03)
		cdown.SetGridy()
		h_sig[h].GetYaxis().SetTitle('Significance')
		h_sig[h].GetYaxis().SetTitleOffset( 0.3 )
		h_sig[h].GetYaxis().SetTitleSize(0.13)
		h_sig[h].GetYaxis().SetLabelSize(0.1)
		h_sig[h].GetYaxis().SetNdivisions(508)
		# h_sig[h].GetYaxis().SetLabelOffset(0.01)

	h_sorted2 = [x for _,x in sorted(zip(h_max_sig,samples_sig))]

	for h in h_sorted2:
		h_sig[h].GetYaxis().SetRangeUser( 0 , max(h_max_sig)*1.2 )
		h_sig[h].Draw('e0 same')

	#########################################

	can.Print( com.eos_path_plots+'opt/'+tag+'/'+reg+'/'+var+'_'+reg+'.pdf' )
	can.Close()




def get_significance(sig, bkg, var):

	z = TH1D('','',com.binning_dict[var][0], com.binning_dict[var][1], com.binning_dict[var][2])
	for i in xrange(1,sig.GetNbinsX()+1):

		b=0.
		s=0.

		# for j in xrange(i,sig.GetNbinsX()):
		# 	b+=bkg.GetBinContent(bkg.GetNbinsX())
		# 	s+=sig.GetBinContent(sig.GetNbinsX())

		b=bkg.Integral(i, bkg.GetNbinsX(), 'width')
		s=sig.Integral(i, sig.GetNbinsX(), 'width')

		z_tmp = ROOT.RooStats.NumberCountingUtils.BinomialExpZ(s, b, 0.3)
		# z_tmp = significance(s,b,0.3*b)

		if z_tmp < 0. or z_tmp == float('Inf'):
			z_tmp=0.
		z.SetBinContent(i,z_tmp)
		z.SetBinError(i,0.)

	return z

def significance(s,b,db):

	print b
	print s

	if b<=0.:
		return 0.
	if s<=0.:
		return 0.

	s = math.sqrt( 2 * ( (s+b) * math.log( ((s+b)*(b+db*db))/(b*b+(s+b)*db*db) ) - (b*b/(db*db))*math.log( 1 + ((db*db*s)/(b*(b+db*db))) ) ))

	return s

def plot_grid():

	c1 = TCanvas('c1','c1',0,0,800,600)

	gStyle.SetOptStat( 0 )
	gStyle.SetOptTitle(0)

	gPad.SetRightMargin(0.04)
	gPad.SetLeftMargin(0.12)
	gPad.SetTopMargin(0.05)
	gPad.SetBottomMargin(0.11)

	legend = ROOT.TLegend(0.2,0.7,0.35,0.9)

	TG = []
	MG = ROOT.TMultiGraph()
	n_points = 0

	for i,mgo in enumerate(grd.grid_go_n1):

		n = len(grd.grid_go_n1[mgo])
		vx = array( 'd', [mgo] * n )
		vy = array( 'd', grd.grid_go_n1[mgo] )

		TG.append(ROOT.TGraph(n,vx,vy))

		TG[i].SetMarkerStyle(20)
		TG[i].SetMarkerSize(1.2)
		TG[i].SetMarkerColor(ROOT.TColor.GetColor('#65979b'))

		MG.Add(TG[i])

		n_points+=n

	legend.AddEntry( TG[0] , 'Run2 proposal' , 'p' )

	TG_run1 = []

	for i,mgo in enumerate(grd.grid_go_n1_run1):

		n = len(grd.grid_go_n1_run1[mgo])
		vx = array( 'd', [mgo] * n )
		vy = array( 'd', grd.grid_go_n1_run1[mgo] )

		TG_run1.append(ROOT.TGraph(n,vx,vy))

		TG_run1[i].SetMarkerStyle(20)
		TG_run1[i].SetMarkerSize(0.5)
		TG_run1[i].SetMarkerColor(ROOT.TColor.GetColor('#e28413'))

		MG.Add(TG_run1[i])

	legend.AddEntry( TG_run1[0] , 'Run1 grid' , 'p' )

	TG_bm = []
	n_bpoints = 0

	for i,mgo in enumerate(grd.grid_go_n1_benchmark):

		n = len(grd.grid_go_n1_benchmark[mgo])
		vx = array( 'd', [mgo] * n )
		vy = array( 'd', grd.grid_go_n1_benchmark[mgo] )

		TG_bm.append(ROOT.TGraph(n,vx,vy))

		TG_bm[i].SetMarkerStyle(20)
		TG_bm[i].SetMarkerSize(1.2)
		TG_bm[i].SetMarkerColor(ROOT.TColor.GetColor('#dd403a'))

		MG.Add(TG_bm[i])

		n_bpoints+=n

	legend.AddEntry( TG_bm[0] , 'Benchmark points ' , 'p' )

	MG.Draw('apz')

	MG.GetXaxis().SetRangeUser( 650. , 2850. )
	MG.GetXaxis().SetLabelFont(42)
	MG.GetXaxis().SetLabelSize(0.04)
	MG.GetXaxis().SetTitleSize(0.04)
	MG.GetXaxis().SetTitleOffset(1.1)
	MG.GetXaxis().SetTitleFont(42)
	MG.GetXaxis().SetTitle( 'm_{#tilde{g}} [GeV]' )
	# MG.GetXaxis().SetMaxDigits(3)

	MG.GetYaxis().SetRangeUser( 100. , 2900. )
	MG.GetYaxis().SetLabelFont(42)
	MG.GetYaxis().SetLabelSize(0.04)
	MG.GetYaxis().SetTitleSize(0.04)
	MG.GetYaxis().SetTitleOffset(1.4)
	MG.GetYaxis().SetTitleFont(42)
	MG.GetYaxis().SetTitle( 'm_{#tilde{#chi} #kern[-0.8]{#lower[1.2]{#scale[0.6]{1}}} #kern[-1.6]{#lower[-0.6]{#scale[0.6]{0}}}} [GeV]' )

	line = TLine()
	line.SetY1(650.)
	line.SetY2(2845.)
	line.SetX1(650.)
	line.SetX2(2845.)
	line.SetLineColor(ROOT.kGray)
	line.SetLineStyle(7)
	line.Draw('same')

	line_exc = TLine()
	line_exc.SetY1(400.)
	line_exc.SetY2(1250.)
	line_exc.SetX1(1250.)
	line_exc.SetX2(1250.)
	line_exc.SetLineColor(ROOT.TColor.GetColor('#9bc53d'))
	line_exc.SetLineWidth(5)
	line_exc.Draw('same')
	legend.AddEntry( line_exc , 'Run1 aprox. exclusion limit' , 'l' )

	TL_excl = TLatex(0.68,0.76,'m_{#tilde{#chi} #kern[-0.8]{#lower[1.2]{#scale[0.6]{1}}} #kern[-1.6]{#lower[-0.6]{#scale[0.6]{0}}}} > m_{#tilde{g}} forbidden')
	TL_excl.SetNDC()
	TL_excl.SetTextAngle(30.1)
	TL_excl.SetTextFont(42)
	TL_excl.SetTextSize(0.035)
	TL_excl.SetTextColor(ROOT.kGray)
	TL_excl.Draw('same')

	legend.SetTextSize(0.04)
	legend.SetBorderSize(0)
	legend.Draw('same')

	if not os.path.exists(com.eos_path_plots + 'grid'):
		os.makedirs(com.eos_path_plots + 'grid')
	c1.Print(com.eos_path_plots+'grid/grid.pdf')

	print 'Number of points: %i' % n_points
	print 'Number of benchmark points: %i' % n_bpoints



def theo_syst_plots(inputdir, tag, mod_reg):


	samples = ['photonjet_nnlo', 'wgamma', 'ttgamma', 'znunugamma', 'zllgamma']
	# samples = ['wgamma']

	years = ['fullR2', '20152016', '2017', '2018']
	# years = ['20152016']

	# regions = ['SRL', 'SRM', 'SRH', 'CRQ', 'CRW', 'CRT', 'VRQ', 'VRM1L', 'VRM2L', 'VRM1H', 'VRM2H', 'VRL1', 'VRL2', 'VRL3', 'VRL4', 'VRE']
	# regions = ['SRL200', 'SRL300', 'SRH', 'CRQ', 'CRW', 'CRT', 'VRQ', 'VRM1L', 'VRM2L', 'VRM1H', 'VRM2H', 'VRL1', 'VRL2', 'VRL3', 'VRL4', 'VRE']
	regions = mod_reg.regions

	if not os.path.exists(com.eos_path_plots + 'syst/'+tag):
		os.makedirs(com.eos_path_plots + 'syst/'+tag)

	dict_all = {}
	lst_vars = {}

	for sam in samples:

		# print sam

		dict_all[sam] = {}

		for yr in years:

			# print yr

			dict_all[sam][yr] = {}

			for reg in regions:

				# print reg

				dict_all[sam][yr][reg] = {}

				lst_vars[sam] = glob.glob(inputdir+'/syst_'+sam+'_'+yr+'/*.root')

				# if 'output/syst/syst_'+sam+'_'+yr+'/all.root' in lst_vars[sam]:
				# 	lst_vars[sam].remove('output/syst/syst_'+sam+'_'+yr+'/all.root')

				nom_ele = [s for s in lst_vars[sam] if 'Nominal' in s]
				altpdf1_ele = [s for s in lst_vars[sam] if 'Sherpa_ME_PDF25300' in s]
				altpdf2_ele = [s for s in lst_vars[sam] if 'Sherpa_ME_PDF13000' in s]
				all_ele = [s for s in lst_vars[sam] if 'all' in s]

				lst_vars[sam].insert(0, lst_vars[sam].pop(lst_vars[sam].index(nom_ele[0])))
				if len(altpdf1_ele)>0:
					lst_vars[sam].append(lst_vars[sam].pop(lst_vars[sam].index(altpdf1_ele[0])))
				if len(altpdf2_ele)>0:
					lst_vars[sam].append(lst_vars[sam].pop(lst_vars[sam].index(altpdf2_ele[0])))
				if len(all_ele)>0:
					lst_vars[sam].append(lst_vars[sam].pop(lst_vars[sam].index(all_ele[0])))

				label_dict = {'Sherpa_ME_PDF13000.root':'alt_PDF1', 'Sherpa_ME_PDF25300.root':'alt_PDF2', 'Sherpa_ME_PDF261000_alphaS_NNPDF_NNLO.root':'alphaS', 'Sherpa_ME_PDF261000_scale.root':'Scale', 'Sherpa_ME_PDF261000_var.root':'PDF_ME', 'Sherpa_PDF261000_Nominal.root':'Nominal', 'Sherpa_PDF261000_Normalisation.root':'Normalisation', 'aMcAtNlo_PDF260000_Nominal_type2.root' : 'Nominal', 'aMcAtNlo_ME_PDF260000_scale_type2.root' : 'Scale' , 'aMcAtNlo_ME_PDF260000_var_type2.root' : 'PDF_ME', 'all.root' : 'Total'}


				nom = array('f')
				xvar = array('f')
				xerr = array('f')
				ydn = array('f')
				yup = array('f')
				labels = []

				r_dn = array('f')
				r_up = array('f')

				for i,f in enumerate(lst_vars[sam]):
			
					inputfile = ROOT.TFile(f)
					tgae_tmp = inputfile.Get(reg+'_nevents')
					
					x = ROOT.Double(0)
					y = ROOT.Double(0)
					tgae_tmp.GetPoint(0,x,y)
					
					xvar.append(ROOT.Double(i+0.5))
					xerr.append(ROOT.Double(0.5))
					nom.append(y)
					ydn.append(tgae_tmp.GetErrorYlow(0))
					yup.append(tgae_tmp.GetErrorYhigh(0))
					
					if y!=0:
						r_dn.append(-100*tgae_tmp.GetErrorYlow(0)/y)
						r_up.append(100*tgae_tmp.GetErrorYhigh(0)/y)
					else:
						r_dn.append(0)
						r_up.append(0)

					dict_all[sam][yr][reg][label_dict[f.split('/')[-1]]] = (y, tgae_tmp.GetErrorYlow(0), tgae_tmp.GetErrorYhigh(0))
				

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


				can.Print(com.eos_path_plots+'syst/'+tag+'/syst_'+reg+'_'+sam+'_'+yr+'.pdf')
				can.Close()

	print 'Merging pdf files in %s' % (com.eos_path_plots+'syst/'+tag+'/all.pdf')
	pwd = os.getcwd()
	os.chdir(com.eos_path_plots+'syst/'+tag)
	if os.path.isfile('all.pdf'):
		os.remove('all.pdf')

	bashCommand = 'pdfunite *.pdf all.pdf'
	process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE, shell=True)
	output, error = process.communicate()

	print 'Done\n'

	print 'Creating tex in %s.tex' % com.eos_path_plots+'syst/'+tag+'/table/syst_table.tex'
	os.system('mkdir -p table')
	os.chdir('table')


	# print dict_all
	table_output = open ('syst_table.tex','w')

	table_output.write('\\documentclass[a4paper,12pt,twoside,spanish]{article}\n')
	table_output.write('\\usepackage[legalpaper, landscape, margin=0.2in]{geometry}\n')
	table_output.write('\\usepackage{multirow}\n')
	table_output.write('\\usepackage{graphicx}\n')
	table_output.write('\\usepackage{caption}\n')
	table_output.write('\\begin{document}\n')
	table_output.write('\\centering\n')


	for sam in samples:
		for yr in years:
			table_output.write('\\begin{table}\\caption*{%s %s}\n' % (sam.replace('_',''), yr))
			table_output.write('\\resizebox{\\textwidth}{!}{\\begin{tabular}{l ' + '| r r r ' *len(lst_vars[sam]) + '}\n')

			vars_tmp = '\\multirow{2}{*}{Region} & '

			for f in lst_vars[sam]: 
				vars_tmp += '\\multicolumn{3}{|c}{'+ label_dict[f.split('/')[-1]] + '} & '

			vars_tmp = vars_tmp.replace('_','\\_')
			vars_tmp = vars_tmp[:-2] + '\\\\\n'
			table_output.write(vars_tmp)

			table_output.write('\\cline{2-%i}' % (3*len(lst_vars[sam])+1) )

			vars2_tmp = ' & ' + ' Central & $\\Delta^{-}$ & $\\Delta^{+}$ &' * len(lst_vars[sam])
			vars2_tmp = vars2_tmp[:-2] + '\\\\\n'
			table_output.write(vars2_tmp)

			table_output.write('\\hline\n')

			reg_tmp = regions.keys()[0][0]
			for reg in regions:

				if not reg.startswith(reg_tmp):
					reg_tmp = reg[0]
					table_output.write('\\hline\n')

				line = '%s & ' % reg
				for f in lst_vars[sam]: 

					label = label_dict[f.split('/')[-1]]

					syst_tmp = '%.2f & %.2f (%.2f \\%%) & %.2f (%.2f \\%%) & ' % (dict_all[sam][yr][reg][label][0], dict_all[sam][yr][reg][label][1], 100*safeDiv(dict_all[sam][yr][reg][label][1],dict_all[sam][yr][reg][label][0]), dict_all[sam][yr][reg][label][2],100*safeDiv(dict_all[sam][yr][reg][label][2],dict_all[sam][yr][reg][label][0]))

					line+=syst_tmp 

				line = line[:-2] + '\\\\\n'
				table_output.write(line)

			table_output.write('\\end{tabular}}\n')
			table_output.write('\\end{table}\n')

	table_output.write('\\end{document}\n')
	table_output.close()

	if os.path.isfile('*.aux'):
		os.remove('*.aux')
	if os.path.isfile('*.log'):
		os.remove('*.log')
	if os.path.isfile('*.nav'):
		os.remove('*.nav')
	if os.path.isfile('*.out'):
		os.remove('*.out')
	if os.path.isfile('*.snm'):
		os.remove('*.snm')
	if os.path.isfile('*.toc'):
		os.remove('*.toc')
	if os.path.isfile('*.vrb'):
		os.remove('*.vrb')
	if os.path.isfile('*.pdf'):
		os.remove('*.pdf')

	
	# process = subprocess.Popen(['pdflatex', 'syst_table.tex'])
	# output, error = process.communicate()

	os.chdir(pwd) 

	# input for hist fitter
	print 'Creating input for HF in %s' % com.eos_path_plots+'syst/'+tag+'/config_input.py'
	config_input = open(com.eos_path_plots+'syst/'+tag+'/config_input.py','w')
	for sam in samples:
		for reg in regions:
			if dict_all[sam]['fullR2'][reg]['Total'][0] == 0:
				config_input.write('sigma_%s_%s_up = 0. # 0 events in region \n' % (sam, reg))
				config_input.write('sigma_%s_%s_dn = 0. # 0 events in region \n' % (sam, reg))
			else:
				config_input.write('sigma_%s_%s_up = %f \n' % (sam, reg, dict_all[sam]['fullR2'][reg]['Total'][2]/dict_all[sam]['fullR2'][reg]['Total'][0]))
				config_input.write('sigma_%s_%s_dn = %f \n' % (sam, reg, dict_all[sam]['fullR2'][reg]['Total'][1]/dict_all[sam]['fullR2'][reg]['Total'][0]))
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
