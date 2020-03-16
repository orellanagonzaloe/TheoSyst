
samples = [	
			# 'GGM_GG_bhmix_2000_250',
			# 'GGM_GG_bhmix_2000_1050',
			# 'GGM_GG_bhmix_2000_1950',
			# 'GGM_GG_bhmix_2200_250',
			# 'GGM_GG_bhmix_2200_1050',
			# 'GGM_GG_bhmix_2200_2150',
			# 'GGM_GG_bhmix_2400_250',
			# 'GGM_GG_bhmix_2400_1050',
			# 'GGM_GG_bhmix_2400_2350',

			# 'MG_phb_go_1400_mu_-250',
			# 'MG_phb_go_1400_mu_-1050',
			# 'MG_phb_go_1400_mu_-1350',
			# 'MG_phb_go_1600_mu_-250',
			# 'MG_phb_go_1600_mu_-1050',
			# 'MG_phb_go_1600_mu_-1550',
			# 'MG_phb_go_2000_mu_-250',
			# 'MG_phb_go_2000_mu_-1050',
			# 'MG_phb_go_2000_mu_-1950',
			# 'MG_phb_go_2200_mu_-250',
			# 'MG_phb_go_2200_mu_-1050',
			# 'MG_phb_go_2200_mu_-2150',
			# 'MG_phb_go_2400_mu_-250',
			# 'MG_phb_go_2400_mu_-1050',
			# 'MG_phb_go_2400_mu_-2350',

			# 'MG_phj_go_2000_mu_250',
			# 'MG_phj_go_2000_mu_1050',
			# 'MG_phj_go_2000_mu_1950',
			# 'MG_phj_test3_go_2000_mu_250',
			# 'MG_phj_test3_go_2000_mu_1050',
			# 'MG_phj_test3_go_2000_mu_1950',

			# 'MG_phb_go_2000_mu_-250_Gmass_1E-07',
			# 'MG_phb_go_2000_mu_-1050_Gmass_1E-07',
			# 'MG_phb_go_2000_mu_-1950_Gmass_1E-07',
			# 'MG_phb_go_2000_mu_-250_Gmass_4E-07',
			# 'MG_phb_go_2000_mu_-1050_Gmass_4E-07',
			# 'MG_phb_go_2000_mu_-1950_Gmass_4E-07',
			# 'MG_phb_go_2000_mu_-250_Gmass_6E-08',
			# 'MG_phb_go_2000_mu_-1050_Gmass_6E-08',
			# 'MG_phb_go_2000_mu_-1950_Gmass_6E-08',

			# 'MG_phb_go_2000_mu_-250_Gmass_4E-07_2',
			# 'MG_phb_go_2000_mu_-1050_Gmass_4E-07_2',
			# 'MG_phb_go_2000_mu_-1950_Gmass_4E-07_2',
			# 'MG_phb_go_2000_mu_-250_Gmass_6E-08_2',
			# 'MG_phb_go_2000_mu_-1050_Gmass_6E-08_2',
			# 'MG_phb_go_2000_mu_-1950_Gmass_6E-08_2',

			# 'MG_phb_test4_go_2000_mu_-250',
			# 'MG_phb_test4_go_2000_mu_-1050',
			# 'MG_phb_test4_go_2000_mu_-1950',
			# 'MG_phb_test5_go_2000_mu_-250',
			# 'MG_phb_test5_go_2000_mu_-1050',
			# 'MG_phb_test5_go_2000_mu_-1950',
			# 'MG_phb_test6_go_2000_mu_-250',
			# 'MG_phb_test6_go_2000_mu_-1050',
			# 'MG_phb_test6_go_2000_mu_-1950',

			# 'MG_phb_good1_go_1600_mu_-250',
			# 'MG_phb_good1_go_1600_mu_-1050',
			# 'MG_phb_good1_go_1600_mu_-1550',

			'MG_phb_good1_go_2000_mu_-250_1',
			'MG_phb_good1_go_2000_mu_-1050_1',
			'MG_phb_good1_go_2000_mu_-1950_1',

			# 'MG_phb_good1_go_2400_mu_-250',
			# 'MG_phb_good1_go_2400_mu_-1050',
			# 'MG_phb_good1_go_2400_mu_-2350',

			'vgammagamma',
			'znunugamma',
			'zjets',
			'wgamma',
			'wjets',
			'ttbar',
			'ttgamma',
			'multijet',
			'photonjet_nnlo',
			# 'diphoton', # is not ready for 2018
			# 'zllgamma', # no lo uso joaco
			'higgs',

			# 'data',

			# 'bkg1',
			# 'bkg2',
			# 'bkg3',
			# 'bkg4',
			# 'bkg5',
			# 'bkg6',
			# 'bkg7',
			# 'bkg8',
			# 'bkg9',
			# 'bkg10',
			# 'bkg11',
			# 'bkg12',
			# 'bkg13',
			# 'bkg14',

			]

variables = [	
				'ph_pt[0]',
				'jet_n',
				'bjet_n',
				'el_n+mu_n',
				'met_et',
				'mt_gam',
				'dphi_jetmet',
				'dphi_gammet',
				'ht',
				'meff',
				'rt4',
				'met_sig',
				# 'bbmass_lead',
				# 'bbmass_w',
			]

lumi_dict = {
	'2015':  3219.56,
	'2016': 32965.30,
	'20152016': 36184.86,
	'2017': 44307.40,
	'2018': 59937.20,
	}

year_dict = {
	'2015' : ['2015'],
	'2016' : ['2016'],
	'2017' : ['2017'],
	'2018' : ['2018'],
	'20152016' : ['20152016'],
	'fullR2' : ['20152016','2017','2018'],
	}

tag_dict = {
	'2015': 'mc16a',
	'2016': 'mc16a',
	'20152016': 'mc16a',
	'2017': 'mc16d',
	'2018': 'mc16e',
	}

did_dict = {
	'photonjet': '364544',
	'ttgamma': '407320',
	'wgamma': '364525',
	'zllgamma': '364504',
	'znunugamma': '364519',
	}


eos_path = '/eos/user/f/falonso/data/mini2/'
eos_path_gonza = '/eos/user/g/goorella/data/mini2/'
eos_path_plots = '/eos/user/g/goorella/plots/optimization/'

binning_dict = dict()
binning_dict['ph_pt[0]']  = (14, 145., 1545.)  ##(145., 200, 250, 300, 350, 400, 450, 500, 550, 600, 700, 800, 900, 1000, 1250, 1500, 1750, 2000)
binning_dict['jet_n']   = (20, 0, 20)
binning_dict['bjet_n']  = (20, 0, 20)
binning_dict['el_n+mu_n']  = (20, 0, 20)
binning_dict['met_et']  = (10, 0., 1000.)
binning_dict['mt_gam']  = (60, 0., 1500.)
binning_dict['dphi_jetmet']     = (17, 0., 3.4)
binning_dict['dphi_gammet']     = (17, 0., 3.4)
binning_dict['ht']              = (30, 0., 6000.)
binning_dict['bbmass_w']          = (50, 0., 500.)
binning_dict['bbmass_lead']          = (50, 0., 500.)
binning_dict['meff']            = (12, 0., 6000.)
binning_dict['rt4']             = (22, 0., 1.1)
binning_dict['met_sig']             = (50, 0., 50.)


def clean_var(var):
	return var.replace(':', '_').replace('[','').replace(']', '').replace('(', '').replace(')','')


def get_xs_norm(sample):


	d_norm = {

		'1400' : 0.284E-01,
		'1600' : 0.887E-02,
		'2000' : 0.101E-02,
		'2200' : 0.356E-03,
		'2400' : 0.128E-03,

	}

	m_go = sample.split('_').index('bhmix')

	return d_norm[sample.split('_')[m_go+1]]



