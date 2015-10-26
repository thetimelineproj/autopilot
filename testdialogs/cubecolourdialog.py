import time
import wx
import wx.lib.agw.cubecolourdialog as CCD


if __name__ == "__main__":
    app = wx.App()
    try:
        dialog = wx.lib.agw.cubecolourdialog.CubeColourDialog(None)
    except Exception, ex:
        f = open(r"c:\temp\log.txt", "w")
        f.write("%s" % ex)
        f.close
    dialog.ShowModal()
    dialog.Destroy()