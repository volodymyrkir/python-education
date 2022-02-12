#!/usr/bin/env bash
path=$PWD
curtime=$(date +"%T")
echo "Scanning in : $path"
echo "Systime : $curtime"
ls -a | sort
