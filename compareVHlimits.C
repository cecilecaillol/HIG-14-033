#include "string" 
#include "vector" 
#include "fstream"
#include "iomanip"
#include "iostream"
#include "algorithm"

#include "TTree.h"
#include "TFile.h"
#include "TAxis.h"
#include "TGraph.h"
#include "TString.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TPaveLabel.h"
#include "TGraphAsymmErrors.h"

#include "/afs/cern.ch/work/c/ccaillol/VH_HIG-13-004/CMSSW_6_1_1/src/HiggsAnalysis/HiggsToTauTau/macros/Utils.h"
#include "/afs/cern.ch/work/c/ccaillol/VH_HIG-13-004/CMSSW_6_1_1/src/HiggsAnalysis/HiggsToTauTau/interface/HttStyles.h"
#include "/afs/cern.ch/work/c/ccaillol/VH_HIG-13-004/CMSSW_6_1_1/src/HiggsAnalysis/HiggsToTauTau/src/HttStyles.cc"

static const double MARKER_SIZE = 1.3;  // 0.7

bool
channel(std::string& label){
  return (label==std::string("cmb")          ||
	  label==std::string("emu_btag")      ||
	  label==std::string("eleTau_btag")  ||
	  label==std::string("muTau_btag")      ||
          label==std::string("btag")          ||
          label==std::string("nobtag")          ||
          label==std::string("emu_nobtag")          ||
          label==std::string("eleTau_nobtag")         ||
          label==std::string("muTau_nobtag")         ||
          label==std::string("emu")         ||
          label==std::string("etau")         ||
          label==std::string("mutau")          ||
          label==std::string("ett")         
	  );
}

std::string legendEntry(const std::string& channel){
  std::string title;
  if(channel==std::string("emu_btag"        )) title = std::string("e#mu btag");
  if(channel==std::string("eleTau_btag"        )) title = std::string("e#tau btag");
  if(channel==std::string("muTau_btag"        )) title = std::string("#mu#tau btag");
  if(channel==std::string("cmb"       )) title = std::string("Combined");
  if(channel==std::string("emu_nobtag"        )) title = std::string("e#mu no btag");
  if(channel==std::string("eleTau_nobtag"        )) title = std::string("e#tau no btag");
  if(channel==std::string("muTau_nobtag"        )) title = std::string("#mu#tau no btag");
  if(channel==std::string("btag"        )) title = std::string("btag");
  if(channel==std::string("nobtag"        )) title = std::string("no btag");
  if(channel==std::string("emu"        )) title = std::string("e#mu");
  if(channel==std::string("etau"        )) title = std::string("e#tau");
  if(channel==std::string("mutau"        )) title = std::string("#mu#tau");
  if(channel==std::string("ett"        )) title = std::string("e#tau_{h}#tau_{h}");
  return title;
}

void compareVHlimits(const char* filename, const char* channelstr, bool expected, bool observed, const char* type, double minimum=0., double maximum=100., bool log=false, const char* label="CMS Preliminary,  H#rightarrow#tau#tau,  5.0 fb^{-1} at 7 TeV, 19.7 fb^{-1} at 8 TeV", bool legendOnRight=true, bool legendOnTop=true)
{
  SetStyle();

  std::map<std::string, unsigned int> colors;
  colors["emu_btag"      ] = kViolet-6;
  colors["eleTau_btag"  ] = kGreen+2;
  colors["muTau_btag"      ] = kPink+7;
  colors["cmb"          ] = kBlack;
  colors["emu_nobtag"          ] = kOrange+7;
  colors["muTau_nobtag"          ] = kCyan+2;
  colors["eleTau_nobtag"          ] = kBlue+1;
  colors["emu"         ] = kGreen-1;
  colors["etau"         ] = kOrange-5;
  colors["mutau"         ] = kRed-4;
  colors["btag"         ] = kCyan+3;
  colors["nobtag"          ] = kRed;
  colors["ett"          ] = kBlue-4;

  std::cout << " *******************************************************************************************************\n"
	    << " * Usage     : root -l                                                                                  \n"
	    << " *             .x MitLimits/Higgs2Tau/macros/compareLimits.C+(file, chn, exp, obs, type, min, max, log) \n"
	    << " *                                                                                                      \n"
	    << " * Arguments :  + file     const char*      full path to the input file                                 \n"
	    << " *              + chn      const char*      list of channels; choose between: 'cmb', 'htt', 'emu',      \n"
	    << " *                                          'etau', 'mutau', 'mumu', 'vhtt', 'hgg', 'hww', 'ggH',       \n"
	    << " *                                          'bbH', 'nomix[-200, +200]', 'mhmax[-400, -200, +200]'       \n"
	    << " *                                          'mhmax[+400, +600, +800]', 'test-0...5', 'saeff', 'gluph'   \n"
	    << " *                                          The list should be comma separated and may contain          \n"
	    << " *                                          whitespaces                                                 \n"
	    << " *              + exp       bool            compare expected limits                                     \n"
	    << " *              + obs       bool            compare observed limits                                     \n"
	    << " *              + type      const char*     type of plot; choose between 'sm-xsec', 'mssm-xsec' and     \n"
	    << " *                                          'mssm-tanb'                                                 \n"
	    << " *              + max       double          maximum of the plot (default is 20.)                        \n"
	    << " *                                                                                                      \n"
	    << " *              + min       double          minimum of the plot (default is  0.)                        \n"
	    << " *                                                                                                      \n"
	    << " *              + log       bool            set log scale yes or no (default is false)                  \n"
	    << " *                                                                                                      \n"
	    << " *******************************************************************************************************\n";

  /// open input file  
  TFile* inputFile = new TFile(filename); if(inputFile->IsZombie()){ std::cout << "ERROR:: file: " << filename << " does not exist.\n"; }

  /// prepare input parameters
  std::vector<std::string> channels;
  string2Vector(cleanupWhitespaces(channelstr), channels);

  /// prepare histograms
  std::vector<TGraph*> hobs, hexp;
  for(unsigned i=0; i<channels.size(); ++i){
    if(observed) hobs.push_back(get<TGraph>(inputFile, std::string(channels[i]).append("/observed").c_str()));
    if(expected) hexp.push_back(get<TGraph>(inputFile, std::string(channels[i]).append("/expected").c_str()));
  }

  /// do the drawing
  TCanvas* canv1 = new TCanvas("canv1", "Limit Comparison", 600, 600);
  canv1->cd();
  canv1->SetGridx(1);
  canv1->SetGridy(1);
 
  bool firstPlot=true;
  for(unsigned int i=0; i<hexp.size(); ++i){
    if(firstPlot){
      if(std::string(type) == std::string("mssm-xsec")){
	if(log){ canv1->SetLogy(1); }
	hexp[i]->SetMaximum(maximum);
	hexp[i]->SetMinimum(minimum);
      }
      else{
	if(log){ canv1->SetLogy(1); }
	hexp[i]->SetMaximum(maximum);
	hexp[i]->SetMinimum(minimum);
      }
      
      // format x-axis
      std::string x_title;
      if(std::string(type).find("mssm")!=std::string::npos){
	x_title = std::string("m_{#phi} [GeV]");
      }
      else{
	x_title = std::string("m_{a1} [GeV]");
      }
      hexp[i]->GetXaxis()->SetTitle(x_title.c_str());
      hexp[i]->GetXaxis()->SetLabelFont(62);
      hexp[i]->GetXaxis()->SetTitleFont(62);
      hexp[i]->GetXaxis()->SetTitleColor(1);
      hexp[i]->GetXaxis()->SetTitleOffset(1.05);
      if(std::string(type) == std::string("mssm-tanb")) hexp[i]->GetYaxis()->SetRangeUser(0,maximum);

      // format y-axis
      std::string y_title;
      if( std::string(type) == std::string("mssm-xsec") ){
	y_title = std::string("#sigma(#phi#rightarrow#tau#tau)_{95% CL} [pb]");
      }
      else if(  std::string(type) == std::string("mssm-tanb")  ){
	y_title = std::string("#bf{tan#beta}");
      }
      else{
	//y_title = std::string("#sigma(H#rightarrow#tau#tau)_{95% CL} / #sigma(H#rightarrow#tau#tau)_{SM}");
	y_title = std::string("95% CL limit on #sigma *BR [pb]");
      }
      hexp[i]->GetYaxis()->SetTitle(y_title.c_str());
      hexp[i]->GetYaxis()->SetLabelFont(62);
      hexp[i]->GetYaxis()->SetTitleOffset(1.05);
      hexp[i]->GetYaxis()->SetLabelSize(0.03);
      hexp[i]->GetXaxis()->SetLimits(hexp[i]->GetX()[0]-.1, hexp[i]->GetX()[hexp[i]->GetN()-1]+.1);
    }
    hexp[i]->SetLineStyle(11.);
    hexp[i]->SetLineWidth( 3.); 
    hexp[i]->SetLineColor(colors.find(channels[i])->second);
    hexp[i]->SetMarkerStyle(20);
    hexp[i]->SetMarkerSize(MARKER_SIZE);
    hexp[i]->SetMarkerColor(colors.find(channels[i])->second);
    hexp[i]->Draw(firstPlot ? "APL" : "PLsame");
    //hexp[i]->Draw(firstPlot ? "AL" : "Lsame");
    firstPlot=false;
  }
  for(unsigned int i=0; i<hobs.size(); ++i){
    if(firstPlot){
      if(std::string(type) == std::string("mssm-xsec")){
	if(log){ canv1->SetLogy(1); }
	hobs[i]->SetMaximum(maximum);
	hobs[i]->SetMinimum(minimum);
      }
      else{
	if(log){ canv1->SetLogy(1); }
	hobs[i]->SetMaximum(maximum);
	hobs[i]->SetMinimum(minimum);
      }
      
      // format x-axis
      std::string x_title;
      if(std::string(type).find("mssm")!=std::string::npos){
	x_title = std::string("m_{#phi} [GeV]");
      }
      else{
	x_title = std::string("m_{a1} [GeV]");
      }
      hobs[i]->GetXaxis()->SetTitle(x_title.c_str());
      hobs[i]->GetXaxis()->SetLabelFont(62);
      hobs[i]->GetXaxis()->SetTitleFont(62);
      hobs[i]->GetXaxis()->SetTitleColor(1);
      hobs[i]->GetXaxis()->SetTitleOffset(1.05);
      if(std::string(type) == std::string("mssm-tanb")) hobs[i]->GetYaxis()->SetRangeUser(0,maximum);
      
      // format y-axis
      std::string y_title;
      if( std::string(type) == std::string("mssm-xsec") ){
	y_title = std::string("#sigma(#phi#rightarrow#tau#tau)_{95% CL} [pb]");
      }
      else if(  std::string(type) == std::string("mssm-tanb")  ){
	y_title = std::string("#bf{tan#beta}");
      }
      else{
	y_title = std::string("95% CL limit on #sigma/#sigma_{SM}");
	//y_title = std::string("#sigma(H)_{95% CL} / #sigma(H)_{SM}");
      }
      hobs[i]->GetYaxis()->SetTitle(y_title.c_str());
      hobs[i]->GetYaxis()->SetLabelFont(62);
      hobs[i]->GetYaxis()->SetTitleOffset(1.05);
      hobs[i]->GetYaxis()->SetLabelSize(0.03);
      hobs[i]->GetXaxis()->SetLimits(hobs[i]->GetX()[0]-.1, hobs[i]->GetX()[hobs[i]->GetN()-1]+.1);
    }
    hobs[i]->SetLineStyle(11.);
    hobs[i]->SetLineWidth( 3.); 
    hobs[i]->SetLineColor(colors.find(channels[i])->second);
    hobs[i]->SetMarkerStyle(20);
    hobs[i]->SetMarkerSize(MARKER_SIZE);
    hobs[i]->SetMarkerColor(colors.find(channels[i])->second);
    hobs[i]->Draw(firstPlot ? "APL" : "PLsame");
    //hobs[i]->Draw(firstPlot ? "AL" : "Lsame");
    firstPlot=false;
  }
  canv1->RedrawAxis();
  bool firstLeg=true;
  if(observed){
    TLegend* leg1;
    if(expected && observed){
      /// setup the CMS Preliminary
       if(std::string(type) == std::string("mssm-tanb")){
	  if (firstLeg) CMSPrelim(label, "", 0.15, 0.835);
	  leg1 = new TLegend(firstLeg ? 0.60 : 0.20, hobs.size()<5 ? 0.20-0.06*hobs.size() : 0.4, firstLeg ? 0.93 : 0.60, 0.20);
       }
       else{
	  if (firstLeg) CMSPrelim(label, "", 0.15, 0.835);
	  leg1 = new TLegend(firstLeg ? 0.20 : 0.20, hobs.size()<5 ? 0.90-0.08*hobs.size() : 0.6, firstLeg ? 0.63 : 0.60, 0.90);
       }
    }
    else{
      /// setup the CMS Preliminary
      if(std::string(type) == std::string("mssm-tanb")){
	CMSPrelim(label, "", 0.15, 0.835);
	leg1 = new TLegend(legendOnRight?0.60:0.20, hobs.size()<5 ? (legendOnTop?0.90:0.20)-0.06*hobs.size() : (legendOnTop?0.6:0.4), legendOnRight?0.94:0.45, (legendOnTop?0.90:0.20));
	   }
      else{
	CMSPrelim(label, "", 0.15, 0.835);
	leg1 = new TLegend(legendOnRight ? 0.50 : 0.20, hobs.size()<5 ? 0.90-0.08*hobs.size() : 0.6, legendOnRight ? 0.94 : 0.64, 0.90);
      }
    }
    //leg1->SetTextSize(0.02);
    leg1->SetBorderSize( 0 );
    leg1->SetFillStyle ( 1001 );
    //leg1->SetFillColor ( 0 );
    leg1->SetFillColor (kWhite);
    leg1->SetHeader( "#bf{Observed Limit}" );
    for(unsigned int i=0; i<hobs.size(); ++i){
      // skip one of the two split options
      if(channels[i] == std::string("hzz2l2q+")){ continue; }
      leg1->AddEntry( hobs[i] , channel(channels[i]) ? legendEntry(channels[i]).c_str() : legendEntry(channels[i]).append("-Channel").c_str(),  "PL" );
    }
    leg1->Draw("same");
    firstLeg=false;
  }
  if(expected){
    TLegend* leg0;
    if(expected && observed){
      /// setup the CMS Preliminary
      if(std::string(type) == std::string("mssm-tanb")){
	CMSPrelim(label, "", 0.15, 0.835);
	leg0 = new TLegend(legendOnRight ? 0.60 : 0.20, hexp.size()<5 ? 0.20-0.06*hexp.size() : 0.4, legendOnRight ? 0.94 : 0.63, 0.20);
      }
      else{
	CMSPrelim(label, "", 0.15, 0.835);
	leg0 = new TLegend(legendOnRight ? 0.20 : 0.20, hexp.size()<5 ? 0.75-0.08*hexp.size() : 0.6, legendOnRight ? 0.94 : 0.63, 0.75);
      }
    }
    else{
      /// setup the CMS Preliminary
      if(std::string(type) == std::string("mssm-tanb")){
	CMSPrelim(label, "", 0.15, 0.835);
	leg0 = new TLegend(legendOnRight?0.60:0.20, hexp.size()<5 ? (legendOnTop?0.90:0.40)-0.04*hexp.size() : (legendOnTop?0.6:0.2), legendOnRight?0.94:0.45, (legendOnTop?0.90:0.40));
	   }
      else{
	CMSPrelim(label, "", 0.15, 0.835);
	leg0 = new TLegend(legendOnRight ? 0.50 : 0.20, hexp.size()<5 ? 0.90-0.06*hexp.size() : 0.6, legendOnRight ? 0.94 : 0.63, 0.90);
	//leg0 = new TLegend(legendOnRight ? 0.50 : 0.20, hexp.size()<5 ? 0.90-0.08*hexp.size() : 0.6, legendOnRight ? 0.94 : 0.80, 0.90);
      }
    }
    if(std::string(type) == std::string("mssm-tanb")) {leg0->SetTextSize(0.03);}
    leg0->SetBorderSize( 0 );
    leg0->SetFillStyle ( 1001 );
    leg0->SetFillColor (kWhite);
    leg0->SetHeader( "#bf{Expected Limit}" );
    for(unsigned int i=0; i<hexp.size(); ++i){
      // skip one of the two split options
      if(channels[i] == std::string("hzz2l2q+")){ continue; }
      leg0->AddEntry( hexp[i] , channel(channels[i]) ? legendEntry(channels[i]).c_str() : legendEntry(channels[i]).append("-Channel").c_str(),  "PL" );
    }
    leg0->Draw("same");
    firstLeg=false;
  }
  canv1->Print(std::string("singleLimits").append(expected ? "_expected" : "").append(observed ? "_observed" : "").append(std::string(type).find("mssm")!=std::string::npos ? "_mssm.png" : "_sm.png").c_str());
  canv1->Print(std::string("singleLimits").append(expected ? "_expected" : "").append(observed ? "_observed" : "").append(std::string(type).find("mssm")!=std::string::npos ? "_mssm.pdf" : "_sm.pdf").c_str());
  canv1->Print(std::string("singleLimits").append(expected ? "_expected" : "").append(observed ? "_observed" : "").append(std::string(type).find("mssm")!=std::string::npos ? "_mssm.pdf" : "_sm.eps").c_str());
  return;
}
