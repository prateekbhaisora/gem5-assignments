import os
import matplotlib.pyplot as plt
import numpy as np
from prettytable import PrettyTable

def extract_values_from_stat(file_path, parameters):
    values = {param: None for param in parameters}
    with open(file_path, 'r') as file:
        for line in file:
            for param in parameters:
                if line.startswith(param):
                    values[param] = float(line.split()[1])  
                    break
    return values

def process_directory(base_dir, parameters):
    stats_file = os.path.join(base_dir, 'stats.txt')
    if os.path.isfile(stats_file):
        return extract_values_from_stat(stats_file, parameters)
    else:
        return {param: None for param in parameters}

def plot_parameter_values(values_inbuilt, values_custom, parameter, output_dir):
    x_labels = ['Inbuilt', 'Custom']
    
    plt.figure(figsize=(8, 6))
    
    colors = ['blue', 'orange']  
    plt.bar(x_labels, [values_inbuilt, values_custom], color=colors, edgecolor='black')

    plt.ylabel(parameter)
    plt.title(f'{parameter} Comparison (Inbuilt vs Custom)')
    
    for i, v in enumerate([values_inbuilt, values_custom]):
        plt.text(i, v, str(round(v, 2)), ha='center', va='bottom', fontsize=12)
    
    output_path = os.path.join(output_dir, f'{parameter}_comparison_bar_chart.png')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def main():
    base_dirs = ['m5out-inbuilt', 'm5out-custom']
    output_dir = './gen_graphs'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    parameters = [
        'simSeconds',
        'simTicks',
        'system.cpu.numCycles',
        'system.cpu.ipc',
        'system.cpu.cpi'
    ]
    
    summary_table = PrettyTable()
    summary_table.field_names = ["Parameter", "Inbuilt Value", "Custom Value"]
    
    for param in parameters:
        values_inbuilt = process_directory(base_dirs[0], [param])[param]
        values_custom = process_directory(base_dirs[1], [param])[param]
        
        summary_table.add_row([param, values_inbuilt, values_custom])
        
        plot_parameter_values(values_inbuilt, values_custom, param, output_dir)

    print(summary_table)

if __name__ == '__main__':
    main()