#!/bin/bash

DIR_PATH="configs/my_scripts"
LOG_FILE="./output.log"

CPU_MODELS=(
    "O3CPU"
    "TimingSimpleCPU"
    "AtomicSimpleCPU"
)

MEMORY_CONFIGS=(
    "DDR3_1600_8x8"
    "LPDDR2_S4_1066_1x32"
    "HBM_1000_4H_1x64"
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

setup_frequencies() {
    FREQUENCIES=()
    for freq in $(seq 600 200 3300); do
        FREQUENCIES+=("${freq}MHz")
    done
}

compile_mm_code() {
    g++ ./$DIR_PATH/mm.cpp -o ./$DIR_PATH/mm 2>> $LOG_FILE
}

run_tests() {
    ind=1

    for cpu in "${CPU_MODELS[@]}"; do
        for mem in "${MEMORY_CONFIGS[@]}"; do
            for freq in "${FREQUENCIES[@]}"; do

                print_separator
                echo "Testing with CPU: $cpu, Memory: $mem, Frequency: $freq" | tee -a $LOG_FILE
                print_separator

                sed -i "/system.cpu = .*/c\system.cpu = ${cpu}()" ./configs/my_scripts/run_mm.py
                sed -i "/system.mem_ctrl.dram = .*/c\system.mem_ctrl.dram = ${mem}()" ./$DIR_PATH/run_mm.py
                sed -i "/system.cpu_clk_domain.clock = .*/c\system.cpu_clk_domain.clock = \"${freq}\"" ./$DIR_PATH/run_mm.py

                if [[ "$cpu" == "AtomicSimpleCPU" ]]; then
                    sed -i "/system.mem_mode = .*/c\system.mem_mode = \"atomic\"" ./$DIR_PATH/run_mm.py
                else
                    sed -i "/system.mem_mode = .*/c\system.mem_mode = \"timing\"" ./$DIR_PATH/run_mm.py
                fi

                ./build/X86/gem5.opt ./$DIR_PATH/run_mm.py 2>> $LOG_FILE
                print_separator

                mv $LOG_FILE m5out
                if [ ! -d "./gen_outputs" ]; then
                    mkdir -p ./gen_outputs
                fi
                mv ./m5out ./gen_outputs/${ind}
                (( ind++ ))

            done
        done
    done
}

main() {
    clear_tmp_files
    setup_frequencies
    compile_mm_code
    run_tests
}

main