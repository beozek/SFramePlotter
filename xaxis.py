import ROOT

def modify_histogram(file_names, folder_names, hist_names):
    for file_name in file_names:
        file = ROOT.TFile(file_name, "UPDATE")

        for folder_name in folder_names:
            if not file.cd(folder_name):
                print "Folder '%s' not found in the file." % folder_name
                continue
            
            for hist_name in hist_names:
                histogram = ROOT.gDirectory.Get(hist_name)
                if not histogram:
                    print "Histogram '%s' not found in folder '%s'." % (hist_name, folder_name)
                    continue

        

                histogram.GetXaxis().SetRangeUser(0, 10)

                histogram.Write(hist_name, ROOT.TObject.kOverwrite)

        file.Close()

# Example usage
# file_name = "/nfs/dust/cms/user/beozek/uuh2-106X_v2/CMSSW_10_6_28/src/UHH2/ZprimeSemiLeptonic/output_combine/UL18/muon/workdir_AnalysisDNN_UL18_muon/nominal/uhh2.AnalysisModuleRunner.TTToSemiLeptonic.root" 

file_names = ["/nfs/dust/cms/user/beozek/uuh2-106X_v2/CMSSW_10_6_28/src/UHH2/ZprimeSemiLeptonic/output_combine/UL18/muon/workdir_AnalysisDNN_UL18_muon/nominal/uhh2.AnalysisModuleRunner.TTToOthers.root", 
              "/nfs/dust/cms/user/beozek/uuh2-106X_v2/CMSSW_10_6_28/src/UHH2/ZprimeSemiLeptonic/output_combine/UL18/muon/workdir_AnalysisDNN_UL18_muon/nominal/uhh2.AnalysisModuleRunner.WJets.root",
             "/nfs/dust/cms/user/beozek/uuh2-106X_v2/CMSSW_10_6_28/src/UHH2/ZprimeSemiLeptonic/output_combine/UL18/muon/workdir_AnalysisDNN_UL18_muon/nominal/uhh2.AnalysisModuleRunner.ST.root", 
             "/nfs/dust/cms/user/beozek/uuh2-106X_v2/CMSSW_10_6_28/src/UHH2/ZprimeSemiLeptonic/output_combine/UL18/muon/workdir_AnalysisDNN_UL18_muon/nominal/uhh2.AnalysisModuleRunner.Diboson.root", 
            "/nfs/dust/cms/user/beozek/uuh2-106X_v2/CMSSW_10_6_28/src/UHH2/ZprimeSemiLeptonic/output_combine/UL18/muon/workdir_AnalysisDNN_UL18_muon/nominal/uhh2.AnalysisModuleRunner.QCD.root", 
             "/nfs/dust/cms/user/beozek/uuh2-106X_v2/CMSSW_10_6_28/src/UHH2/ZprimeSemiLeptonic/output_combine/UL18/muon/workdir_AnalysisDNN_UL18_muon/nominal/uhh2.AnalysisModuleRunner.DYJets.root", 
                "/nfs/dust/cms/user/beozek/uuh2-106X_v2/CMSSW_10_6_28/src/UHH2/ZprimeSemiLeptonic/output_combine/UL18/muon/workdir_AnalysisDNN_UL18_muon/nominal/uhh2.AnalysisModuleRunner.DATA.DATA.root"] 

folder_names = ["DNN_output0_beforeChi2Cut_General","DNN_output0_TopTag_beforeChi2Cut_General", "DNN_output0_NoTopTag_beforeChi2Cut_General", "DNN_output0_General", "DNN_output0_TopTag_General", "DNN_output0_NoTopTag_General", "DNN_output1_General", "DNN_output1_TopTag_General", "DNN_output1_NoTopTag_General", "DNN_output2_General", "DNN_output2_TopTag_General", "DNN_output2_NoTopTag_General"]
# hist_names = ["ditop_mass", "M_Zprime_rebin3", "M_Zprime", "NN_M_tt_weighted", "toplep_pt", "tophad_pt"]
# hist_names = ["NN_chi2", "chi2_Zprime"]
hist_names = ["N_jets"]
# hist_names = ["toplep_pt", "tophad_pt"]
modify_histogram(file_names, folder_names, hist_names)
