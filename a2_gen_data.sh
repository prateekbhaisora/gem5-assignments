#!/bin/bash

DIR_PATH="configs/my_scripts"
LOG_FILE="./output.log"

BRANCH_PREDICTION_SCHEMES=(
    "LocalBP"
    "TournamentBP"
    "BiModeBP"
    "MultiperspectivePerceptronTAGE64KB"
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

compile_bmm_code() {
    g++ ./$DIR_PATH/bmm.cpp -o ./$DIR_PATH/bmm 2>> $LOG_FILE
}

run_tests() {

    ind=1

    for bps in "${BRANCH_PREDICTION_SCHEMES[@]}"; do

        print_separator
        echo "Testing with Branch Predictor: $bps" | tee -a $LOG_FILE
        print_separator

        sed -i "/system.cpu.branchPred = .*/c\system.cpu.branchPred = ${bps}()" ./configs/my_scripts/run_bmm_bp_stats.py
    
        ./build/X86/gem5.opt ./$DIR_PATH/run_bmm_bp_stats.py 2>> $LOG_FILE
        print_separator

        mv $LOG_FILE m5out
        if [ ! -d "./gen_outputs" ]; then
            mkdir -p ./gen_outputs
        fi
        mv ./m5out ./gen_outputs/${ind}
        (( ind++ ))

    done
}

main() {
    clear_tmp_files
    compile_bmm_code
    run_tests
}

main