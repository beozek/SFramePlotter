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

void ResponseMatrix()

{

    gStyle->SetOptStat(0);

    // A chain is a collection of files containing TTree objects. 
    // TChain(const char *name, const char *title="", Mode mode=kWithGlobalRegistration or kWithoutGlobalReg)
    // TTree tree(name, title)

    TChain *gen = new TChain("AnalysisTree","");
    gen -> Add("/nfs/dust/cms/user/beozek/uuh2-106X_v2/CMSSW_10_6_28/src/UHH2/ZprimeSemiLeptonic/event_numbers/UL18/muon/workdir_Zprime_Analysis_UL18_unfolding/uhh2.AnalysisModuleRunner.MC.TTToSemiLeptonic_UL18_0.root");
    TTree *treegen = (TTree*) gen;

    //ADD ALL SEMILEPTONIC ROOT HERE

    TChain *reco = new TChain("AnalysisTree","");
    reco-> Add("/nfs/dust/cms/user/beozek/uuh2-106X_v2/CMSSW_10_6_28/src/UHH2/ZprimeSemiLeptonic/output_unfolding/UL18/muon/nominal_new_correct/uhh2.AnalysisModuleRunner.TTToSemiLeptonic1.root");
    reco-> Add("/nfs/dust/cms/user/beozek/uuh2-106X_v2/CMSSW_10_6_28/src/UHH2/ZprimeSemiLeptonic/output_unfolding/UL18/muon/nominal_new_correct/uhh2.AnalysisModuleRunner.TTToSemiLeptonic2.root");
    reco-> Add("/nfs/dust/cms/user/beozek/uuh2-106X_v2/CMSSW_10_6_28/src/UHH2/ZprimeSemiLeptonic/output_unfolding/UL18/muon/nominal_new_correct/uhh2.AnalysisModuleRunner.TTToSemiLeptonic3.root");
    TTree *treereco = (TTree*) reco;

    cout << "Number of Events:"<< treereco-> GetEntries()<<endl;


 
    // ===   TH1D & TH2F   ===

    // Float_t bin_gen[] = {-2.5,-2.25,-2.,-1.75,-1.5,-1.25,-1.,-0.75,-0.5,-0.25,0.,0.25,0.5,0.75,1.,1.25,1.5,1.75,2.,2.25,2.5};
    // Float_t bin_rec[] = {-2.5,-2.25,-2.,-1.75,-1.5,-1.25,-1.,-0.75,-0.5,-0.25,0.,0.25,0.5,0.75,1.,1.25,1.5,1.75,2.,2.25,2.5};

    // Int_t bingen = sizeof(bin_gen)/sizeof(Float_t) - 1;
    // Int_t binreco = sizeof(bin_rec)/sizeof(Float_t) - 1;

    
    
    // TH1D DeltaY Plots

    //DeltaY gen without mass cut
    TH1D *h_DeltaY_gen = new TH1D("DeltaY_gen","#Delta_Y_{gen}",10,-2.5,2.5);
    //DeltaY gen with mass cut
    TH1D *h_DeltaY_gen_mass = new TH1D("DeltaY_gen_mass","(#Delta_Y)_{gen}, M > 750",10,-2.5,2.5);
    //POSITIVE gen without mass
    TH1D *h_DeltaY_P_gen_nomass = new TH1D("DeltaY_P_gen_nomass","#Delta_Y_{gen}>0",1,0,2.5);
    //POSITIVE gen with mass
    TH1D *h_DeltaY_P_gen = new TH1D("DeltaY_P_gen","#Delta_Y_{gen}>0, M > 750",1,0,2.5);
    //NEGATIVE gen without mass
    TH1D *h_DeltaY_N_gen_nomass = new TH1D("DeltaY_N_gen_nomass","#Delta_Y_{gen} < 0",1,-2.5,0);
    //NEGATIVE gen with mass
    TH1D *h_DeltaY_N_gen = new TH1D("DeltaY_N_gen","(#Delta_Y_{gen} < 0, M > 750",1,-2.5,0);

    //DeltaY reco without mass cut
    TH1D *h_DeltaY_reco = new TH1D("DeltaY_reco","#Delta_Y_{reco}",10,-2.5,2.5);
    //DeltaY with mass cut
    TH1D *h_DeltaY_reco_mass = new TH1D("DeltaY_reco_mass","(#Delta_Y)_{gen}, M > 750",10,-2.5,2.5);
    //POSITIVE reco without mass
    TH1D *h_DeltaY_P_reco_nomass = new TH1D("DeltaY_P_reco_nomass","#Delta_Y_{reco}>0",1,0,2.5);
    //POSITIVE reco with mass
    TH1D *h_DeltaY_P_reco = new TH1D("DeltaY_P_reco","#Delta_Y_{reco}>0, M>750",1,0,2.5);
    //NEGATIVE reco without mass
    TH1D *h_DeltaY_N_reco_nomass = new TH1D("DeltaY_N_reco_nomass","#Delta_Y_{reco}<0",1,-2.5,0);
    //NEGATIVE reco with mass
    TH1D *h_DeltaY_N_reco = new TH1D("DeltaY_N_reco","#Delta_Y_{reco}<0, M>750",1,-2.5,0);


    // POSITIVE gen, POSITIVE reco, without mass cut
    TH1D *h_DeltaY_P_P_nomass = new TH1D("DeltaY_P_P_nomass","#Delta_Y_{gen} > 0, #Delta_Y_{reco} > 0 ",1,0,2.5);
    // POSITIVE gen, POSITIVE reco, with mass cut
    TH1D *h_DeltaY_P_P = new TH1D("DeltaY_P_P","#Delta_Y_{gen} > 0, #Delta_Y_{reco} > 0, M >750",1,0,2.5);
    // POSITIVE gen, NEGATIVE reco, without mass cut
    TH1D *h_DeltaY_P_N_nomass = new TH1D("DeltaY_P_N_nomass","#Delta_Y_{gen} > 0, #Delta_Y_{reco} < 0",1,-2.5,2.5);
    // POSITIVE gen, NEGATIVE reco, with mass cut
    TH1D *h_DeltaY_P_N = new TH1D("DeltaY_P_N","#Delta_Y_{gen} > 0, #Delta_Y_{reco} < 0, M >750",1,-2.5,2.5);
    // NEAGATIVE gen, POSITIVE reco, without mass cut
    TH1D *h_DeltaY_N_P_nomass = new TH1D("DeltaY_N_P_nomass","#Delta_Y_{gen} < 0, #Delta_Y_{reco} > 0",1,-2.5,2.5);
    // NEGATIVE gen, POSITIVE reco, with mass cut
    TH1D *h_DeltaY_N_P = new TH1D("DeltaY_N_P","#Delta_Y_{gen} < 0, #Delta_Y_{reco} > 0, M >750",1,-2.5,2.5);
    // NEGATIVE gen, NEGATIVE reco, without mass cut
    TH1D *h_DeltaY_N_N_nomass = new TH1D("DeltaY_N_N_nomass","#Delta_Y_{gen} < 0, #Delta_Y_{reco} < 0",1,-2.5,0);
    // NEGATIVE gen, NEGATIVE reco, with mass cut
    TH1D *h_DeltaY_N_N = new TH1D("DeltaY_N_N","#Delta_Y_{gen} < 0, #Delta_Y_{reco} < 0, M >750",1,-2.5,0);
    
   
    TH2D *Matrix = new TH2D("Matrix","", 2,-2.5,2.5,2,-2.5,2.5);

    float DeltaY_gen;
    float DeltaY_gen_mass;
    float DeltaY_P_gen;
    float DeltaY_P_gen_nomass;
    float DeltaY_N_gen;
    float DeltaY_N_gen_nomass;
    
    float DeltaY_reco;
    float DeltaY_reco_mass;
    float DeltaY_P_reco;
    float DeltaY_P_reco_nomass;
    float DeltaY_N_reco;
    float DeltaY_N_reco_nomass;

    float DeltaY_N_N;
    float DeltaY_N_P;
    float DeltaY_P_N;
    float DeltaY_P_P;
    float DeltaY_N_N_nomass;
    float DeltaY_N_P_nomass;
    float DeltaY_P_N_nomass;
    float DeltaY_P_P_nomass;
    
    
    treereco->SetBranchAddress("DeltaY_gen", &DeltaY_gen);
    treereco->SetBranchAddress("DeltaY_gen_mass", &DeltaY_gen_mass);
    treereco->SetBranchAddress("DeltaY_P_gen", &DeltaY_P_gen);
    treereco->SetBranchAddress("DeltaY_P_gen_nomass", &DeltaY_P_gen_nomass);
    treereco->SetBranchAddress("DeltaY_N_gen", &DeltaY_N_gen);
    treereco->SetBranchAddress("DeltaY_N_gen_nomass", &DeltaY_N_gen_nomass);

    treereco->SetBranchAddress("DeltaY_reco", &DeltaY_reco);
    treereco->SetBranchAddress("DeltaY_reco_mass", &DeltaY_reco_mass);
    treereco->SetBranchAddress("DeltaY_P_reco", &DeltaY_P_reco);
    treereco->SetBranchAddress("DeltaY_P_reco_nomass", &DeltaY_P_reco_nomass);
    treereco->SetBranchAddress("DeltaY_N_reco", &DeltaY_N_reco);
    treereco->SetBranchAddress("DeltaY_N_reco_nomass", &DeltaY_N_reco_nomass);

    treereco->SetBranchAddress("DeltaY_N_N", &DeltaY_N_N);
    treereco->SetBranchAddress("DeltaY_N_P", &DeltaY_N_P);
    treereco->SetBranchAddress("DeltaY_P_P", &DeltaY_P_P);
    treereco->SetBranchAddress("DeltaY_P_N", &DeltaY_P_N);
    treereco->SetBranchAddress("DeltaY_N_N_nomass", &DeltaY_N_N_nomass);
    treereco->SetBranchAddress("DeltaY_N_P_nomass", &DeltaY_N_P_nomass);
    treereco->SetBranchAddress("DeltaY_P_N_nomass", &DeltaY_P_N_nomass);
    treereco->SetBranchAddress("DeltaY_P_P_nomass", &DeltaY_P_P_nomass);

    for (Int_t i = 0; i < treereco->GetEntries(); i++){
    // for (Int_t i = 0; i < 10000; i++){

        treereco->GetEntry(i);
        if (i%1000000 == 0) std::cout << "--- ... Processing event: " << i <<std::endl;
       
        h_DeltaY_gen->Fill(DeltaY_gen);
        h_DeltaY_gen_mass->Fill(DeltaY_gen_mass);
        h_DeltaY_P_gen_nomass->Fill(DeltaY_P_gen_nomass);
        h_DeltaY_P_gen->Fill(DeltaY_P_gen);
        h_DeltaY_N_gen_nomass->Fill(DeltaY_N_gen_nomass);
        h_DeltaY_N_gen->Fill(DeltaY_N_gen);

        h_DeltaY_reco->Fill(DeltaY_reco);
        h_DeltaY_reco_mass->Fill(DeltaY_reco_mass);
        h_DeltaY_P_reco_nomass->Fill(DeltaY_P_reco_nomass);
        h_DeltaY_P_reco->Fill(DeltaY_P_reco);
        h_DeltaY_N_reco_nomass->Fill(DeltaY_N_reco_nomass);
        h_DeltaY_N_reco->Fill(DeltaY_N_reco);

        h_DeltaY_P_P->Fill(DeltaY_P_P);
        h_DeltaY_P_N->Fill(DeltaY_P_N);
        h_DeltaY_N_N->Fill(DeltaY_N_N);
        h_DeltaY_N_P->Fill(DeltaY_N_P);
        h_DeltaY_P_P_nomass->Fill(DeltaY_P_P_nomass);
        h_DeltaY_P_N_nomass->Fill(DeltaY_P_N_nomass);
        h_DeltaY_N_P_nomass->Fill(DeltaY_N_P_nomass);
        h_DeltaY_N_N_nomass->Fill(DeltaY_N_N_nomass);
        
    }

    double integral [2][2] = {{h_DeltaY_N_N->Integral(),h_DeltaY_P_N->Integral()},{h_DeltaY_N_P->Integral(),h_DeltaY_P_P->Integral()}};

     for(int i=0; i<2; i++){
        for(int j=0; j<2; j++){
              Matrix->SetBinContent(i+1,j+1,integral[i][j]);
       }
    }

    TFile* myFile = new TFile("DeltaY_tt.root", "RECREATE");
    
    h_DeltaY_gen->Write();
    h_DeltaY_gen_mass->Write();
    h_DeltaY_P_gen_nomass->Write();
    h_DeltaY_P_gen->Write();
    h_DeltaY_N_gen_nomass->Write();
    h_DeltaY_N_gen->Write();

    h_DeltaY_reco->Write();
    h_DeltaY_reco_mass->Write();
    h_DeltaY_P_reco_nomass->Write();
    h_DeltaY_P_reco->Write();
    h_DeltaY_N_reco_nomass->Write();
    h_DeltaY_N_reco->Write();  
    
    h_DeltaY_P_P->Write();
    h_DeltaY_P_N->Write();
    h_DeltaY_N_P->Write();
    h_DeltaY_N_N->Write();
    h_DeltaY_P_P_nomass->Write();
    h_DeltaY_P_N_nomass->Write();
    h_DeltaY_N_P_nomass->Write();
    h_DeltaY_N_N_nomass->Write();

    Matrix->Write();

    ProjY_1->Write();
    ProjY_2->Write();
    ProjX_1->Write();
    ProjX_2->Write();


   //// ===== CANVAS =====

    //TCanvas(name,title,ww,wh)
    TCanvas* dd = new TCanvas("Scatter","Scatter",2400,1200);

    dd->Divide(1,1);
    dd->cd(1);

    Matrix->GetXaxis()->SetTitle("#Delta |Y_{rec}|");
    Matrix->GetYaxis()->SetTitle("#Delta |Y_{gen}|");
    // Matrix->GetZaxis()->SetRangeUser(0,1);
    Matrix->Draw("colz");
    dd->Print("Response_Matrix_tt.pdf");


    // treereco->SetBranchAddress("DeltaY_N_N", &DeltaY_N_N);
    // treereco->SetBranchAddress("DeltaY_N_P", &DeltaY_N_P);
    // treereco->SetBranchAddress("DeltaY_P_P", &DeltaY_P_P);
    // treereco->SetBranchAddress("DeltaY_P_N", &DeltaY_P_N);

    // for (Int_t i = 0; i < treereco->GetEntries(); i++){
    //     treereco->GetEntry(i);
    //     h_11->Fill(DeltaY_P_P);
    //     h_12->Fill(DeltaY_P_N);
    //     h_22->Fill(DeltaY_N_N);
    //     h_21->Fill(DeltaY_N_P);
    // }


    // double integral[2][2];
   
    // Matrix->SetBinContent(1,1,h_11->GetIntegral());
    // Matrix->SetBinContent(1,2,h_12->GetIntegral());
    // Matrix->SetBinContent(2,1,h_21->GetIntegral());
    // Matrix->SetBinContent(2,2,h_22->GetIntegral());

    // Double_t integral11 = h_11->Integral();
    // Double_t integral12 = h_12->Integral();
    // Double_t integral21 = h_21->Integral();
    // Double_t integral22 = h_22->Integral();

    // Matrix->SetBinContent(1,1,integral11);
    // Matrix->SetBinContent(1,2,integral12);
    // Matrix->SetBinContent(2,1,integral21);
    // Matrix->SetBinContent(2,2,integral22);

    // for(int i=0; i<2; i++){
    //     for(int j=0; j<2; j++){ 
    //         Matrix->SetBinContent(i,j,integral[i][j]);
    //         cout<< integral[i][j] <<endl;
    //      }

    // }
    // ===   Projection   ===
    // Make a projection of a tree using selections. projection of the tree will be filled in histogram hname.
    // Project(hname,char varexp (input variable)) || "varexp" is an expression of the general form e1:e2:e3 where e1,etc is a formula referencing a combination of the columns
    // Form(): Formats a string using a printf style format descriptor
    

    // string rap_diff = "TMath::Abs(0.5*TMath::Log((top.energy() + top.pt()*TMath::SinH(top.eta())))/(top.energy() - top.pt()*TMath::SinH(top.eta()))) - TMath::Abs(0.5*TMath::Log((antitop.energy() + antitop.pt()*TMath::SinH(antitop.eta()))/(antitop.energy() - antitop.pt()*TMath::SinH(antitop.eta()))))";

    // string rap_diff = "TMath::Abs(0.5*TMath::Log((GenParticles.m_energy[2] + GenParticles.m_pt[2]*TMath::SinH(GenParticles.m_eta[2]))/(GenParticles.m_energy[2] - GenParticles.m_pt[2]*TMath::SinH(GenParticles.m_eta[2])))) - TMath::Abs(0.5*TMath::Log((GenParticles.m_energy[3] + GenParticles.m_pt[3]*TMath::SinH(GenParticles.m_eta[3]))/(GenParticles.m_energy[3] - GenParticles.m_pt[3]*TMath::SinH(GenParticles.m_eta[3]))))";
    // treereco->Project("Matrix",Form("%s < -2. ? TMath::Max(-1.75,%s): (%s > 2. ? TMath::Min(1.75,%s) : %s):%s < -2. ? TMath::Max(-1.75,%s): (%s > 2. ? TMath::Min(1.75,%s) : %s)",rap_diff.c_str(),rap_diff.c_str(),rap_diff.c_str(),rap_diff.c_str(),rap_diff.c_str(),"DeltaY","DeltaY","DeltaY","DeltaY","DeltaY"));
    // treereco->Project("Matrix",Form("%s < -2.5 ? TMath::Max(-1.75,%s): (%s > 2. ? TMath::Min(1.75,%s) : %s):%s < -2. ? TMath::Max(-1.75,%s): (%s > 2. ? TMath::Min(1.75,%s) : %s)",rap_diff.c_str(),rap_diff.c_str(),rap_diff.c_str(),rap_diff.c_str(),rap_diff.c_str(),rap_diff.c_str(),rap_diff.c_str(),rap_diff.c_str(),rap_diff.c_str(),rap_diff.c_str()));


    // ===  Filling Plots   ===

    // treereco->Project("Matrix", Form());
    // SetBinContent(int_t binx, int_t biny, double_t content)
    //Filling the response matrix with its elements


 




}