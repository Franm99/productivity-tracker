# Productivity Tracker

![Sample graph](src/sample.png "Sample Graph")

Short script to execute while you're on your daily work routine to keep track
of your productivity based on the time you spent on different actions.

Sample actions given are: PROJECT, COURSE, HOUSE, REST

## Structure

The module **habit_tracker** implements the 
[MVC (Model-View-Controller) Design Pattern](https://www.geeksforgeeks.org/mvc-design-pattern/) 
to separate the data model, the business logic and the presentation to the user.


![Structure diagram](src/mvc.svg "Structure Diagram")

Some of the main benefits from this architecture are :
* Improves **maintainability** while reducing **dependencies**.
* Gives the **capability to change the view, or UI**, making it easier to test.


## How to run from startup (Windows 10)

1. Create shortcut to `productivity_tracker.bat`.
2. Run Windows + R and run `shell:startup` to open startup folder.
3. Move the shortcut to that folder.

This way, each time your computer turns on, the script will be run and the productivity tracker
will start to work for your new journey.
