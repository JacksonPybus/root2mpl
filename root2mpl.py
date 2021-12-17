import ROOT
import numpy as np
import matplotlib.pyplot as plt

class File:
    def __init__(self,infile):
        if (isinstance(infile,ROOT.TFile)):
            self.TFile = infile
        else:
            self.TFile = ROOT.TFile(infile)

    def get(self,name):
        if (not self.TFile.GetListOfKeys().Contains(name)):
            raise ValueError("File does not contain specified object")
        h = self.TFile.Get(name)
        if (isinstance(h,ROOT.TH2)):
            return Hist2D(h)
        elif (isinstance(h,ROOT.TH1)):
            return Hist1D(h)
        else:
            raise ValueError("Object is not a supported type")

class Hist1D:
    def __init__(self,hist):
        self.TH1 = hist
        g = ROOT.TGraphAsymmErrors(self.TH1)
        self.x = np.array(g.GetX())
        self.y = np.array(g.GetY())
        xerr = []
        yerr = []
        for i in range(g.GetN()):
            xerr.append(g.GetErrorX(i))
            yerr.append(g.GetErrorY(i))
        self.xerr = np.array(xerr)
        self.yerr = np.array(yerr)

    def scale(self,factor):
        self.y *= factor
        self.yerr *= factor

    def rebin(self,factor):
        self.TH1 = self.TH1.Rebin(factor)
        g = ROOT.TGraphAsymmErrors(self.TH1)
        self.x = np.array(g.GetX())
        self.y = np.array(g.GetY())
        xerr = []
        yerr = []
        for i in range(g.GetN()):
            xerr.append(g.GetErrorX(i))
            yerr.append(g.GetErrorY(i))
        self.xerr = np.array(xerr)
        self.yerr = np.array(yerr)

    def areaNorm(self,reference):
        factor = np.sum(reference.y)/np.sum(self.y)
        self.scale(factor)
        return factor
        
    def plotPoints(self,**kwargs):
        return plt.errorbar(self.x,self.y,yerr=self.yerr,**kwargs)

    def plotBand(self,alpha=0.25,**kwargs):
        line = plt.plot(self.x,self.y,**kwargs)[0]
        band = plt.fill_between(self.x,self.y-self.yerr,self.y+self.yerr,
                                color=line.get_color(),zorder=line.zorder,
                                alpha=alpha)
        return line, band

class Hist2D:
    def __init__(self,hist):
        self.TH2 = hist

        NX = hist.GetNbinsX()
        NY = hist.GetNbinsY()
        
        left = hist.GetXaxis().GetBinLowEdge(1)
        right = hist.GetXaxis().GetBinUpEdge(NX)
        bottom = hist.GetYaxis().GetBinLowEdge(1)
        top = hist.GetYaxis().GetBinUpEdge(NY)
        self.extent = (left, right, bottom, top)
        
        x = []
        y = []
        z = []
        xerr = []
        yerr = []
        zerr = []
        
        for j in range(NX):
            x.append(hist.GetXaxis().GetBinCenter(j+1))
            xerr.append(hist.GetXaxis().GetBinWidth(j+1)/2.)
    
        for i in range(NY):
            y.append(hist.GetYaxis().GetBinCenter(i+1))
            yerr.append(hist.GetYaxis().GetBinWidth(i+1)/2.)
            zcol = []
            zerrcol = []
            for j in range(NX):
                zval = hist.GetBinContent(j+1,i+1)
                zcol.append(zval)
                zerrcol.append(hist.GetBinError(j+1,i+1))
            z.append(zcol)
            zerr.append(zerrcol)

        self.x = np.array(x)
        self.y = np.array(y)
        self.z = np.array(z)
        self.xerr = np.array(xerr)
        self.yerr = np.array(yerr)
        self.zerr = np.array(zerr)
        
    def plotHeatmap(self,kill_zeros=True,**kwargs):
        z = self.z
        if (kill_zeros):
            z = np.ma.masked_where(z == 0, z)
        return plt.imshow(z,extent=self.extent,**kwargs)
