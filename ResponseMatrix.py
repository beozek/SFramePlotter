# importing libraries

import ROOT, math, os, sys, re, random
import numpy as np
from subprocess import call
ROOT.gStyle.SetOptStat(0)


def makeResponseMatrix():
    global shapes
# TH1D (const char *name, const char *title, Int_t nbinsx, Double_t xlow, Double_t xup)   
hGen  = ROOT.TH1D("hgen","hgen",2, -2.5,2.5) #histograms with one double per channel. Maximum precision 14 digits.
hReco = ROOT.TH1D("hreco","hreco",2,-2.5,2.5)
# TH2D (const char *name, const char *title, Int_t nbinsx, Double_t xlow, Double_t xup, Int_t nbinsy, Double_t ylow, Double_t yup)
hResp = ROOT.TH2D("hresp","hresp",2,-2.5,2.5,2,-2.5,2.5)

# Fill hGen,hReco,hResp

hReco.Fill(x)