#!/usr/bin/env python3

# Based on stacks-for-windows-linux
# by Emilian Zawrotny
# https://github.com/synnek1337/stacks-for-windows-linux

import os
import pathlib
import subprocess
from sys import argv

IMAGES = 'Images'
VIDEOS = 'Videos'
AUDIO = 'Audio'
SOURCECODES = 'Source Codes'
DOCUMENTS = 'Documents'
APPS = 'Apps'
ARCHIVES = 'Archives'
ADOBE = 'Adobe Files'
OTHERS = 'Others'

IGNORE_LIST = [ '.desktop' ]

file_type_by_extension = {
    IMAGES: [
        '.jpg', '.jpeg', '.jfif', '.jpe', '.jif', '.jfi',      
        '.jp2', '.j2k', '.jpf', '.jpx', 'jpm', 'mj2',          
        '.tiff', '.tif',                                       
        '.gif',                                                
        '.bmp', '.dib',                                        
        '.png',                                                
        '.pbm', '.pgm', '.ppm', '.pnm',                        
        '.webp',                                               
        '.heif', '.heic',                                      
        '.3fr', '.ari', '.arw', '.srf', '.sr2', '.bay',        
        '.crw', '.cr2', '.cap', '.iiq', '.eip', '.dcs',        
        '.dcr', '.drf', '.k25', '.kdc', '.dng', '.erf',        
        '.fff', '.mef', '.mos', '.mrw', '.nef', '.nrw',        
        '.orf', '.ptx', '.pef', '.pxn', '.r3d', '.raf',        
        '.raw', '.rw2', '.rw1', '.rwz', '.x3f'                 
    ],
    VIDEOS: [
        '.webm', '.mkv', '.flv', '.vob', '.ogv' '.ogg',
        '.drc', '.gifv', '.mng', '.avi', '.mts', '.m2ts',
        '.mov', '.qt', '.wmv', '.yuv', '.rm', '.rmvb',
        '.asf', '.amv', '.mp4', '.m4p', '.m4v', '.mpg',
        '.mp2', '.mpeg', '.mpe', '.mpv', '.m2v', '.m4v',
        '.svi', '.3gp', '.3g2', '.mxf', '.roq', '.nsv',
        '.fl4', '.f4p', '.f4v', '.f4a', '.f4b'
    ],
    AUDIO: [
        '.3gp', '.aa', '.aac', '.aax', '.act', '.aiff',
        '.amr', '.ape', '.au', '.awb', '.dct', '.dss',
        '.dvf', '.flac', '.gsm', '.iklax', '.ivs', '.m4a',
        '.m4b', '.m4p', '.mmf', '.mp3', '.mpc', '.msv',
        '.nmf', '.nsf', '.ogg', '.oga', '.mogg', '.opus',
        '.ra', '.rm', '.tta', '.vox', '.wav', '.wma',
        '.wv', '.webm', '.8svx'
    ],
    SOURCECODES: [
        '.C', '.cc', '.cpp', '.cxx', '.c++', '.h', '.hh',
        '.hpp', '.hxx', '.h++', '.py', '.pyc', '.c',
        '.java', '.class', '.bash', '.sh', '.bat', '.ps1',
        '.perl', '.asm', '.S', '.js', '.html', '.css',
        '.scss', '.ts', '.go', '.rs', '.json', '.bin'
    ],
    DOCUMENTS: [
        '.txt', '.doc', '.docx', '.pptx', '.ppt', '.xls',
        '.xlsx', '.md', '.pdf', '.odt', '.ods', '.odp',
        '.odf', '.odb'
    ],
    APPS: [
        '.exe', '.elf', '.lnk', '.msi'
    ],
    ARCHIVES: [
        '.zip', '.rar', '.7z', '.gz', '.bz2', '.Z', '.lzma',
        '.tar', '.xz'
    ],
    ADOBE: [
        '.psd', '.aep', '.prproj', '.ai', '.xd'
    ]
}

def get_desktop_path():
    return subprocess.check_output(['/usr/bin/xdg-user-dir', 'DESKTOP']).decode("utf-8")[:-1]

def get_file_type(file, types):  # types = file_type_by_extension
    for type, extension in types.items():
        if pathlib.Path(file).suffix.lower() in extension:
            return type

def create_folders(types):     # types = file_type_by_extension
    for type_ in types:
        os.makedirs(type_, exist_ok=True)

def stack():
    create_folders(file_type_by_extension)
    files = os.listdir()
    for file in files:
        if get_file_type(file, file_type_by_extension):
            os.rename(file, os.path.join(get_file_type(file,
                                                       file_type_by_extension), file))
    files = os.listdir()
    for file in files:
        if os.path.isfile(file):
            filename, file_ext = os.path.splitext(file)
            if not file_ext in IGNORE_LIST:
                os.makedirs(OTHERS, exist_ok=True)
                os.rename(file, os.path.join(OTHERS, file))
            
    for folder in file_type_by_extension:
        if not os.listdir(folder):
            os.removedirs(folder)


def unstack():
    for folder_name in file_type_by_extension:
        try:
            os.chdir(folder_name)
        except FileNotFoundError:
            print(folder_name + " not found.")
        else:
            for file in os.listdir():
                os.rename(file, os.path.join('..', file))
            os.chdir('..')
            os.removedirs(folder_name)
            
    try:
        os.chdir(OTHERS)
    except FileNotFoundError:
        print("Others not found.")
    else:
        for file in os.listdir():
            os.rename(file, os.path.join('..', file))
        os.chdir('..')
        os.removedirs(OTHERS)


if __name__ == "__main__":
    os.chdir(get_desktop_path())
    if "--stack" in argv:
        stack()
    elif "--unstack" in argv:
        unstack()
    else:
        print("Error: Argument missing.")
