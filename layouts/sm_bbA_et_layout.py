import FWCore.ParameterSet.Config as cms

layout = cms.PSet(
    ## dataset
    #dataset = cms.string(" 2012, #sqrt{s} = 8 TeV, H #rightarrow #tau #tau, L = 5.0 fb^{-1}"),
    #dataset = cms.string(" 2011, #sqrt{s} = 7 TeV, H #rightarrow #tau #tau, L = 4.9 fb^{-1}"),
    dataset = cms.string("e#tau_{h}"),
    #dataset = cms.string("CMS Preliminary, #sqrt{s} = 7 TeV, A#rightarrow Zh#rightarrow ll#tau#tau, L = 4.9 fb^{-1}"),
    ## x-axis title
    xaxis = cms.string("m_{A} [GeV]"),
    ## x-axis title
    yaxis = cms.string("95% CL #sigma(bbA) #times B(A#rightarrow#tau#tau) [pb]"),
    ## plot expected only
    expectedOnly = cms.bool(False),
    ## is this mssm?
    mssm = cms.bool(True),
    ## print to png
    png  = cms.bool(True),
    ## print to pdf
    pdf  = cms.bool(True),
    ## print to txt
    txt  = cms.bool(True),
    ## print to root
    root = cms.bool(True),
    ## min for plotting
    min = cms.double(12),
    ## max for plotting
    max = cms.double(10), ##12
    ## min for plotting
    log = cms.int32(1),
    ## define verbosity level
    verbosity   = cms.uint32(2),
    ## define output label
    outputLabel = cms.string("limit"),
    ## define masspoints for limit plot
    #masspoints = cms.vdouble(range(110, 146, 5))
    masspoints = cms.vdouble(range(25, 81, 5))
)
