#!/usr/bin/env bash
docker build -t submitty-base-worker ./workers/
docker build -t submitty-python-worker ./workers/python