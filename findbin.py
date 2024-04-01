import ROOT

def integrate_histogram(file_names, folder_name, hist_name, x_max):
    for file_name in file_names:
        file = ROOT.TFile(file_name)

        if not file or file.IsZombie():
            print "Could not open file:", file_name
            continue

        if not file.cd(folder_name):
            print "Folder '%s' not found in file: %s" % (folder_name, file_name)
            continue

        hist = ROOT.gDirectory.Get(hist_name)
        if not hist:
            print "Histogram '%s' not found in file: %s" % (hist_name, file_name)
            file.Close()
            continue

        bin_max = hist.GetXaxis().FindBin(x_max)

        integral_up_to_x_max = hist.Integral(1, bin_max)
        print "File: %s, Integral up to x = %d is: %f" % (file_name, x_max, integral_up_to_x_max)

        total_bins = hist.GetNbinsX()
        integral_after_x_max = hist.Integral(bin_max, total_bins)
        print "File: %s, Integral after x = %d is: %f" % (file_name, x_max, integral_after_x_max)
        
        integral = hist.Integral()
        print "File: %s, Integral  x = %d is: %f" % (file_name, x_max, integral)
        
        print integral_up_to_x_max, integral_after_x_max, integral
        
        print "\n"
        file.Close()


file_names = ["/nfs/dust/cms/user/beozek/uuh2-106X_v2/CMSSW_10_6_28/src/UHH2/ZprimeSemiLeptonic/output_DNN/UL18/muon/workdir_AnalysisDNN_UL18_muon_newxrange/nominal/uhh2.AnalysisModuleRunner.TTToSemiLeptonic.root",
             "/nfs/dust/cms/user/beozek/uuh2-106X_v2/CMSSW_10_6_28/src/UHH2/ZprimeSemiLeptonic/output_DNN/UL18/muon/workdir_AnalysisDNN_UL18_muon_newxrange/nominal/uhh2.AnalysisModuleRunner.TTToOthers.root", 
              "/nfs/dust/cms/user/beozek/uuh2-106X_v2/CMSSW_10_6_28/src/UHH2/ZprimeSemiLeptonic/output_DNN/UL18/muon/workdir_AnalysisDNN_UL18_muon_newxrange/nominal/uhh2.AnalysisModuleRunner.WJets.root",
             "/nfs/dust/cms/user/beozek/uuh2-106X_v2/CMSSW_10_6_28/src/UHH2/ZprimeSemiLeptonic/output_DNN/UL18/muon/workdir_AnalysisDNN_UL18_muon_newxrange/nominal/uhh2.AnalysisModuleRunner.ST.root", 
             "/nfs/dust/cms/user/beozek/uuh2-106X_v2/CMSSW_10_6_28/src/UHH2/ZprimeSemiLeptonic/output_DNN/UL18/muon/workdir_AnalysisDNN_UL18_muon_newxrange/nominal/uhh2.AnalysisModuleRunner.Diboson.root", 
             "/nfs/dust/cms/user/beozek/uuh2-106X_v2/CMSSW_10_6_28/src/UHH2/ZprimeSemiLeptonic/output_DNN/UL18/muon/workdir_AnalysisDNN_UL18_muon_newxrange/nominal/uhh2.AnalysisModuleRunner.QCD.root", 
             "/nfs/dust/cms/user/beozek/uuh2-106X_v2/CMSSW_10_6_28/src/UHH2/ZprimeSemiLeptonic/output_DNN/UL18/muon/workdir_AnalysisDNN_UL18_muon_newxrange/nominal/uhh2.AnalysisModuleRunner.DYJets.root", 
                "/nfs/dust/cms/user/beozek/uuh2-106X_v2/CMSSW_10_6_28/src/UHH2/ZprimeSemiLeptonic/output_DNN/UL18/muon/workdir_AnalysisDNN_UL18_muon_newxrange/nominal/uhh2.AnalysisModuleRunner.DATA.DATA.root"] 
folder_name = "DNN_output0_NoTopTag_beforeChi2Cut_General"  
hist_name = 'NN_chi2'  
x_max = 30  

integrate_histogram(file_names, folder_name, hist_name, x_max)
