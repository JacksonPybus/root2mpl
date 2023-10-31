import ROOT
import numpy as np
import matplotlib.pyplot as plt

ROOT.gROOT.SetBatch(True)
nObj = 0

class File:
    def __init__(self,infile):
        if (isinstance(infile,ROOT.TFile)):
            self.TFile = infile
        else:
            self.TFile = ROOT.TFile(infile)

    def setDirectory(self,dirName):
        self.dir="." + dirName
        
    def get(self,name,**kwargs):
        if (not eval("self.TFile"+self.dir+".GetListOfKeys()").Contains(name)):
            raise ValueError("File does not contain specified object")
        h = eval("self.TFile"+self.dir+".Get(name)")
        if (isinstance(h,ROOT.TH2)):
            return Hist2D(h,**kwargs)
        elif (isinstance(h,ROOT.TH1)):
            return Hist1D(h,**kwargs)
        elif (isinstance(h,ROOT.TDirectory)):
              return Directory(h,**kwargs)
        else:
            raise ValueError("Object is not a supported type")
        
    def getNames(self):
        return [i.GetName() for i in eval("self.TFile"+self.dir+".GetListOfKeys()")]
    
    def getNames(self):
        return [i.GetName() for i in self.TFile.GetListOfKeys()]

    def plotPoints(self,name,rebin=1,scale=1,**kwargs):
        h = self.get(name,rebin=rebin,scale=scale)
        if (isinstance(h,Hist1D)):
            return h.plotPoints(**kwargs)
        else:
            raise ValueError("This is not a 1D histogram and cannot be plotted with this method")
        
    def plotBand(self,name,rebin=1,scale=1,**kwargs):
        h = self.get(name,rebin=rebin,scale=scale)
        if (isinstance(h,Hist1D)):
            return h.plotBand(**kwargs)
        else:
            raise ValueError("This is not a 1D histogram and cannot be plotted with this method")
        
    def plotBar(self,name,rebin=1,scale=1,**kwargs):
        h = self.get(name,rebin=rebin,scale=scale)
        if (isinstance(h,Hist1D)):
            return h.plotBar(**kwargs)
        else:
            raise ValueError("This is not a 1D histogram and cannot be plotted with this method")
        
    def plotHeatmap(self,name,rebinx=1,rebiny=1,**kwargs):
        h = self.get(name,rebinx=rebinx,rebiny=rebiny)
        if (isinstance(h,Hist2D)):
            return h.plotHeatmap(**kwargs)
        else:
            raise ValueError("This is not a 2D histogram and cannot be plotted with this method")

class Directory:
    def __init__(self,directory):
        if (isinstance(directory,ROOT.TDirectory)):
            self.TDirectory = directory
        else:
            self.TDirectory = ROOT.TDirectory(directory)
       
    def get(self,name,**kwargs):
        if (not self.TDirectory.GetListOfKeys().Contains(name)):
            raise ValueError("Directory does not contain specified object")
        h = self.TDirectory.Get(name)
        if (isinstance(h,ROOT.TH2)):
            return Hist2D(h,**kwargs)
        elif (isinstance(h,ROOT.TH1)):
            return Hist1D(h,**kwargs)
        elif (isinstance(h,ROOT.TDirectory)):
              return Directory(h,**kwargs)
        else:
            raise ValueError("Object is not a supported type")

    def getNames(self):
        return [i.GetName() for i in self.TDirectory.GetListOfKeys()]

    def plotPoints(self,name,rebin=1,scale=1,**kwargs):
        h = self.get(name,rebin=rebin,scale=scale)
        if (isinstance(h,Hist1D)):
            return h.plotPoints(**kwargs)
        else:
            raise ValueError("This is not a 1D histogram and cannot be plotted with this method")
        
    def plotBand(self,name,rebin=1,scale=1,**kwargs):
        h = self.get(name,rebin=rebin,scale=scale)
        if (isinstance(h,Hist1D)):
            return h.plotBand(**kwargs)
        else:
            raise ValueError("This is not a 1D histogram and cannot be plotted with this method")
        
    def plotBar(self,name,rebin=1,scale=1,**kwargs):
        h = self.get(name,rebin=rebin,scale=scale)
        if (isinstance(h,Hist1D)):
            return h.plotBar(**kwargs)
        else:
            raise ValueError("This is not a 1D histogram and cannot be plotted with this method")
        
    def plotHeatmap(self,name,rebinx=1,rebiny=1,**kwargs):
        h = self.get(name,rebinx=rebinx,rebiny=rebiny)
        if (isinstance(h,Hist2D)):
            return h.plotHeatmap(**kwargs)
        else:
            raise ValueError("This is not a 2D histogram and cannot be plotted with this method")
 
        
class Hist1D:
    def __init__(self,hist,rebin=None,scale=1):
        global nObj
        self.TH1 = hist.Clone(str(nObj))
        nObj = nObj + 1
        
        if (not (rebin is None)):
            self.TH1.Rebin(rebin)
            
        g = ROOT.TGraphAsymmErrors(self.TH1)
        self.x = np.array(g.GetX())
        self.y = np.array(g.GetY())*scale
        xerr = []
        yerr = []
        for i in range(g.GetN()):
            xerr.append(g.GetErrorX(i))
            yerr.append(g.GetErrorY(i))
        self.xerr = np.array(xerr)
        self.yerr = np.array(yerr)*scale

    def scale(self,factor):
        self.y *= factor
        self.yerr *= factor

    def rebin(self,factor):
        if (factor.all() != 1):
            self.TH1.Rebin(factor)
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
    
    def norm(self,):
        factor = 1/np.sum(self.y)
        self.scale(factor)
        return factor
        
    def plotPoints(self,xscale=1,**kwargs):
        return plt.errorbar(xscale*self.x,self.y,yerr=self.yerr,**kwargs)

    def plotBand(self,xscale=1,alpha=0.25,**kwargs):
        line = plt.plot(xscale*self.x,self.y,**kwargs)[0]
        band = plt.fill_between(xscale*self.x,self.y-self.yerr,self.y+self.yerr,
                                color=line.get_color(),zorder=line.zorder,
                                alpha=alpha)
        return line, band

    def plotBar(self,shift=0,wfactor=1,**kwargs):
        bar = plt.bar(self.x+shift, self.y, width = self.xerr*2*wfactor, **kwargs)
        
        return bar

class Hist2D:
    def __init__(self,hist,rebinx=1,rebiny=1):
        global nObj
        self.TH2 = hist.Clone(str(nObj))
        nObj = nObj + 1
        
        if (rebinx != 1):
            self.TH2.RebinX(rebinx)
        if (rebiny != 1):
            self.TH2.RebinY(rebiny)

        NX = self.TH2.GetNbinsX()
        NY = self.TH2.GetNbinsY()
    
        xedge = []
        yedge = []
        z = []
        zerr = []
        
        for j in range(NX):
            xedge.append(self.TH2.GetXaxis().GetBinLowEdge(j+1))
        xedge.append(self.TH2.GetXaxis().GetBinUpEdge(NX))
    
        for i in range(NY):
            yedge.append(self.TH2.GetYaxis().GetBinLowEdge(i+1))
            zcol = []
            zerrcol = []
            for j in range(NX):
                zval = self.TH2.GetBinContent(j+1,i+1)
                zcol.append(zval)
                zerrcol.append(self.TH2.GetBinError(j+1,i+1))
            z.append(zcol)
            zerr.append(zerrcol)
        yedge.append(self.TH2.GetYaxis().GetBinUpEdge(NY))
            
        self.xedge = np.array(xedge)
        self.yedge = np.array(yedge)
        self.z = np.array(z)
        self.zerr = np.array(zerr)
    
    def plotHeatmap(self,kill_zeros=True,transpose=False,xscale=1,yscale=1,**kwargs):
        xedge = self.xedge
        yedge = self.yedge
        z = self.z
        if (kill_zeros):
            z[z==0] = np.nan
        if (transpose):
            xedge, yedge = self.yedge, self.xedge
            z = np.transpose(self.z)
        
        return plt.pcolormesh(xedge*xscale,yedge*yscale,z,**kwargs)

    def projectionX(self,firstbin=0,lastbin=-1,**kwargs):
        return Hist1D(self.TH2.ProjectionX("_px",firstbin,lastbin),**kwargs)

    def projectionY(self,firstbin=0,lastbin=-1,**kwargs):
        return Hist1D(self.TH2.ProjectionY("_py",firstbin,lastbin),**kwargs)
