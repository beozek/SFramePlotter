import ROOT

# 1. Setup
ROOT.gROOT.SetBatch(True)
from Style import *
thestyle = Style()

HasCMSStyle = False
style = None

# If you have the CMS style defined, you can load and set it here.
ROOT.gROOT.ProcessLine('.L CMSStyle.C')
style = ROOT.CMSStyle()
ROOT.gROOT.SetStyle("CMSStyle")

# 2. Configuration based on the steer
inputFiles = [fCycleName + "/" + name for name in fInputFiles.split(",")]
sampleNames = fSampleNames.split(",")
sampleWeights = [float(w) for w in fSamplesWeight.split(",")]

# 3. Plotting
canvas = ROOT.TCanvas("c", "c", 800, 800)

# Split canvas for ratio plot
pad1 = ROOT.TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
pad2 = ROOT.TPad("pad2", "pad2", 0, 0.05, 1, 0.3)
pad1.SetBottomMargin(0.02)
pad2.SetTopMargin(0)
pad2.SetBottomMargin(0.3)
pad1.Draw()
pad2.Draw()

for histName in histograms:
    stack = ROOT.THStack("stack", "")
    dataHist = None
    mcSum = None

    for file, sample, weight in zip(inputFiles, sampleNames, sampleWeights):
        f = ROOT.TFile(file)
        hist = f.Get(histName).Clone()
        hist.Scale(weight)

        if sample == "Data":
            dataHist = hist
        else:
            stack.Add(hist)

            if mcSum:
                mcSum.Add(hist)
            else:
                mcSum = hist.Clone()

    # Draw MC stack and data
    pad1.cd()
    stack.Draw("HIST")
    dataHist.Draw("SAME PE")

    # Draw ratio
    if bRatioPlot:
        pad2.cd()
        ratio = dataHist.Clone("ratio")
        ratio.Divide(mcSum)
        ratio.Draw("PE")

    # Add CMS Preliminary
    lumi = ROOT.TLatex()
    lumi.SetTextSize(0.035)
    lumi.SetTextAlign(11)
    lumi.DrawLatexNDC(0.1, 0.93, "CMS Preliminary #sqrt{s} = 13 TeV, L = {:.1f} fb^{{-1}}".format(fLumi))

    canvas.SaveAs(fOutputPsFile.replace(".ps", "_{}.ps".format(histName)))

print("Plots saved in:", fOutputPsFile)
