import wx

if __name__ == "__main__":
    app = wx.App()
    dialog = wx.FontDialog(None, wx.FontData())
    dialog.ShowModal()
    dialog.Destroy()