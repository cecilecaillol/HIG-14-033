'''

Make plots for the HIG-12-053 PAS

'''

from RecoLuminosity.LumiDB import argparse
import math
import os
from poisson import convert
from poisson import poisson_errors
from HttStyles import GetStyleHtt
from HttStyles import MakeCanvas
from HiggsAnalysis.HiggsToTauTau.sigfigs import sigfigs
from sobWeightedCombine import SOBPlotter
from sobWeightedCombine import *
import ROOT

ROOT.gROOT.SetBatch(True)
#ROOT.gROOT.ProcessLine('.x tdrStyle.C')
postfit_src = os.path.join(os.environ['CMSSW_BASE'],
                           'src/HiggsAnalysis/HiggsToTauTau/test/',
                           'root_postfit')

is_blind=True

def getSOverSplusB_EMu(signal1, wz1, zz1, fakes1, hww1):
    sumBG=zz1.Clone()
    sumBG.Add(wz1)
    sumBG.Add(fakes1)
    sumBG.Add(hww1)
    signal=sumBG.Clone()
    signal.Add(signal1)
    bb=range(10)
    x=SOBPlotter()
    x.getSoB(signal, sumBG,bb)
    return bb[0]

def rebin_dN(hist):
    output=hist.Clone()
    for bin in range(output.GetNbinsX()+1):
        output.SetBinContent(bin,output.GetBinContent(bin)/output.GetBinWidth(bin))
        output.SetBinError(bin,output.GetBinError(bin)/output.GetBinWidth(bin))
    return output

def rebin_data_dN(graph,hist):
    output=graph.Clone()
    ref=hist.Clone()
    for bin in range(output.GetN()):
        output.SetPoint(bin, output.GetX()[bin], output.GetY()[bin]/ref.GetBinWidth(bin+1))
        output.SetPointEYhigh(bin, output.GetErrorYhigh(bin)/ref.GetBinWidth(bin+1))
        output.SetPointEYlow(bin, output.GetErrorYlow(bin)/ref.GetBinWidth(bin+1))
    return output

def text_channel(canal):   
   """ Writes channel name """
   subchannels_left=['em']
   #chan     = ROOT.TPaveText(0.22, 0.76+0.013, 0.44, 0.76+0.155, "NDC")
   chan     = ROOT.TPaveText(0.22, 0.68+0.013, 0.46, 0.68+0.155, "NDC")
   #chan     = ROOT.TPaveText(0.80, 0.77+0.013, 0.90, 0.77+0.155, "NDC")#droite
   #chan     = ROOT.TPaveText(0.68, 0.76+0.013, 0.90, 0.76+0.155, "NDC")
   chan.SetBorderSize(   0 )
   chan.SetFillStyle(    0 )
   chan.SetTextAlign(   12 )
   chan.SetTextSize ( 0.04 )
   chan.SetTextColor(    1 )
   chan.SetTextFont (   62 )
   texte=' '
   if canal=='emu_btag':
	 texte='e#mu'
   if canal=='emu_btag':
         texte='e#mu'
   if canal=='muTau_btag':
         texte='#mu#tau_{h}'
   if canal=='muTau_nobtag':
         texte='#mu#tau'
   if canal=='eleTau_btag':
         texte='e#tau_{h}'
   if canal=='eleTau_nobtag':
         texte='e#tau'
   chan.AddText(texte)
   return chan


def fix_maximum(channel_dict, type):
    """ Make sure everything is visible """
    max = channel_dict['stack'].GetMaximum()
    histo = channel_dict['data']
    cushion=1.3
    #for bin in range(histo.GetNbinsX()):
    #    content = histo.GetBinContent(bin)
	#L,U=poisson_errors(content)
        #if content>0:
        #   upper = content + math.sqrt(content)
        #else:
        #   upper = content
        #print bin, upper, max
        #if  U > max:
        #    max = U
    channel_dict['stack'].SetMaximum(cushion*max/1)
    #if type=="ZH":
    #    channel_dict['stack'].SetMaximum(cushion * max/20)

def add_lumi():
    lowX=0.64
    lowY=0.835
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.30, lowY+0.16, "NDC")
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.SetTextSize(0.045)
    lumi.AddText("19.7 fb^{-1} (8 TeV)")
    return lumi

def add_CMS():
    lowX=0.21
    lowY=0.75
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.15, lowY+0.16, "NDC")
    lumi.SetTextFont(61)
    lumi.SetTextSize(0.06)
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.AddText("CMS")
    return lumi 

def add_Preliminary():
    lowX=0.21
    lowY=0.73
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.15, lowY+0.16, "NDC")
    lumi.SetTextSize(0.03)
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.SetTextFont(52)
    lumi.AddText("Preliminary")
    return lumi 

def add_cms_blurb(sqrts, intlumi, preliminary=False, blurb=''):
    """ Add a CMS blurb to a plot """
    # Same style as Htt
    label_text = "CMS Preliminary"
    if preliminary:
        label_text += " Preliminary"
    label_text +=","
    label_text += " %s fb^{-1}" % (intlumi)
    label_text += " at %s TeV" % sqrts
    label_text += " " + blurb
    lowX=0.16
    lowY=0.835
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.30, lowY+0.16, "NDC")
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextSize ( 0.04 )
    lumi.SetTextColor(    1 )
    lumi.SetTextFont (   62 )
    lumi.AddText(label_text)
    return lumi

_styles = {
    "ztt": {
        # Same as Z+jets
        'fillstyle': 1001,
        'fillcolor': ROOT.TColor.GetColor(248,206,104),
        'linecolor': ROOT.EColor.kBlack,
        'linewidth': 3,
    },
    "low": {
        # Same as Z+jets
        'fillstyle': 1001,
        'fillcolor': ROOT.TColor.GetColor(148,106,4),
        'linecolor': ROOT.EColor.kBlack,
        'linewidth': 3,
    },
    "EWK": {
        # Same as W+jets
        'fillstyle': 1001,
        'fillcolor': ROOT.TColor.GetColor(222,90,106),
        'linecolor': ROOT.EColor.kBlack,
        'linewidth': 3,
    },
    "fakes": {
        # Same as QCD
        'fillcolor': ROOT.TColor.GetColor(250,202,255),
        'linecolor': ROOT.EColor.kBlack,
        'fillstyle': 1001,
        'linewidth': 3,
    },
    "ttbar": {
        # Same as QCD
        'fillcolor': ROOT.TColor.GetColor(132,112,255),
        'linecolor': ROOT.EColor.kBlack,
        'fillstyle': 1001,
        'linewidth': 3,
    },
    "hww": {
        'fillstyle': 1001,
        'fillcolor': ROOT.EColor.kGreen + 2,
        'linecolor': ROOT.EColor.kBlack,
        'linewidth': 3,
    },
    "signal": {
        'fillcolor': 0,
        'fillstyle': 0,
        'linestyle': 11,
        'linewidth': 3,
        'linecolor': ROOT.EColor.kBlue,
        'name': "VH",
    },
    "signal2": {
        'fillcolor': 0,
        'fillstyle': 0,
        'linestyle': 11,
        'linewidth': 3,
        'linecolor': ROOT.EColor.kGreen,
        'name': "VH",
    },
    "data": {
        'markerstyle': 20,
        'markersize': 1,
        'linewidth': 3,
        'markercolor': ROOT.EColor.kBlack,
        'legendstyle': 'pe',
        'format': 'pe',
        'name': "Observed",
    }
}


def apply_style(histogram, style_type):
    style = _styles[style_type]
    if 'fillstyle' in style:
        histogram.SetFillStyle(style['fillstyle'])
    if 'fillcolor' in style:
        histogram.SetFillColor(style['fillcolor'])
    if 'linecolor' in style:
        histogram.SetLineColor(style['linecolor'])
    if 'linestyle' in style:
        histogram.SetLineStyle(style['linestyle'])
    if 'linewidth' in style:
        histogram.SetLineWidth(style['linewidth'])
    if 'markersize' in style:
        histogram.SetMarkerSize(style['markersize'])
    if 'markercolor' in style:
        histogram.SetMarkerColor(style['markercolor'])


def get_combined_histogram(histograms, directories, files, title=None,
                           scale=None, style=None):
    """ Get a histogram that is the combination of all paths/files"""
    if isinstance(histograms, basestring):
        histograms = [histograms]
    output = None
    for file in files:
        for path in directories:
            for histogram in histograms:
                   th1 = file.Get(path + '/' + histogram)
                   if output is None:
                       output = th1.Clone()
                   else :
                       output.Add(th1)
                   #if histogram=="data_obs":
                   #         for i in range(1,14):#partial blinding
                   #              output.SetBinContent(i,-100)
    if scale is not None:
        output.Scale(scale)
    if title is not None:
        output.SetTitle(title)
    if style:
        apply_style(output, style)
    return output


if __name__ == "__main__":

    style1=GetStyleHtt()
    style1.cd()


    parser = argparse.ArgumentParser()

    parser.add_argument('--prefit', action='store_true',
                        help="Don't use postfit")

    parser.add_argument('--period', default="all",
                        choices=['7TeV', '8TeV', 'all'],
                        help="Which data taking period")

    parser.add_argument('--MLfit', default="all",
                        choices=['channel', 'all'],
                        help="Which fit")

    args = parser.parse_args()

    prefit_8TeV_file = ROOT.TFile.Open(
        "limits/cmb/common/htt_em.input_8TeV.root")

    postfit_8TeV_file = ROOT.TFile.Open(postfit_src + "/htt_em.input_8TeV.root")

    files_to_use_map_emu = {
        (True, '8TeV'): [prefit_8TeV_file],
        (False, '8TeV'): [postfit_8TeV_file],
    }
    files_to_use_emu = files_to_use_map_emu[(args.prefit, args.period)]

    if args.MLfit=="all":
        postfit_8TeV_file = ROOT.TFile.Open(postfit_src + "/htt_em.input_8TeV.root")
        files_to_use_map = {
            (True, '8TeV'): [prefit_8TeV_file],
            (False, '8TeV'): [postfit_8TeV_file],
        }
        files_to_use_emu = files_to_use_map[(args.prefit, args.period)]

    # Get all our histograms
    histograms = {}
    yield_errors = {}
    yields = {}

    emu_subplots = {
        #'emu_btag': ['emu_btag'],
        'emu_btag': ['emu_btag'],
    }
    etau_subplots = {
        #'eleTau_nobtag': ['eleTau_nobtag'],
        'eleTau_btag': ['eleTau_btag'],
    }
    mutau_subplots = {
        #'muTau_nobtag': ['muTau_nobtag'],
        'muTau_btag': ['muTau_btag'],
    }
    num_bins_emu=10#15
    # ZH
    #histograms['emu'] = {}
    #yields['emu']={}
    #yield_errors['emu'] = {}
    #emu_channels = [
    #    'emu_btag','emu_btag',
    #]
    emu_channels = [
        'emu_btag',
    ]
    for emusubset, channel_subset in emu_subplots.iteritems():
        emu_plots = {}
        emu_erreurs = {}
	emu_integrales = {}
        histograms[emusubset] = emu_plots
	yields[emusubset] = emu_integrales
        yield_errors[emusubset] = emu_erreurs

        emu_plots['EWK'] = get_combined_histogram(['EWK'], channel_subset, files_to_use_emu, title='EWK',style='EWK')
        erreur=ROOT.Double(0)
        integrale=emu_plots['EWK'].IntegralAndError(1,num_bins_emu,erreur)
        emu_integrales['EWK']=float(integrale)
        emu_erreurs['EWK']=float(erreur)

        emu_plots['ztt'] = get_combined_histogram(['Ztt','DYlow'], channel_subset, files_to_use_emu, title='ztt',style='ztt')
        erreur=ROOT.Double(0)
        integrale=emu_plots['ztt'].IntegralAndError(1,num_bins_emu,erreur)
        emu_integrales['ztt']=float(integrale)
        emu_erreurs['ztt']=float(erreur)

        emu_plots['low'] = get_combined_histogram(['DYlow'], channel_subset, files_to_use_emu, title='low',style='low')
        erreur=ROOT.Double(0)
        integrale=emu_plots['low'].IntegralAndError(1,num_bins_emu,erreur)
        emu_integrales['low']=float(integrale)
        emu_erreurs['low']=float(erreur)

        emu_plots['fakes'] = get_combined_histogram(
            'Fakes', channel_subset, files_to_use_emu, title='Reducible bkg.',
            style='fakes'
        )
        integrale=emu_plots['fakes'].IntegralAndError(1,num_bins_emu,erreur)
        emu_integrales['fakes']=float(integrale)
        emu_erreurs['fakes']=float(erreur)

        emu_plots['ttbar'] = get_combined_histogram(
            'ttbar', channel_subset, files_to_use_emu, title='ttbar',
            style='ttbar'
        )
        integrale=emu_plots['ttbar'].IntegralAndError(1,num_bins_emu,erreur)
        emu_integrales['ttbar']=float(integrale)
        emu_erreurs['ttbar']=float(erreur)

        emu_plots['hww'] = get_combined_histogram(
            ['ggH_SM125','qqH_SM125','VH_SM125'], channel_subset, files_to_use_emu,title='m_{H}=125 GeV', style='hww'
        )
        integrale=emu_plots['hww'].IntegralAndError(1,num_bins_emu,erreur)
        emu_integrales['hww']=float(integrale)
        emu_erreurs['hww']=float(erreur)

        emu_plots['signal'] = get_combined_histogram(
            'bba135', channel_subset, files_to_use_emu,
            title='m_{a1}=35 GeV', style='signal',
        )

        emu_plots['signal2'] = get_combined_histogram(
            'bba130', channel_subset, files_to_use_emu,
            title='m_{a1}=30 GeV', style='signal2',
        )

        integrale=emu_plots['signal'].IntegralAndError(1,num_bins_emu,erreur)
        emu_integrales['signal']=float(integrale)
        emu_erreurs['signal']=float(erreur)
        emu_plots['data'] = get_combined_histogram(
            'data_obs', channel_subset, files_to_use_emu,
            title='data', style='data',
        )
        #emu_plots['data'].GetXaxis().SetRangeUser(0,50)
        integrale=emu_plots['data'].IntegralAndError(1,num_bins_emu,erreur)
        emu_integrales['data']=float(integrale)
        emu_erreurs['data']=float(erreur)
        emu_plots['stack'] = ROOT.THStack("emu_stack", "emu_stack")
        emu_plots['stack'].Add(rebin_dN(emu_plots['hww']), 'hist')
        emu_plots['stack'].Add(rebin_dN(emu_plots['fakes']), 'hist')
        emu_plots['stack'].Add(rebin_dN(emu_plots['EWK']), 'hist')
        emu_plots['stack'].Add(rebin_dN(emu_plots['ttbar']), 'hist')
        emu_plots['stack'].Add(rebin_dN(emu_plots['ztt']), 'hist')
        #emu_plots['stack'].Add(rebin_dN(emu_plots['low']), 'hist')
	emu_plots['signal'].Scale(40) #Signal scaling !!!!!!!!!
        emu_plots['signal2'].Scale(40)
        emu_plots['stack2']=emu_plots['stack'].Clone()
        emu_plots['stack'].Add(rebin_dN(emu_plots['signal']), 'hist')
        emu_plots['stack2'].Add(rebin_dN(emu_plots['signal2']), 'hist')


        errorZH=emu_plots['ztt'].Clone()
        errorZH.SetFillStyle(3013)
        #errorZH.Add(emu_plots['low'])
        errorZH.Add(emu_plots['fakes'])
        errorZH.Add(emu_plots['ttbar'])
        errorZH.Add(emu_plots['EWK'])
        errorZH.SetMarkerSize(0)
        errorZH.SetFillColor(13)
        errorZH.SetLineWidth(1)
        errorZH_rebin=rebin_dN(errorZH)

	emu_plots['error'] = errorZH_rebin
	emu_plots['data'].SetMarkerStyle(20)
        emu_plots['data'].SetMarkerColor(ROOT.EColor.kBlack)
        emu_plots['data'].SetLineColor(ROOT.EColor.kBlack)
        emu_plots['data'].SetLineWidth(2)
        emu_plots['data'].SetMarkerSize(2)
	#emu_plots['data_rebin']=rebin_dN(emu_plots['data'])
	def make_legend():
            output = ROOT.TLegend(0.60, 0.65, 0.92, 0.90, "", "brNDC")
	    #output = ROOT.TLegend(0.22, 0.55, 0.54, 0.80, "", "brNDC")
            output.SetLineWidth(0)
            output.SetLineStyle(0)
            output.SetFillStyle(0)
            output.SetBorderSize(0)
            output.SetTextFont(62)
            return output

        emu_plots['legend'] = make_legend()
        emu_plots['legend'].AddEntry(emu_plots['signal'],
                                        "A (m=35 GeV, xs=40 pb)", "l")
        #emu_plots['legend'].AddEntry(emu_plots['signal2'],
        #                                "a1(m=30 GeV, xs=40 pb)", "l")
        emu_plots['legend'].AddEntry(emu_plots['data'],
                                        "Observed", "lp")
        #emu_plots['legend'].AddEntry(emu_plots['hww'],
        #                                "SM H(125 GeV)", "f")
        #emu_plots['legend'].AddEntry(emu_plots['low'], "Z#rightarrow#tau#tau (low mass)", "f")
        emu_plots['legend'].AddEntry(emu_plots['ztt'], "Z#rightarrow#tau#tau", "f")
        emu_plots['legend'].AddEntry(emu_plots['ttbar'], "t#bar{t}", "f")
        emu_plots['legend'].AddEntry(emu_plots['EWK'],"EWK", "f")
        emu_plots['legend'].AddEntry(emu_plots['fakes'],"Fakes", "f")
        if args.prefit==False:
           emu_plots['legend'].AddEntry(errorZH, "Bkg. uncertainty", "F")

    # etau
    #histograms['etau'] = {}
    #yields['etau']={}
    #yield_errors['etau'] = {}
    #etau_channels = [
    #    'eleTau_nobtag','eleTau_btag',
    #]
    etau_channels = [
        'eleTau_btag',
    ]
    for etausubset, channel_subset in etau_subplots.iteritems():
        etau_plots = {}
        etau_erreurs = {}
        etau_integrales = {}
        histograms[etausubset] = etau_plots
        yields[etausubset] = etau_integrales
        yield_errors[etausubset] = etau_erreurs
	print channel_subset
        etau_plots['EWK'] = get_combined_histogram(['VV','W','ZJ','ZL'], channel_subset, files_to_use_emu, title='EWK',style='EWK')
        erreur=ROOT.Double(0)
        integrale=etau_plots['EWK'].IntegralAndError(1,num_bins_emu,erreur)
        etau_integrales['EWK']=float(integrale)
        etau_erreurs['EWK']=float(erreur)

        etau_plots['ztt'] = get_combined_histogram(['ZTT','ZTT_lowMass'], channel_subset, files_to_use_emu, title='ztt',style='ztt')
        erreur=ROOT.Double(0)
        integrale=etau_plots['ztt'].IntegralAndError(1,num_bins_emu,erreur)
        etau_integrales['ztt']=float(integrale)
        etau_erreurs['ztt']=float(erreur)

        etau_plots['low'] = get_combined_histogram(['ZTT_lowMass'], channel_subset, files_to_use_emu, title='low',style='low')
        erreur=ROOT.Double(0)
        integrale=etau_plots['low'].IntegralAndError(1,num_bins_emu,erreur)
        etau_integrales['low']=float(integrale)
        etau_erreurs['low']=float(erreur)

        etau_plots['fakes'] = get_combined_histogram('QCD', channel_subset, files_to_use_emu, title='Reducible bkg.',
            style='fakes'
        )
        integrale=etau_plots['fakes'].IntegralAndError(1,num_bins_emu,erreur)
        etau_integrales['fakes']=float(integrale)
        etau_erreurs['fakes']=float(erreur)

        etau_plots['ttbar'] = get_combined_histogram('TT', channel_subset, files_to_use_emu, title='ttbar',
            style='ttbar'
        )
        integrale=etau_plots['ttbar'].IntegralAndError(1,num_bins_emu,erreur)
        etau_integrales['ttbar']=float(integrale)
        etau_erreurs['ttbar']=float(erreur)

        etau_plots['hww'] = get_combined_histogram(
            ['ggH_SM125','qqH_SM125','VH_SM125'], channel_subset, files_to_use_emu,
            title='m_{H}=125 GeV', style='hww'
        )
        integrale=etau_plots['hww'].IntegralAndError(1,num_bins_emu,erreur)
        etau_integrales['hww']=float(integrale)
        etau_erreurs['hww']=float(erreur)

        etau_plots['signal'] = get_combined_histogram(
            'bba135', channel_subset, files_to_use_emu,
            title='m_{a1}=35 GeV', style='signal',
        )
        etau_plots['signal2'] = get_combined_histogram(
            'bba130', channel_subset, files_to_use_emu,
            title='m_{a1}=30 GeV', style='signal2',
        )
        integrale=etau_plots['signal'].IntegralAndError(1,num_bins_emu,erreur)
        etau_integrales['signal']=float(integrale)
        etau_erreurs['signal']=float(erreur)
        etau_plots['data'] = get_combined_histogram(
            'data_obs', channel_subset, files_to_use_emu,
            title='data', style='data',
        )
        integrale=etau_plots['data'].IntegralAndError(1,num_bins_emu,erreur)
        etau_integrales['data']=float(integrale)
        etau_erreurs['data']=float(erreur)
        etau_plots['stack'] = ROOT.THStack("etau_stack", "etau_stack")
        etau_plots['stack'].Add(rebin_dN(etau_plots['hww']), 'hist')
        etau_plots['stack'].Add(rebin_dN(etau_plots['fakes']), 'hist')
        etau_plots['stack'].Add(rebin_dN(etau_plots['EWK']), 'hist')
        etau_plots['stack'].Add(rebin_dN(etau_plots['ttbar']), 'hist')
        etau_plots['stack'].Add(rebin_dN(etau_plots['ztt']), 'hist')
        #etau_plots['stack'].Add(rebin_dN(etau_plots['low']), 'hist')
        etau_plots['signal'].Scale(40) #Signal scaling !!!!!!!!!
        etau_plots['signal2'].Scale(40)
        etau_plots['stack2']=etau_plots['stack'].Clone()
        etau_plots['stack'].Add(rebin_dN(etau_plots['signal']), 'hist')
        etau_plots['stack2'].Add(rebin_dN(etau_plots['signal2']), 'hist')

        errorETAU=etau_plots['ztt'].Clone()
        errorETAU.SetFillStyle(3013)
        #errorETAU.Add(etau_plots['low'])
        errorETAU.Add(etau_plots['fakes'])
        errorETAU.Add(etau_plots['ttbar'])
        errorETAU.Add(etau_plots['EWK'])
        errorETAU.SetMarkerSize(0)
        errorETAU.SetFillColor(13)
        errorETAU.SetLineWidth(1)
        errorETAU_rebin=rebin_dN(errorETAU)

        etau_plots['error'] = errorETAU_rebin
        etau_plots['data'].SetMarkerStyle(20)
        etau_plots['data'].SetMarkerColor(ROOT.EColor.kBlack)
        etau_plots['data'].SetLineColor(ROOT.EColor.kBlack)
        etau_plots['data'].SetLineWidth(2)
        etau_plots['data'].SetMarkerSize(2)
        #emu_plots['data_rebin']=rebin_dN(emu_plots['data'])

        etau_plots['legend'] = make_legend()
        etau_plots['legend'].AddEntry(etau_plots['signal'],
                                        "A (m=35 GeV, xs=40 pb)", "l")
        #etau_plots['legend'].AddEntry(etau_plots['signal2'],
        #                                "a1(m=30 GeV, xs=40 pb)", "l")
        etau_plots['legend'].AddEntry(etau_plots['data'],
                                        "Observed", "lp")
        #etau_plots['legend'].AddEntry(etau_plots['hww'],
        #                                "SM H(125 GeV)", "f")
        #etau_plots['legend'].AddEntry(etau_plots['low'], "Z#rightarrow#tau#tau (low mass)", "f")
        etau_plots['legend'].AddEntry(etau_plots['ztt'], "Z#rightarrow#tau#tau", "f")
        etau_plots['legend'].AddEntry(etau_plots['ttbar'], "t#bar{t}", "f")
        etau_plots['legend'].AddEntry(etau_plots['EWK'],
                                        "EWK", "f")
        etau_plots['legend'].AddEntry(etau_plots['fakes'],
                                        "QCD", "f")
        if args.prefit==False:
           etau_plots['legend'].AddEntry(errorETAU, "Bkg. uncertainty", "F")

    # mutau
    #histograms['mutau'] = {}
    #yields['mutau']={}
    #yield_errors['mutau'] = {}
    #mutau_channels = [
    #    'muTau_nobtag','muTau_btag',
    #]
    mutau_channels = [
        'muTau_btag',
    ]
    for mutausubset, channel_subset in mutau_subplots.iteritems():
        mutau_plots = {}
        mutau_erreurs = {}
        mutau_integrales = {}
        histograms[mutausubset] = mutau_plots
        yields[mutausubset] = mutau_integrales
        yield_errors[mutausubset] = mutau_erreurs

        mutau_plots['EWK'] = get_combined_histogram(['VV','W','ZJ','ZL'], channel_subset, files_to_use_emu, title='EWK',style='EWK')
        erreur=ROOT.Double(0)
        integrale=mutau_plots['EWK'].IntegralAndError(1,num_bins_emu,erreur)
        mutau_integrales['EWK']=float(integrale)
        mutau_erreurs['EWK']=float(erreur)

        mutau_plots['ztt'] = get_combined_histogram(['ZTT','ZTT_lowMass'], channel_subset, files_to_use_emu, title='ztt',style='ztt')
        erreur=ROOT.Double(0)
        integrale=mutau_plots['ztt'].IntegralAndError(1,num_bins_emu,erreur)
        mutau_integrales['ztt']=float(integrale)
        mutau_erreurs['ztt']=float(erreur)

        mutau_plots['low'] = get_combined_histogram(['ZTT_lowMass'], channel_subset, files_to_use_emu, title='low',style='low')
        erreur=ROOT.Double(0)
        integrale=mutau_plots['low'].IntegralAndError(1,num_bins_emu,erreur)
        mutau_integrales['low']=float(integrale)
        mutau_erreurs['low']=float(erreur)

        mutau_plots['fakes'] = get_combined_histogram(
            'QCD', channel_subset, files_to_use_emu, title='Reducible bkg.',
            style='fakes'
        )
        integrale=mutau_plots['fakes'].IntegralAndError(1,num_bins_emu,erreur)
        mutau_integrales['fakes']=float(integrale)
        mutau_erreurs['fakes']=float(erreur)

        mutau_plots['ttbar'] = get_combined_histogram(
            'TT', channel_subset, files_to_use_emu, title='ttbar',
            style='ttbar'
        )
        integrale=mutau_plots['ttbar'].IntegralAndError(1,num_bins_emu,erreur)
        mutau_integrales['ttbar']=float(integrale)
        mutau_erreurs['ttbar']=float(erreur)

        mutau_plots['hww'] = get_combined_histogram(
            ['ggH_SM125','qqH_SM125','VH_SM125'], channel_subset, files_to_use_emu,
            title='m_{H}=125 GeV', style='hww'
        )
        integrale=mutau_plots['hww'].IntegralAndError(1,num_bins_emu,erreur)
        mutau_integrales['hww']=float(integrale)
        mutau_erreurs['hww']=float(erreur)

        mutau_plots['signal'] = get_combined_histogram(
            'bba135', channel_subset, files_to_use_emu,
            title='m_{a1}=35 GeV', style='signal',
        )
        mutau_plots['signal2'] = get_combined_histogram(
            'bba130', channel_subset, files_to_use_emu,
            title='m_{a1}=30 GeV', style='signal2',
        )
        integrale=mutau_plots['signal'].IntegralAndError(1,num_bins_emu,erreur)
        mutau_integrales['signal']=float(integrale)
        mutau_erreurs['signal']=float(erreur)
        mutau_plots['data'] = get_combined_histogram(
            'data_obs', channel_subset, files_to_use_emu,
            title='data', style='data',
        )
        integrale=mutau_plots['data'].IntegralAndError(1,num_bins_emu,erreur)
        mutau_integrales['data']=float(integrale)
        mutau_erreurs['data']=float(erreur)
        mutau_plots['stack'] = ROOT.THStack("mutau_stack", "mutau_stack")
        mutau_plots['stack'].Add(rebin_dN(mutau_plots['hww']), 'hist')
        mutau_plots['stack'].Add(rebin_dN(mutau_plots['fakes']), 'hist')
        mutau_plots['stack'].Add(rebin_dN(mutau_plots['EWK']), 'hist')
        mutau_plots['stack'].Add(rebin_dN(mutau_plots['ttbar']), 'hist')
        mutau_plots['stack'].Add(rebin_dN(mutau_plots['ztt']), 'hist')
        #mutau_plots['stack'].Add(rebin_dN(mutau_plots['low']), 'hist')
        mutau_plots['stack2']=mutau_plots['stack'].Clone()
        mutau_plots['signal'].Scale(40) #Signal scaling !!!!!!!!!
        mutau_plots['signal2'].Scale(40)
        mutau_plots['stack'].Add(rebin_dN(mutau_plots['signal']), 'hist')
        mutau_plots['stack2'].Add(rebin_dN(mutau_plots['signal2']), 'hist')

        errorMUTAU=mutau_plots['ztt'].Clone()
        errorMUTAU.SetFillStyle(3013)
        #errorMUTAU.Add(mutau_plots['low'])
        errorMUTAU.Add(mutau_plots['fakes'])
        errorMUTAU.Add(mutau_plots['ttbar'])
        errorMUTAU.Add(mutau_plots['EWK'])
        errorMUTAU.SetMarkerSize(0)
        errorMUTAU.SetFillColor(13)
        errorMUTAU.SetLineWidth(1)
        errorMUTAU_rebin=rebin_dN(errorMUTAU)

        mutau_plots['error'] = errorMUTAU_rebin
        mutau_plots['data'].SetMarkerStyle(20)
        mutau_plots['data'].SetMarkerColor(ROOT.EColor.kBlack)
        mutau_plots['data'].SetLineColor(ROOT.EColor.kBlack)
        mutau_plots['data'].SetLineWidth(2)
        mutau_plots['data'].SetMarkerSize(2)
        #mutau_plots['data_rebin']=rebin_dN(mutau_plots['data'])

        mutau_plots['legend'] = make_legend()
        mutau_plots['legend'].AddEntry(mutau_plots['signal'],
                                        "A (m=35 GeV, xs=40 pb)", "l")
        #mutau_plots['legend'].AddEntry(mutau_plots['signal2'],
        #                                "a1(m=30 GeV, xs=40 pb)", "l")
        mutau_plots['legend'].AddEntry(mutau_plots['data'],
                                        "Observed", "lp")
        #mutau_plots['legend'].AddEntry(mutau_plots['hww'],
        #                                "SM H(125 GeV)", "f")
        #mutau_plots['legend'].AddEntry(mutau_plots['low'], "Z#rightarrow#tau#tau (low mass)", "f")
        mutau_plots['legend'].AddEntry(mutau_plots['ztt'], "Z#rightarrow#tau#tau", "f")
        mutau_plots['legend'].AddEntry(mutau_plots['ttbar'], "t#bar{t}", "f")
        mutau_plots['legend'].AddEntry(mutau_plots['EWK'],
                                        "EWK", "f")
        mutau_plots['legend'].AddEntry(mutau_plots['fakes'],
                                        "QCD", "f")
        if args.prefit==False:
           mutau_plots['legend'].AddEntry(errorMUTAU, "Bkg. uncertainty", "F")

    # Apply some styles to all the histograms
    for channel in histograms.keys():
	print channel
        histograms[channel]['poisson'] = convert(histograms[channel]['data'],set_zero_bins=-10)
        fix_maximum(histograms[channel],'ZH')
        histograms[channel]['stack'].Draw("")
        histograms[channel]['stack'].GetYaxis().SetTitle("#bf{Events / GeV}")#("#bf{dN/dm_{#tau#tau} [1/GeV]}" )
        histograms[channel]['stack'].GetXaxis().SetTitle("#bf{m_{#tau#tau} [GeV]}")
        histograms[channel]['stack2'].Draw("same")

    plot_suffix = "_%s_%s_%s.pdf" % (
        'prefit' if args.prefit else 'postfit',
        args.period,
        'FitByChannel' if args.MLfit=="channel" else 'FitAllChannels'
    )
    plot_suffix_png = "_%s_%s_%s.png" % (
        'prefit' if args.prefit else 'postfit',
        args.period,
        'FitByChannel' if args.MLfit=="channel" else 'FitAllChannels'
    )
    blurb_map = {
        '8TeV': ('19.7', '8'),
    }
    int_lumi, sqrts = blurb_map[args.period]

    canvas = MakeCanvas("asdf","asdf",800,800)
    #canvas.SetLogy()

    for emu_key in emu_subplots:
        histograms[emu_key]['stack'].Draw()
        #histograms[emu_key]['stack'].GetHistogram().GetXaxis().SetRangeUser(0,50)
        #histograms[emu_key]['stack'].Draw("same")
	#histograms[emu_key]['stack'].Draw("axis same")
        #histograms[emu_key]['stack2'].Draw("same")
        if args.prefit==False:
           histograms[emu_key]['error'].Draw("e2same")
        histograms[emu_key]['poisson'].SetMarkerStyle(20)
        #histograms[emu_key]['poisson'].GetXaxis().SetRangeUser(0,50)
        histograms[emu_key]['poisson'].SetMarkerColor(ROOT.EColor.kBlack)
        histograms[emu_key]['poisson'].SetLineColor(ROOT.EColor.kBlack)
        histograms[emu_key]['poisson'].SetLineWidth(2)
        histograms[emu_key]['poisson'].SetMarkerSize(2)
	histograms[emu_key]['poisson_rebin']=rebin_data_dN(histograms[emu_key]['poisson'],histograms[emu_key]['data'])
        histograms[emu_key]['poisson_rebin'].Draw('pe same')
	histograms[emu_key]['legend'].SetTextFont(62)
        histograms[emu_key]['legend'].Draw()
        #histograms[emu_key]['stack'].Draw("same")
        #if args.prefit==False:
        #   histograms[emu_key]['error'].Draw("e2same")

        #lumiBlurb=add_cms_blurb(sqrts, int_lumi)
        #lumiBlurb.Draw("same")
        lumiBlurb1=add_CMS()
        lumiBlurb1.Draw("same")
        lumiBlurb2=add_Preliminary()
        #lumiBlurb2.Draw("same")
        lumiBlurb=add_lumi()
        lumiBlurb.Draw("same")
        channel_text=text_channel(emu_key)
        channel_text.Draw('same')
        canvas.SaveAs('plots/' + emu_key + plot_suffix)
        canvas.SaveAs('plots/' + emu_key + plot_suffix_png)

    for etau_key in etau_subplots:
        histograms[etau_key]['stack'].Draw()
        #histograms[etau_key]['stack'].GetHistogram().GetXaxis().SetRangeUser(0,50)
        #histograms[etau_key]['stack'].Draw("same")
        #histograms[etau_key]['stack'].Draw("axis same")
        #histograms[etau_key]['stack2'].Draw("same")
        if args.prefit==False:
           histograms[etau_key]['error'].Draw("e2same")
        histograms[etau_key]['poisson'].SetMarkerStyle(20)
        histograms[etau_key]['poisson'].SetMarkerColor(ROOT.EColor.kBlack)
        histograms[etau_key]['poisson'].SetLineColor(ROOT.EColor.kBlack)
        histograms[etau_key]['poisson'].SetLineWidth(2)
        histograms[etau_key]['poisson'].SetMarkerSize(2)
        histograms[etau_key]['poisson_rebin']=rebin_data_dN(histograms[etau_key]['poisson'],histograms[etau_key]['data'])
        histograms[etau_key]['poisson_rebin'].Draw('pe same')
        histograms[etau_key]['legend'].SetTextFont(62)
        histograms[etau_key]['legend'].Draw()
        #lumiBlurb=add_cms_blurb(sqrts, int_lumi)
        #lumiBlurb.Draw("same")
        lumiBlurb1=add_CMS()
        lumiBlurb1.Draw("same")
        lumiBlurb2=add_Preliminary()
        #lumiBlurb2.Draw("same")
        lumiBlurb=add_lumi()
        lumiBlurb.Draw("same")
        channel_text=text_channel(etau_key)
        channel_text.Draw('same')
        canvas.SaveAs('plots/' + etau_key + plot_suffix)
        canvas.SaveAs('plots/' + etau_key + plot_suffix_png)

    for mutau_key in mutau_subplots:
        histograms[mutau_key]['stack'].Draw()
        #histograms[mutau_key]['stack'].GetHistogram().GetXaxis().SetRangeUser(0,50)
        #histograms[mutau_key]['stack'].Draw("same")
        #histograms[mutau_key]['stack'].Draw("axis same")
        #histograms[mutau_key]['stack2'].Draw("same")
        if args.prefit==False:
           histograms[mutau_key]['error'].Draw("e2same")
        histograms[mutau_key]['poisson'].SetMarkerStyle(20)
        histograms[mutau_key]['poisson'].SetMarkerColor(ROOT.EColor.kBlack)
        histograms[mutau_key]['poisson'].SetLineColor(ROOT.EColor.kBlack)
        histograms[mutau_key]['poisson'].SetLineWidth(2)
        histograms[mutau_key]['poisson'].SetMarkerSize(2)
        histograms[mutau_key]['poisson_rebin']=rebin_data_dN(histograms[mutau_key]['poisson'],histograms[mutau_key]['data'])
        histograms[mutau_key]['poisson_rebin'].Draw('pe same')
	print mutau_key
        histograms[mutau_key]['legend'].SetTextFont(62)
        histograms[mutau_key]['legend'].Draw()
        #lumiBlurb=add_cms_blurb(sqrts, int_lumi)
        #lumiBlurb.Draw("same")
        lumiBlurb1=add_CMS()
        lumiBlurb1.Draw("same")
        lumiBlurb2=add_Preliminary()
        #lumiBlurb2.Draw("same")
        lumiBlurb=add_lumi()
        lumiBlurb.Draw("same")
        channel_text=text_channel(mutau_key)
        channel_text.Draw('same')
        canvas.SaveAs('plots/' + mutau_key + plot_suffix)
        canvas.SaveAs('plots/' + mutau_key + plot_suffix_png)

################ Combined ##################

    #histogramsCmb=ROOT.THStack("cmb_stack", "cmb_stack")
    #histogramsCmb.Add(mutau_plots['fakes'])
    #histogramsCmb.Add(etau_plots['fakes'])
    #histogramsCmb.Add(emu_plots['fakes'])
    #histogramsCmb.Add(mutau_plots['EWK'])
    #histogramsCmb.Add(etau_plots['EWK'])
    #histogramsCmb.Add(emu_plots['EWK'])
    #histogramsCmb.Add(mutau_plots['ttbar'])
    #histogramsCmb.Add(etau_plots['ttbar'])
    #histogramsCmb.Add(emu_plots['ttbar'])
    #histogramsCmb.Add(mutau_plots['ztt'])
    #histogramsCmb.Add(etau_plots['ztt'])
    #histogramsCmb.Add(emu_plots['ztt'])
    #histogramsCmb.GetYaxis().SetTitle("#bf{dN/dm_{#tau#tau} [1/GeV]}" )
    #histogramsCmb.GetXaxis().SetTitle("#bf{m_{#tau#tau} [GeV]}")
    #histogramsCmb.GetHistogram().GetYaxis().SetRangeUser(0,0.2*histogramsCmb.GetMaximum())
    #histogramsCmb.Draw()
    #histogramsCmb.GetHistogram().GetYaxis().SetRangeUser(0,0.2*histogramsCmb.GetMaximum())
    #histogramsCmb.GetHistogram().GetXaxis().SetRangeUser(0,50)
    #histogramsCmb.Draw("same")
    #histogramsD=histograms["muTau_btag"]['poisson']
    #histogramsD.Add(histograms["eleTau_btag"]['poisson'])
    #histogramsD.Add(histograms["emu_btag"]['poisson'])
    #histogramsD.Draw('pe same')
    #histograms["muTau_btag"]['legend'].Draw()
    #lumiBlurb=add_cms_blurb(sqrts, int_lumi)
    #lumiBlurb.Draw("same")
    #channel_text=text_channel("Combined")
    #channel_text.Draw('same')
    #canvas.SaveAs('plots/cmb' + plot_suffix)
    #canvas.SaveAs('plots/cmb' + plot_suffix_png)

    postfit="postfit"
    if args.prefit:
        postfit="prefit"
    text_file2=open("nMSSM_table_paper_"+postfit+".tex","w")
    text_file2.write('\\begin{tabular}{l | c | c | c | c} \n')
    text_file2.write('Process & Signal & Background & Data & $\\frac{S}{S+B}$ \\\\ \n')
    text_file2.write('\hline \n\hline \n')
    text_file2.write('$\\Pe\\Pgm btag & %.3f $\\pm %.3f & %.1f $\\pm$ %.1f & %.0f & %.3f \\\\ \n' %(yields['emu_btag']['signal'],yield_errors['emu_btag']['signal'],yields['emu_btag']['fakes']+yields['emu_btag']['ttbar']+yields['emu_btag']['EWK']+yields['emu_btag']['ztt'],(yield_errors['emu_btag']['fakes']**2+yield_errors['emu_btag']['EWK']**2+yield_errors['emu_btag']['ttbar']**2+yield_errors['emu_btag']['ztt']**2)**0.5,yields['emu_btag']['data'],getSOverSplusB_EMu(histograms['emu_btag']['signal'],histograms['emu_btag']['fakes'],histograms['emu_btag']['ztt'],histograms['emu_btag']['ttbar'],histograms['emu_btag']['EWK'])))
    text_file2.write('$\\Pe\\Pgth btag & %.3f $\\pm %.3f & %.1f $\\pm$ %.1f & %.0f & %.3f \\\\ \n' %(yields['eleTau_btag']['signal'],yield_errors['eleTau_btag']['signal'],yields['eleTau_btag']['fakes']+yields['eleTau_btag']['ttbar']+yields['eleTau_btag']['EWK']+yields['eleTau_btag']['ztt'],(yield_errors['eleTau_btag']['fakes']**2+yield_errors['eleTau_btag']['EWK']**2+yield_errors['eleTau_btag']['ttbar']**2+yield_errors['eleTau_btag']['ztt']**2)**0.5,yields['eleTau_btag']['data'],getSOverSplusB_EMu(histograms['eleTau_btag']['signal'],histograms['eleTau_btag']['fakes'],histograms['eleTau_btag']['ztt'],histograms['eleTau_btag']['ttbar'],histograms['eleTau_btag']['EWK'])))
    text_file2.write('$\\Pgm\\Pgth btag & %.3f $\\pm %.3f & %.1f $\\pm$ %.1f & %.0f & %.3f \\\\ \n' %(yields['muTau_btag']['signal'],yield_errors['muTau_btag']['signal'],yields['muTau_btag']['fakes']+yields['muTau_btag']['ttbar']+yields['muTau_btag']['EWK']+yields['muTau_btag']['ztt'],(yield_errors['muTau_btag']['fakes']**2+yield_errors['muTau_btag']['EWK']**2+yield_errors['muTau_btag']['ttbar']**2+yield_errors['muTau_btag']['ztt']**2)**0.5,yields['muTau_btag']['data'],getSOverSplusB_EMu(histograms['muTau_btag']['signal'],histograms['muTau_btag']['fakes'],histograms['muTau_btag']['ztt'],histograms['muTau_btag']['ttbar'],histograms['muTau_btag']['EWK'])))
    text_file2.write('\\hline \n')
    text_file2.write('\\end{tabular} \n')

    print yields['emu_btag']['signal'],yields['emu_btag']['ztt'],yields['emu_btag']['ttbar'],yields['emu_btag']['fakes'],yields['emu_btag']['EWK']
    print yields['muTau_btag']['signal'],yields['muTau_btag']['ztt'],yields['muTau_btag']['ttbar'],yields['muTau_btag']['fakes'],yields['muTau_btag']['EWK']
    print yields['eleTau_btag']['signal'],yields['eleTau_btag']['ztt'],yields['eleTau_btag']['ttbar'],yields['eleTau_btag']['fakes'],yields['eleTau_btag']['EWK']
