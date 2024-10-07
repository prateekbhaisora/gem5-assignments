import os
import matplotlib.pyplot as plt
import numpy as np
from prettytable import PrettyTable  # Importing the PrettyTable library

def extract_values_from_stat(file_path, parameters):
    values = {param: None for param in parameters}
    
    with open(file_path, 'r') as file:
        for line in file:
            for param in parameters:
                if line.startswith(param):
                    values[param] = int(line.split()[1])  
                    break
    return values

def process_directory(base_dir, subfolder_index, parameters):
    stats_file = os.path.join(base_dir, str(subfolder_index), 'stats.txt')
    
    if os.path.isfile(stats_file):
        return extract_values_from_stat(stats_file, parameters)
    else:
        return {param: None for param in parameters}

def plot_histograms(paired_values, labels, y_axis_val, output_dir, subfolder):
    colors = ['red', 'green']  # Red and green for the two bars in each pair
    
    plt.figure(figsize=(10, 6))
    
    bar_width = 0.35  # Width of each bar
    index = np.arange(len(paired_values))  # X-axis positions for each bar pair

    for i, (values1, values2) in enumerate(paired_values):
        # Plot two bars side by side
        plt.bar(index[i] - bar_width/2, values1, bar_width, color=colors[0], edgecolor='black')
        plt.bar(index[i] + bar_width/2, values2, bar_width, color=colors[1], edgecolor='black')
    
    plt.xlabel('')  # No x-axis label

    # Map y_axis_val to descriptive titles
    title_map = {
        'system.cpu.dcache.overallHits::total': 'Overall Hits in L1 dcache',
        'system.cpu.dcache.overallMisses::total': 'Overall Misses in L1 dcache',
        'system.cpu.icache.overallHits::total': 'Overall Hits in L1 icache',
        'system.cpu.icache.overallMisses::total': 'Overall Misses in L1 icache',
        'system.l2cache.overallHits::total': 'Overall Hits in L2 cache',
        'system.l2cache.overallMisses::total': 'Overall Misses in L2 cache'
    }

    plt.ylabel(title_map[y_axis_val])  # Use mapped title for y-axis

    # Update title to include subfolder name
    output_names = {
        1: 'O3CPU, BiModeBP',
        2: 'O3CPU, TournamentBP',
        3: 'O3CPU, TAGE',
        4: 'TimingSimpleCPU, BiModeBP',
        5: 'TimingSimpleCPU, TournamentBP',
        6: 'TimingSimpleCPU, TAGE',
        7: 'AtomicSimpleCPU, BiModeBP',
        8: 'AtomicSimpleCPU, TournamentBP',
        9: 'AtomicSimpleCPU, TAGE'
    }

    subfolder_name = output_names.get(subfolder, f'Subfolder_{subfolder}')
    plt.title(f'{title_map[y_axis_val]} - {subfolder_name} Distribution')

    plt.xticks(index, ['ijk', 'ikj', 'bijk'])  # Label groups on the x-axis
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)

    # Add exact values on top of each bar
    for i, (values1, values2) in enumerate(paired_values):
        if values1 is not None:
            plt.text(index[i] - bar_width/2, values1, int(values1), va='bottom', ha='center', fontsize=10, color='black')
        if values2 is not None:
            plt.text(index[i] + bar_width/2, values2, int(values2), va='bottom', ha='center', fontsize=10, color='black')

    # Add a single legend to indicate color meaning, placed outside the graph
    plt.legend(['Cache Config 1', 'Cache Config 2'], loc='upper left', bbox_to_anchor=(1, 1))

    plt.tight_layout()
    
    output_path = os.path.join(output_dir, f'{title_map[y_axis_val]}_{subfolder_name}.png')
    plt.savefig(output_path)
    plt.close()

def main():
    base_dirs = [
        ('./gen_outputs_ijk_1', './gen_outputs_ijk_2'), 
        ('./gen_outputs_ikj_1', './gen_outputs_ikj_2'),
        ('./gen_outputs_bijk_1', './gen_outputs_bijk_2')
    ]
    subfolders = [1, 2, 3, 4, 5, 6, 7, 8, 9]  
    output_dir = './gen_graphs'
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    parameters = [
        'system.cpu.dcache.overallHits::total',
        'system.cpu.dcache.overallMisses::total',
        'system.cpu.icache.overallHits::total',
        'system.cpu.icache.overallMisses::total',
        'system.l2cache.overallHits::total',
        'system.l2cache.overallMisses::total'
    ]
    
    # Create a PrettyTable for summarizing observations
    summary_table = PrettyTable()
    summary_table.field_names = ["Subfolder", "Parameter", "Config 1 Value", "Config 2 Value"]

    for subfolder in subfolders:
        for param in parameters:
            paired_values = []
            folder_pairs = []
            
            for dir1, dir2 in base_dirs:
                values1 = process_directory(dir1, subfolder, [param])[param]
                values2 = process_directory(dir2, subfolder, [param])[param]
                paired_values.append((values1, values2))
                folder_pairs.append((os.path.basename(dir1), os.path.basename(dir2)))
                
                # Add row to summary table
                summary_table.add_row([subfolder, param, values1, values2])
            
            plot_histograms(paired_values, folder_pairs, param, output_dir, subfolder)
    
    # Print the summary table
    print(summary_table)

if __name__ == '__main__':
    main()