void entry()
{

    TFile *f = new TFile("/nfs/dust/cms/user/beozek/uuh2-106X_v2/CMSSW_10_6_28/src/UHH2/ZprimeSemiLeptonic/output/UL18/muon/workdir_Zprime_Analysis_UL18_muon_mistag/nominal/uhh2.AnalysisModuleRunner.DATA.DATA.root");
    // TH1F *h = (TH1F*)f->Get("Chi2_General/N_jets");
    TH1F *h = (TH1F*)f->Get("Chi2_General/N_AK8PuppiTaggedjets");
    cout << " Integral: " << h->Integral(2.,5.) << endl;



    // t->SetBranchAddress("b1",&h);
    // t->GetEntry(0);
    // h->Draw();

    // t->GetEntry(1);
    // h->Draw();
    // TBranch *b = t->Branch("hBranch","TH1F",&h);
    // t->Fill();
    // h->Draw();

    // t->Print();
    // t->GetEntries();
    // f->Close();
    // TH1F *h = new TH1F("h","number of events",100,0,4);
    // double i = h->Integral(0,2);
    // cout << i;
        // TFile *myfile = TFile::Open("/nfs/dust/cms/user/beozek/uuh2-106X_v2/CMSSW_10_6_28/src/UHH2/ZprimeSemiLeptonic/output/UL18/muon/workdir_Zprime_Analysis_UL18_muon_mistag/nominal/uhh2.AnalysisModuleRunner.DATA.DATA.root");
    // TH1F("h1", "ntuple", 100,-4,4);
   
    // TTreeReader myReader("ntuple", myfile);
    // myfile->Get("Chi2_General/Njets");
    // TH1F * myhist = new TH1F("myhist","number of events",100,0,4);
// myhist = (TH1F)myfile->Get("");
    // myhist->Draw("HIST");
    // TH1F * h1 = new TH1F("h1","number of events",100,0,500);
    // cout << "number of entries:" << h1->GetIntegral();
    
//Integral(bin-ignore bin0)
}
// TFile *myfile = TFile::Open("/nfs/dust/cms/user/beozek/uuh2-106X_v2/CMSSW_10_6_28/src/UHH2/ZprimeSemiLeptonic/output/UL18/muon/workdir_Zprime_Analysis_UL18_muon_mistag/nominal");
// TH1F * myhist = new TH1F("myhist","number of events",100,0,4);

// myhist = (TH1F)myfile->Get("");
// myhist->Integral(myhist->FindFixBin(0),myhist->FindFixBin(50));
// myhist->Draw("HIST")

