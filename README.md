HIG-14-033
==========

Limits nMSSM bba1--> bb tau tau analysis

Installation
------------

Install the HiggsToTauTau limit package,


```shell
export SCRAM_ARCH=slc5_amd64_gcc472
cmsrel CMSSW_6_1_1
cd CMSSW_6_1_1/src/
cmsenv
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
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
cp HIG-14-033/sm_em*.py HiggsAnalysis/HiggsToTauTau/python/layouts/.
```

Changes to HiggsTauTau package:

Extend mass range in setup-datacard.py (line 129), cvs2local.py (line 162). In python/utils.py (line 237):

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

