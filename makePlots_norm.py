#from ROOT import TFile, TLegend, TCanvas, TPad, THStack, TF1, TPaveText, TGaxis, SetOwnership, TObject, gStyle,TH1F
from ROOT import *
from ROOT import TGaxis
import os
import sys
from optparse import OptionParser
from numpy import log10
from array import array

parser = OptionParser()
parser.add_option("-c", "--channel", dest="channel", default="mu", type='str', 
                  help="Specify which channel mu or ele? default is mu")
parser.add_option("--Log", "--isLog", dest="isLog", default=True, action="store_true", 
                  help="Plot the plots in log ?")
parser.add_option("--Norm", "--isNorm", dest="isNorm", default=False, action="store_true", 
                  help="Plot the plots normalized ?")

(options, args) = parser.parse_args()

padRatio = 0.25
padOverlap = 0.15
padGap = 0.01
# Norm = options.isNorm
channel = options.channel
Log = options.isLog

if channel == "ele":
    _channelText = "e+jets"
    plotDirectory = "data_pre_plots_ele"
    _fileDir = "/nfs/dust/cms/user/beozek/uuh2-106X_v2/CMSSW_10_6_28/src/UHH2/ZprimeSemiLeptonic/output_DNN/UL18/muon/workdir_AnalysisDNN_UL18_muon_newbins/nominal"
else:
    _channelText = "#mu+jets"
    plotDirectory = "/nfs/dust/cms/user/beozek/uuh2-106X_v2/CMSSW_10_6_28/src/UHH2/ZprimeSemiLeptonic/output_DNN/UL18/muon/workdir_AnalysisDNN_UL18_muon_newbins/plots2/DNN_output0_TopTag/all"
    _fileDir = "/nfs/dust/cms/user/beozek/uuh2-106X_v2/CMSSW_10_6_28/src/UHH2/ZprimeSemiLeptonic/output_DNN/UL18/muon/workdir_AnalysisDNN_UL18_muon_newbins/nominal"

gROOT.SetBatch(True)

histogram_folder = "DNN_output0_TopTag_General"

if channel == "mu":
    histogram_settings = {
        # "NN_chi2": ["Chi2", "Events", 20, [0, 100]],
        # "NN_N_Ak4" : ["NN_N_Ak4", "Events", 20,[0, 20]],
        # "NN_N_Ak8" : ["NN_N_Ak8", "Events", 20, [0, 20]],
        # "NN_MET_pt" : ["NN_MET_pt", "Events", 150, [0, 1500]],
        # "NN_Mu_pt "  :  ["NN_Mu_pt", "Events", 50, [0, 1000]],
        # "NN_Mu_eta"  :["NN_Mu_eta", "Events", 50,[ -2.5, 2.5]],
        # "NN_Mu_phi" : ["NN_Mu_phi", "Events", 35, [-3.5, 3.5]]
        "pt_mu" : ["p_{T}^{#mu} [GeV]", 90, [0, 900]],
        # "pt_jet1" : ["p_{T}^{jet 1 AK4} [GeV]", 90, [0, 900]],
        # "toplep_pt" : ["p_{T}^{t,lep} [GeV]", "Events", 70, 0, 3000],
        # "tophad_pt" : ["p_{T}^{t,had} [GeV]", "Events", 70, 0, 3000],
        # "dRmin_mu_jet" : ["#DeltaR_{min}(#mu, jet)", "Events", 60, 0, 3],
        # "chi2_Zprime" : ["Chi2_2", "Events", 20, [0,100]],
        # "ditop_mass": ["M_{TT}", "Events", 100, [0,3000]],
        # "M_Zprime" : ["M_{t\bar{t}}_2", "Events", 100, [0,3000]],
        # "M_Zprime_rebin3" : ["M_{TT}_3", "Events", 100, [0,3000]],
        # "NN_M_tt_weighted": ["M_{TT}_weighted", "Events", 100, [0, 3000]],
        # "DeltaY_reco": ["#DeltaY_{reco}", "Events", 2, [-2.5, 2.5]],
        # "N_jets": ["N_{jets}", "Events", 21, [0, 10]],
        # "ditop_deltaR": ["ditop_deltaR", "Events", 100, [0, 10.0]],
    }
else:
    histogram_settings = {}

import CMS_lumi
from Style import *
thestyle = Style()

HasCMSStyle = False
style = None
if os.path.isfile('tdrstyle.C'):
    ROOT.gROOT.ProcessLine('.L tdrstyle.C')
    ROOT.setTDRStyle()
    print("Found tdrstyle.C file, using this style.")
    HasCMSStyle = True
    if os.path.isfile('CMSTopStyle.cc'):
        gROOT.ProcessLine('.L CMSTopStyle.cc+')
        style = CMSTopStyle()
        style.setupICHEPv1()
        print("Found CMSTopStyle.cc file, use TOP style if requested in xml file.")
if not HasCMSStyle:
    print("Using default style defined in cuy package.")
    thestyle.SetStyle()

ROOT.gROOT.ForceStyle()

stackList = {
    "TTToSemiLeptonic": [kRed], 
    "TTToOthers": [kPink + 3], 
    "DYJets": [kOrange], 
    "QCD": [kCyan], 
    "WJets": [kGreen], 
    "ST": [kBlue], 
    "Diboson": [kMagenta]
}

CMS_lumi.channelText = _channelText
CMS_lumi.writeChannelText = True
CMS_lumi.writeExtraText = True

H = 600
W = 800

# references for T, B, L, R
T = 0.08 * H
B = 0.12 * H
L = 0.12 * W
R = 0.1 * W

legendHeightPer = 0.04
legList = stackList.keys()
legendStart = 0.75
legendEnd = 0.97 - (R / W)

legend = TLegend(2 * legendStart - legendEnd, 0.99 - (T / H) / (1. - padRatio + padOverlap) - legendHeightPer / (1. - padRatio + padOverlap) * round((len(legList) + 1) / 2.), legendEnd, 0.99 - (T / H) / (1. - padRatio + padOverlap))
legend.SetNColumns(2)

_file = {}

canvas = TCanvas('c1', 'c1', W, H)
canvas.SetFillColor(0)
canvas.SetBorderMode(0)
canvas.SetFrameFillStyle(0)
canvas.SetFrameBorderMode(0)
canvas.SetLeftMargin(L / W)
canvas.SetRightMargin(R / W)
canvas.SetTopMargin(T / H)
canvas.SetBottomMargin(B / H)
canvas.SetTickx(0)

canvasRatio = TCanvas('c1Ratio', 'c1Ratio', W, H)
canvasRatio.SetFillColor(0)
canvasRatio.SetBorderMode(0)
canvasRatio.SetFrameFillStyle(0)
canvasRatio.SetFrameBorderMode(0)
canvasRatio.SetLeftMargin(L / W)
canvasRatio.SetRightMargin(R / W)
canvasRatio.SetTopMargin(T / H)
canvasRatio.SetBottomMargin(B / H)
canvasRatio.SetTickx(0)
canvasRatio.SetTicky(0)
canvasRatio.Draw()
canvasRatio.cd()

pad1 = TPad("zxc_p1", "zxc_p1", 0, padRatio - padOverlap, 1, 1)
pad2 = TPad("qwe_p2", "qwe_p2", 0, 0, 1, padRatio + padOverlap)
pad1.SetLeftMargin(L / W)
pad1.SetRightMargin(R / W)
pad1.SetTopMargin(T / H / (1 - padRatio + padOverlap))
pad1.SetBottomMargin((padOverlap + padGap) / (1 - padRatio + padOverlap))
pad2.SetLeftMargin(L / W)
pad2.SetRightMargin(R / W)
pad2.SetTopMargin((padOverlap) / (padRatio + padOverlap))
pad2.SetBottomMargin(B / H / (padRatio + padOverlap))
pad1.SetFillColor(0)
pad1.SetBorderMode(0)
pad1.SetFrameFillStyle(0)
pad1.SetFrameBorderMode(0)
pad1.SetTickx(0)
pad1.SetTicky(0)

pad2.SetFillColor(0)
pad2.SetFillStyle(4000)
pad2.SetBorderMode(0)
pad2.SetFrameFillStyle(0)
pad2.SetFrameBorderMode(0)
pad2.SetTickx(0)
pad2.SetTicky(0)

canvasRatio.cd()
pad1.Draw()
pad2.Draw()

canvas.cd()
canvas.ResetDrawn()

#stack = THStack("hs", "stack")
#SetOwnership(stack, True)

sum_ = 0
tree_MC = {}
hist = {}

sample_names = ["TTToSemiLeptonic", "TTToOthers", "WJets", "DYJets", "ST", "QCD", "Diboson" ]
stack = {}
legendR = {}

def load_histogram(sample, hist_name):
    global _file
    file_path = "%s/uhh2.AnalysisModuleRunner.%s.root" % (_fileDir, sample)
    print("Attempting to open file:", file_path)
    _file[sample] = ROOT.TFile(file_path, "read")

    if _file[sample].IsZombie() or not _file[sample].IsOpen():
        print("Error opening file:", file_path)
        return None, None
    # print("Listing keys in file:", file_path)
    # _file[sample].ls()

    full_hist_name = histogram_folder + "/" + hist_name
    print("Attempting to load histogram:", full_hist_name)
    histogram = _file[sample].Get(full_hist_name)

    if not histogram or not isinstance(histogram, ROOT.TH1):
        print("Histogram not found:", full_hist_name, "in file", file_path)
        return None, None
    
    # integral_before = histogram.Integral()
    # print "Integral before scaling for %s, %s: %f" % (sample, hist_name, integral_before)

    
    # integral_after = histogram.Integral()
    # print "Integral after scaling for %s, %s: %f" % (sample, hist_name, integral_after)
        
    return histogram, _file[sample]

mc_sum = None

for histName in histogram_settings:
    hist[histName] = {}
    stack[histName] = THStack("hs", "stack")
    legendR[histName] = TLegend(2 * legendStart - legendEnd, 0.99 - (T / H) / (1. - padRatio + padOverlap) - legendHeightPer / (1. - padRatio + padOverlap) * round((len(legList) + 1) / 2.) - 0.1, legendEnd, 0.99 - (T / H) / (1. - padRatio + padOverlap))
    legendR[histName].SetNColumns(2)
    legendR[histName].SetBorderSize(0)
    legendR[histName].SetFillColor(0)


canvas.cd()

    
for histName in histogram_settings.keys():
    mc_sum = None
    
    for sample in sample_names:
        
        hist[histName][sample], _file[sample] = load_histogram(sample, histName)
        # print("X-axis range for histogram", histName, ":", hist[histName][sample].GetXaxis().GetXmin(), "-", hist[histName][sample].GetXaxis().GetXmax())

        if mc_sum is None:
            mc_sum = hist[histName][sample].Clone(histName + "_sum")
            mc_sum.Reset()
            
        mc_sum.Add(hist[histName][sample])
        
    # mc_integral = mc_sum.Integral()
    
    for sample in sample_names:
        hist[histName][sample].Scale(1.0 / (mc_sum.Integral()))
        hist[histName][sample].SetFillColor(stackList[sample][0])
        hist[histName][sample].SetLineColor(stackList[sample][0])
        legendR[histName].AddEntry(hist[histName][sample], sample, 'f')
        stack[histName].Add(hist[histName][sample])

    mc_sum.Scale(1.0 / (mc_sum.Integral()))
    
    
    data_file_path = "%s/uhh2.AnalysisModuleRunner.DATA.DATA.root" % _fileDir
    data_file = ROOT.TFile(data_file_path, "read")
    dataHist = data_file.Get("%s/%s" % (histogram_folder, histName))
    
    if dataHist.Integral() != 0:
        scale_factor_data = (1.0/ (dataHist.Integral()))
        dataHist.Scale(scale_factor_data)
        
    
    # for sample in sample_names:
    #     hist[histName][sample].Scale(scale_factor)
    #     stack[histName].Add(hist[histName][sample])
        
    # if dataHist.Integral() != 0:
    #     dataHist.Scale(1/ dataHist.Integral())
    
    # integral_data_after = dataHist.Integral()
    # print "Integral after scaling for data: %f" % (integral_data_after)
        


    dataHist.SetMarkerColor(kBlack)
    dataHist.SetYTitle("Events (Normalized)")  
    # dataHist.GetXaxis().SetRangeUser(x_range[0], x_range[1]) 
    
    legendR[histName].AddEntry(dataHist, "Data", 'pe')
    
    canvas.cd()
    pad1.cd()
    pad1.SetLogy(Log)
        
    TGaxis.SetMaxDigits(4)
    dataHist.Draw("E,X0,SAME")
    stack[histName].Draw("HIST")
    
    stack[histName].GetXaxis().SetTitle('')
    stack[histName].GetYaxis().SetTitle(dataHist.GetYaxis().GetTitle())
    stack[histName].SetTitle('')
    
    stack[histName].GetXaxis().SetLabelSize(0)
    stack[histName].GetXaxis().SetTitleSize(0.06)
    
    stack[histName].GetYaxis().SetLabelSize(gStyle.GetLabelSize() / (1. - padRatio + padOverlap))
    stack[histName].GetYaxis().SetTitleSize(gStyle.GetTitleSize() / (1. - padRatio + padOverlap))
    # stack[histName].GetYaxis().SetTitleOffset(gStyle.GetTitleYOffset() * (1. - padRatio + padOverlap))
    
    # Adjusting the Y-axis title offset
    stack[histName].GetYaxis().SetTitleOffset(gStyle.GetTitleYOffset() * (1. - padRatio + padOverlap) * 0.8)

    

    ratio = dataHist.Clone("temp")
    temp = stack[histName].GetStack().Last().Clone("temp")

    for i_bin in range(1, temp.GetNbinsX() + 1):
        temp.SetBinError(i_bin, 0.)

    ratio.Divide(temp)

    pad2.cd()
    ratio.SetTitle('')
    ratio.GetXaxis().SetLabelSize(gStyle.GetLabelSize() / (padRatio + padOverlap))
    ratio.GetYaxis().SetLabelSize(gStyle.GetLabelSize() / (padRatio + padOverlap))
    ratio.GetXaxis().SetTitleSize(gStyle.GetTitleSize() / (padRatio + padOverlap))
    ratio.GetYaxis().SetTitleSize(gStyle.GetTitleSize() / (padRatio + padOverlap))
    ratio.GetYaxis().SetTitleOffset(gStyle.GetTitleYOffset() * (padRatio + padOverlap - padGap)*0.7)
    
    reduced_title_size = 0.7 
    ratio.GetXaxis().SetTitleSize(gStyle.GetTitleSize() / (padRatio + padOverlap) * reduced_title_size)
    
    increased_offset = 1.1  
    ratio.GetXaxis().SetTitleOffset(gStyle.GetTitleXOffset() * increased_offset)
    
    ratio.GetYaxis().SetRangeUser(0.35, 1.65)
    ratio.GetYaxis().SetNdivisions(504)
    ratio.GetXaxis().SetTitle(histogram_settings[histName][0])
    ratio.GetYaxis().SetTitle("Data/MC")

    ratio.SetMarkerStyle(dataHist.GetMarkerStyle())
    ratio.SetMarkerSize(dataHist.GetMarkerSize())
    ratio.SetLineColor(dataHist.GetLineColor())
    ratio.SetLineWidth(dataHist.GetLineWidth())
    ratio.Draw('e,x0')

    CMS_lumi.CMS_lumi(pad1, 4, 11)
    legendR[histName].Draw()
    
    maxVal = stack[histName].GetMaximum()
    minVal = max(stack[histName].GetStack()[0].GetMinimum(), 1)
    print("TYPE!")
    print(type(histName))
    
    if Log:
        stack[histName].SetMaximum(1.001)
        # stack[histName].SetMaximum(15**(1.5 * log10(maxVal) - 0.5 * log10(minVal)))
        # stack[histName].SetMinimum(0)
    # if Norm:
    #     stack[histName].SetMaximum(-5)
    #     stack[histName].SetMinimum(-5)
    else:
        # stack[histName].SetMaximum(1.7 * maxVal)
        # stack[histName].SetMinimum(minVal)
        stack[histName].SetMaximum(0.5)
        stack[histName].SetMinimum(0)
        # stack[histName].SetMaximum(30000)
        # stack[histName].SetMinimum(minVal)
        # dataHist.SetMaximum(2)
        # dataHist.SetMinimum(0)

    errorband = stack[histName].GetStack().Last().Clone("error")
    errorband.Sumw2()
    errorband.SetLineColor(kBlack)
    errorband.SetFillColor(kBlack)
    errorband.SetFillStyle(3245)
    errorband.SetMarkerSize(0)

    canvasRatio.cd()
    pad1.Draw()
    pad2.Draw()
    

    pad1.cd()
    pad1.SetLogy(Log)
    stack[histName].Draw("HIST")
    dataHist.Draw("E,X0,SAME")
    errorband.Draw('e2,same')
    
    # Drawing the ratio plot in the lower pad
    pad2.cd()
    # oneLine = TF1("oneline", "1", -9e9, 9e9)
    # oneLine.SetLineColor(kBlack)    
    # oneLine.SetLineWidth(1)
    # oneLine.SetLineStyle(2)
    # ratio.Draw('e,x0')
    # errorband.Divide(temp)  # Error band for ratio
    # errorband.Draw('e2,same')
    # oneLine.Draw("same")
    # Draw CMS Lumi, legend and save the canvas
    
    # line = ROOT.TLine(ratio.GetXaxis().GetXmin(), 1, ratio.GetXaxis().GetXmax(), 1)
    ROOT.TLine(ratio.GetXaxis().GetXmin(), 1, ratio.GetXaxis().GetXmax(), 1).SetLineColor(ROOT.kBlack) 
    ROOT.TLine(ratio.GetXaxis().GetXmin(), 1, ratio.GetXaxis().GetXmax(), 1).SetLineWidth(1)
    ROOT.TLine(ratio.GetXaxis().GetXmin(), 1, ratio.GetXaxis().GetXmax(), 1).SetLineStyle(ROOT.kDotted) 
    ratio.Draw('e,x0')
    errorband.Divide(temp)  # Error band for ratio
    errorband.Draw('e2,same')
    ROOT.TLine(ratio.GetXaxis().GetXmin(), 1, ratio.GetXaxis().GetXmax(), 1).Draw("same")
    
    
    CMS_lumi.CMS_lumi(pad1, 4, 11)
    legendR[histName].Draw()
    canvasRatio.Update()
    canvasRatio.RedrawAxis()

    if Log:
        canvasRatio.SaveAs("%s/%s_norm_log.pdf" % (plotDirectory, histName))
    # if Norm:
    #     canvasRatio.SaveAs("%s/%s_norm.pdf" % (plotDirectory, histName))
    else:
        canvasRatio.SaveAs("%s/%s_norm_try.pdf" % (plotDirectory, histName))