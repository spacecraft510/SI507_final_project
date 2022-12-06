import os

home_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(home_dir)
os.system('final_project.py')
print(home_dir)

