Your Game Title
===============

Entry in PyWeek #14  <http://www.pyweek.org/14/>
URL: http://pyweek.org/e/bot_uprise
Team: Willyfrog
Members: Willyfrog
License: BSD (see LICENSE.txt)


Running the Game
----------------

On Windows or Mac OS X, locate the "run_game.pyw" file and double-click it.

Othewise open a terminal / console and "cd" to the game directory and run:

  python run_game.py


How to Play the Game
--------------------

A rogue AI has taken over anything resembling a weapon to exterminate
anyone who tries to switch it off.

use wasd/cursors to move ship, and qe/zx to rotate


Development notes 
-----------------

Creating a source distribution with::

   python setup.py sdist

You may also generate Windows executables and OS X applications::

   python setup.py py2exe
   python setup.py py2app

Upload files to PyWeek with::

   python pyweek_upload.py

Upload to the Python Package Index with::

   python setup.py register
   python setup.py sdist upload

