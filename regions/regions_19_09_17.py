
# FullR2 unblind

regions = {

	'SRL200_phj' : 'pass_g140==1 && ph_n>=1 && ph_pt[0]>145 && el_n+mu_n==0 && jet_n>=5 && dphi_jetmet>0.4 && dphi_gammet>0.4 && met_et>200 && meff>2000 && rt4<0.9',
	'SRL300_phj' : 'pass_g140==1 && ph_n>=1 && ph_pt[0]>145 && el_n+mu_n==0 && jet_n>=5 && dphi_jetmet>0.4 && dphi_gammet>0.4 && met_et>300 && meff>2000 && rt4<0.9',
	'SRH_phj'    : 'pass_g140==1 && ph_n>=1 && ph_pt[0]>400 && el_n+mu_n==0 && jet_n>=3 && dphi_jetmet>0.4 && dphi_gammet>0.4 && met_et>400 && meff>2400',

	# 'CRQ' : 'pass_g140==1 && ph_n>=1 && ph_pt[0]>145 && el_n+mu_n==0 && met_et>100 && jet_n>=3 && dphi_jetmet<0.4 && dphi_gammet>0.4 && meff>2000',
	# 'CRW' : 'pass_g140==1 && ph_n>=1 && ph_pt[0]>145 && el_n+mu_n>=1 && met_et>100 && met_et<200 && jet_n>=1 && bjet_n==0 && dphi_jetmet>0.4 && meff>500',
	# 'CRT' : 'pass_g140==1 && ph_n>=1 && ph_pt[0]>145 && el_n+mu_n>=1 && met_et>50  && met_et<200 && jet_n>=2 && bjet_n>=2 && dphi_jetmet>0.4 && meff>500',

	# 'VRQ'   : 'pass_g140==1 && ph_n>=1 && ph_pt[0]>145 && el_n+mu_n==0 && jet_n>=3 && dphi_jetmet>0.4 && dphi_gammet>0.4 && met_et>100 && met_et<200 && meff>2000',
	# 'VRM1L' : 'pass_g140==1 && ph_n>=1 && ph_pt[0]>145 && el_n+mu_n==0 && jet_n>=5 && dphi_jetmet>0.4 && dphi_gammet>0.4 && met_et>100 && met_et<200 && meff>2000 && rt4<0.9',
	# 'VRM2L' : 'pass_g140==1 && ph_n>=1 && ph_pt[0]>145 && el_n+mu_n==0 && jet_n>=5 && dphi_jetmet>0.4 && dphi_gammet>0.4 && met_et>150 && met_et<200 && meff>2000 && rt4<0.9',
	# 'VRM1H' : 'pass_g140==1 && ph_n>=1 && ph_pt[0]>145 && el_n+mu_n==0 && jet_n>=3 && dphi_jetmet>0.4 && dphi_gammet>0.4 && met_et>100 && met_et<200 && meff>2000',
	# 'VRM2H' : 'pass_g140==1 && ph_n>=1 && ph_pt[0]>145 && el_n+mu_n==0 && jet_n>=3 && dphi_jetmet>0.4 && dphi_gammet>0.4 && met_et>150 && met_et<200 && meff>2000',

	# 'VRL1' : 'pass_g140==1 && ph_n>=1 && ph_pt[0]>145 && el_n+mu_n>=1 && jet_n>=2 && dphi_jetmet>0.4 && met_et<200 && meff>1000',
	# 'VRL2' : 'pass_g140==1 && ph_n>=1 && ph_pt[0]>145 && el_n+mu_n>=1 && jet_n>=2 && dphi_jetmet>0.4 && met_et<200 && meff>1500',
	# 'VRL3' : 'pass_g140==1 && ph_n>=1 && ph_pt[0]>145 && el_n+mu_n>=1 && jet_n>=2 && dphi_jetmet>0.4 && met_et>200 && meff>1000 && meff<2000',
	# 'VRL4' : 'pass_g140==1 && ph_n>=1 && ph_pt[0]>145 && el_n+mu_n>=1 && jet_n>=2 && dphi_jetmet>0.4 && met_et>200 && meff>1500',

	# 'VRE' : 'pass_g140==1 && ph_n>=1 && ph_pt[0]>145 && jet_n>=1 && bjet_n>=1 && dphi_jetmet>0.4 && dphi_gammet<0.4 && met_et>200 && meff>500 && meff<2000',

}