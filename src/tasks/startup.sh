#!/bin/bash

export PYTHONPATH=/home/janowski/jahs_bench/jahs_bench_201/tabular_sampling/:$PYTHONPATH
export PYTHONPATH=/home/janowski/jahs_bench/ICGen/:$PYTHONPATH
export PYTHONPATH=/home/janowski/jahs_bench/ICGen/icgen/:$PYTHONPATH
export PYTHONPATH=/home/janowski/jahs_bench/NASLib/:$PYTHONPATH
export PYTHONPATH=/home/janowski/jahs_bench/NASLib/naslib/:$PYTHONPATH
export PYTHONPATH=/home/janowski/jahs_bench/jahs_bench_201/src/tasks/:$PYTHONPATH
export PYTHONPATH=/home/janowski/jahs_bench/:$PYTHONPATH
export PYTHONPATH=/home/janowski/jahs_bench/jahs_bench_201/:$PYTHONPATH

source ~/anaconda3/bin/activate jahs_benchs_201

basedir=/home/janowski/jahs_bench/jahs_bench_201/src/tasks/
work=/work/dlclarge2/janowski-jahs_neurips2022/

cd $basedir

echo "base:"$basedir
echo "work:"$work
