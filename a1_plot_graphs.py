import os
import matplotlib.pyplot as plt

def extract_values_from_file(file_path):
    ipc_value, cpi_value, numCycles_value, simSeconds_value = None, None, None, None
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('system.cpu.ipc'):
                ipc_value = float(line.split()[1])
            elif line.startswith('system.cpu.cpi'):
                cpi_value = float(line.split()[1])
            elif line.startswith('system.cpu.numCycles'):
                numCycles_value = int(line.split()[1])
            elif line.startswith('simSeconds '):
                simSeconds_value = float(line.split()[1])
    return ipc_value, cpi_value, numCycles_value, simSeconds_value

def extract_sys_info_from_file(file_path):
    cpu_model, memory_config, freq_value = None, None, None
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('Testing with'):
                cpu_model = str(line.split()[3][:-1])
                memory_config = str(line.split()[5][:-1])
                freq_value = int(line.split()[-1][:-3])
                break
    sys_info = [cpu_model, memory_config, freq_value]
    return sys_info

def process_directory(base_dir, start_index, end_index):
    ipc_values = []
    cpi_values = []
    numCycles_values = []
    simSeconds_values = []
    sys_info_values = []

    for ind in range(start_index, end_index + 1):
        ind_dir = os.path.join(base_dir, str(ind))
        stats_file = os.path.join(ind_dir, 'stats.txt')
        log_file = os.path.join(ind_dir, 'output.log')

        if os.path.isfile(stats_file):
            ipc_value, cpi_value, numCycles_value, simSeconds_value = extract_values_from_file(stats_file)
            sys_info_value = extract_sys_info_from_file(log_file)
            ipc_values.append(ipc_value)
            cpi_values.append(cpi_value)
            numCycles_values.append(numCycles_value)
            simSeconds_values.append(simSeconds_value)
            sys_info_values.append(sys_info_value)

    return sys_info_values, ipc_values, cpi_values, numCycles_values, simSeconds_values

def plot_graph(sys_info_values, values, y_axis_val, color, index_range, output_dir):
    cpu_models, memory_configs, freq_values = [], [], []
    for ele in sys_info_values:
        cpu_models.append(ele[0])
        memory_configs.append(ele[1])
        freq_values.append(ele[2])

    plt.figure(figsize=(12, 6))
    plt.plot(freq_values, values, marker='x', linestyle='--', color=color)
    plt.xlabel('Frequency Value (MHz)')
    plt.ylabel(y_axis_val)
    plt.title(f'{y_axis_val} vs Frequency\nIndex Range: {index_range}')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    output_path = os.path.join(output_dir, f'{y_axis_val}_vs_freq_{index_range}.png')
    plt.savefig(output_path)  # Save to file without showing
    plt.close()  # Close the figure to prevent displaying

def main():
    base_dir = './gen_outputs'
    output_dir = './gen_graphs'
    
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    ranges = [
        (1, 14),    # O3CPU, DDR3_1600_8x8
        (15, 28),   # O3CPU, LPDDR2_S4_1066_1x32
        (29, 42),   # O3CPU, HBM_1000_4H_1x64
        (43, 56),   # TimingSimpleCPU, DDR3_1600_8x8
        (57, 70),   # TimingSimpleCPU, LPDDR2_S4_1066_1x32
        (71, 84),   # TimingSimpleCPU, HBM_1000_4H_1x64
        (85, 98),   # AtomicSimpleCPU, DDR3_1600_8x8
        (99, 112),  # AtomicSimpleCPU, LPDDR2_S4_1066_1x32
        (113, 126)  # AtomicSimpleCPU, HBM_1000_4H_1x64
    ]
    
    for start_index, end_index in ranges:
        print(f"Processing indices from {start_index} to {end_index}...")
        sys_info_values, ipc_values, cpi_values, numCycles_values, simSeconds_values = process_directory(base_dir, start_index, end_index)
        
        print("Sys info values:", sys_info_values)
        print("IPC values:", ipc_values)
        print("CPI values:", cpi_values)
        print("Num. Cycle values:", numCycles_values)
        print("Sim. Seconds values:", simSeconds_values)
        
        plot_graph(sys_info_values, ipc_values, 'IPC_value', 'b', f'{start_index}_{end_index}', output_dir)
        plot_graph(sys_info_values, cpi_values, 'CPI_value', 'r', f'{start_index}_{end_index}', output_dir)
        plot_graph(sys_info_values, numCycles_values, 'numCycles_value', 'g', f'{start_index}_{end_index}', output_dir)
        plot_graph(sys_info_values, simSeconds_values, 'simSeconds_value', 'c', f'{start_index}_{end_index}', output_dir)

if __name__ == '__main__':
    main()
