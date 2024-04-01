#from ROOT import TFile, TLegend, TCanvas, TPad, THStack, TF1, TPaveText, TGaxis, SetOwnership, TObject, gStyle,TH1F
from ROOT import *
from ROOT import TGaxis
import os
import sys
from optparse import OptionParser
from numpy import log10
from array import array

parser = OptionParser()
parser.add_option("-c", "--channel", dest="channel", default="ele", type='str', 
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
    plotDirectory = "/nfs/dust/cms/user/beozek/uuh2-106X_v2/CMSSW_10_6_28/src/UHH2/ZprimeSemiLeptonic/output_DNN/UL18/muon/"
    _fileDir = "/nfs/dust/cms/user/beozek/uuh2-106X_v2/CMSSW_10_6_28/src/UHH2/ZprimeSemiLeptonic/output_DNN/UL18/ele/workdir_AnalysisDNN_UL18_ele_dY/nominal"
else:
    _channelText = "#mu+jets"
    plotDirectory = "/nfs/dust/cms/user/beozek/uuh2-106X_v2/CMSSW_10_6_28/src/UHH2/ZprimeSemiLeptonic/output_DNN/UL18/muon/"
    _fileDir = "/nfs/dust/cms/user/beozek/uuh2-106X_v2/CMSSW_10_6_28/src/UHH2/ZprimeSemiLeptonic/output_DNN/UL18/muon/workdir_AnalysisDNN_UL18_muon_dY/nominal"

gROOT.SetBatch(True)

histogram_folder = "DNN_output0_beforeChi2Cut_General"

if channel == "mu":
    histogram_settings = {
        # "NN_chi2": ["Chi2", "Events", 20, [0, 100]],
        # "pt_mu" : ["p_{T}^{#mu} [GeV]", "Events", 90, [0, 900]],
        # "eta_mu " : ["#eta^{#mu}", "Events", 50, [-2.5, 2.5]],        
        # "pt_jet1" : ["p_{T}^{jet 1 AK4} [GeV]", "Events",90, [0, 900]],
        # "eta_jet1" : ["#eta^{jet 1}", "Events", 50, [-3, 3]],
        # "toplep_pt" : ["p_{T}^{t,lep} [GeV]", "Events", 70, 0, 3000],
        # "tophad_pt" : ["p_{T}^{t,had} [GeV]", "Events", 70, 0, 3000],
        # "chi2_Zprime" : ["Chi2_2", "Events", 20, [0,100]],
        # "ditop_mass": ["M_{TT}", "Events", 100, [0,3000]],
        # "DeltaY_reco": ["#DeltaY_{reco}", "Events", 2, [-2.5, 2.5]],
        # "N_jets": ["N_{jets}", "Events", 21, [0, 10]],
    }
else:
    histogram_settings = {
        "pt_ele" : ["p_{T}^{electron} [GeV]", "Events", 90, [0, 900]],
        # "eta_ele " : ["#eta^{e}", "Events", 50, -2.5, 2.5],
    }

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
legendStart = 0.69
legendEnd = 0.97 - (R / W)

legend = TLegend(2 * legendStart - legendEnd, 0.99 - (T / H) / (1. - padRatio + padOverlap) - legendHeightPer / (1. - padRatio + padOverlap) * round((len(legList) + 1) / 2.), legendEnd, 0.99 - (T / H) / (1. - padRatio + padOverlap))
legend.SetNColumns(2)

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

sample_names = ["TTToSemiLeptonic", "TTToOthers", "WJets", "DYJets", "ST", "QCD", "Diboson" ]

_file = {}
hist = {}
stack = {}
legendR = {}


for histName in histogram_settings.keys():
    stack[histName] = THStack("hs_" + histName, histName)
    hist[histName] = {} 
    
    legendR[histName] = TLegend(0.7, 0.7, 0.9, 0.9) 
    legendR[histName].SetNColumns(2)
    legendR[histName].SetBorderSize(0)
    legendR[histName].SetFillColor(0)

def load_histogram(sample, hist_name):
    global _file
    file_path = "%s/%s.root" % (_fileDir, sample)
    print "Attempting to open file:", file_path
    
    _file[sample] = ROOT.TFile(file_path, "read")
    if _file[sample].IsZombie() or not _file[sample].IsOpen():
        print "Error opening file:", file_path
        return None
    
    full_hist_name = histogram_folder + "/" + hist_name
    print "Attempting to load histogram:", full_hist_name
    histogram = _file[sample].Get(full_hist_name)
    if not histogram or not histogram.InheritsFrom("TH1"):
        print "Histogram not found or not a TH1:", full_hist_name, "in file", file_path
        return None
    return histogram



for histName, settings in histogram_settings.items():
    for sample in sample_names:
        histogram = load_histogram(sample, histName)
        if histogram:
            histogram.SetFillColor(stackList[sample][0])
            histogram.SetLineColor(stackList[sample][0])
            stack[histName].Add(histogram)
            hist[histName][sample] = histogram
            legendR[histName].AddEntry(histogram, sample, "f")


for histName in histogram_settings:
    canvas.cd()
    if stack[histName]:
        stack[histName].Draw("HIST")
        stack[histName].GetXaxis().SetTitle(histogram_settings[histName][0])
        stack[histName].GetYaxis().SetTitle(histogram_settings[histName][1])
    
    # errorband = stack[histName].GetStack().Last().Clone("errorban")
    # errorband.Sumw2()
    # errorband.SetLineColor(kBlack)
    # errorband.SetFillColor(kBlack)
    # errorband.SetFillStyle(3245)
    # errorband.SetMarkerSize(0) 
    
    data_file_path = "%s/DATA.root" % _fileDir
    data_file = ROOT.TFile(data_file_path, "read")
    dataHist = data_file.Get("%s/%s" % ("AfterChi2_General", histName))
    dataHist.SetMarkerColor(kBlack)
    dataHist.SetYTitle("Events")
    legendR[histName].AddEntry(dataHist, "Data", 'pe')
    
    # testCanvas = TCanvas("test", "test", 600, 600)
    # dataHist.Draw("E")
    # testCanvas.SaveAs("dataHist_test.pdf")

    canvas.cd()
    pad1.cd()
    pad1.SetLogy(Log)
        
    TGaxis.SetMaxDigits(4)
    
    stack[histName].Draw("HIST")
    dataHist.Draw("E,X0,SAME")
    
    stack[histName].GetXaxis().SetTitle('')
    stack[histName].GetYaxis().SetTitle(dataHist.GetYaxis().GetTitle())
    stack[histName].SetTitle('')
    
    stack[histName].GetXaxis().SetLabelSize(0)
    stack[histName].GetXaxis().SetTitleSize(0.06)
    
    stack[histName].GetYaxis().SetLabelSize(gStyle.GetLabelSize() / (1. - padRatio + padOverlap))
    stack[histName].GetYaxis().SetTitleSize(gStyle.GetTitleSize() / (1. - padRatio + padOverlap))
    # stack[histName].GetYaxis().SetTitleOffset(gStyle.GetTitleYOffset() * (1. - padRatio + padOverlap))
    
    stack[histName].GetYaxis().SetTitleOffset(gStyle.GetTitleYOffset() * (1. - padRatio + padOverlap) * 0.8)


    # ratio = dataHist.Clone("temp")

    pad2.cd()
    ratio = dataHist.Clone("ratio_" + histName)
    
    temp = stack[histName].GetStack().Last().Clone("temp")

    for i_bin in range(1, temp.GetNbinsX() + 1):
        temp.SetBinError(i_bin, 0.)

    ratio.Divide(temp)
    ratio.Draw("EP")
    
    ratio.SetTitle('')
    ratio.GetXaxis().SetLabelSize(gStyle.GetLabelSize() / (padRatio + padOverlap))
    ratio.GetYaxis().SetLabelSize(gStyle.GetLabelSize() / (padRatio + padOverlap))
    # ratio.GetXaxis().SetTitleSize(gStyle.GetTitleSize() / (padRatio + padOverlap))
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

    maxVal = stack[histName].GetMaximum()
    minVal = max(stack[histName].GetStack()[0].GetMinimum(), 1)
    
    if Log:
        stack[histName].SetMaximum(15**(1.5 * log10(maxVal) - 0.5 * log10(minVal)))
        stack[histName].SetMinimum(1)
    # elif Norm:
    #     stack[histName].SetMaximum(-5)
    #     stack[histName].SetMinimum(-5)
    else:
        stack[histName].SetMaximum(1.7 * maxVal)
        # stack[histName].SetMinimum(minVal)
        # stack[histName].SetMaximum(2)
        stack[histName].SetMinimum(0)
        # stack[histName].SetMaximum(30000)
        # stack[histName].SetMinimum(minVal)
        # dataHist.SetMaximum(2)
        # dataHist.SetMinimum(0)
    beren = histName

    canvasRatio.cd()
    pad1.Draw()
    pad2.Draw()

    pad1.cd()
    stack[beren].Draw("HIST")

    dataHist.Draw("E,X0,SAME")
    
    # Drawing the ratio plot in the lower pad
    
    
    errorband = stack[beren].GetStack().Last().Clone("errorban")
    errorband.Sumw2()
    errorband.SetLineColor(kBlack)
    errorband.SetFillColor(kBlack)
    errorband.SetFillStyle(3245)
    errorband.SetMarkerSize(0) 
    
    pad2.cd()
    line = ROOT.TLine(ratio.GetXaxis().GetXmin(), 1, ratio.GetXaxis().GetXmax(), 1)
    line.SetLineColor(ROOT.kBlack)
    line.SetLineStyle(2)
    line.SetLineWidth(1)
    line.Draw("same")

    errorband.Divide(temp)  # Error band for ratio
    errorband.Draw('e2,same')

    # Draw CMS Lumi, legend and save the canvas
    CMS_lumi.CMS_lumi(pad1, 4, 11)
    legendR[beren].Draw()
    canvasRatio.Update()
    canvasRatio.RedrawAxis()

    canvasRatio.SaveAs("%s/%s_try.pdf" % (plotDirectory, beren))
    