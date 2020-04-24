# Loose regions to measure systematics, based on Joaco's newRegions branch

regions = {

# Signal Regions
	'SR'  : 'pass_g140==1 && ph_n>0 && el_n+mu_n==0 && ph_pt[0]>145 && met_et>200 && jet_n>2 && dphi_gammet>0.4 && ht>1600',

# NEW Control Regions
	'CRQ' : 'pass_g140==1 && ph_n>0 && el_n+mu_n==0 && ph_pt[0]>145 && jet_n>2 && met_et>100 && ht>1600 && dphi_jetmet<0.4 && dphi_gammet>0.4',
	'CRW' : 'pass_g140==1 && ph_n>0 && el_n+mu_n>0  && ph_pt[0]>145 && jet_n>0 && met_et>100 && met_et<200 && dphi_jetmet>0.4 && ht>400 && bjet_n==0',
	'CRT' : 'pass_g140==1 && ph_n>0 && el_n+mu_n>0  && ph_pt[0]>145 && jet_n>1 && met_et>50  && met_et<200 && dphi_jetmet>0.4 && ht>400 && bjet_n>=2',

# Validation Regions
## Intermediate MET
	'VRM' : 'pass_g140==1 && ph_n>0 && el_n+mu_n==0 && ph_pt[0]>300 && met_et>100 && jet_n>2 && dphi_gammet>0.4 && ht>1000',

## lepton VR: Wgamma/ttbarg
	'VRL' : 'pass_g140==1 && ph_n>0 && el_n+mu_n>0 && ph_pt[0]>145 && jet_n>1 && met_et>100 && ht>800',

## efakes VR:
	'VRE' : 'pass_g140==1 && ph_n>=1 && ph_pt[0]>145 && jet_n>=1 && bjet_n>=1 && dphi_jetmet>0.4 && met_et>200 && ht>100 && ht<1600',

}