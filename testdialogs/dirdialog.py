import wx

if __name__ == "__main__":
    app = wx.App()
    dialog = wx.DirDialog(None)
    dialog.ShowModal()
    dialog.Destroy()