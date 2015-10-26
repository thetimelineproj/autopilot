import wx

app = wx.App()
po = wx.Printout(title="Printout")
pp = wx.PrintPreview(po, po)
fr = wx.PreviewFrame(pp, None, "")

def window_on_close(evt):
    fr.Destroy()    
    
if __name__ == "__main__":
    fr.Initialize()
    fr.Bind(wx.EVT_CLOSE, window_on_close)
    fr.Show(True)
    app.MainLoop()
    