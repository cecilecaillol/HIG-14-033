HIG-14-033
==========

Limits nMSSM bba1--> bb tau tau analysis

Installation
------------

Install the HiggsToTauTau limit package,


```shell
setenv SCRAM_ARCH slc6_amd64_gcc481
cmsrel CMSSW_7_1_5 ### must be a 7_1_X release  >= 7_1_5;  (7.0.X and 7.2.X are NOT supported either) 
cd CMSSW_7_1_5/src 
cmsenv
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit
git fetch origin
git checkout v5.0.1
scramv1 b clean; scramv1 b # always make a clean build
cd ../..
git clone https://github.com/cms-analysis/HiggsAnalysis-HiggsToTauTau.git HiggsAnalysis/HiggsToTauTau
git clone https://github.com/roger-wolf/HiggsAnalysis-HiggsToTauTau-auxiliaries.git auxiliaries
scram b -j 4; rehash
```

then check out this package:

```shell
git clone https://github.com/cecilecaillol/HIG-14-033.git
```

Copy the files:

```shell
cp HIG-14-033/uncertainty_files/* HiggsAnalysis/HiggsToTauTau/setup/em/.
cp HIG-14-033/root_file/*.root auxiliaries/shapes/VHTT/.
cp HIG-14-033/postfit_right_errors.py HiggsAnalysis/HiggsToTauTau/test/postfit.py
cp HIG-14-033/layouts/*.py HiggsAnalysis/HiggsToTauTau/python/layouts/.
cp HIG-14-033/Limit.cc HiggsAnalysis/HiggsToTauTau/src/Limit.cc
```

Changes to HiggsTauTau package:

Extend mass range in setup-datacards.py (line 129), cvs2local.py (line 162). In python/utils.py (line 237):

```shell
        'em' : {
        '00' : ['0jet_low' ],
        '01' : ['emu_btag'],
        '02' : ['1jet_low' ],
        '03' : ['mutau_btag'],
        '04' : ['etau_btag'],
        '05' : ['vbf_tight'],

```

In python/utils.py (line 156):

```shell
        'em'  : '',
```

To clean the directories from previous files and results:
```shell
cd HIG-14-033
sh clean.sh
```

Producing Results
-----------------

All the tricks to build the results are contained in the Makefile.  The
important commands are:

```shell
cd HIG-14-033
```

Run the post fit and make all the final mass distribution plots

```shell
make massplots
```

Compute all the limits

```shell
make limits
```

Plot the limits (they show up in limits/*pdf)

```shell
make plotlimits
```

