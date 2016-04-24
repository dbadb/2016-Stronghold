Introduction
============

During the Stronghold/2016 season, Spartronics programmers grappled with
a number of programming challenges.  A few programmers expressed minor
frustration with our use of Java as the principal programming language.
Other programmers were quite happy and comfortable with the programming
experience.  As a newcomer to FRC Robot programming, I can certainly state
that I was frustrated by the environment on a few counts:

1. the WPI Java documentation was often inadequate and sometimes misleading.
I found myself resolving answers to questions by inspecting the source code
directly.  Unfortunately, the Java source bridges to the WPI C++ Libraries and
this meant I needed to spelunk through both C++ and Java source code to get to
the bottom of some questions.
2. the Eclipse environment is quite powerful but also quite unwieldy. 
Installation requires at least a full 2-hour session with students and its 
memory consumption seems quite steep (> 4GB) for the role it plays on our team.
Eclipse offers all sorts of coding conveniences, but I found myself wondering 
if these conveniences make it too easy for students to avoid thinking about 
their software design choices.  The build machinery was entirely hidden from 
all but one student.
3. Java itself can be quite esoteric and only differs from C++ in its 
elimination of the concept of a pointer.  Most of our programmers don't 
understand class inheritance, variable scoping rules and intent behind 
public and private keywords. The static keyword became a virus in our 
codebase. The Java namespacing of modules means that source code is 
distributed across the filesystem and this makes it harder to navigate 
for information gathering.

Since we had selected the python/opencv/jetson environment for the vision 
subteam, I discovered the robotpy initiative in order to communicate with 
roborio. Their networktable implementation was very clean, very readable 
and very easy to use.  I also found their WPIlib docs and source to be much 
easier to navigate than the original WPI libraries. When I need to understand 
WPIlib design or functionality, I regularly start with the robotpy docs and 
python source code even though I'm looking for a Java solution.

As 2016 comes to a close, I felt compelled to evaluate the question of whether
it would be viable to adopt python as the primary environment for Spartronics
programming.  The only way to evaluate this completely was to get a 
fully-functional python codebase to serve as a point of comparison. This is 
what is represented here. As of the initial check-in, this codebase represents 
all the significant functionality of the student-developed robot code.  I took 
a few liberties in cleaning up some of the interfaces and also eliminated the 
module-manager.

RobotPy offers some testing and simulation capabilities out-of-the-box
and these helped me to ensure that the code mostly works.  I haven't had
access to a real robot yet and the next evaluation step would require that
the roborio-side of the robotpy environment be evaluated.

It's apparent to me, after arriving at this first milestone, that adopting
python for our programming environment is indeed a viable strategy.  If it were
only up to me, I'd probably go for it on the grounds that it will be easier to
teach and bring our students much closer to the things that matter in robotpy
programming.  For example, access to the implementation of the WPILib
command-scheduler is a button-click away and reveals this code:

		self.runningCommandsChanged = False

		if self.disabled:
				return # Don't run when disabled

		# Get button input (going backwards preserves button priority)
		for button in reversed(self.buttons):
				button()

		# Loop through the commands
		for command in list(self.commandTable):
				if not command.run():
						self.remove(command)
						self.runningCommandsChanged = True

		# Add the new things
		for command in self.additions:
				self._add(command)
		self.additions.clear()

		# Add in the defaults
		for lock in self.subsystems:
				if lock.getCurrentCommand() is None:
						self._add(lock.getDefaultCommand())
				lock.confirmCommand()

		self.updateTable()

Simple, right? The code sure seems easy to read and to understand, but that
doesn't make this decision a no-brainer.

Steps to a Decision
===================

I've gotten us close to proving that python is a viable choice, but that
doesn't mean that it's the right choice for Spartronics in the 2017 season.
This is where you, dear readers, enter the fray.  

Please evaluate the code presented herein.  

Please evaluate the robotpy environment for yourself.

Please also consider the pros and cons (below, plus new ones you add).

You may find that the amount of fundamental complexity in both python and 
Java implementations is quite similar. Does python really deliver on its 
promised simplicity for this application?  

You might argue that the interpreted nature of python will make it harder
for us to verify our implementation stability.  RobotPy acknowledge this
point and suggests that there is no substitute for a good regression testing
regime.  This is new territory for us, but one we need to investigate no matter
which language we choose.  

Finally, you might also argue that with only a handful of teams using
robotpy (< 20 in 2016 (?)) that the FUD principal suggests we steer clear.  

So the question is, where do you stand?

Thank you,
Dana Batali, Spartronics 4915 Mentor, April 2016-Stronghold


Threads
=======

https://www.reddit.com/r/FRC/comments/41vwo3/help_me_convince_our_programmer_not_to_use_python/

https://robotpy.github.io/faq/

https://robotpy.github.io/community/  (13 teams used it during 2016)


The Pros and Cons
=================

Java
----
	Pro:
		Language:
			BHS Coursework exists
			Widely used by FRC and Spartronics (if it ain't broke…)
				Lots of example code available, though quality is variable.
		Libraries:
		Environment:
            Eclipse is powerful and offers lots of java-tuned facilities
              to improve code quality.

	Con:
		Language:
			Lots of subtleties:
				Static caused lots of problems
                Private vs public
                Implements vs Extends
                Threading model is obscured
			Code factoring can be awkward (one file per class)
			On the decline?
		Environment:
			Eclipse is bloated and tedious to install
			WPI Libs are poorly documented, hard to install
			Build system is mysterious to most (ant is part of Eclipse)
            Java environment is a separate install on roborio

Python/RobotPy
--------------
	Pro:
		Language:
			- Easy to learn (interactive, raspberry pi, …)
			- Can be used on desktop, robot and vision coprocessor
		Libraries:
			- WPILib Supported by RobotPy
			- Better documentation
			- Source is much easier to read
			- Integrated Testing
			- Easy Simulation on Desktop
		Environment:
			- Easier To Install, Portable
			- Support in a variety of environments: Eclipse, Atom, etc..
			- No build system needed
	Con:
		Higher posibility of runtime bugs?
		Fewer FRC Teams
			- Means less example code & shareware
		Still has bridge to roborio runtime
		Little experience on Spartronics and BHS
			• Mentors
			• coursework
		Theoretically Lower Performance
			- Interpretter overhead
			- Threading model isn't ideal

C++
---
	Pro:
		Language not going away
		WPI Libs are C++ at bottom
		Better Source & docs than java
		Highest Theoretical Performance
		Static typing and compilation - means fewer runtime errors
	Con:
		Hardest of 3 languages
		Heavier installation of dependency burden than python

Installation Details
====================

* Install python 3.5
* python -m pip install robotpy and pyfrc (see robotpy docs)
* I used the atom editor with python IDE extensions:
	* autocomplete-python
* Install python & pyfrc on roborio  
