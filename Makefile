
# Working directory
BASE=$(CMSSW_BASE)/src
WD=$(BASE)/HIG-14-033

# Location of the CGS and uncertainty configuration files
SETUP=$(BASE)/HiggsAnalysis/HiggsToTauTau/setup/em
SETUP1=$(BASE)/HiggsAnalysis/HiggsToTauTau/setup
SETUPBBB=$(BASE)/HiggsAnalysis/HiggsToTauTau/setup_bbb
SETUPBBB2=$(BASE)/HiggsAnalysis/HiggsToTauTau/setup_bbb2
HTT_TEST=$(BASE)/HiggsAnalysis/HiggsToTauTau/test

LIMITDIR=$(WD)/limits

# where the raw generated cards are generated.
CARDDIR=$(BASE)/auxiliaries/datacards
CARDS=$(BASE)/auxiliaries/datacards/sm/htt_em
COLLECT=$(BASE)/auxiliaries/shapes/VHTT


################################################################################
#####  Recipes for combining all shape files ###################################
################################################################################

# Combine all 8TeV shape files
$(SETUP)/htt_em.inputs-sm-8TeV.root: $(COLLECT)/EMu_SVMass_8TeV.root 
	hadd -f $@ $^

SHAPEFILE8=$(SETUP)/htt_em.inputs-sm-8TeV.root


################################################################################
#####  Recipes for building ZH cards ###########################################
################################################################################

ZH_CONFIGS8=$(wildcard $(SETUP)/*-sm-8TeV-01.* $(SETUP)/*-sm-8TeV-02.* $(SETUP)/*-sm-8TeV-03.*)

$(CARDS)/.zh8_timestamp: $(SHAPEFILE8) $(ZH_CONFIGS8)
	@echo "Recipes for building ZH cards 8TeV"
	rm -f $(CARDS)/em_1_8TeV*
	#rm -f $(CARDS)/em_2_8TeV*
	rm -f $(CARDS)/em_3_8TeV*
	#rm -f $(CARDS)/em_0_8TeV*
	rm -f $(CARDS)/em_4_8TeV*
	#rm -f $(CARDS)/em_5_8TeV*
	rm -f $@
	cd $(BASE)  && $(WD)/add_bbb_errors_VH.py -f 'em:8TeV:01:Fakes,DYlow' -i $(SETUP1) -o $(SETUPBBB) --threshold 0.10 && $(WD)/add_bbb_errors_VH.py -f 'em:8TeV:03,04:W,QCD,ZTT_lowMass' -i $(SETUPBBB) -o $(SETUPBBB2) --threshold 0.10 && setup-datacards.py -i $(SETUPBBB2) -p 8TeV --a sm 25_80:5 -c em --sm-categories-em "1 3 4" && touch $@
	#cd $(BASE)  && $(WD)/add_bbb_errors_VH.py -f 'em:8TeV:01,02:Fakes,Ztt,ttbar,EWK' -i $(SETUP1) -o $(SETUPBBB) --threshold 0.10 --normalize && setup-datacards.py -i $(SETUPBBB) -p 8TeV --a sm 25-80:5 -c em --sm-categories-em "1 2" && touch $@

zh: $(CARDS)/.zh8_timestamp

cards: zh 

################################################################################
#####  Recipes for generating the limit combo directory ########################
################################################################################

$(LIMITDIR)/.timestamp: $(CARDS)/.zh8_timestamp 
	rm -rf $(LIMITDIR)
	cd $(BASE) && $(WD)/setup_htt_channels.py -o $(LIMITDIR) -c em --sm-categories-em "1 3 4" -p 8TeV 25_80:5 && touch $@

limitdir: $(LIMITDIR)/.timestamp


pulls/.timestamp: $(LIMITDIR)/.timestamp do_pull.sh
	rm -rf pulls
	mkdir -p pulls
	cp -r $(LIMITDIR)/cmb/40 pulls/40
	cp -r $(LIMITDIR)/cmb/common pulls/common	
	./do_pull.sh && touch $@

pulls: pulls/.timestamp

$(HTT_TEST)/.fit_timestamp: $(LIMITDIR)/.timestamp
	cd $(HTT_TEST) && ./mlfit_and_copy.py $(LIMITDIR)/cmb/40 && touch $@
	cp $(HTT_TEST)/fitresults/mlfit_sm.txt mlfit_vh.txt

$(HTT_TEST)/root_postfit/.timestamp: $(HTT_TEST)/.fit_timestamp
	rm -fr $(HTT_TEST)/root_postfit
	cp -r $(HTT_TEST)/root $(HTT_TEST)/root_postfit
	#cd $(HTT_TEST) && ./postfit.py root_postfit/htt_em.input_8TeV.root datacards/htt_em_0_8TeV.txt \
	#  --bins muTau_nobtag \
	#  --verbose
	cd $(HTT_TEST) && ./postfit.py root_postfit/htt_em.input_8TeV.root datacards/htt_em_1_8TeV.txt \
          --bins emu_btag \
          --verbose
	#cd $(HTT_TEST) && ./postfit.py root_postfit/htt_em.input_8TeV.root datacards/htt_em_2_8TeV.txt \
        #  --bins emu_nobtag \
        #  --verbose
	cd $(HTT_TEST) && ./postfit.py root_postfit/htt_em.input_8TeV.root datacards/htt_em_3_8TeV.txt \
          --bins muTau_btag \
          --verbose
	cd $(HTT_TEST) && ./postfit.py root_postfit/htt_em.input_8TeV.root datacards/htt_em_4_8TeV.txt \
          --bins eleTau_btag \
          --verbose
	#cd $(HTT_TEST) && ./postfit.py root_postfit/htt_em.input_8TeV.root datacards/htt_em_5_8TeV.txt \
        #  --bins eleTau_nobtag \
        #  --verbose
	touch $@

plots/.mass_timestamp: $(HTT_TEST)/root_postfit/.timestamp
	rm -rf plots
	mkdir -p plots
	python VH_massplots.py --prefit --period 8TeV --MLfit all
	python VH_massplots.py --period 8TeV --MLfit all
	touch $@

postfit: $(HTT_TEST)/root_postfit/.timestamp

massplots: plots/.mass_timestamp


#########################################a#######################################
#####  Computing the limits ####################################################
################################################################################

NPROCS=10

$(LIMITDIR)/.computed: $(LIMITDIR)/.timestamp
	echo "Computing ZH combined limits"
	./compute_limits.sh cmb $(NPROCS)
	touch $@

$(LIMITDIR)/.chan_computed: $(LIMITDIR)/.timestamp
	echo "Computing ZH combined limits"
	./compute_limits.sh emu $(NPROCS)
	./compute_limits.sh etau $(NPROCS)
	./compute_limits.sh mutau $(NPROCS)
	#./compute_limits.sh btag $(NPROCS)
	#./compute_limits.sh nobtag $(NPROCS)
	#./compute_limits.sh eleTau_btag $(NPROCS)
	#./compute_limits.sh muTau_btag $(NPROCS)
	#./compute_limits.sh emu_btag $(NPROCS)
	#./compute_limits.sh eleTau_nobtag $(NPROCS)
	#./compute_limits.sh muTau_nobtag $(NPROCS)
	#./compute_limits.sh emu_nobtag $(NPROCS)
	touch $@

limits: $(LIMITDIR)/.computed $(LIMITDIR)/.chan_computed


################################################################################
#####  Plotting the limits #####################################################
################################################################################

# This dumb macro needs to be compiled.
$(BASE)/HiggsAnalysis/HiggsToTauTau/macros/compareLimits_C.so: $(BASE)/HiggsAnalysis/HiggsToTauTau/macros/compareLimits.C
	cd $(BASE) && source HiggsAnalysis/HiggsToTauTau/environment.sh

comparemacro: $(BASE)/HiggsAnalysis/HiggsToTauTau/macros/compareLimits_C.so

$(LIMITDIR)/.plot_timestamp: $(LIMITDIR)/.computed $(BASE)/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_em_*.py
	rm -f $@
	cd $(LIMITDIR) && plot --asymptotic $(BASE)/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_em_exp_layout.py cmb/ max=80.0
	#cd $(LIMITDIR) && plot --asymptotic $(BASE)/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_em_exp_layout.py eleTau_btag/ max=100.0
	#cd $(LIMITDIR) && plot --asymptotic $(BASE)/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_em_exp_layout.py muTau_btag/ max=100.0
	#cd $(LIMITDIR) && plot --asymptotic $(BASE)/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_em_exp_layout.py emu_btag/ max=100.0
	#cd $(LIMITDIR) && plot --asymptotic $(BASE)/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_em_exp_layout.py eleTau_nobtag/ max=400.0
	#cd $(LIMITDIR) && plot --asymptotic $(BASE)/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_em_exp_layout.py muTau_nobtag/ max=400.0
	#cd $(LIMITDIR) && plot --asymptotic $(BASE)/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_em_exp_layout.py emu_nobtag/ max=400.0
	cd $(LIMITDIR) && plot --asymptotic $(BASE)/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_em_exp_layout.py emu/ max=100.0
	cd $(LIMITDIR) && plot --asymptotic $(BASE)/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_em_exp_layout.py etau/ max=100.0
	cd $(LIMITDIR) && plot --asymptotic $(BASE)/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_em_exp_layout.py mutau/ max=100.0
	#cd $(LIMITDIR) && plot --asymptotic $(BASE)/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_em_exp_layout.py btag/ max=100.0
	#cd $(LIMITDIR) && plot --asymptotic $(BASE)/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_em_exp_layout.py nobtag/ max=400.0
	#cd $(LIMITDIR) && plot --asymptotic $(BASE)/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_em_exp_layout.py eleTau_btag/ max=180.0
	#cd $(LIMITDIR) && plot --asymptotic $(BASE)/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_em_exp_layout.py muTau_btag/ max=180.0
	#cd $(LIMITDIR) && plot --asymptotic $(BASE)/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_em_exp_layout.py emu_btag/ max=180.0
	touch $@

plots/.limits_timestamp: $(LIMITDIR)/.plot_timestamp
	mkdir -p plots
	#cp $(LIMITDIR)/vhtt_zh_exp_limit.pdf plots/
	#cp $(LIMITDIR)/vhtt_zh_exp_limit.tex plots/
	#cp $(LIMITDIR)/vhtt_zh_limit.pdf plots/
	#cp $(LIMITDIR)/vhtt_zh_limit.tex plots/
	touch $@

$(LIMITDIR)/.chan_plot_timestamp: $(LIMITDIR)/.chan_computed $(BASE)/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_em_*.py
	rm -f $@
	#cd $(LIMITDIR) && plot --asymptotic $(BASE)/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_em_exp_layout.py lowDR/ max=200.0
	#cd $(LIMITDIR) && plot --asymptotic $(BASE)/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_em_exp_layout.py mediumDR/ max=200.0
	#cd $(LIMITDIR) && plot --asymptotic $(BASE)/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_em_exp_layout.py highDR/ max=200.0
	#cd $(LIMITDIR) && plot --asymptotic $(BASE)/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_em_exp_layout.py nocat/ max=200.0
	#cd $(LIMITDIR) && plot --asymptotic $(BASE)/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_vhtt_layout.py llem/ max=40.0
	#cd $(LIMITDIR) && plot --asymptotic $(BASE)/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_vhtt_layout.py llmt/ max=40.0
	#cd $(LIMITDIR) && plot --asymptotic $(BASE)/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_vhtt_layout.py llet/ max=40.0
	#cd $(LIMITDIR) && plot --asymptotic $(BASE)/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_vhtt_layout.py lltt/ max=40.0
	rm -f $(LIMITDIR)/limits_limit.root 
	hadd $(LIMITDIR)/limits_limit.root $(LIMITDIR)/*_limit.root
	#root -b -q 'compareVHlimits.C+("limits/limits_limit.root", "eleTau_btag,emu_btag,muTau_btag,cmb", true, false, "sm-xsex", 0, 200, false,"CMS Preliminary, 19.7 fb^{-1} at 8TeV",false,true)'
	#mv singleLimits_expected_sm.pdf plots/compa_zh.pdf
	touch $@

plots/.chan_limits_timestamp: $(LIMITDIR)/.chan_plot_timestamp
	mkdir -p plots
	cp $(LIMITDIR)/*limit.pdf plots/
	cp $(LIMITDIR)/*limit.txt plots/
	touch $@

plotlimits: plots/.limits_timestamp plots/.chan_limits_timestamp

clean:
	rm -f vh_table.tex
	rm -rf plots/
	rm -rf pulls
	rm -rf $(LIMITDIR)
	rm -rf $(SETUP)/*.root

.PHONY: cards zh ltt llt limitdir pulls postfit massplots limits significance comparemacro plotlimits plotsignificances clean
