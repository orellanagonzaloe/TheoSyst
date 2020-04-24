
# FullR2 unblind Joaco's proposal

regions = {

	'SRL' : 'pass_g140==1 && ph_n>=1 && ph_pt[0]>145 && el_n+mu_n==0 && jet_n>=5 && dphi_jetmet>0.4 && dphi_gammet>0.4 && met_et>250 && ht>2000 && rt4<0.9',
	'SRM' : 'pass_g140==1 && ph_n>=1 && ph_pt[0]>300 && el_n+mu_n==0 && jet_n>=5 && dphi_jetmet>0.4 && dphi_gammet>0.4 && met_et>300 && ht>1600 && rt4<0.9',
	'SRH' : 'pass_g140==1 && ph_n>=1 && ph_pt[0]>400 && el_n+mu_n==0 && jet_n>=3 && dphi_jetmet>0.4 && dphi_gammet>0.4 && met_et>600 && ht>1600',

	# 'CRQ' : 'pass_g140==1 && ph_n>=1 && ph_pt[0]>145 && el_n+mu_n==0 && jet_n>=3              && dphi_jetmet<0.4 && dphi_gammet>0.4 && met_et>100               && ht>1600',
	# 'CRW' : 'pass_g140==1 && ph_n>=1 && ph_pt[0]>145 && el_n+mu_n>=1 && jet_n>=1 && bjet_n==0 && dphi_jetmet>0.4                    && met_et>100 && met_et<200 && ht>400 ',
	# 'CRT' : 'pass_g140==1 && ph_n>=1 && ph_pt[0]>145 && el_n+mu_n>=1 && jet_n>=2 && bjet_n>=2 && dphi_jetmet>0.4                    && met_et>50  && met_et<200 && ht>400 ',

	# 'VRL1' : 'pass_g140==1 && ph_n>=1 && ph_pt[0]>145 && el_n+mu_n>=1 && jet_n>=2 && dphi_jetmet>0.4 && met_et>50  && met_et<200 && ht>800 ',
	# 'VRL2' : 'pass_g140==1 && ph_n>=1 && ph_pt[0]>145 && el_n+mu_n>=1 && jet_n>=2 && dphi_jetmet>0.4 && met_et>50  && met_et<200 && ht>1300',
	# 'VRL3' : 'pass_g140==1 && ph_n>=1 && ph_pt[0]>145 && el_n+mu_n>=1 && jet_n>=2 && dphi_jetmet>0.4 && met_et>200               && ht>600  && ht<1600',
	# 'VRL4' : 'pass_g140==1 && ph_n>=1 && ph_pt[0]>145 && el_n+mu_n>=1 && jet_n>=2 && dphi_jetmet>0.4 && met_et>200               && ht>1100',

	# 'VRQ'   : 'pass_g140==1 && ph_n>=1 && ph_pt[0]>145 && el_n+mu_n==0 && jet_n>=3 && dphi_jetmet>0.4 && dphi_gammet>0.4 && met_et>100 && met_et<200 && ht>1600',
	# 'VRM1L' : 'pass_g140==1 && ph_n>=1 && ph_pt[0]>145 && el_n+mu_n==0 && jet_n>=5 && dphi_jetmet>0.4 && dphi_gammet>0.4 && met_et>100 && met_et<200 && ht>1600 && rt4<0.9',
	# 'VRM2L' : 'pass_g140==1 && ph_n>=1 && ph_pt[0]>145 && el_n+mu_n==0 && jet_n>=5 && dphi_jetmet>0.4 && dphi_gammet>0.4 && met_et>150 && met_et<200 && ht>1600 && rt4<0.9',
	# 'VRM1H' : 'pass_g140==1 && ph_n>=1 && ph_pt[0]>300 && el_n+mu_n==0 && jet_n>=3 && dphi_jetmet>0.4 && dphi_gammet>0.4 && met_et>100 && met_et<200 && ht>1600',
	# 'VRM2H' : 'pass_g140==1 && ph_n>=1 && ph_pt[0]>300 && el_n+mu_n==0 && jet_n>=3 && dphi_jetmet>0.4 && dphi_gammet>0.4 && met_et>150 && met_et<200 && ht>1600',

	# 'VRE' : 'pass_g140==1 && ph_n>=1 && ph_pt[0]>145 && jet_n>=1 && bjet_n>=1 && dphi_jetmet>0.4 && dphi_gammet<0.4 && met_et>200 && ht>100 && ht<1600',

}