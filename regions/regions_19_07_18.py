regions = {

	# 'SRL_phb' : 'pass_g140==1 && ph_n>0 && el_n+mu_n==0 && ph_pt[0]>125 && met_et>100 && jet_n>1 && jet_n<5 && bjet_n>1 && dphi_jetmet>0.3 && mt_gam>90', # avoiding: && bbmass>75 && bbmass<150
	# 'SRH_phb' : 'pass_g140==1 && ph_n>0 && ph_pt[0]>150 && met_et>200 && jet_n>3 && bjet_n>0 && dphi_jetmet>0.3 && mt_gam>90 && ht>1000',

	# 'SRL1_phb' : 'pass_g140==1 && ph_n>0 && el_n+mu_n==0 && ph_pt[0]>145 && met_et>200 && jet_n>4 && jet_n<5 && bjet_n>1 && dphi_jetmet>0.3 && rt4<0.9',

	# 'SRL200_phj' : 'pass_g140==1 && ph_n>0 && el_n+mu_n==0 && ph_pt[0]>145 && met_et>200 && jet_n>4 && dphi_jetmet>0.4 && dphi_gammet>0.4 && meff>2000 && rt4<0.9',
	# 'SRL300_phj' : 'pass_g140==1 && ph_n>0 && el_n+mu_n==0 && ph_pt[0]>145 && met_et>300 && jet_n>4 && dphi_jetmet>0.4 && dphi_gammet>0.4 && meff>2000 && rt4<0.9',
	# 'SRH_phj' : 'pass_g140==1 && ph_n>0 && el_n+mu_n==0 && ph_pt[0]>400 && met_et>400 && jet_n>2 && dphi_jetmet>0.4 && dphi_gammet>0.4 && meff>2400',

	# 'SRL_phj_new' : 'pass_g140==1 && ph_n>0 && el_n+mu_n==0 && ph_trackiso[0]<0.05 && ph_pt[0]>145 && met_et>300 && jet_n>4 && dphi_jet1met>0.4 && dphi_gamjet <3. && ht>2000 && rt4<0.9',
	# 'SRM_phj_new' : 'pass_g140==1 && ph_n>0 && el_n+mu_n==0 && ph_trackiso[0]<0.05 && ph_pt[0]>300 && met_et>300 && jet_n>4 && dphi_jet1met>0.4 && dphi_gammet>0.5 && dphi_gamjet <3. && ht>1600 && rt4<0.9',
	# 'SRH_phj_new' : 'pass_g140==1 && ph_n>0 && el_n+mu_n==0 && ph_trackiso[0]<0.05 && ph_pt[0]>400 && met_et>400 && jet_n>2 && dphi_jet1met>0.4 && dphi_gammet>0.5 && dphi_gamjet <3. && ht>1200',

	# 'SRL1_phj' : 'pass_g140==1 && ph_n>0 && el_n+mu_n==0 && ph_pt[0]>145 && jet_n>4 && dphi_jetmet>0.4 && dphi_gammet>0.4 && rt4<0.9',
	# 'SRL2_phj' : 'pass_g140==1 && ph_n>0 && el_n+mu_n==0 && ph_pt[0]>145 && jet_n>4 && dphi_jetmet>0.4 && dphi_gammet>0.4 && rt4<0.9 && met_et>200',
	# 'SRH1_phj' : 'pass_g140==1 && ph_n>0 && el_n+mu_n==0 && ph_pt[0]>400 && jet_n>2 && dphi_jetmet>0.4 && dphi_gammet>0.4',
	# 'SRH2_phj' : 'pass_g140==1 && ph_n>0 && el_n+mu_n==0 && ph_pt[0]>400 && jet_n>2 && dphi_jetmet>0.4 && dphi_gammet>0.4 && met_et>200',

	# 'CRQ_phj' : 'pass_g140==1 && ph_n>0 && el_n+mu_n==0 && ph_pt[0]>145 && jet_n>2 && met_et>100 && meff>2000 && dphi_jetmet<0.4 && dphi_gammet>0.4',
	# 'CRW_phj' : 'pass_g140==1 && ph_n>0 && el_n+mu_n>0  && ph_pt[0]>145 && jet_n>0 && met_et>100 && met_et<200 && dphi_jetmet>0.4 && meff>500 && bjet_n==0',
	# 'CRT_phj' : 'pass_g140==1 && ph_n>0 && el_n+mu_n>0  && ph_pt[0]>145 && jet_n>1 && met_et>50  && met_et<200 && dphi_jetmet>0.4 && meff>500 && bjet_n>=2',

	# 'VRQ_phj' : 'pass_g140==1 && ph_n>0 && el_n+mu_n==0 && ph_pt[0]>145 && jet_n>2 && met_et>100 && met_et<200 && meff>2000 && dphi_jetmet>0.4 && dphi_gammet>0.4',

	# 'VRM1L_phj' : 'pass_g140==1 && ph_n>0 && el_n+mu_n==0 && ph_pt[0]>145 && met_et>100  && met_et<200 && jet_n>4 && dphi_jetmet>0.4 && dphi_gammet>0.4 && meff>2000 && rt4<0.9',
	# 'VRM2L_phj' : 'pass_g140==1 && ph_n>0 && el_n+mu_n==0 && ph_pt[0]>145 && met_et>150  && met_et<200 && jet_n>4 && dphi_jetmet>0.4 && dphi_gammet>0.4 && meff>2000 && rt4<0.9',

	# 'VRM1H_phj' : 'pass_g140==1 && ph_n>0 && el_n+mu_n==0 && ph_pt[0]>300 && met_et>100  && met_et<200 && jet_n>2 && dphi_jetmet>0.4 && dphi_gammet>0.4 && meff>2000',
	# 'VRM2H_phj' : 'pass_g140==1 && ph_n>0 && el_n+mu_n==0 && ph_pt[0]>300 && met_et>150  && met_et<200 && jet_n>2 && dphi_jetmet>0.4 && dphi_gammet>0.4 && meff>2000',

	# 'VRL1_phj' : 'pass_g140==1 && ph_n>0 && el_n+mu_n>0 && ph_pt[0]>145 && jet_n>1 && met_et<200 && dphi_jetmet>0.4 && meff>1000',
	# 'VRL2_phj' : 'pass_g140==1 && ph_n>0 && el_n+mu_n>0 && ph_pt[0]>145 && jet_n>1 && met_et<200 && dphi_jetmet>0.4 && meff>1500',
	# 'VRL3_phj' : 'pass_g140==1 && ph_n>0 && el_n+mu_n>0 && ph_pt[0]>145 && jet_n>1 && met_et>200 && dphi_jetmet>0.4 && meff>1000 && meff<2000',
	# 'VRL4_phj' : 'pass_g140==1 && ph_n>0 && el_n+mu_n>0 && ph_pt[0]>145 && jet_n>1 && met_et>200 && dphi_jetmet<0.4 && meff>1500',
	# 'VRL5_phj' : 'pass_g140==1 && ph_n>0 && el_n+mu_n>0 && ph_pt[0]>145 && jet_n>1 && met_et>200 && dphi_jetmet<0.4 && meff>1000 && bjet_n>0',

	# 'VRLW1_phj' : 'pass_g140==1 && ph_n>0 && el_n+mu_n>0 && ph_pt[0]>145 && jet_n>1 && met_et>100 && met_et<200 && dphi_jetmet>0.4 && meff>1000 && bjet_n==0',
	# 'VRLT1_phj' : 'pass_g140==1 && ph_n>0 && el_n+mu_n>0 && ph_pt[0]>145 && jet_n>1 && met_et>100 && met_et<200 && dphi_jetmet>0.4 && meff>1000 && bjet_n>0',
	# 'VRLW3_phj' : 'pass_g140==1 && ph_n>0 && el_n+mu_n>0 && ph_pt[0]>145 && jet_n>1 && met_et>200 && dphi_jetmet>0.4 && meff>1000 && meff<2000 && bjet_n==0',
	# 'VRLT3_phj' : 'pass_g140==1 && ph_n>0 && el_n+mu_n>0 && ph_pt[0]>145 && jet_n>1 && met_et>200 && dphi_jetmet>0.4 && meff>1000 && meff<2000 && bjet_n>0',

	# 'VRE_phj'  : 'pass_g140==1 && ph_n>0 && ph_pt[0]>145 && met_et>200 && jet_n>=1 && meff>500 && meff<2000 && bjet_n>=1 && dphi_jetmet>0.4 && dphi_gammet<0.4',

	###### 4

	# 'CRQ1_phb' : 'pass_g140==1 && ph_n>0 && ph_pt[0]>145 && met_et>100 && jet_n>4 && bjet_n>0 && dphi_jetmet<0.4 && mt_gam>200 && ht>1000',
	# 'CRW1_phb' : 'pass_g140==1 && ph_n>0 && ph_pt[0]>145 && met_et>100 && met_et<200 && jet_n==0 && bjet_n>1 && dphi_jetmet>0.4 && mt_gam>200 && ht>1000',
	# 'CRT1_phb' : 'pass_g140==1 && ph_n>0 && ph_pt[0]>145 && met_et>50 && jet_n>5 && bjet_n>0 && dphi_jetmet>0.4 && mt_gam>200 && ht>1000',
	# 'SRH1_1L_phb' : 'pass_g140==1 && ph_n>0 && ph_pt[0]>200 && met_et>300 && jet_n>4 && bjet_n>0 && dphi_jetmet>0.4 && mt_gam>200 && ht>1000',
	# 'SRH1_2L_phb' : 'pass_g140==1 && ph_n>0 && ph_pt[0]>200 && met_et>300 && jet_n>4 && bjet_n>1 && dphi_jetmet>0.4 && mt_gam>200 && ht>1000',
	# 'SRH1_3L_phb' : 'pass_g140==1 && ph_n>0 && ph_pt[0]>145 && met_et>300 && jet_n>5 && bjet_n>0 && dphi_jetmet>0.4 && mt_gam>200 && ht>1000',
	# 'SRH1_M_phb' : 'pass_g140==1 && ph_n>0 && ph_pt[0]>400 && met_et>400 && jet_n>3 && bjet_n>0 && dphi_jetmet>0.4 && mt_gam>200 && ht>1000',
	# 'SRH1_1H_phb' : 'pass_g140==1 && ph_n>0 && ph_pt[0]>400 && met_et>400 && jet_n>2 && bjet_n>0 && dphi_jetmet>0.4 && mt_gam>200 && ht>1000',
	# 'SRH1_2H_phb' : 'pass_g140==1 && ph_n>0 && ph_pt[0]>400 && met_et>400 && jet_n>2 && dphi_jetmet>0.4 && mt_gam>200 && ht>1000',
	# 'SRH1_3H_phb' : 'pass_g140==1 && ph_n>0 && ph_pt[0]>450 && met_et>450 && jet_n>1 && dphi_jetmet>0.4 && mt_gam>200 && ht>1000',

	# 'CRQ2_phb' : 'pass_g140==1 && ph_n>0 && ph_pt[0]>145 && met_et>100 && jet_n>4 && bjet_n>0 && dphi_jetmet>0.4 && mt_gam>90 && ht>2000',
	# 'CRW2_phb' : 'pass_g140==1 && ph_n>0 && ph_pt[0]>145 && met_et>100 && met_et<200 && jet_n>4 && bjet_n==0 && dphi_jetmet>0.4 && mt_gam>90 && ht>2000',
	# 'CRT2_phb' : 'pass_g140==1 && ph_n>0 && ph_pt[0]>145 && met_et>50 && jet_n>5 && bjet_n>0 && dphi_jetmet>0.4 && mt_gam>90 && ht>2000',
	# 'SRH2_1L_phb' : 'pass_g140==1 && ph_n>0 && ph_pt[0]>200 && met_et>300 && jet_n>4 && bjet_n>0 && dphi_jetmet>0.4 && mt_gam>90 && ht>2000',
	# 'SRH2_2L_phb' : 'pass_g140==1 && ph_n>0 && ph_pt[0]>200 && met_et>300 && jet_n>4 && bjet_n>1 && dphi_jetmet>0.4 && mt_gam>90 && ht>2000',
	'SRH2_3L_phb' : 'pass_g140==1 && ph_n>0 && ph_pt[0]>145 && met_et>300 && jet_n>5 && bjet_n>0 && dphi_jetmet>0.4 && mt_gam>90 && ht>2000',
	# 'SRH2_M_phb' : 'pass_g140==1 && ph_n>0 && ph_pt[0]>400 && met_et>400 && jet_n>3 && bjet_n>0 && dphi_jetmet>0.4 && mt_gam>90 && ht>2000',
	# 'SRH2_1H_phb' : 'pass_g140==1 && ph_n>0 && ph_pt[0]>400 && met_et>400 && jet_n>2 && bjet_n>0 && dphi_jetmet>0.4 && mt_gam>90 && ht>2000',
	# 'SRH2_2H_phb' : 'pass_g140==1 && ph_n>0 && ph_pt[0]>400 && met_et>400 && jet_n>2 && dphi_jetmet>0.4 && mt_gam>90 && ht>2000',
	# 'SRH2_3H_phb' : 'pass_g140==1 && ph_n>0 && ph_pt[0]>450 && met_et>450 && jet_n>1 && dphi_jetmet>0.4 && mt_gam>90 && ht>2000',

	# 'CRQ3_phb' : 'pass_g140==1 && ph_n>0 && ph_pt[0]>145 && met_et>100 && jet_n>4 && bjet_n>1 && dphi_jetmet<0.4 && mt_gam>90 && ht>1000',
	# 'CRW3_phb' : 'pass_g140==1 && ph_n>0 && ph_pt[0]>145 && met_et>100 && met_et<200 && jet_n>4 && bjet_n==0 && dphi_jetmet>0.4 && mt_gam>90 && ht>1000',
	# 'CRT3_phb' : 'pass_g140==1 && ph_n>0 && ph_pt[0]>145 && met_et>50 && jet_n>5 && bjet_n>1 && dphi_jetmet>0.4 && mt_gam>90 && ht>1000',
	'SRH3_1L_phb' : 'pass_g140==1 && ph_n>0 && ph_pt[0]>200 && met_et>300 && jet_n>4 && bjet_n>1 && dphi_jetmet>0.4 && mt_gam>90 && ht>1000',
	# 'SRH3_2L_phb' : 'pass_g140==1 && ph_n>0 && ph_pt[0]>200 && met_et>300 && jet_n>4 && bjet_n>2 && dphi_jetmet>0.4 && mt_gam>90 && ht>1000',
	# 'SRH3_3L_phb' : 'pass_g140==1 && ph_n>0 && ph_pt[0]>145 && met_et>300 && jet_n>5 && bjet_n>1 && dphi_jetmet>0.4 && mt_gam>90 && ht>1000',
	# 'SRH3_M_phb' : 'pass_g140==1 && ph_n>0 && ph_pt[0]>400 && met_et>400 && jet_n>3 && bjet_n>1 && dphi_jetmet>0.4 && mt_gam>90 && ht>1000',
	# 'SRH3_1H_phb' : 'pass_g140==1 && ph_n>0 && ph_pt[0]>400 && met_et>400 && jet_n>2 && bjet_n>1 && dphi_jetmet>0.4 && mt_gam>90 && ht>1000',
	# 'SRH3_2H_phb' : 'pass_g140==1 && ph_n>0 && ph_pt[0]>400 && met_et>400 && jet_n>2 && bjet_n>0 && dphi_jetmet>0.4 && mt_gam>90 && ht>1000',
	# 'SRH3_3H_phb' : 'pass_g140==1 && ph_n>0 && ph_pt[0]>450 && met_et>450 && jet_n>1 && bjet_n>0 && dphi_jetmet>0.4 && mt_gam>90 && ht>1000',

	# 'CRQ4_phb' : 'pass_g140==1 && ph_n>0 && ph_pt[0]>145 && met_et>100 && jet_n>4 && bjet_n>1 && dphi_jetmet<0.4 && meff>500',
	# 'CRW4_phb' : 'pass_g140==1 && ph_n>0 && ph_pt[0]>145 && met_et>100 && met_et<200 && jet_n>4 && bjet_n==0 && dphi_jetmet>0.4 && meff>500',
	# 'CRT4_phb' : 'pass_g140==1 && ph_n>0 && ph_pt[0]>145 && met_et>50 && jet_n>5 && bjet_n>1 && dphi_jetmet>0.4 && meff>500',
	# 'SRH4_1L_phb' : 'pass_g140==1 && ph_n>0 && ph_pt[0]>200 && met_et>300 && jet_n>4 && bjet_n>1 && dphi_jetmet>0.4 && meff>2000',
	# 'SRH4_2L_phb' : 'pass_g140==1 && ph_n>0 && ph_pt[0]>200 && met_et>300 && jet_n>4 && bjet_n>2 && dphi_jetmet>0.4 && meff>2000',
	# 'SRH4_3L_phb' : 'pass_g140==1 && ph_n>0 && ph_pt[0]>145 && met_et>300 && jet_n>5 && bjet_n>1 && dphi_jetmet>0.4 && meff>2000',
	# 'SRH4_M_phb' : 'pass_g140==1 && ph_n>0 && ph_pt[0]>400 && met_et>400 && jet_n>3 && bjet_n>1 && dphi_jetmet>0.4 && meff>2000',
	# 'SRH4_1H_phb' : 'pass_g140==1 && ph_n>0 && ph_pt[0]>400 && met_et>400 && jet_n>2 && bjet_n>1 && dphi_jetmet>0.4 && meff>2000',
	# 'SRH4_2H_phb' : 'pass_g140==1 && ph_n>0 && ph_pt[0]>400 && met_et>400 && jet_n>2 && bjet_n>0 && dphi_jetmet>0.4 && meff>2000',
	# 'SRH4_3H_phb' : 'pass_g140==1 && ph_n>0 && ph_pt[0]>450 && met_et>450 && jet_n>1 && bjet_n>0 && dphi_jetmet>0.4 && meff>2000',

	# 'CRQ5_phb' : 'pass_g140==1 && ph_n>0 && el_n+mu_n==0 && ph_pt[0]>145 && met_et>100 && jet_n>4 && bjet_n>0 && dphi_jetmet<0.4 && mt_gam>200 && ht>1000',
	# 'CRW5_phb' : 'pass_g140==1 && ph_n>0 && el_n+mu_n==0 && ph_pt[0]>145 && met_et<200 && met_et>100 && jet_n>4 && bjet_n==0 && dphi_jetmet>0.4 && mt_gam>200 && ht>1000',
	# 'CRT5_phb' : 'pass_g140==1 && ph_n>0 && el_n+mu_n==0 && ph_pt[0]>145 && met_et>50 && jet_n>5 && bjet_n>0 && dphi_jetmet>0.4 && mt_gam>200 && ht>1000',
	# 'SRH5_1L_phb' : 'pass_g140==1 && ph_n>0 && el_n+mu_n==0 && ph_pt[0]>200 && met_et>300 && jet_n>4 && bjet_n>0 && dphi_jetmet>0.4 && mt_gam>200 && ht>1000',
	# 'SRH5_2L_phb' : 'pass_g140==1 && ph_n>0 && el_n+mu_n==0 && ph_pt[0]>200 && met_et>300 && jet_n>4 && bjet_n>1 && dphi_jetmet>0.4 && mt_gam>200 && ht>1000',
	# 'SRH5_3L_phb' : 'pass_g140==1 && ph_n>0 && el_n+mu_n==0 && ph_pt[0]>145 && met_et>300 && jet_n>5 && bjet_n>0 && dphi_jetmet>0.4 && mt_gam>200 && ht>1000',
	# 'SRH5_M_phb' : 'pass_g140==1 && ph_n>0 && el_n+mu_n==0 && ph_pt[0]>400 && met_et>400 && jet_n>3 && bjet_n>0 && dphi_jetmet>0.4 && mt_gam>200 && ht>1000',
	'SRH5_1H_phb' : 'pass_g140==1 && ph_n>0 && el_n+mu_n==0 && ph_pt[0]>400 && met_et>400 && jet_n>2 && bjet_n>0 && dphi_jetmet>0.4 && mt_gam>200 && ht>1000',
	# 'SRH5_2H_phb' : 'pass_g140==1 && ph_n>0 && el_n+mu_n==0 && ph_pt[0]>400 && met_et>400 && jet_n>2 && dphi_jetmet>0.4 && mt_gam>200 && ht>1000',
	# 'SRH5_3H_phb' : 'pass_g140==1 && ph_n>0 && el_n+mu_n==0 && ph_pt[0]>450 && met_et>450 && jet_n>1 && dphi_jetmet>0.4 && mt_gam>200 && ht>1000',

	###### 5

	# 'SRH6_1_phb' : 'pass_g140==1 && ph_n>0 && el_n+mu_n==0 && ph_pt[0]>400 && met_et>400 && jet_n>0 && dphi_jetmet>0.4 && mt_gam>200',
	# 'SRH6_1_phb' : 'pass_g140==1 && ph_n>0 && el_n+mu_n==0 && ph_pt[0]>400 && met_et>400 && jet_n>1 && dphi_jetmet>0.4 && mt_gam>200', #forgot to change name :/
	# 'SRH6_2_phb' : 'pass_g140==1 && ph_n>0 && el_n+mu_n==0 && ph_pt[0]>400 && met_et>400 && jet_n>1 && dphi_jetmet>0.4 && mt_gam>200 && met_sig>15',
	# 'SRH6_3_phb' : 'pass_g140==1 && ph_n>0 && el_n+mu_n==0 && ph_pt[0]>400 && met_et>400 && jet_n>1 && dphi_jetmet>0.4 && mt_gam>200 && rt4>0.7',


	# 'SRL2_1_phb' : 'pass_g140==1 && ph_n>0 && el_n+mu_n==0 && ph_pt[0]>145 && met_et>200 && jet_n>6 && bjet_n>1 && dphi_jetmet>0.4 && mt_gam>90 && ht>2000',
	# 'SRL2_2_phb' : 'pass_g140==1 && ph_n>0 && el_n+mu_n==0 && ph_pt[0]>145 && met_et>200 && jet_n>4 && bjet_n>1 && dphi_jetmet>0.4 && mt_gam>90 && ht>2000',
	# 'SRL2_2_phb' : 'pass_g140==1 && ph_n>0 && el_n+mu_n==0 && ph_pt[0]>145 && met_et>200 && jet_n>5 && bjet_n>2 && dphi_jetmet>0.4 && mt_gam>90 && ht>2000',

	# 'CRQ6_phb' : 'pass_g140==1 && ph_n>0 && el_n+mu_n==0 && ph_pt[0]>200 && met_et>100 && jet_n>1 && dphi_jetmet<0.4 && mt_gam>200',

	# 'CRT6_1_phb' : 'pass_g140==1 && ph_n>0 && el_n+mu_n>0 && ph_pt[0]>150 && met_et>50 && met_et<200 && jet_n>1 && bjet_n>1 && dphi_jetmet>0.4 && mt_gam>300',
	# 'CRT6_2_phb' : 'pass_g140==1 && ph_n>0 && el_n+mu_n>0 && ph_pt[0]>150 && met_et>50 && met_et<200 && jet_n>1 && bjet_n>1 && dphi_jetmet>0.4 && mt_gam>200',
	# 'CRT6_3_phb' : 'pass_g140==1 && ph_n>0 && el_n+mu_n>0 && ph_pt[0]>150 && met_et>50 && met_et<200 && jet_n>1 && bjet_n>1 && dphi_jetmet>0.4 && mt_gam>100',
	# 'CRT6_4_phb' : 'pass_g140==1 && ph_n>0 && el_n+mu_n>0 && ph_pt[0]>150 && met_et>300 && jet_n>1 && bjet_n>1 && dphi_jetmet>0.4 && mt_gam>100',
	# 'CRT6_5_phb' : 'pass_g140==1 && ph_n>0 && ph_pt[0]>150 && met_et>50 && met_et<200 && jet_n>1 && bjet_n>1 && dphi_jetmet>0.4 && mt_gam>200',

	# 'CRW6_1_phb' : 'pass_g140==1 && ph_n>0 && el_n+mu_n>0 && ph_pt[0]>150 && met_et>50 && met_et<200 && jet_n>0 && bjet_n==0 && dphi_jetmet>0.4 && mt_gam>300',
	# 'CRW6_2_phb' : 'pass_g140==1 && ph_n>0 && el_n+mu_n>0 && ph_pt[0]>150 && met_et>50 && met_et<200 && jet_n>0 && bjet_n==0 && dphi_jetmet>0.4 && mt_gam>200',
	# 'CRW6_3_phb' : 'pass_g140==1 && ph_n>0 && el_n+mu_n>0 && ph_pt[0]>150 && met_et>50 && met_et<200 && jet_n>0 && bjet_n==0 && dphi_jetmet>0.4 && mt_gam>100',
	# 'CRW6_4_phb' : 'pass_g140==1 && ph_n>0 && el_n+mu_n>0 && ph_pt[0]>150 && met_et>300 && jet_n>0 && bjet_n==0 && dphi_jetmet>0.4 && mt_gam>200',
	# 'CRW6_5_phb' : 'pass_g140==1 && ph_n>0 && ph_pt[0]>150 && met_et>50 && met_et<200 && jet_n>0 && bjet_n==0 && dphi_jetmet>0.4 && mt_gam>200',

	###### 6

	# 'SRH7_1_phb' : 'pass_g140==1 && ph_n>0 && el_n+mu_n==0 && ph_pt[0]>400 && met_et>400 && jet_n>1 && dphi_jetmet>0.4 && mt_gam>200 && ht>1000',
	# 'SRH7_2_phb' : 'pass_g140==1 && ph_n>0 && el_n+mu_n==0 && ph_pt[0]>400 && met_et>400 && jet_n>2 && dphi_jetmet>0.4 && mt_gam>200',
	# 'SRH7_3_phb' : 'pass_g140==1 && ph_n>0 && el_n+mu_n==0 && ph_pt[0]>400 && met_et>400 && jet_n>2 && dphi_jetmet>0.4 && mt_gam>200 && ht>1000 && rt4>0.7',
	# 'SRH7_4_phb' : 'pass_g140==1 && ph_n>0 && el_n+mu_n==0 && ph_pt[0]>400 && met_et>400 && jet_n>1 && dphi_jetmet>0.4 && mt_gam>200 && ht>1000 && rt4>0.7',
	# 'SRH7_5_phb' : 'pass_g140==1 && ph_n>0 && ph_pt[0]>400 && met_et>400 && jet_n>1 && dphi_jetmet>0.4 && mt_gam>200 && ht>1000',
	# 'SRH7_6_phb' : 'pass_g140==1 && ph_n>0 && el_n+mu_n==0 && ph_pt[0]>400 && met_et>400 && jet_n>1 && dphi_jetmet>0.4 && meff>2400',
	# 'SRH7_7_phb' : 'pass_g140==1 && ph_n>0 && el_n+mu_n>0 && ph_pt[0]>400 && met_et>400 && jet_n>1 && dphi_jetmet>0.4 && mt_gam>200 && ht>1000',
	 

	# 'SRL3_1_phb' : 'pass_g140==1 && ph_n>0 && el_n+mu_n==0 && ph_pt[0]>145 && met_et>200 && jet_n>4 && bjet_n>1 && dphi_jetmet>0.4 && mt_gam>90 && ht>2000',
	# 'SRL3_2_phb' : 'pass_g140==1 && ph_n>0 && el_n+mu_n==0 && ph_pt[0]>145 && met_et>200 && jet_n>5 && bjet_n>1 && dphi_jetmet>0.4 && mt_gam>90 && ht>2000',
	# 'SRL3_3_phb' : 'pass_g140==1 && ph_n>0 && el_n+mu_n==0 && ph_pt[0]>145 && met_et>200 && jet_n>5 && bjet_n>1 && dphi_jetmet>0.4 && mt_gam>90',
	# 'SRL3_4_phb' : 'pass_g140==1 && ph_n>0 && el_n+mu_n==0 && ph_pt[0]>145 && met_et>200 && jet_n>5 && bjet_n>1 && dphi_jetmet>0.2 && mt_gam>90',
	# 'SRL3_5_phb' : 'pass_g140==1 && ph_n>0 && el_n+mu_n==0 && ph_pt[0]>145 && met_et>200 && jet_n>5 && bjet_n>1 && dphi_jetmet>0.2 && mt_gam>90 && ht>2000',
	# 'SRL3_6_phb' : 'pass_g140==1 && ph_n>0 && el_n+mu_n==0 && ph_pt[0]>145 && met_et>200 && jet_n>4 && bjet_n>1 && dphi_jetmet>0.2 && mt_gam>90 && ht>2000',
	# 'SRL3_7_phb' : 'pass_g140==1 && ph_n>0 && el_n+mu_n>0 && ph_pt[0]>145 && met_et>200 && jet_n>5 && bjet_n>1 && dphi_jetmet>0.2 && mt_gam>90',

}	
