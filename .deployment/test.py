import os
import sys
import logging
import argparse
import paramiko

some_dir = "../_themes"
print(os.path.abspath(some_dir))
for root, dirs, files in os.walk(os.path.abspath(some_dir), topdown=True):
    # print(files)
    pass
