#!/usr/bin/env bash

## ASSUMING CONDA IS INSTALLED

ENV_NAME=DB_ENV

# create the environment
conda create -p ./env/$ENV_NAME -y

# remove env prefix from shell prompts
conda config --set env_prompt '({name})'

# add env to config (env is now found by --name, -n)
conda config --append envs_dirs ./env/

# activate the environemnt
conda activate $ENV_NAME

conda env update -f env.yml --prune
