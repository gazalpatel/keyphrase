
import os, sys

example_folder = os.path.dirname(os.path.abspath(__file__))
files_path = [os.path.join(example_folder, x) for x in os.listdir(example_folder)]

for i, file in enumerate(files_path):
    if file.endswith(".py"):
        if __file__ in file:
            continue
        else:
            print("\n========== [Running - %s: %s] ==========" % (i, file))
            command = "python %s" % (file)
            os.system(command)