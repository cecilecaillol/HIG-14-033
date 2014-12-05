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

To clean the directories from previous files and results:
```shell
sh clean.sh
```

Producing Results
-----------------

All the tricks to build the results are contained in the Makefile.  The
important commands are:

```shell
cd HIG-14-033
```

# Run the post fit and make all the final mass distribution plots
make massplots

# Compute all the limits
make limits
# Plot the limits (they show up in limits/*pdf)
make plotlimits

