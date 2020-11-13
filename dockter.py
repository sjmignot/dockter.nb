import getpass
import argparse
import os
import pkg_resources

IMAGE_MAP = {
    'base': 'jupyter/minimal-notebook',
    'scipy': 'jupyter/scipy-notebook',
    'tf': 'jupyter/tensorfolow-notebook'
}

parser = argparse.ArgumentParser()
parser.add_argument('-a',
                    '--author',
                    default=getpass.getuser(),
                    help='creater of jupyter notebook')

parser.add_argument('-i',
                    '--base-image',
                    choices=('base', 'scipy', 'tf'),
                    default='base',
                    help='notebook uses scipy functionality')

parser.add_argument('-b',
                    '--build',
                    action='store_true',
                    help='build docker image')

parser.add_argument('-r',
                    '--run',
                    action='store_true',
                    help='run jupyter while mapping current working directory')

args = parser.parse_args()
print(args)

image = IMAGE_MAP[args.base_image]

installed_packages = [
    f"{d.project_name}=={d.version}" for d in pkg_resources.working_set
]

with open('Dockerfile', 'w+') as f:
    f.write(f'FROM {image}\n'
            f'LABEL author="{args.author}"\n'
            f'USER root\n'
            f'RUN pip install {" ".join(installed_packages)}\n'
            f'USER $NB_UID\n')

if args.build:
    os.system('docker build .')

if args.run:
    os.system('docker run -p 8888:8888 -v $(pwd):/home/jovyan/work')
