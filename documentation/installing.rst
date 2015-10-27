Installation instructions
=========================

Autopilot runs on multiple platforms. If you can run `Python
<http://www.python.org/>`_ and `wxPython <http://www.wxpython.org/>`_ you
should be able to run Autopilot. However, Autopilot is only tested on Windows and
Linux.

Installing from source
----------------------

.. image:: /images/logo-source.png
    :align: right

Get the source code here: |latest_zip|_.
(:sfl:`Other downloads <files/thetimelineproj>`.)

When you install from source, you have to install all required dependencies
yourself. Autopilot requires:

* Python version 2.7 or greater (http://www.python.org)
* wxPython version 2.8.9.2 or greater (http://www.wxpython.org)

On Windows you also need:
* PyWin32 (http://sourceforge.net/projects/pywin32/files/pywin32/)

On Linux systems, you can often install these via the package manager.

Once you have extracted the Autopilot zip and installed the required
dependencies, you should be able to run the application with this command::

    python <path-to-autopilot-directory>/src/run.py

Preferable you create a shortcut on your platform that issues the command.
