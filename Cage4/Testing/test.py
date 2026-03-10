import os
root_path = 'results'
path = os.path.join(root_path, 'training')

dirs = [f.name for f in os.scandir(root_path) if f.is_dir()]

#max_dir = max(dirs, key=lambda file: file[-1])

max_dir = max([file[-1] for file in dirs])

print(path)