//  importing libraries

#include <algorithm>
#include <iterator>
#include <TROOT.h>
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <TLatex.h>
#include "TCanvas.h"
#include "RooPlot.h"
#include "TTree.h"
#include "TH1D.h"
#include "TH1D.h"
#include "THStack.h"
#include "TRandom.h"
#include "TUnfoldDensity.h"
#include "TGraph.h"
#include "TGraphErrors.h"
#include "TFrame.h"
#include "TPaveLabel.h"
#include "TPad.h"
#include "TLegend.h"
#include "TRandom3.h"
#include "TFile.h"
#include "TMath.h"

using namespace RooFit ;

void HistogramAnalysis() {

    std::vector<std::string> inputFiles = {"Semileptonic.root", "DYJets.root", "WJets.root", "ST.root", "QCD.root", "OtherTT.root", "Diboson.root"};

    std::vector<std::string> histNames = {"DY_N_N_Mass_0_250_reco_muon_General/DeltaY_muon", "DY_N_P_Mass_0_250_reco_muon_General/DeltaY_muon", "DY_P_N_Mass_0_250_reco_muon_General/DeltaY_muon", "DY_P_P_Mass_0_250_reco_muon_General/DeltaY_muon"};

    TH2F* Matrix = new TH2F("Matrix", "Matrix", 2, 0, 2, 2, 0, 2);

    double integral[2][2];

    for (int i = 0; i < histNames.size(); i++) {
        TFile* file = new TFile(inputFiles[i].c_str(), "READ");

        TH1F* h = (TH1F*)file->Get(histNames[i].c_str());

        if(h != nullptr) {
         integral[i/2][i%2] = h->Integral();
        } else {
            std::cerr << "Histogram " << histNames[i] << " not found in file " << inputFiles[i] << std::endl;
            integral[i/2][i%2] = 0;
        }

        file->Close();
    }
    // double integral [2][2] = {{h_DeltaY_N_N->Integral(),h_DeltaY_P_N->Integral()},{h_DeltaY_N_P->Integral(),h_DeltaY_P_P->Integral()}};

    for(int i=0; i<2; i++){
        for(int j=0; j<2; j++){
         Matrix->SetBinContent(i+1,j+1,integral[i][j]);
        }
    }

    Matrix->Draw("colz");
}



