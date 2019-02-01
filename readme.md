# source-delivery

## install
- `python3 -m venv .venv`
- `. .venv/bin/activate`
- `pip install -U pip`
- `pip install poetry`
- `poetry install`

## run
- `poetry run archive` to create archives
- `poetry run clean` to remove all archives

## config
Update the configuration file, `config.yml` with the list of remotes you would like to archive under the `repos` field. Once ready, run the `archive` command to update the latest zip file.

## archive
After creating an archive, you will find a zip version tagged with the run's date. There will also be an untagged version of the file that will always be the _latest_ version of the archive.

## note
This script expects git and ssh to be correctly configured before running it. It does not make any calls on how you setup your connection over git.