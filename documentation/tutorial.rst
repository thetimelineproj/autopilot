Tutorial
========

This tutorial demonstrates basic usage of ``autopilot`` by showing and
explaining a few examples.

FooBar
------

First we need an application to test.
Our first example is an application that has a dialog that displays a 
static text, a textbox and a button. When the application is run, it 
looks something like this:

.. image:: /images/FooBar.png

In order to run this application with autopilot you have to issue the
following command:

.. literalinclude:: /examples/foobar.cmd

When this command file is executed it starts the application under test
and runs the commands descibed in the foobar.txt manuscript file.
In this first example the manuscript file looks like this:

.. literalinclude:: /examples/foobar_manuscript.txt

So autopilot starts the application under test, clicks the OK button
and thereafter closes the application.
A logfile, autopilot.log is created in the manuscript directory.
After this first example execution the logfile contains the following information

.. literalinclude:: /examples/autopilot.log


Here we import the ``hubmlewx`` module that is used to access its
functionality. The ``wx`` import is only needed in the example program to
create the ``App`` object so that we can display our dialog.

.. literalinclude:: ../examples/hello_world.py
    :language: python
    :lines: 5

Here we say that we want to create a dialog. The ``humblewx.Dialog`` is
actually a subclass of ``wx.Dialog``. This subclass adds the functionality to
create the GUI from a description in XML.

.. literalinclude:: ../examples/hello_world.py
    :language: python
    :lines: 7-9

This is the description of the GUI. It is written in the dosctring of the
class. It is written in XML and describes what components should be in our
dialog. In this case we have only one component.

.. literalinclude:: ../examples/hello_world.py
    :language: python
    :lines: 10-12

Here we create the dialog. The :py:meth:`~humblewx.Dialog.__init__` method will
read the GUI description and construct the components. The first argument,
``HelloWorldDialogController`` is a class that will be instantiated and used as
a controller for this dialog. We'll come back to what the controller does. For
now we just need to know that it must be a subclass of
:py:meth:`humblewx.Controller`.

.. literalinclude:: ../examples/hello_world.py
    :language: python
    :lines: 15-16

Here we define our controller. At the moment it doesn't do anything.

.. literalinclude:: ../examples/hello_world.py
    :language: python
    :lines: 18-

This code displays our dialog when we run the Python file.

Greeting
--------

Our second example is a greeting dialog that allows us to enter our name, and
when we press a button a greeting will be shown. It looks something like this:

.. image:: /images/greeting.png

Here is the dialog class:

.. literalinclude:: ../examples/greeting.py
    :language: python
    :pyobject: GreetingDialog

Here is the controller class:

.. literalinclude:: ../examples/greeting.py
    :language: python
    :pyobject: GreetingDialogController

We can see that the GUI description has been extended from the previous
example. We have more components and we use sizers to control how they are laid
out.

The second interesting addition in this example is that we have communication
between the dialog and the controller. They collaborate in a pattern inspired
by the `Humbe Dialog Box
<http://www.objectmentor.com/resources/articles/TheHumbleDialogBox.pdf>`_.  The
dialog corresponds to the view and the controller corresponds to the smart
object.

The controller receives events from the view (such as a button click) and
responds to them by calling methods on the view.

The way to connect events to the controller is via ``event_`` attributes in the
XML. When ``humblewx`` sees ``event_EVT_BUTTON="on_greet_clicked"``, it will
automatically bind the ``EVT_BUTTON`` event to the ``on_greet_clicked`` method
on the controller.

What happens when we click the greet button?

* ``on_greet_clicked`` is called.

* It calls ``GetName`` on the view.

* ``GetName`` in turn gets the name from the text control. The view can access
  the text control by the name ``name_text_ctrl`` because we specified the name
  attribute in the XML.

* ``on_greet_clicked`` then calls ``SetGreeting`` on the view with the
  greeting string constructed from the name.

* ``SetGreeting`` sets the label on the static text similarly to how
  ``GetName`` got the text from the text control.

Summary
-------

In our experience it's very pleasant to be able to describe how the GUI should
look like in XML instead of manually calling ``wx`` APIs. We feel that we can
more rapidly create new dialogs that also look better. Changing existing ones
is also more pleasant.

The separation between the view and the control makes the code even cleaner and
the controller can be tested in isolation without ever invoking a GUI.

We encourage you to try this approach to creating user interfaces in wxPython.
Let us know what you think.