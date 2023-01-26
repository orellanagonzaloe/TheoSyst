
presel = 'pass_g140==1 && ph_n>0 && jet_n>0 && el_baseline_n==el_n && mu_baseline_n==mu_n && ph_pt[0]>145'
myy_cut = '(m_yy<120 || m_yy>130)'

preselSRd = '%s && %s && el_n+mu_n==0 && dphi_jetmet>0.4 && dphi_gammet>0.4 && met_et/meff>0.5 && met_sig_obj>21' % (presel, myy_cut)
preselSRe = '%s && %s && el_n+mu_n==0 && dphi_jetmet>0.4 && dphi_gammet>0.4 && met_sig_obj>21' % (presel, myy_cut)

regions = {

	# Signal Regions for discovery
	'SRd200': '%s && met_et>200' % (preselSRd),
	'SRd300': '%s && met_et>300' % (preselSRd),
	'SRd400': '%s && met_et>400' % (preselSRd),
	'SRd500': '%s && met_et>500' % (preselSRd),

	# Signal Regions for exclusion
	'SRe200': '%s && met_et>200 && met_et<=300' % (preselSRe),
	'SRe300': '%s && met_et>300 && met_et<=500' % (preselSRe),
	'SRe400': '%s && met_et>400 && met_et<=500' % (preselSRe),
	'SRe500': '%s && met_et>500' % (preselSRe),

	# Control Regions
	'CRT': '%s && el_n+mu_n>=1 && dphi_jetmet>0.4 && dphi_gammet>0.4 && bjet_n>=2 && met_et>150 && met_et/meff<0.35' % (presel),
	'CRW': '%s && el_n+mu_n==1 && bjet_n==0 && dphi_jetmet>0.4 && dphi_gammet>0.4 && met_et>200 && mt_lep<100 && met_et/meff<0.35' % (presel),
	'CRZee': '%s && el_n==2 && mu_n==0 && met_et<50 && met_noele_et>100 && dphi_jetmet_noele>0.4 && dphi_gammet_noele>0.4 && met_noele_et/meff_noele<0.35' % (presel),
	'CRZmm': '%s && el_n==0 && mu_n==2 && met_et<50 && met_nomuon_et>100 && dphi_jetmet_nomuon>0.4 && dphi_gammet_nomuon>0.4 && met_nomuon_et/meff_nomuon<0.35' % (presel),

	# Validation Regions
	'VRW': '%s && el_n+mu_n==1 && dphi_jetmet>0.4 && dphi_gammet>0.4 && met_et>200 && met_et/meff>0.35' % (presel),
	'VRT': '%s && el_n+mu_n>=1 && bjet_n>=1 && dphi_jetmet>0.4 && dphi_gammet>0.4 && met_et>200 && met_et/meff>0.35' % (presel),
	'VRE': '%s && dphi_jetmet>0.4 && dphi_gammet<0.4 && met_et>200 && met_et/meff>0.25 && met_sig_obj>10 && mt_gam<80' % (presel),
	'VRZee': '%s && el_n==2 && dphi_jetmet_noele>0.4 && dphi_gammet_noele>0.4 && met_et<50 && met_noele_et>200' % (presel),
	'VRZmm': '%s && mu_n==2 && dphi_jetmet_nomuon>0.4 && dphi_gammet_nomuon>0.4 && met_et<50 && met_nomuon_et>200 && met_nomuon_et/meff_nomuon>0.35' % (presel),

	# Additional Validation Regions
	'VRS': '%s && el_n+mu_n==0 && dphi_jetmet>0.4 && dphi_gammet>0.4 && met_et>120 && met_et<180 && dphi_gamjet<2 && met_et/meff>0.45 && dphi_gammet<2.9'  % (presel),

	# Loose regions to measure systematics

	# Signal Regions
	'SR'  : '%s && el_n+mu_n==0 && dphi_jetmet>0.4 && dphi_gammet>0.4 && met_et/meff>0.35 && met_sig_obj>15 && met_et>200' % (presel),

	# Validation Regions
	## Intermediate MET
	'VRWloose': '%s && el_n+mu_n==1 && dphi_jetmet>0.4 && dphi_gammet>0.4 && met_et>200' % (presel),
	'VRTloose': '%s && el_n+mu_n>=1 && bjet_n>=1 && dphi_jetmet>0.4 && dphi_gammet>0.4 && met_et>200' % (presel),
	'VREloose': '%s && dphi_jetmet>0.4 && dphi_gammet<0.4 && met_et>200 && met_sig_obj>10 && mt_gam<80' % (presel),
	'VRZeeloose': '%s && el_n==2 && dphi_jetmet_noele>0.4 && dphi_gammet_noele>0.4 && met_et<50 && met_noele_et>200' % (presel),
	'VRZmmloose': '%s && mu_n==2 && dphi_jetmet_nomuon>0.4 && dphi_gammet_nomuon>0.4 && met_et<50 && met_nomuon_et>200' % (presel),

}

