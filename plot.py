from ROOT import *
import os
import sys
from optparse import OptionParser

parser = OptionParser()
parser.add_option("--Log","--isLog", dest="isLog", default=True,action="store_true",
                     help="Plot the plots in log ?" )
parser.add_option("--QCD","--isQCD", dest="isQCD", default=False,action="store_true",
                     help="Plot as QCD and others" )

(options, args) = parser.parse_args()

padRatio = 0.25
padOverlap = 0.15
padGap = 0.01

Log=options.isLog
QCD = options.isQCD

channelText = "#mu+jets"
plotDirectory = "nominal"
fileDir = "/nfs/dust/cms/user/beozek/uuh2-106X_v2/CMSSW_10_6_28/src/UHH2/ZprimeSemiLeptonic/output_combine/UL18/muon/workdir_Analysis_UL18_muon_new_massranges/nominal/"

gROOT.SetBatch(True)

regionText ="loose selection"

import CMS_lumi
from Style import *
thestyle = Style()

HasCMSStyle = False
style = None
if os.path.isfile('tdrstyle.C'):
    ROOT.gROOT.ProcessLine('.L tdrstyle.C')
    ROOT.setTDRStyle()
    print "Found tdrstyle.C file, using this style."
    HasCMSStyle = True
    if os.path.isfile('CMSTopStyle.cc'):
        gROOT.ProcessLine('.L CMSTopStyle.cc+')
        style = CMSTopStyle()
        style.setupICHEPv1()
        print "Found CMSTopStyle.cc file, use TOP style if requested in xml file."
if not HasCMSStyle:
    print "Using default style defined in cuy package."
    thestyle.SetStyle()

ROOT.gROOT.ForceStyle()

stackList = { "TTbar_Semi_1":[kRed], "DY":[kGreen], "QCD":[kYellow],"WJets":[kBlue], "ST":[kOrange], "Diboson":[kTeal]}

print(stackList)

CMS_lumi.channelText = channelText
CMS_lumi.writeChannelText = True
CMS_lumi.writeExtraText = True



H = 600
W = 800

T = 0.08*H
B = 0.12*H
L = 0.12*W
R = 0.1*W

legendHeightPer = 0.04
legList = stackList.keys()

legendStart = 0.69
legendEnd = 0.97-(R/W)
legend = TLegend(2*legendStart - legendEnd , 0.99 - (T/H)/(1.-padRatio+padOverlap) - legendHeightPer/(1.-padRatio+padOverlap)*round((len(legList)+1)/2.), legendEnd, 0.99-(T/H)/(1.-padRatio+padOverlap))
legend.SetNColumns(2)

canvas = TCanvas('c1','c1',W,H)
canvas.SetFillColor(0)
canvas.SetBorderMode(0)
canvas.SetFrameFillStyle(0)
canvas.SetFrameBorderMode(0)
canvas.SetLeftMargin( L/W )
canvas.SetRightMargin( R/W )
canvas.SetTopMargin( T/H )
canvas.SetBottomMargin( B/H )
canvas.SetTickx(0)

canvasRatio = TCanvas('c1Ratio','c1Ratio',W,H)
canvasRatio.SetFillColor(0)
canvasRatio.SetBorderMode(0)
canvasRatio.SetFrameFillStyle(0)
canvasRatio.SetFrameBorderMode(0)
canvasRatio.SetLeftMargin( L/W )
canvasRatio.SetRightMargin( R/W )
canvasRatio.SetTopMargin( T/H )
canvasRatio.SetBottomMargin( B/H )
canvasRatio.SetTickx(0)
canvasRatio.SetTicky(0)
canvasRatio.Draw()
canvasRatio.cd()

pad1 = TPad("zxc_p1","zxc_p1",0,padRatio-padOverlap,1,1)
pad2 = TPad("qwe_p2","qwe_p2",0,0,1,padRatio+padOverlap)
pad1.SetLeftMargin( L/W )
pad1.SetRightMargin( R/W )
pad1.SetTopMargin( T/H/(1-padRatio+padOverlap) )
pad1.SetBottomMargin( (padOverlap+padGap)/(1-padRatio+padOverlap) )
pad2.SetLeftMargin( L/W )
pad2.SetRightMargin( R/W )
pad2.SetTopMargin( (padOverlap)/(padRatio+padOverlap) )
pad2.SetBottomMargin( B/H/(padRatio+padOverlap) )
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

histograms = {
              "st"    : ["S_{T} [GeV]",  "Events", 50, [0,5000]],
              "rec_chi" : ["Chi_2", "Events", 20, [0,300]]
              
		}
for histName in histograms:
    
	for sample in sample_names:
 		
        print sample, histName
	    file[sample] = TFile("%s/uhh2.AnalysisModuleRunner.MC.%s.root"%(fileDir,sample),"read")
        print ".root"%(fileDir,sample)
		tree_MC[histName][sample]=file[sample].Get("AnalysisTree")
        print histName, sample, histograms[histName][2], histograms[histName][3][0], histograms[histName][3][1]
        tree_MC[histName][sample].Draw("%s>>h_%s_%s(%i,%f,%f)"%(histName,histName,sample,histograms[histName][2],histograms[histName][3][0],histograms[histName][3][1]),"weight*weight_pu")
        hist[histName][sample] = tree_MC[histName][sample].GetHistogram()

        hist[histName][sample].SetFillColor(stackList[sample][0])
        hist[histName][sample].SetLineColor(stackList[sample][0])
                	    
		   
	file["Data"] = TFile("%s/uhh2.AnalysisModuleRunner.DATA.DATA.root"%(fileDir),"read")
	print "%s/uhh2.AnalysisModuleRunner.DATA.DATA.root"%(fileDir)

	tree = file["Data"].Get("AnalysisTree")
	tree.Draw("%s>>dat_hist(%i,%f,%f)"%(histName,histograms[histName][2],histograms[histName][3][0],histograms[histName][3][1]))
	dataHist=tree.GetHistogram()
	dataHist.SetMarkerColor(kBlack)
	dataHist.SetYTitle(histograms[histName][1])     
	stack[histName].Draw("HIST")
	dataHist.Draw("pe,x0,same")    

	oneLine = TF1("oneline","1",-9e9,9e9)
	oneLine.SetLineColor(kBlack)
	oneLine.SetLineWidth(1)
	oneLine.SetLineStyle(2)
	

	maxVal = stack[histName].GetMaximum()

	minVal = 1
	minVal = max(stack[histName].GetStack()[0].GetMinimum(),1)
    if Log:
		#stack[histName].SetMaximum(10**(1.5*log10(maxVal) - 0.5*log10(minVal)))
                stack[histName].SetMaximum(15**(1.5*log10(maxVal) - 0.5*log10(minVal)))

	else:
        	stack.SetMaximum(1.7*maxVal)
	stack[histName].SetMinimum(minVal)

	errorband=stack[histName].GetStack().Last().Clone("error")
	errorband.Sumw2()
	errorband.SetLineColor(kBlack)
	errorband.SetFillColor(kBlack)
	errorband.SetFillStyle(3245)
	errorband.SetMarkerSize(0)

	canvasRatio.cd()
	canvasRatio.ResetDrawn()
	canvasRatio.Draw()
	canvasRatio.cd()

	pad1.Draw()
	pad2.Draw()

	pad1.cd()
	pad1.SetLogy(Log)


	y2 = pad1.GetY2()

	stack[histName].Draw("HIST")

	stack[histName].GetXaxis().SetTitle('')
	stack[histName].GetYaxis().SetTitle(dataHist.GetYaxis().GetTitle())

	stack[histName].SetTitle('')
	stack[histName].GetXaxis().SetLabelSize(0)
	stack[histName].GetYaxis().SetLabelSize(gStyle.GetLabelSize()/(1.-padRatio+padOverlap))
	stack[histName].GetYaxis().SetTitleSize(gStyle.GetTitleSize()/(1.-padRatio+padOverlap))
	stack[histName].GetYaxis().SetTitleOffset(gStyle.GetTitleYOffset()*(1.-padRatio+padOverlap))
	stack[histName].GetYaxis().SetTitle("Events")

	dataHist.Draw("E,X0,SAME")

	legendR[histName].AddEntry(dataHist, "Data", 'pe')

	ratio = dataHist.Clone("temp")
	temp = stack[histName].GetStack().Last().Clone("temp")

	for i_bin in range(1,temp.GetNbinsX()+1):
       		temp.SetBinError(i_bin,0.)
	ratio.Divide(temp)

	print ratio.GetMaximum(), ratio.GetMinimum()

	ratio.SetTitle('')


	ratio.GetXaxis().SetLabelSize(gStyle.GetLabelSize()/(padRatio+padOverlap))
	ratio.GetYaxis().SetLabelSize(gStyle.GetLabelSize()/(padRatio+padOverlap))
	ratio.GetXaxis().SetTitleSize(gStyle.GetTitleSize()/(padRatio+padOverlap))
	ratio.GetYaxis().SetTitleSize(gStyle.GetTitleSize()/(padRatio+padOverlap))
	ratio.GetYaxis().SetTitleOffset(gStyle.GetTitleYOffset()*(padRatio+padOverlap-padGap))


	ratio.GetYaxis().SetRangeUser(0.35,1.65)
	ratio.GetYaxis().SetNdivisions(504)
	ratio.GetXaxis().SetTitle(histograms[histName][0])
	ratio.GetYaxis().SetTitle("Data/MC")
	CMS_lumi.CMS_lumi(pad1, 4, 11)
	legendR[histName].Draw()
	pad2.cd()
	ratio.SetMarkerStyle(dataHist.GetMarkerStyle())
	ratio.SetMarkerSize(dataHist.GetMarkerSize())
	ratio.SetLineColor(dataHist.GetLineColor())
	ratio.SetLineWidth(dataHist.GetLineWidth())
	ratio.Draw('e,x0')
	errorband.Divide(temp)
	errorband.Draw('e2,same')
	oneLine.Draw("same")
	
	#    pad2.Update()
	canvasRatio.Update()
	canvasRatio.RedrawAxis()
	if Log:
		canvasRatio.SaveAs("%s/%s_log.pdf"%(plotDirectory,histName))
	else:
		canvasRatio.SaveAs("%s/%s.pdf"%(plotDirectory,histName))



