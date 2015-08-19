#include "HiggsAnalysis/HiggsToTauTau/interface/PlotLimits.h"

/// This is the core plotting routine that can also be used within
/// root macros. It is therefore not element of the PlotLimits class.
void plottingLimit(TCanvas& canv, TGraphAsymmErrors* innerBand, TGraphAsymmErrors* outerBand, TGraph* expected, TGraph* observed, TGraph* unit, std::string& xaxis, std::string& yaxis, TGraph* injected, double min, double max, bool log, std::string PLOT, std::string injectedMass, bool legendOnRight, std::string extra_label=std::string("")); 

void
PlotLimits::plotLimit(TCanvas& canv, TGraphAsymmErrors* innerBand, TGraphAsymmErrors* outerBand, TGraph* expected, TGraph* observed)
{
  // set up styles
  SetStyle();
  // create the unit line
  TGraph* unit = 0;
  if(!mssm_ && !mssm_nolog_){
    unit = new TGraph();
    for(unsigned int imass=0, ipoint=0; imass<bins_.size(); ++imass){
      if(valid_[imass]){
	unit->SetPoint(ipoint, bins_[imass], 1.); ++ipoint;
      }
    }
  }
  // set proper maximum
  float max = maximum(expected);
  float min = minimum(expected);
  if(log_){ max*=10; min/=10; }
  std::cout << "max:" << max << std::endl;
  std::cout << "min:" << min << std::endl;

  // do the plotting 
  std::string PLOT("LIMIT");
  if(injected_){ PLOT=std::string("INJECTED"); }
  if(BG_Higgs_){ PLOT=std::string("BG_HIGGS"); }	  
  if(bestfit_ ){ PLOT=std::string("BESTFIT" ); }
  if(mssm_    ){ PLOT=std::string("MSSM-LOG"); }
  if(mssm_nolog_    ){ PLOT=std::string("MSSM-NOLOG"); }
  if(mssm_ && injected_){ PLOT=std::string("MSSM-LOG_INJECTED"); }
  if(mssm_nolog_ && injected_){ PLOT=std::string("MSSM-NOLOG_INJECTED"); }
  plottingLimit(canv, innerBand, outerBand, expected, observed, unit, xaxis_, yaxis_, 0, min, max, log_, PLOT, injectedMass_, mssm_, extra_);
  // setup CMS Preliminary
  //CMSPrelim(dataset_.c_str(), "", 0.160, 0.835);
  //CMSPrelim(dataset_.c_str(), "", 0.135, 0.835);
  TPaveText* chan     = new TPaveText(0.21, 0.67+0.06, 0.21+0.15, 0.67+0.16, "NDC");
  chan->SetBorderSize(   0 );
  chan->SetFillStyle(    0 );
  chan->SetTextAlign(   12 );
  chan->SetTextSize ( 0.06 );
  chan->SetTextColor(    1 );
  chan->SetTextFont (   62 );
  chan->AddText(dataset_.c_str());
  chan->Draw();

  TPaveText* lumi  = new TPaveText(0.21, 0.75+0.06, 0.21+0.15, 0.75+0.16, "NDC");
  lumi->SetTextFont(61);
  lumi->SetTextSize(0.07);
  lumi->SetBorderSize(   0 );
  lumi->SetFillStyle(    0 );
  lumi->SetTextAlign(   12 );
  lumi->SetTextColor(    1 );
  lumi->AddText("CMS");
  lumi->Draw();

  TPaveText *lumi4 = new TPaveText(0.16, 0.835+0.06, 0.16+0.30, 0.835+0.16, "NDC");
  lumi4->SetTextFont(42);
  lumi4->SetTextSize(0.045);
  lumi4->SetBorderSize(   0 );
  lumi4->SetFillStyle(    0 );
  lumi4->SetTextAlign(   12 );
  lumi4->SetTextColor(    1 );
  lumi4->AddText("A#rightarrow Zh#rightarrow#it{ll}#tau#tau");
  //lumi4->Draw("same");


  TPaveText* lumi2  = new TPaveText(0.21, 0.70+0.06, 0.21+0.15, 0.70+0.16, "NDC");
  lumi2->SetTextSize(0.03);
  lumi2->SetBorderSize(   0 );
  lumi2->SetFillStyle(    0 );
  lumi2->SetTextAlign(   12 );
  lumi2->SetTextColor(    1 );
  lumi2->SetTextFont(52);
  //lumi2->AddText("Preliminary");
  //lumi2->Draw();

  TPaveText* lumi3  = new TPaveText(0.64, 0.835+0.06, 0.64+0.30, 0.835+0.16, "NDC");
  lumi3->SetBorderSize(   0 );
  lumi3->SetFillStyle(    0 );
  lumi3->SetTextAlign(   12 );
  lumi3->SetTextColor(    1 );
  lumi3->SetTextSize(0.045);
  lumi3->AddText("19.7 fb^{-1} (8 TeV)");
  lumi3->Draw();

  /*TPaveText* lumi7  = new TPaveText(0.14, 0.835+0.06, 0.14+0.30, 0.835+0.16, "NDC");
  lumi7->SetBorderSize(   0 );
  lumi7->SetFillStyle(    0 );
  lumi7->SetTextAlign(   12 );
  lumi7->SetTextColor(    1 );
  lumi7->SetTextSize(0.045);
  lumi7->AddText("A#rightarrow#Zh#rightarrow#it{ll}#tau#tau");
  lumi7->Draw();*/

  /*
  TPaveText* chan     = new TPaveText(0.60, 0.82, 0.80, 0.92, "NDC");
  chan->SetBorderSize(   0 );
  chan->SetFillStyle(    0 );
  chan->SetTextAlign(   12 );
  chan->SetTextSize ( 0.05 );
  chan->SetTextColor(    1 );
  chan->SetTextFont (   62 );
  chan->AddText("e#mu, e#tau_{h}, #mu#tau_{h}, #tau_{h}#tau_{h}");
  chan->Draw();
  */

  /*
  TPaveText* ext0     = new TPaveText(0.60, 0.85, 0.80, 0.90, "NDC");
  ext0->SetBorderSize(   0 );
  ext0->SetFillStyle(    0 );
  ext0->SetTextAlign(   12 );
  ext0->SetTextSize ( 0.035 );
  ext0->SetTextColor(    1 );
  ext0->SetTextFont (   42 );
  ext0->AddText("CMS Preliminary");
  ext0->Draw();

  TPaveText* ext1     = new TPaveText(0.60, 0.80, 0.80, 0.85, "NDC");
  ext1->SetBorderSize(   0 );
  ext1->SetFillStyle(    0 );
  ext1->SetTextAlign(   12 );
  ext1->SetTextSize ( 0.035 );
  ext1->SetTextColor(    1 );
  ext1->SetTextFont (   42 );
  ext1->AddText("#sqrt{s} = 7 TeV, L = 4.9 fb^{-1}");
  ext1->Draw();

  TPaveText* ext2     = new TPaveText(0.60, 0.75, 0.80, 0.80, "NDC");
  ext2->SetBorderSize(   0 );
  ext2->SetFillStyle(    0 );
  ext2->SetTextAlign(   12 );
  ext2->SetTextSize ( 0.035 );
  ext2->SetTextColor(    1 );
  ext2->SetTextFont (   42 );
  ext2->AddText("#sqrt{s} = 8 TeV, L = 19.4 fb^{-1}");
  ext2->Draw();
  
  TPaveText* ext3     = new TPaveText(0.60, 0.70, 0.80, 0.75, "NDC");
  ext3->SetBorderSize(   0 );
  ext3->SetFillStyle(    0 );
  ext3->SetTextAlign(   12 );
  ext3->SetTextSize ( 0.035 );
  ext3->SetTextColor(    1 );
  ext3->SetTextFont (   42 );
  ext3->AddText("H#rightarrow#tau#tau");
  ext3->Draw();
  */

  // write results to files
  if(png_){ canv.Print(std::string(output_).append("_").append(label_).append(".png").c_str()); 
     canv.Print(std::string(output_).append("_").append(label_).append(".C").c_str());
     canv.Print(std::string(output_).append("_").append(label_).append("_canvas.root").c_str());}
  if(pdf_){ 
    canv.Print(std::string(output_).append("_").append(label_).append(".pdf").c_str()); 
    canv.Print(std::string(output_).append("_").append(label_).append(".eps").c_str()); 
  }
  if(txt_){
    print(std::string(output_).append("_").append(label_).c_str(), outerBand, innerBand, expected, observed, "txt");
    print(std::string(output_).append("_").append(label_).c_str(), outerBand, innerBand, expected, observed, "tex");
  }
  if(root_){
    TFile* output = new TFile(std::string(output_).append("_").append(label_).append(".root").c_str(), "update");
    if(!output->cd(output_.c_str())){
      output->mkdir(output_.c_str());
      output->cd(output_.c_str());
    }
    if(observed ){ observed ->Write("observed" ); }
    if(expected ){ expected ->Write("expected" ); }
    if(innerBand){ innerBand->Write("innerBand"); }
    if(outerBand){ outerBand->Write("outerBand"); }
    output->Close();
  }
  return;
}

