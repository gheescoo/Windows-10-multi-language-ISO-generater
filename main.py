import os
from subprocess import call
import sys

from constants import *
from simple_io import *

''''''''''''''''''''''''
def add_lp():
    if(confirm("Install Language Packs? [y/n]:") == False):
        print("Aborted.")
        return
    LP_PATH = input("Specify the path Language Pack files are located:\n")

    for filename in os.listdir(LP_PATH):
        fullpath = os.path.join(LP_PATH, filename)
        if(os.path.isfile(fullpath)):
            for lang in lang_list:
                if(lang.casefold() in filename.casefold()):
                    call(DISM_ADDPKG.format(mntdir = "wim", pkg = quoted(fullpath)), shell = True)
                    break

def add_lxp():
    if(confirm("Install Local Experience Packs? [y/n]:") == False):
        print("Aborted.")
        return
    LXP_PATH = input("Specify the path Local Experience Packs directories are located:\n")

    for dirname in os.listdir(LXP_PATH):
        fullpath = os.path.join(LXP_PATH, dirname)
        if(os.path.isdir(fullpath)):
            for lang in lang_list:
                if(lang.casefold() in dirname.casefold()):
                    call(DISM_ADDPAP.format(mntdir = "wim", pkg = quoted(os.path.join(fullpath, "LanguageExperiencePack.{}.Neutral.appx".format(lang))), ca = quoted(os.path.join(dirname, "License.xml"))), shell = True)
                    break

def add_lf():
    if(confirm("Install Language Features? [y/n]:") == False):
        print("Aborted.")
        return
    LF_PATH = input("Specify the path Language Features files are located:\n")

    for filename in os.listdir(LF_PATH):
        fullpath = os.path.join(LF_PATH, filename)
        if(os.path.isfile(fullpath)):
            if("Fonts" in filename):
                call(DISM_ADDPKG.format(mntdir = "wim", pkg = quoted(fullpath)), shell = True)
                continue
            for lang in lang_list:
                if(lang.casefold() in filename.casefold() and "Basic" in filename):
                    call(DISM_ADDPKG.format(mntdir = "wim", pkg = quoted(fullpath)), shell = True)
                    break

def add_re():
    if(confirm("Add languages to Windows RE? [y/n]:") == False):
        print("Aborted.")
        return

    LF_PATH = input("Specify the path WinRE Language Pack directories are located:\n")
    print("\tYOU ARE RICK ROLLED. I WON'T DD /dev/null to /dev/*\n"*10)

def add_setup():
    if(confirm("Add languages to Windows Setup? [y/n]:") == False):
        print("Aborted.")
        return

    call(cmd_mount_setup, shell = True)
    WINPEOCS_PATH = input("Specify the path WinPE Language Pack files are located:\n")
    for name in os.listdir(WINPEOCS_PATH):
        fullpath = os.path.join(WINPEOCS_PATH, name)
        if(os.path.isfile(fullpath)):
            if("FontSupport" in name):
                call(DISM_ADDPKG.format(mntdir = "setup", pkg = quoted(fullpath), shell = True))
        else:
            for lang in lang_list:
                if(lang.casefold() in name.casefold()):
                    call(DISM_ADDPKG.format(mntdir = "setup", pkg = quoted(os.path.join(fullpath, "lp.cab"))), shell = True)
                    call(DISM_ADDPKG.format(mntdir = "setup", pkg = quoted(os.path.join(fullpath, "WinPE-Setup_{}.cab".format(name)))), shell = True)
                    call(DISM_ADDPKG.format(mntdir = "setup", pkg = quoted(os.path.join(fullpath, "WinPE-Setup-Client_{}.cab".format(name)))), shell = True)
                    break

    call(XCOPY_LANGINI.format(src = quoted(WIN_PATH), dest = "setup", shell = True))
    call(cmd_commit_setup, shell = True)
            

''''''''''''''''''''''''
WIN_PATH = input("Specify the path Windows 10 ISO is extracted, which should be writable:\n")
WORK_PATH = input("Specify the path of working folder:\n")
PY_PATH = os.path.dirname(os.path.realpath(__file__))
os.chdir(WORK_PATH)
call("md wim re setup", shell = True)

try:
    with open(os.path.join(PY_PATH, "lang.txt")) as f:
        lang_list = f.read().split()
except IOError:
    with open(os.path.join(PY_PATH, "iso_langcode.list")) as f:
        lang_list = f.read().split()


# Add language packs, LIPs, and Features on Demand
while(True):
    print("Check the WIM file using the command:\n\tDISM /Get-WimInfo /WimFile:path_to_wim_file")
    WIM_INDEX = input("Choose the index in the WIM file you want to edit with:")
    if(not WIM_INDEX): break

    cmd_mount_wim = DISM_MOUNT.format(img = quoted(os.path.join(WIN_PATH, WIM_path)), idx = WIM_INDEX, mntdir = "wim")
    cmd_commit_wim = DISM_UNMOUNT_COMMIT.format(mntdir = "wim")
    
    call(cmd_mount_wim, shell = True)
    add_lp()
    add_lxp()
    add_lf()
    call(DISM_GENLANGINI.format(img = "wim", dis = quoted(WIN_PATH)))

    # Add languages to the recovery environment (Windows RE)
    cmd_mount_re = DISM_MOUNT.format(img = quoted(os.path.join("wim", RE_path)), idx = "1", mntdir = "re")
    cmd_commit_re = DISM_UNMOUNT_COMMIT.format(mntdir = "re")

    call(cmd_mount_re, shell = True)
    add_re()
    call(cmd_commit_re, shell = True)

    call(cmd_commit_wim, shell = True)

cmd_mount_setup = DISM_MOUNT.format(img = quoted(os.path.join(WIN_PATH, BOOT_path)), idx = "2", mntdir = "setup")
cmd_commit_setup = DISM_UNMOUNT_COMMIT.format(mntdir = "setup")

add_setup()

input("Press any key to generate ISO...")
cmd_make_iso = "{} -m -n -yo{} -b{} {} {}".format(\
    quoted(os.path.join(ADK_PATH, 'amd64\\Oscdimg', "OSCDIMG")),\
    quoted(os.path.join(PY_PATH, "BootOrder.txt")),\
    quoted(os.path.join(ADK_PATH, 'amd64\\Oscdimg', "efisys.bin")),\
    quoted(WIN_PATH),\
    quoted(os.path.join(WORK_PATH, "generated_iso.iso")),)
call(cmd_make_iso, shell = True)

input("Press any key to end...")



