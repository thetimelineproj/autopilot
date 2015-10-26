import wx

if __name__ == "__main__":
    app = wx.App()
    dialog = wx.PasswordEntryDialog(None, "Message")
    dialog.ShowModal()
    dialog.Destroy()