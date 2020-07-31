# screen-lapse
A simple python application that allows for recording screens over long periods (ie speedpaints).

Requires ffmpeg to be installed! Simply run screenlapse.py, choose the area of your screen recording as well as shots per minute, then record. Finally, export the file. It will export to "video.mp4". Very simple, nothing special.

Note that you can also record both screens if you wish: for two 1080p screens, you'd make offset (0,0) and resolution (3840,1080). If you just want the right screen, then offset should be (1920,0) and resolution (1920,1080).

![Screenshot](https://i.imgur.com/7hYNKtZ.png)
