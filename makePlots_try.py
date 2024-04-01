from ROOT import *
import os
import sys
from optparse import OptionParser
from numpy import log10
from array import array
import CMS_lumi
from Style import *


ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.gStyle.SetOptStat(0)

parser = OptionParser()
parser.add_option("-c", "--channel", dest="channel", default="mu", type='str',
                  help="Specify which channel mu or ele? default is mu")
parser.add_option("--Log", "--isLog", dest="isLog", default=False, action="store_true",
                  help="Plot the plots in log ?")

(options, args) = parser.parse_args()

histograms = {
     "pt_mu" : ["p_{T}^{#mu} [GeV]", "Events", 90, [0, 900]],
            #   "Chi_2" : ["Chi2", "Events", 20, [0,100]],
            #   "ditop_mass" : ["M_{tt}", "Events", 100, [0,2000]],
            #   "DeltaY_reco"  : ["#DeltaY_{reco{}", "Events", 2, [-2.5,2.5]],
  			#   "N_jets"       :["N_{jets}", "Events", 10, [0, 10]],
 			#   "ditop_deltaR" : ["ditop_deltaR", "Events", 100, [0, 3]]
              
		}

padRatio = 0.25
padOverlap = 0.15
padGap = 0.01

channel = options.channel
Log = options.isLog

if channel == "ele":
    _channelText = "e+jets"
    plotDirectory = "data_pre_plots_ele"
    file_dir = "/nfs/dust/cms/user/beozek/uuh2-106X_v2/CMSSW_10_6_28/src/UHH2/ZprimeSemiLeptonic/output_combine/UL18/muon/workdir_Analysis_UL18_muon_all/nominal/"
else:
    _channelText = "#mu+jets"
    plotDirectory = "../../plots"
    file_dir = "/nfs/dust/cms/user/beozek/uuh2-106X_v2/CMSSW_10_6_28/src/UHH2/ZprimeSemiLeptonic/output_DNN/UL18/muon/workdir_AnalysisDNN_UL18_muon_dY/nominal/"

mc_samples = ["QCD", "Diboson","ST", "DYJets", "WJets","TTToSemiLeptonic","TTToOthers"]
hist_folder = "DNN_output0_beforeChi2Cut_General"

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
    
H = 600
W = 800
# references for T, B, L, R                                                                                                             
T = 0.08*H
B = 0.12*H
L = 0.12*W
R = 0.1*W

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

pad1 = ROOT.TPad("pad1", "", 0, padRatio - padOverlap, 1, 1.0)
pad2 = ROOT.TPad("pad2", "", 0, 0, 1, padRatio + padOverlap)

pad1.SetBottomMargin(0)
pad1.SetGridx()
pad1.SetLogy(Log)
pad1.Draw()

pad2.SetTopMargin(0)
pad2.SetBottomMargin(0.3)
pad2.SetGridx()
pad2.Draw()

# canvas.cd()
# pad1.Draw()
# pad2.Draw()
    
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


legendHeightPer = 0.04
legList = stackList.keys()
legendStart = 0.69
legendEnd = 0.97 - (R / W)

legend = TLegend(2 * legendStart - legendEnd, 0.99 - (T / H) / (1. - padRatio + padOverlap) - legendHeightPer / (1. - padRatio + padOverlap) * round((len(legList) + 1) / 2.), legendEnd, 0.99 - (T / H) / (1. - padRatio + padOverlap))
legend.SetNColumns(2)
    
hs = ROOT.THStack("hs", "")

for hist_name, hist_info in histograms.items():
    # Unpack histogram info
    x_title, y_title, rebin, x_range = hist_info
    
    for sample in mc_samples:
        file_path = file_dir + sample + ".root"
        file = ROOT.TFile(file_path, "READ")
        hist_path = hist_folder + "/" + hist_name
        hist = file.Get(hist_path)
        hist.SetDirectory(0)  
        hist.SetFillColor(stackList[sample][0]) 
        hist.SetLineColor(ROOT.kBlack)  
        # if isNorm and hist.Integral() > 0: 
        #     hist.Scale(1.0 / hist.Integral()) 
        hs.Add(hist)
        file.Close()

    data_file_path = file_dir + "DATA" + ".root"
    data_file = ROOT.TFile(data_file_path, "READ")
    data_hist_path = hist_folder + "/" + hist_name 
    data_hist = data_file.Get(data_hist_path)
    data_hist.SetDirectory(0)
    data_hist.SetMarkerStyle(20)
    # if isNorm: data_hist.Scale(1.0 / data_hist.Integral()) 
    data_file.Close()
    
    legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
    legend.SetTextSize(0.03)
    legend.AddEntry(data_hist, "Data", "lep")
    for sample in mc_samples:
        legend.AddEntry(hs.GetHists().FindObject(sample), sample, "f")
    pad1.cd()
    hs.Draw("HIST")
    data_hist.Draw("SAME E")
    legend.Draw()

    # Ratio plot
    pad2.cd()
    ratio_hist = data_hist.Clone("ratio")
    mc_hist_sum = hs.GetStack().Last().Clone("mc_hist_sum") 
    ratio_hist.Divide(mc_hist_sum)
    ratio_hist.Draw("EP")

    ratio_hist.GetYaxis().SetTitle("Data / MC")
    ratio_hist.GetYaxis().SetNdivisions(505)
    ratio_hist.GetYaxis().SetTitleSize(20)
    ratio_hist.GetYaxis().SetTitleFont(43)
    ratio_hist.GetYaxis().SetTitleOffset(1.55)


canvas.SaveAs("pt_mu.pdf")
