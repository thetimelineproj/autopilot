import wx

if __name__ == "__main__":
    app = wx.App()
    dialog = wx.ColourDialog(None)
    dialog.ShowModal()
    dialog.Destroy()