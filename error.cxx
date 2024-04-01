#include <iostream>

#include "string" 
#include "list" 
#include "iostream" 
#include "sstream" 
#include "iterator"
using namespace std;

void error()
{

//Select root file
    TFile *f1 = new TFile("/nfs/dust/cms/user/beozek/uuh2-106X_v2/CMSSW_10_6_28/src/UHH2/ZprimeSemiLeptonic/output_v2mistag/UL16postVFP/muon/workdir_Analysis_UL16postVFP_muon_mistag/nominal/uhh2.AnalysisModuleRunner.TTToSemiLeptonic.root");
    TFile *f2 = new TFile("/nfs/dust/cms/user/beozek/uuh2-106X_v2/CMSSW_10_6_28/src/UHH2/ZprimeSemiLeptonic/output_v2mistag/UL16postVFP/muon/workdir_Analysis_UL16postVFP_muon_mistag/nominal/uhh2.AnalysisModuleRunner.WJets.root");
    TFile *f3= new TFile("/nfs/dust/cms/user/beozek/uuh2-106X_v2/CMSSW_10_6_28/src/UHH2/ZprimeSemiLeptonic/output_v2mistag/UL16postVFP/muon/workdir_Analysis_UL16postVFP_muon_mistag/nominal/uhh2.AnalysisModuleRunner.ST.root");
    TFile *f4 = new TFile("/nfs/dust/cms/user/beozek/uuh2-106X_v2/CMSSW_10_6_28/src/UHH2/ZprimeSemiLeptonic/output_v2mistag/UL16postVFP/muon/workdir_Analysis_UL16postVFP_muon_mistag/nominal/uhh2.AnalysisModuleRunner.DATA.DATA.root");
    TFile *f5 = new TFile("/nfs/dust/cms/user/beozek/uuh2-106X_v2/CMSSW_10_6_28/src/UHH2/ZprimeSemiLeptonic/output_v2mistag/UL16postVFP/muon/workdir_Analysis_UL16postVFP_muon_mistag/nominal/uhh2.AnalysisModuleRunner.TTToOthers.root");
    TFile *f6 = new TFile("/nfs/dust/cms/user/beozek/uuh2-106X_v2/CMSSW_10_6_28/src/UHH2/ZprimeSemiLeptonic/output_v2mistag/UL16postVFP/muon/workdir_Analysis_UL16postVFP_muon_mistag/nominal/uhh2.AnalysisModuleRunner.DYJets.root");
    TFile *f7 = new TFile("/nfs/dust/cms/user/beozek/uuh2-106X_v2/CMSSW_10_6_28/src/UHH2/ZprimeSemiLeptonic/output_v2mistag/UL16postVFP/muon/workdir_Analysis_UL16postVFP_muon_mistag/nominal/uhh2.AnalysisModuleRunner.QCD.root");
    TFile *f8 = new TFile("/nfs/dust/cms/user/beozek/uuh2-106X_v2/CMSSW_10_6_28/src/UHH2/ZprimeSemiLeptonic/output_v2mistag/UL16postVFP/muon/workdir_Analysis_UL16postVFP_muon_mistag/nominal/uhh2.AnalysisModuleRunner.Diboson.root");


   
//Select tagged or No-Tagged
    TH1F *h1 = (TH1F*)f1->Get("Chi2_General/pt_AK8Puppijet");
    TH1F *h2 = (TH1F*)f1->Get("Chi2_General/pt_AK8PuppiTaggedjet");

//     for (int bin=1; bin<=h1->GetNbinsX(); bin++) {
//     double lowerEdge = h1->GetBinLowEdge(bin);
//     double upperEdge = lowerEdge + h1->GetBinWidth(bin);
//     std::cout << "Bin " << bin << ": [" << lowerEdge << ", " << upperEdge << ")" << std::endl;
// }

    TH1F *h3 = (TH1F*)f2->Get("Chi2_General/pt_AK8Puppijet");
    TH1F *h4 = (TH1F*)f2->Get("Chi2_General/pt_AK8PuppiTaggedjet");

    TH1F *h5 = (TH1F*)f3->Get("Chi2_General/pt_AK8Puppijet");
    TH1F *h6 = (TH1F*)f3->Get("Chi2_General/pt_AK8PuppiTaggedjet");
    
    TH1F *h7 = (TH1F*)f4->Get("Chi2_General/pt_AK8Puppijet");
    TH1F *h8 = (TH1F*)f4->Get("Chi2_General/pt_AK8PuppiTaggedjet");

    TH1F *h9 = (TH1F*)f5->Get("Chi2_General/pt_AK8Puppijet");
    TH1F *h10 = (TH1F*)f5->Get("Chi2_General/pt_AK8PuppiTaggedjet");

    TH1F *h11 = (TH1F*)f6->Get("Chi2_General/pt_AK8Puppijet");
    TH1F *h12 = (TH1F*)f6->Get("Chi2_General/pt_AK8PuppiTaggedjet");

    TH1F *h13 = (TH1F*)f7->Get("Chi2_General/pt_AK8Puppijet");
    TH1F *h14 = (TH1F*)f7->Get("Chi2_General/pt_AK8PuppiTaggedjet");

    TH1F *h15 = (TH1F*)f8->Get("Chi2_General/pt_AK8Puppijet");
    TH1F *h16 = (TH1F*)f8->Get("Chi2_General/pt_AK8PuppiTaggedjet");


//Integral(minbin,maxbin)
    // cout<< "path:"<<
    // cout << " Integral No Tagged: " << h1->Integral(0,10000) << endl;

    double_t error1;
    double_t error_notagged1;

    double_t error2;
    double_t error_notagged2;

    double_t error3;
    double_t error_notagged3;

    double_t error4;
    double_t error_notagged4;

    double_t error5;
    double_t error_notagged5;

    double_t error6;
    double_t error_notagged6;

    double_t error7;
    double_t error_notagged7;

    double_t error8;
    double_t error_notagged8;

    // cout << " Integral No Tagged: " << h1->Integral(0,10000) << endl;
    cout << " Integral No Tagged TTToSemiLeptonic: " << h1->IntegralAndError(21,10000000, error_notagged1,"") <<  "+-" << error_notagged1 << endl;
    cout << " Integral Tagged TTToSemiLeptonic: " << h2->IntegralAndError(21,10000, error1 , "") << "+-" << error1<< endl;

    cout << " Integral No Tagged WJets: " << h3->IntegralAndError(21,10000000, error_notagged2,"") <<  "+-" << error_notagged2 << endl;
    cout << " Integral Tagged WJets: " << h4->IntegralAndError(21,10000, error2 , "") << "+-" << error2<< endl;

    cout << " Integral No Tagged ST: " << h5->IntegralAndError(21,10000000, error_notagged3,"") <<  "+-" << error_notagged3 << endl;
    cout << " Integral Tagged ST: " << h6->IntegralAndError(21,10000, error3 , "") << "+-" << error3<< endl;

    cout << " Integral No Tagged DATA: " << h7->IntegralAndError(21,10000000, error_notagged4,"") <<  "+-" << error_notagged4 << endl;
    cout << " Integral Tagged DATA: " << h8->IntegralAndError(21,10000, error4 , "") << "+-" << error4<< endl;

    cout << " Integral No Tagged TTToOthers: " << h9->IntegralAndError(21,10000000, error_notagged5,"") <<  "+-" << error_notagged5 << endl;
    cout << " Integral Tagged TTToOthers: " << h10->IntegralAndError(21,10000, error5 , "") << "+-" << error5<< endl;

    cout << " Integral No Tagged DY: " << h11->IntegralAndError(21,10000000, error_notagged6,"") <<  "+-" << error_notagged6 << endl;
    cout << " Integral Tagged DY: " << h12->IntegralAndError(21,10000, error6 , "") << "+-" << error6<< endl;

    cout << " Integral No Tagged QCD: " << h13->IntegralAndError(21,10000000, error_notagged7,"") <<  "+-" << error_notagged7 << endl;
    cout << " Integral Tagged QCD: " << h14->IntegralAndError(21,10000, error7 , "") << "+-" << error7<< endl;

    cout << " Integral No Tagged Diboson: " << h15->IntegralAndError(21,10000000, error_notagged8,"") <<  "+-" << error_notagged8 << endl;
    cout << " Integral Tagged Diboson: " << h16->IntegralAndError(21,10000, error8 , "") << "+-" << error8<< endl;






    double Semi = h1->IntegralAndError(21,10000000, error_notagged1,"");
    double Semi_Tagged = h2->IntegralAndError(21,10000, error1 , "");

    double WJet = h3->IntegralAndError(21,10000000, error_notagged2,"");
    double WJet_Tagged = h4->IntegralAndError(21,10000, error2 , "");

    double ST = h5->IntegralAndError(21,10000000, error_notagged3,"");
    double ST_Tagged = h6->IntegralAndError(21,10000, error3 , "");

    double Data = h7->IntegralAndError(21,10000000, error_notagged4,"");
    double Data_Tagged = h8->IntegralAndError(21,10000, error4 , "");

    double Other = h9->IntegralAndError(21,10000000, error_notagged5,"");
    double Other_Tagged = h10->IntegralAndError(21,10000, error5 , "");

    double DY = h11->IntegralAndError(21,10000000, error_notagged6,"");
    double DY_Tagged = h12->IntegralAndError(21,10000, error6 , "");

    double QCD = h13->IntegralAndError(21,10000000, error_notagged7,"");
    double QCD_Tagged = h14->IntegralAndError(21,10000, error7 , "");

    double Diboson = h15->IntegralAndError(21,10000000, error_notagged8,"") ;
    double Diboson_Tagged = h16->IntegralAndError(21,10000, error8 , "");

    double denominator = Data - Semi - Other - ST;
    double numerator = Data_Tagged - Semi_Tagged - Other_Tagged - ST_Tagged;

    double e_data = 0.0;
    double error_e_data = 0.0;

    if (denominator != 0.0) {
        e_data = numerator / denominator;

        double error_numerator = sqrt(pow(error4, 2) + pow(error1, 2) + pow(error5, 2) + pow(error3, 2));
        double error_denominator = sqrt(pow(error_notagged4, 2) + pow(error_notagged1, 2) + pow(error_notagged5, 2) + pow(error_notagged3, 2));

        if (denominator != 0.0 && error_denominator != 0.0) {
            error_e_data = e_data * sqrt(pow(error_numerator / numerator, 2) + pow(error_denominator / denominator, 2));
        }

    }

    // Output the result
    std::cout << "e_data: " << e_data << std::endl;
    std::cout << "Error on e_data: " << error_e_data << std::endl;


    double denominator_MC = WJet + DY + QCD + Diboson;
    double numerator_MC = WJet_Tagged + DY_Tagged + QCD_Tagged +Diboson_Tagged;

    double e_mc = 0.0;
    double error_e_mc = 0.0;

    if (denominator_MC != 0.0) {
        e_mc = numerator_MC / denominator_MC;

        double error_numerator_MC = sqrt(pow(error2, 2) + pow(error6, 2) + pow(error7, 2) + pow(error8, 2));
        double error_denominator_MC = sqrt(pow(error_notagged2, 2) + pow(error_notagged6, 2) + pow(error_notagged7, 2) + pow(error_notagged8, 2));

        if (error_denominator_MC != 0.0) {
            error_e_mc = e_mc * sqrt(pow(error_numerator_MC / numerator_MC, 2) + pow(error_denominator_MC / denominator_MC, 2));
        }
    }

    // Output the result
    std::cout << "e_mc: " << e_mc << std::endl;
    std::cout << "Error on e_mc: " << error_e_mc << std::endl;

    double denominator_SF = e_mc;
    double numerator_SF = e_data;

    double SF = 0.0;
    double error_SF = 0.0;

    if (denominator_SF != 0.0) {
        SF = numerator_SF / denominator_SF;

        double error_numerator_SF = sqrt(pow(error_e_data, 2));
        double error_denominator_SF = sqrt(pow(error_e_mc, 2));

        if (error_denominator_SF != 0.0) {
            error_SF = SF * sqrt(pow(error_numerator_SF / numerator_SF, 2) + pow(error_denominator_SF / denominator_SF, 2));
        }
    }

    // Output the result
    std::cout << "SF: " << SF << std::endl;
    std::cout << "Error on SF: " << error_SF << std::endl;


}