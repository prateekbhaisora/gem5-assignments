#!/bin/bash

DIR_PATH="configs/my_scripts"
LOG_FILE="./output.log"

CPU_MODELS=(
    "O3CPU"
    "TimingSimpleCPU"
    "AtomicSimpleCPU"
)

BRANCH_PREDICTION_SCHEMES=(
    "BiModeBP"
    "TournamentBP"
    "TAGE"
)

clear_tmp_files(){
    rm -rf $LOG_FILE
    rm -rf ./m5out
    rm -rf ./gen_outputs
}

print_separator() {
    local char="="
    local width=100
    printf '%*s\n' "$width" '' | tr ' ' "$char" | tee -a $LOG_FILE
}

compile_mm_code() {
    g++ ./$DIR_PATH/ikj.cpp -o ./$DIR_PATH/ikj 2>> $LOG_FILE
}

run_tests() {
    ind=1

    for cpu in "${CPU_MODELS[@]}"; do
        for bp in "${BRANCH_PREDICTION_SCHEMES[@]}"; do

            print_separator
            echo "Testing with CPU: $cpu, BP: $bp" | tee -a $LOG_FILE
            print_separator

            sed -i "/system.cpu = .*/c\system.cpu = ${cpu}()" ./$DIR_PATH/run_cache_stats.py
            sed -i "/system.cpu.branchPred = .*/c\system.cpu.branchPred = ${bp}()" ./$DIR_PATH/run_cache_stats.py

            if [[ "$cpu" == "AtomicSimpleCPU" ]]; then
                sed -i "/system.mem_mode = .*/c\system.mem_mode = \"atomic\"" ./$DIR_PATH/run_cache_stats.py
            else
                sed -i "/system.mem_mode = .*/c\system.mem_mode = \"timing\"" ./$DIR_PATH/run_cache_stats.py
            fi

            ./build/X86/gem5.opt ./$DIR_PATH/run_cache_stats.py 2>> $LOG_FILE
            print_separator

            mv $LOG_FILE m5out
            if [ ! -d "./gen_outputs" ]; then
                mkdir -p ./gen_outputs
            fi
            mv ./m5out ./gen_outputs/${ind}
            (( ind++ ))

        done
    done
}

main() {
    clear_tmp_files
    compile_mm_code
    run_tests
}

main