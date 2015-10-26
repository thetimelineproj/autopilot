import wx

if __name__ == "__main__":
    app = wx.App()
    dialog = wx.SingleChoiceDialog(None, "Message", "Title", ["foo", "bar"])
    dialog.ShowModal()
    dialog.Destroy()