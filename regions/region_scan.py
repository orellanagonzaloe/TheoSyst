#! /usr/bin/env python

import os
import argparse
import array

def main():

	l_pass_g140 = ['==1']
	l_ph_n = ['>0']
	l_l_n = ['', '==0'] # '','==0', '>0'
	l_ph_pt = ['>145', '>400']
	l_jet_n = ['>2', '>4'] # >0','>1','>2','>3','>4'
	l_bjet_n = ['>0', '>1']
	l_met_et = ['>200', '>400'] # '>100', '>200', '>300', '>400'
	l_dphi_gammet = ['', '>0.4']
	l_dphi_jetmet = ['', '>0.4']
	l_meff = ['', '>2000', '>2400']
	l_ht = ['', '>1000', '>2000'] # '','>1000','>2000'
	l_mt_gam = ['', '>90', '>200'] # '','>90','>200'
	l_rt4 = ['', '<0.9']
	l_bbmass = ['', '>100 && bbmass_w<150']

	total=len(l_pass_g140)*len(l_ph_n)*len(l_l_n)*len(l_ph_pt)*len(l_jet_n)*len(l_bjet_n)*len(l_met_et)*len(l_dphi_gammet)*len(l_dphi_jetmet)*len(l_meff)*len(l_ht)*len(l_mt_gam)*len(l_rt4)*len(l_bbmass)

	print total

	count=0

	f= open('regions/region_scan_output.py','w+')

	f.write('# number of regions = %i \n' % total)
	f.write('regions = {\n')

	for pass_g140 in l_pass_g140:
		for ph_n in l_ph_n:
			for l_n in l_l_n:
				for ph_pt in l_ph_pt:
					for jet_n in l_jet_n:
						for bjet_n in l_bjet_n:
							for met_et in l_met_et:
								for dphi_gammet in l_dphi_gammet:
									for dphi_jetmet in l_dphi_jetmet:
										for meff in l_meff:
											for ht in l_ht:
												for mt_gam in l_mt_gam:
													for rt4 in l_rt4:
														for bbmass in l_bbmass:

															count+=1
															region = ('\'SRX_%i\' : \'pass_g140%s && ph_n%s')%(count, pass_g140, ph_n)
															if l_n is not '':
																region+=(' && el_n+mu_n%s')%(l_n)
															if ph_pt is not '':
																region+=(' && ph_pt[0]%s')%(ph_pt)
															if jet_n is not '':
																region+=(' && jet_n%s')%(jet_n)
															if bjet_n is not '':
																region+=(' && bjet_n%s')%(bjet_n)
															if met_et is not '':
																region+=(' && met_et%s')%(met_et)
															if dphi_gammet is not '':
																region+=(' && dphi_gammet%s')%(dphi_gammet)
															if dphi_jetmet is not '':
																region+=(' && dphi_jetmet%s')%(dphi_jetmet)
															if meff is not '':
																region+=(' && meff%s')%(meff)
															if ht is not '':
																region+=(' && ht%s')%(ht)
															if mt_gam is not '':
																region+=(' && mt_gam%s')%(mt_gam)
															if rt4 is not '':
																region+=(' && rt4%s')%(rt4)
															if bbmass is not '':
																region+=(' && bbmass_w%s')%(bbmass)
															region+='\','

															# print region
															f.write(region+'\n')




	f.write('}')




	
if __name__ == '__main__':
	main()
#  

