# eldata-ubuntu-indicator

A small application that query Swedish power cost and display in notification bar on Ubuntu


## Install gir1.2-appindicator3* [Gtk3 port of appindicator]:

```bash
$ sudo apt-get install gir1.2-appindicator3* [Look for what package is available in repo. In 12.04 its gir1.2-appindicator3-0.1]
```

**ALTHOUGH NOT RECOMMENDED**

You can use gtk2 as well

```bash
$ sudo apt-get install gir1.2-appindicator
```

## HOW-TO USE

Must be run on system level python due to gir1.2 application dependency that is not possible to install within a virtualenvrionment.

Run code with `python3 main.py`. Should work on most modern versions of python


### Autostart indicator at Startup

_`gnome-session-properties`_ package should be installed

Go to session menu and click on startup applications

A new window appears. Follow the below process:

- Click 'Add'
- Enter following Information
    - Name: Eldata ubuntu indicator
    - Command: PATH/TO/eldata-ubuntu-indicator/main.py
    - Click Add
    - Then Click Close
