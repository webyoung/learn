
Skip to content

DEV Community
Create account

39
Jump to Comments
3
Save

Ngonidzashe Nzenze
Ngonidzashe Nzenze
Posted on Aug 14, 2021 • Updated on Jul 1, 2023


18

2

1

1

1
How to use Google Colab to package KivyMD applications with buildozer.
#
python
#
buildozer
#
android
#
kivymd
Let's face it, packaging your kivy application for android can be pretty rough. First you create the app, then you install buildozer only to realize that python-for-android doesn't even run on windows! Now you're looking into installing a virtual Linux distribution. If you already use Linux, well lucky you, but if not, you are probably pounding your keyboard in frustration.

Is there a better way to do it? The answer is yes. In this article I'm going to show you how to package an application for android using Google Colab.

First thing's first, let's code up our application. I assume you already have kivy and kivymd installed in a virtual environment.

Create two files:

main.py
main.kv
Inside main.py, add the following code:
from kivymd.app import MDApp
from kivymd.uix.list import OneLineIconListItem, IconLeftWidget

class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Purple"

    def add_item(self, text):
        new_list_item = OneLineIconListItem(text=text)
        new_list_item.add_widget(
            IconLeftWidget(icon = "language-python")
            )
        self.root.ids.listcontainer.add_widget(new_list_item)
        self.root.ids.listinput.text = ''


if __name__ == "__main__":
    app = MainApp()
    app.run()
Inside main.kv add the following lines:
MDBoxLayout:
    orientation: 'vertical'
    id: box
    MDTopAppBar:
        title: 'SampleApp'
        pos_hint: {'top': 1}

    MDTextField:
        id: listinput
        hint_text: 'Add Item'
        mode: 'rectangle'
        size_hint_x: .9
        pos_hint: {'center_x': .5} 
        text_validate_unfocus: False
        on_text_validate: app.add_item(listinput.text)

    ScrollView:
        MDList:
            id: listcontainer

This is a simple application that gets text from the user and creates a list item and adds it to the list.

When we run our application, it looks like this:

GIFSample App

Now for packaging!📦
Open google colab on your web browser and create a new notebook or you can use my notebook.

Now create a cell and run the following lines:
!sudo apt update
!sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
!pip3 install --user --upgrade Cython==0.29.33 virtualenv
Luckily for you, the developers of kivymd decided to make the process easier so we can install buildozer dependencies in one fell swoop. Create a cell in your notebook and add the following lines and execute:
# git clone, for working on buildozer
!git clone https://github.com/kivy/buildozer
%cd buildozer
!python setup.py build
!pip install -e .
%cd ..
And now, everything is ready for the packaging process.

Upload your files to colab by clicking on the files icon and then right clicking and clicking upload.(Uuuh what?😫)

After the files have been uploaded, run the following command:
!buildozer init
This will create a file named buildozer.spec. Double click the file to edit it. You can change the application name and the package name. I changed mine as follows:

Changing app configs

Next, scroll down to the requirements and change them as follows:
requirements = python3, kivy==2.1.0, kivymd==1.1.1, sdl2_ttf==2.0.15, pillow
Requirements sample

Note: If your application requires special permissions such as internet or storage, scroll down to android.permissions:
See permissions

Uncomment the android.permissions line and add the permissions. For a full list of all the available permissions, check out this link.

Now to package our application. Run the following command:
!buildozer -v android debug
This process can take up to 20 minutes so you might need a little bit of patience. In the mean time you could skip to the bonus section below or watch an episode of my hero academia(I won't judge😉).

After successful execution, the apk file is saved in the bin folder:

Saved in the bin

Download the apk, transfer it over to your android device and install it!

Download apk

The application works!👏

Full Code is available HERE.

Bonus section(Not really)
Debugging our application.
Packaging applications this way is faster than having to go through installing all the requirements on your PC but this does have a draw back. How do you debug the application? Imagine successfully installing the application and trying to run it only for it to crash. How do you know what the problem is? You can't run buildozer -v android deploy run logcat which displays the logs so that you can search through them to identify errors. You can't do that on colab but you can if you're on Linux(perhaps your should just switch to linux😁).

This is where adb comes in. Android Debug Bridge (adb) is a versatile command-line tool that lets you communicate with a device. You can get more information about it here but for now, we are going to be making use of adb platform tools. Download them here.

download adb

This will download a zipped file. Unzip it then copy the apk that we just made and paste it inside the unzipped folder. The selected item is the apk file in the image below:

Copy the apk

Connect your device, make sure usb debugging is enabled. Now open a command prompt terminal and navigate to the folder containing the adb files we extracted:

Alt Text

Run adb install name-of-the-app.apk

This will install the application on your device! You can open the application and try it out. To view the application log, run the following command in the terminal:

adb logcat

Now you can see the application log. If any error occurs while running the application, you'll probably find the details in the log, but be warned, it can be like looking for a needle in a haystack!

If you want to learn more about adb and it's commands check out this link.

And that just about wraps it up. I hope you found this article helpful. If you're facing any challenges don't hesitate to reach out in the comments section.

profile
Datadog
Promoted

Image of Datadog

Self-Maintaining Browser Tests for Easy Monitoring
Create tests in minutes, reduce maintenance, detect critical issues early, and monitor endpoints with API tests. Gain full-stack visibility to resolve issues faster and enhance user experience.

Download The Guide

Top comments (39)
Subscribe
pic
Add to the discussion
 
 
rhandel profile image
RAH
•
Apr 29 '23 • Edited

NN,
Completed the build but had to change the version of Cython from 0.29.19 to 0.29.21 to complete compile.
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
tables 3.8.0 requires cython>=0.29.21, but you have cython 0.29.19 which is incompatible.

!pip install --upgrade Cython==0.29.21 virtualenv

I suspect that's why the resulting APK builds but bombs after the splash screen.
Do you have any suggestions?

RAHRAH
!sudo apt update
!sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
!pip install --upgrade Cython==0.29.21 virtualenv
!git clone https://github.com/kivy/buildozer
%cd buildozer
!python setup.py build
!pip install -e .
%cd ..
!buildozer -v android debug
# (str) Title of your application
#RAH#
title = Nzeneie test

# (str) Package name
#RAH#
package.name = NzenzieTest
# (str) Application versioning (method 1)
#RAH#
version = 0.100
# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
#RAH#
requirements = python3,kivy==2.1.0,https://github.com/kivymd/KivyMD/archive/master.zip,sdl2_ttf==2.0.15,pillow

# (int) Target Android API, should be as high as possible.
#RAH#
android.api = 31
# (bool) If True, then automatically accept SDK license
# agreements. This is intended for automation only. If set to False,
# the default, you will be shown the license when first running
# buildozer.
#RAH#
# android.accept_sdk_license = False
android.accept_sdk_license = True

# (list) The Android archs to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
# In past, was `android.arch` as we weren't supporting builds for multiple archs at the same time.
#RAH#
android.archs = arm64-v8a

2
Like
 
 
ngonidzashe profile image
Ngonidzashe Nzenze
•
May 1 '23

Hi,

So a few things have changed since I've written the article. I have updated it. You can fix the issues you are facing by changing the requirements to: requirements = python3, kivy==2.1.0, kivymd==1.1.1, sdl2_ttf==2.0.15, pillow

And for installing the initial build packages, instead of using the commands with Cython, use the following:
!sudo dpkg --add-architecture i386
!sudo apt-get update
!sudo apt-get install -y build-essential ccache git zlib1g-dev python3 python3-dev libncurses5:i386 libstdc++6:i386 zlib1g:i386 openjdk-8-jdk unzip ant ccache autoconf libtool libssl-dev
This should fix the errors your were encountering. Hope that helps!


2
Like
 
 
kingdonny profile image
kingdonny
•
Jun 9 '23 • Edited

i have been trying to follow your tutorial on the above project and there
I have tried to follow the required steps from the tutorial including this update but google colab is not creating the apk file as the bin folder is empty.

Please help


1
Like
Thread
 
ngonidzashe profile image
Ngonidzashe Nzenze
•
Jun 9 '23

Hey. Are you getting any errors during execution?


1
Like
Thread
 
kingdonny profile image
kingdonny
•
Jun 9 '23 • Edited

No errors but it creates an empty bin folder


1
Like
Thread
 
kingdonny profile image
kingdonny
•
Jun 9 '23

have you tried running the code from your end again?


1
Like
Thread
 
ngonidzashe profile image
Ngonidzashe Nzenze
•
Jun 9 '23 • Edited

I can't run it at the moment but could you try this notebook.


1
Like
Thread
 
kingdonny profile image
kingdonny
•
Jun 9 '23

thank you very much the apk file was created but the application doesn't on my mobile after installation. i tries to open then shuts down


1
Like
Thread
 
ngonidzashe profile image
Ngonidzashe Nzenze
•
Jun 9 '23

Could you try installing your app with adb, then running adb logcat, before opening it. The error should be printed within the console.


1
Like
Thread
 
kingdonny profile image
kingdonny
•
Jun 10 '23 • Edited

Thank you very much

all working good now i think i missed something along the way

you're are the best keep doing the good job

My question is what did you change in the code to make it work this time


1
Like
 
 
pythonkivyuser profile image
PythonKivyuser
•
Nov 13 '21

Hi, I have a question about an error which appears while running the App on my Android Phone (Huawei P8lite).
The adb logcat log shows me the two Errors [ E libEGL : validate_display:255 error 3008 (EGL_BAD_DISPLAY) ] and [ ModuleNotFoundError: No module named 'PIL' ] and than crashes.

Do you have an idea how to solve this Error?

I have already done some research and tried to get some information but PIL is dead and the requirement for KivyMD is Pillow, like the devolopers published in Github.

I would appreciate your help and thank you in advance.
If you need some logs to look at I will provide it to you.


1
Like
 
 
ngonidzashe profile image
Ngonidzashe Nzenze
•
Nov 14 '21

Hello. Did you try adding pillow to the requirements in the buildozer.spec file?


1
Like
 
 
pythonkivyuser profile image
PythonKivyuser
•
Nov 14 '21

I've tried it with
[requirements = kivy==2.0.0, github.com/kivymd/KivyMD/archive/m...]
as the developers published it on Github(github.com/kivymd/KivyMD)
and with
[requirements = python3, kivy==2.0.0, kivymd==0.104.2, sdl2_ttf == 2.0.15, pillow]

In both cases the adb logcat log showed me the two Errors.
Have i forgotten something?


1
Like
Thread
 
ngonidzashe profile image
Ngonidzashe Nzenze
•
Nov 14 '21

Have you tried running:

buildozer android clean

between the changes? If not, try running it and using the following requirements:

requirements = python3,kivy==2.0.0,github.com/kivymd/KivyMD/archive/m..., sdl2_ttf==2.0.15,pillow

If you have tried this and still gotten the error, could you please provide the logs.
I'm pretty sure that adding pillow to the requirements was supposed to work.


1
Like
Thread
 
pythonkivyuser profile image
PythonKivyuser
•
Nov 15 '21

I've tried running buildozer with your mentioned requirements and it worked finally. Thank you very much for taking your time and for your help. 🥳
I'm so happy that the "compilation" is working.

A new small problem accoured with a more advanced kivy code. The code runs at the PC but not on my phone. [ TypeError: 'int' object is not iterable ]

Is this a typical error? And is the KivyMD/Python code the problem?


1
Like
Thread
 
ngonidzashe profile image
Ngonidzashe Nzenze
•
Nov 16 '21

Awesome, I'm glad that worked.

I think the TypeError is probably a bug in your code. It means somewhere your code is trying to iterate over an int object. Try to look through your code for possible causes if the log is not returning the line causing the error.


1
Like
 
 
jhosuaromero30 profile image
jhosua romero
•
Oct 4 '22

Hey, could you help me with my app?, I've been trying several ways in builderdozer and I still can't get the app to work, it closes when I open it, I use kivymd, pillow in the requirements.


1
Like
Thread
 
ngonidzashe profile image
Ngonidzashe Nzenze
•
Oct 4 '22

Hello.
Are you developing the application described in this article or another?


1
Like
 
 
jhosuaromero30 profile image
jhosua romero
•
Oct 4 '22

Hey, could you help me with my app?, I've been trying several ways in builderdozer and I still can't get the app to work, it closes when I open it, I use kivymd, pillow in the requirements.


1
Like
 
 
ngonidzashe profile image
Ngonidzashe Nzenze
•
Oct 24 '22

Are there no errors appearing in the log?


1
Like
 
 
islamimtiaz profile image
IslamImtiaz
•
May 29 '23

Greetings, I am currently attempting to transform my python code into an APK, however, after converting it and installing the file, it unfortunately crashes right after the kivy logo appears. I am using google collab to convert my code into APK.
Spec file
Image description

main.py
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.uix.image import Image
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.dialog import MDDialog

class ConverterApp(MDApp):

    def flip(self):
        if self.state == 0:
            self.state = 1
            self.toolbar.title = 'CGPA calculator'
            self.GP.hint_text = 'Enter your current GPA'
            self.CH.hint_text = 'Enter your previous GPA'
        else:
            self.state = 0
            self.toolbar.title = 'GPA calculator'
            self.GP.hint_text = 'Enter your GP'
            self.CH.hint_text = 'Enter subject CH'

    def gpa(self, obj):
        gp_text = self.GP.text.strip()
        ch_text = self.CH.text.strip()
        # Check if GP and CH fields are not empty
        if not gp_text or not ch_text:
            # Show an error when GP and CH fields are empty
            dialog = MDDialog(title='Error',text='Both GP and CH fields are required',size_hint=(0.7, 1))
            dialog.open()
            return
        # Check if entered data is valid
        try:
            gp_values = [float(gp) for gp in gp_text.split(',')]
            ch_values = [float(ch) for ch in ch_text.split(',')]
        except ValueError:
            # Show an error when non-numeric value is entered
            dialog = MDDialog(title='Error',text='Invalid input! Please enter comma-separated numbers only',size_hint=(0.7, 1))
            dialog.open()
            return
        # Calculate GPA or CGPA
        if self.state == 0:
            x = sum(gp_values)
            y = sum(ch_values)
            if y == 0:
                # Show an error
                dialog = MDDialog(title='Error',text='Zero division error',size_hint=(0.7, 1))
                dialog.open()
            else:    
                c = x / y
                self.label1.text = str(c)
                self.label.text = "Your GPA is: "
        else:
            x = sum(gp_values)
            len1 = len(gp_values)
            y = sum(ch_values)
            len2 = len(ch_values)
            b = len1 + len2
            z = (x + y) / b
            self.label1.text = str(z)
            self.label.text = 'Your CGPA is: '

    def build(self):
        self.state = 0
        screen = MDScreen()
        # Top toolbar
        self.toolbar = MDTopAppBar(title="GPA Calculator")
        self.toolbar.pos_hint = {'top':1}
        self.toolbar.right_action_items = [['rotate-3d-variant', lambda x: self.flip()]]
        screen.add_widget(self.toolbar)
        # Logo
        screen.add_widget(Image(source ='gpr.png',size_hint=(0.8,1),pos_hint ={'center_x':0.5,'center_y':0.7}))
        # Collect user input
        self.GP = MDTextField(hint_text='Enter your GP',halign='center',size_hint=(0.8,1),pos_hint ={'center_x':0.5,'center_y':0.48},font_size=22)
        screen.add_widget(self.GP)
        self.CH = MDTextField(hint_text='Enter your CH',halign='center',size_hint=(0.8,1),pos_hint ={'center_x':0.5,'center_y':0.4},font_size=22)
        screen.add_widget(self.CH)
        # Secondary + Primary Label
        self.label = MDLabel(halign='center',pos_hint ={'center_x':0.5,'center_y':0.32},theme_text_color='Secondary')
        self.label1 = MDLabel(halign='center',pos_hint ={'center_x':0.5,'center_y':0.28},theme_text_color='Primary',font_style='H5')
        screen.add_widget(self.label)
        screen.add_widget(self.label1)
        # Convert Button
        self.button= MDFillRoundFlatButton(text='Result',font_size='17',pos_hint ={'center_x':0.5,'center_y':0.15})
        self.button.bind(on_press = self.gpa)
        screen.add_widget(self.button)

        return screen

ConverterApp().run()
please help me bro


1
Like
 
 
vjrdnti profile image
vjrdnti
•
Jan 11 '22

hello, im making an app with pandas, kivymd. colab just doesnt work, on research i found i have to edit spec file to p4a.branch=develop but it still doesnt work, i did put kivymd and pandas in requirements with their versions, please help i have put a lot of efforts in this app and its frustrating to see it crash after presplash


1
Like
 
 
ngonidzashe profile image
Ngonidzashe Nzenze
•
Jan 11 '22

Hi.

Did you try to locate the error with adb logcat?


1
Like
 
 
jaumeebusquets profile image
Jaumee
•
Dec 17 '21
Comment hidden by post author
 
 
ngonidzashe profile image
Ngonidzashe Nzenze
•
Jan 11 '22

Hello.

Honestly I have no idea where the problem could be. I haven't worked with tello before but I'm probably guessing it could be something to do with cv2 or how the video is being loaded with get_frame_read. Check out this link which has a demo on using opencv with kivy, it might help.


1
Like
 
 
fidelio1 profile image
fidelio1
•
Apr 7

Hi. I have an issue where after building app (kivy,kivymd), it didn't work. I looked up for the logcat and noticed that there is an issue with kivymd2.0.1.dev0
it doesnt recognize MDFAButton. This is declared requirements:
requirements = python3,pynmea2,kivy_garden==0.1.5,kivy==2.3.0,kivymd==2.0.1.dev0
And another question is how to make a permission for apk app, for socket comm, gps (location) ?


1
Like
 
 
alexndegwa profile image
Alexndegwa
•
Jul 1 '23

ModuleNotFoundError: No module named '_ctypes'
The above error keeps getting raised after following the steps you have outlined. Kindly assist


1
Like
 
 
ngonidzashe profile image
Ngonidzashe Nzenze
•
Jul 1 '23

Hey

I've updated the article. I believe one of the required packages was missing. Try to run your program with the latest notebook.


1
Like
 
 
alexndegwa profile image
Alexndegwa
•
Jul 1 '23

Thank you! This worked out for me.


1
Like
 
 
alexndegwa profile image
Alexndegwa
•
Jul 1 '23 • Edited

Am also using pyrebase in my app. Is there a way to know all the dependencies required?


1
Like
Thread
 
ngonidzashe profile image
Ngonidzashe Nzenze
•
Jul 1 '23

To use pyrebase in your application, you just need to add it to the requirements in the spec file. When you run buildozer, it will automatically download any dependencies that pyrebase needs.

However, if you encounter an error with pyrebase, it could be because it's a Python package that requires compilation, and there is no specific support for it in Python-for-android. In such cases, the package won't work as expected.

If you want to make pyrebase work with Python-for-android, you can contribute to the Python-for-android project by creating a recipe specifically for pyrebase. By creating a recipe, you provide the necessary instructions for Python-for-android to properly compile and include pyrebase in the final application package.


1
Like
Thread
 
alexndegwa profile image
Alexndegwa
•
Jul 1 '23

Okay


1
Like
 
 
airan_250 profile image
Airan250
•
Sep 25 '22

app open and close direct
I/python (32368): [Clang 12.0.8 (android.googlesource.com/toolchain... c935d99d
I/python (32368): [INFO ] [Python ] Interpreter at ""
I/python (32368): [INFO ] [KivyMD ] 1.1.0.dev0, git-Unknown, 2022-09-24 (installed at "/data/data/org.test.eiranstudio/files/app/python_bundle/site-packages/kivymd/init.pyc")
I/python (32368): [INFO ] [Factory ] 186 symbols loaded
I/python (32368): Traceback (most recent call last):
I/python (32368): File "/content/.buildozer/android/app/main.py", line 1, in
I/python (32368): File "/content/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/python-installs/EiranStudio/armeabi-v7a/kivymd/init.py", line 66, in
I/python (32368): File "/content/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/python-installs/EiranStudio/armeabi-v7a/kivymd/font_definitions.py", line 10, in
I/python (32368): File "/content/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/python-installs/EiranStudio/armeabi-v7a/kivy/core/text/init.py", line 85, in
I/python (32368): File "/content/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/python-installs/EiranStudio/armeabi-v7a/kivy/graphics/init_.py", line 89, in
I/python (32368): ModuleNotFoundError: No module named 'kivy.graphics.instructions'


1
Like
 
 
grimycan profile image
Vadim
•
Mar 25 '22

I managed to create an apk using Coollaboratory and it works, but the Android device cannot install subsequent versions to the previous one, even if nothing changes in the code. How can I organize the apk update on the device?


1
Like
 
 
abren profile image
abren
•
Oct 1 '22

Hi, I get this error: No module named 'kivy.graphics.instructions' Thank you for any suggestions


1
Like
 
 
aqulline profile image
aqulline
•
Oct 19 '22

did you manage to solve the problem


1
Like
 
 
ngonidzashe profile image
Ngonidzashe Nzenze
•
Oct 24 '22

Hello,

You can try changing the version of kivy in the buildozer spec file from kivy==2.0.0 to kivy==2.1.0


1
Like
 
 
subalmurugan profile image
subal
•
Sep 13 '23

When i try with my own main.py and main.kv and while getting apk then your application is getting...??????


1
Like
 
 
kattaramana profile image
kattaRamana
•
Feb 17 '22

Pandas does not work


1
Like
View full discussion (39 comments)
Some comments have been hidden by the post's author - find out more

Code of Conduct • Report abuse
profile
Auth0
Promoted

Auth0 image

Calling all devs: Explore all that is possible to build and secure in 24 hours.
A day just for Identity? Heck yeah. 😎 Join devs from around the world for our 24-hour live stream.

Register now

Read next
arseytech profile image
Building a calculator using Flet with python
Arsey Kun - Aug 29

myexamcloud profile image
A Comprehensive Guide to Pattern Matching in Python
MyExamCloud - Aug 20

labby profile image
Mastering Python: A Collection of Coding Challenges 🚀
Labby - Jul 28

kiolk profile image
Developer diary #17. How does it work?
Kiolk - Aug 31


Ngonidzashe Nzenze
Follow
Software developer with a passion for all things python🐍
Location
Harare
Education
B.Tech Software Engineering
Work
Developer
Joined
Aug 5, 2021
More from Ngonidzashe Nzenze
Chat with your CSV: Visualize Your Data with Langchain and Streamlit
#python #chatgpt #openai #datascience
Speak Your Queries: How Langchain Lets You Chat with Your Database
#python #chatgpt #openai #postgres
Create a stopwatch and timer with Python and kivymd Part 1
#python #beginners #mobile #tutorial
profile
AWS
Promoted

AWS Security LIVE! Stream

Get cloud security advice without the sales pitch
Ready to level up your cloud security skills? Tune in to AWS Security LIVE! for expert insights, live demos, and interactive Q&A sessions with AWS and AWS Partners.

Learn More

from kivymd.app import MDApp
from kivymd.uix.list import OneLineIconListItem, IconLeftWidget

class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Purple"

    def add_item(self, text):
        new_list_item = OneLineIconListItem(text=text)
        new_list_item.add_widget(
            IconLeftWidget(icon = "language-python")
            )
        self.root.ids.listcontainer.add_widget(new_list_item)
        self.root.ids.listinput.text = ''


if __name__ == "__main__":
    app = MainApp()
    app.run()
Thank you to our Diamond Sponsor Neon for supporting our community.

DEV Community — A constructive and inclusive social network for software developers. With you every step of your journey.

Home
DEV++
Podcasts
Videos
Tags
DEV Help
Forem Shop
Advertise on DEV
DEV Challenges
DEV Showcase
About
Contact
Free Postgres Database
Guides
Software comparisons
Code of Conduct
Privacy Policy
Terms of use
Built on Forem — the open source software that powers DEV and other inclusive communities.

Made with love and Ruby on Rails. DEV Community © 2016 - 2024.