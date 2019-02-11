#!/usr/bin/env python3

import argparse
import os
import shutil
import subprocess
import sys
from datetime import datetime
from os import scandir, remove
from shutil import copyfile, make_archive, rmtree
from sys import stdout
from time import sleep

from git import Repo
from yaml import load


def load_config():
    with open('config.yml', 'r') as f:
        return load(f)


def clean_repos(repo_path):
    with scandir(repo_path) as repos:
        [rmtree(repo.path) for repo in repos if repo.is_dir()]


def clone_repos(repo_path, config, depth=1):
    repos = config[repo_path]
    exclude_string = config['exclude_string']
    print('Loading', end='')
    for name in repos:
        print(end='.')  # loading indicator
        stdout.flush()
        destination_path = os.path.join(repo_path, name)
        Repo.clone_from(repos[name], destination_path, depth=depth)
        try:
            subprocess.run(
                f"find {destination_path} -name '*{exclude_string}*' -exec rm -rf {{}} \;",
                shell=True,
            )
        except FileNotFoundError:
            print(f'No files with name including {exclude_string} found')
        matching_process = subprocess.run(
            f"find {destination_path} -exec grep -rl {exclude_string} {{}} \;",
            shell=True,
            stdout=subprocess.PIPE,
        )
        matching_files = {file_name for file_name in matching_process.stdout.decode('utf-8').split('\n') if file_name}
        deleted_files = [remove(file_name) for file_name in matching_files]
        rmtree(os.path.join(repo_path, name, '.git'))
    print()


def zip_repos(path, config):
    print('Compressing.')
    now = datetime.now()
    dir_path = os.getcwd()
    zip_name = f'{config["zip_name"]}-{now.strftime("%m%d%Y")}'
    archive = os.path.join(config['zip_path'], zip_name)
    make_archive(archive, 'zip', 'repos')
    downloadable = f'{os.path.join(config["zip_path"], config["zip_name"])}.zip'
    copyfile(f'{archive}.zip', downloadable)  # update downloadable file
    clean_repos(path)


def archive(depth=1):
    print()
    config = load_config()
    path = config['repo_path']
    clean_repos(path)
    clone_repos(path, config, depth)
    zip_repos(path, config)
    print('Archive created.', end='\n\n')


if __name__ == '__main__':
    archive()
