import time
import wx


if __name__ == "__main__":
    app = wx.App()
    msg = "Please wait while we process your request..."
    busyDlg = wx.BusyInfo(msg, None)
    time.sleep(2)
    busyDlg.destroy()