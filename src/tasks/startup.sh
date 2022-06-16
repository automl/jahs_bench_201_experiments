#!/bin/bash

export PYTHONPATH=/home/janowski/jahs_bench/:$PYTHONPATH
export PYTHONPATH=/home/janowski/jahs_bench/jahs_bench_201_experiments/:$PYTHONPATH

source ~/anaconda3/bin/activate jahs_bench_201

basedir=/home/janowski/jahs_bench/jahs_bench_201_experiments/src/tasks/
work=/work/dlclarge2/janowski-jahs_neurips2022/

cd $basedir

echo "base:"$basedir
echo "work:"$work
