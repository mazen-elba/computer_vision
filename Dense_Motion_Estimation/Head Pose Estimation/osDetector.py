"""Detect OS"""
from platform import system


def detectOS(bypass=False):
    """Check OS, as multiprocessing may not work properly on Windows and macOS"""
    if bypass is True:
        return

    osName = system()

    if osName in ['Windows']:
        print("It seems that you are running this code from {}, on which the Python multiprocessing may not work properly. Consider running this code on Linux.".format(osName))
        print("Exiting..")
        exit()
    else:
        print("Linux is fine! Python multiprocessing works.")
