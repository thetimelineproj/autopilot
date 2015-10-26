import wx


if __name__ == "__main__":
    app = wx.App()
    dialog = wx.TextEntryDialog(None, "Message")
    dialog.ShowModal()
    dialog.Destroy()