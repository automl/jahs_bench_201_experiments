#!/bin/bash

basedir=/home/janowski/jahs_bench/jahs_bench_201_experiments/src/tasks/
work=/work/dlclarge2/janowski-jahs_neurips2022/

python $basedir/utils/CMDs/generate_cmds.py

python $basedir/slurm_helper.py \
    -q bosch_cpu-cascadelake \
    --timelimit 86400 \
    --cores 4 \
    --startup $basedir/startup.sh \
    --array_min 1 \
    --array_max 361 \
    --memory_per_job 100000 \
    -o $work/LOGS/ \
    -l $work/LOGS/ \
    $basedir/utils/CMDs/all_experiments.txt
