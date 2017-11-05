#!/bin/bash
git pull origin master && conda env update -f environment.yml && source activate wx
