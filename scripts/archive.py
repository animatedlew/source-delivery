#!/usr/bin/env python3

import sys, os, shutil
from sys import stdout
from os import scandir
from shutil import make_archive, copyfile, rmtree
from git import Repo
from yaml import load
from time import sleep
from datetime import datetime


def load_config():
    with open('config.yml', 'r') as f:
        return load(f)


def clean_repos(repo_path):
    with scandir(repo_path) as repos:
        [rmtree(repo.path) for repo in repos if repo.is_dir()]


def clone_repos(repo_path, config, depth=1):
    repos = config[repo_path]
    print('Loading', end='')
    for name in repos:
        print(end='.')  # loading indicator
        stdout.flush()
        Repo.clone_from(repos[name], os.path.join(repo_path, name), depth=depth)
        rmtree(os.path.join(repo_path, name, '.git'))
    print()


def zip_repos(path, config):
    print('Compressing.')
    now = datetime.now()
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
