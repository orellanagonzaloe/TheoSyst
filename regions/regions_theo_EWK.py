
presel = 'pass_g140==1 && ph_n>0 && jet_n>0 && ph_pt[0]>145'
myy_cut = '(m_yy<120 || m_yy>130)'

preselSR = '%s && %s && dphi_jetmet>0.4 && dphi_gammet>0.4 && met_et/meff>0.5' % (presel, myy_cut)

sel_crze = 'el_n==2 && mu_n==0 && met_noele_et>100 && dphi_jetmet_noele>0.4 && dphi_gammet_noele>0.4 && met_noele_et/meff_noele<0.35'
sel_crzm = 'el_n==0 && mu_n==2 && met_nomuon_et>100 && dphi_jetmet_nomuon>0.4 && dphi_gammet_nomuon>0.4 && met_nomuon_et/meff_nomuon<0.35'

VRpresel = '%s && met_et>50' % (presel)

sel_vrze = 'el_n==2 && mu_n==0 && met_noele_et>200 && dphi_jetmet_noele>0.4 && dphi_gammet_noele>0.4 && met_noele_et/meff_noele>0.35'
sel_vrzm = 'el_n==0 && mu_n==2 && met_nomuon_et>200 && dphi_jetmet_nomuon>0.4 && dphi_gammet_nomuon>0.4 && met_nomuon_et/meff_nomuon>0.35'

regions = {

	# Signal Regions
	'SR1': '%s && met_et>200 && met_sig_obj>20' % (preselSR),
	'SR2': '%s && met_et>300 && met_sig_obj>30' % (preselSR),
	'SR3': '%s && met_et>400 && met_sig_obj>40' % (preselSR),
	'SR4': '%s && met_et>500 && met_sig_obj>45' % (preselSR),

	# Control Regions
	'CRT': '%s && el_n+mu_n>=1 && dphi_jetmet>0.4 && dphi_gammet>0.4 && bjet_n>=2 && met_et>150 && met_et/meff<0.35' % (presel),
	'CRW': '%s && el_n+mu_n==1 && bjet_n==0 && dphi_jetmet>0.4 && dphi_gammet>0.4 && met_et>200 && mt_lep<100 && met_et/meff<0.35' % (presel),
	'CRZ': '%s && met_et<50 && ((%s) || (%s))' % (presel, sel_crze, sel_crzm),
	'CRZee': '%s && met_et<50 && %s' % (presel, sel_crze),
	'CRZmm': '%s && met_et<50 && %s' % (presel, sel_crzm),

	# Validation Regions
	'VRW': '%s && el_n+mu_n==1 && dphi_jetmet>0.4 && dphi_gammet>0.4 && met_et>200 && met_et/meff>0.35' % (presel),
	'VRT': '%s && el_n+mu_n>=1 && bjet_n>=1 && dphi_jetmet>0.4 && dphi_gammet>0.4 && met_et>200 && met_et/meff>0.35' % (presel),
	'VRE': '%s && dphi_jetmet>0.4 && dphi_gammet<0.4 && met_et>200 && met_et/meff>0.25 && met_sig_obj>10 && mt_gam<80' % (presel),
	'VRZ': '%s && met_et<50 && ((%s) || (%s))' % (presel, sel_vrze, sel_vrzm),
	'VRZee': '%s && met_et<50 && %s' % (presel, sel_vrze),
	'VRZmm': '%s && met_et<50 && %s' % (presel, sel_vrzm),

	# Additional Validation Regions
	'VRS': '%s && el_n+mu_n==0 && dphi_jetmet>0.4 && dphi_gammet>0.4 && met_et>120 && met_et<180 && dphi_gamjet<2 && met_et/meff>0.45 && dphi_gammet<2.9'  % (presel),

	# Loose regions to measure systematics
	# Signal Regions
	'SRloose'  : '%s && el_n+mu_n==0 && dphi_jetmet>0.4 && dphi_gammet>0.4 && met_et/meff>0.35 && met_sig_obj>15 && met_et>200' % (presel),

	# Validation Regions
	'VRWloose': '%s && el_n+mu_n==1 && dphi_jetmet>0.4 && dphi_gammet>0.4 && met_et>200' % (presel),
	'VRTloose': '%s && el_n+mu_n>=1 && bjet_n>=1 && dphi_jetmet>0.4 && dphi_gammet>0.4 && met_et>200' % (presel),
	'VREloose': '%s && dphi_jetmet>0.4 && dphi_gammet<0.4 && met_et>200 && met_sig_obj>10 && mt_gam<80' % (presel),
	'VRZloose': '%s && met_et<50 && ((el_n==2 && met_noele_et>200 && dphi_jetmet_noele>0.4 && dphi_gammet_noele>0.4) || (mu_n==2 && met_nomuon_et>200 && dphi_jetmet_nomuon>0.4 && dphi_gammet_nomuon>0.4))' % (presel),
	'VRZeeloose': '%s && met_et<50 && el_n==2 && met_noele_et>200 && dphi_jetmet_noele>0.4 && dphi_gammet_noele>0.4' % (presel),
	'VRZmmloose': '%s && met_et<50 && mu_n==2 && met_nomuon_et>200 && dphi_jetmet_nomuon>0.4 && dphi_gammet_nomuon>0.4' % (presel),

}