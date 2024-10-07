import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def extract_branch_pred_values(file_path):
    lookups_total, TakenMispredicted, NotTakenMispredicted = None, None, None
    predictedBranches, predictedTakenIncorrect, predictedNotTakenIncorrect = None, None, None
    iew_branchMispredicts, commit_branchMispredicts = None, None
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('system.cpu.branchPred.lookups_0::total'):
                lookups_total = int(line.split()[1])
            elif line.startswith('system.cpu.branchPred.TakenMispredicted'):
                TakenMispredicted = int(line.split()[1])
            elif line.startswith('system.cpu.branchPred.NotTakenMispredicted'):
                NotTakenMispredicted = int(line.split()[1])
            elif line.startswith('system.cpu.fetch.predictedBranches'):
                predictedBranches = int(line.split()[1])
            elif line.startswith('system.cpu.iew.predictedTakenIncorrect'):
                predictedTakenIncorrect = int(line.split()[1])
            elif line.startswith('system.cpu.iew.predictedNotTakenIncorrect'):
                predictedNotTakenIncorrect = int(line.split()[1])
            elif line.startswith('system.cpu.iew.branchMispredicts'):
                iew_branchMispredicts = int(line.split()[1])
            elif line.startswith('system.cpu.commit.branchMispredicts'):
                commit_branchMispredicts = int(line.split()[1])
    return (lookups_total, TakenMispredicted, NotTakenMispredicted, 
            predictedBranches, predictedTakenIncorrect, predictedNotTakenIncorrect, 
            iew_branchMispredicts, commit_branchMispredicts)

def process_directory(base_dir, index):
    stats_file = os.path.join(base_dir, str(index), 'stats.txt')
    
    if os.path.isfile(stats_file):
        return extract_branch_pred_values(stats_file)
    else:
        return (None, None, None, None, None, None, None, None)

def plot_histograms(values, labels, y_axis_val, output_dir):
    # Use the updated colormap function
    cmap = plt.colormaps.get_cmap('tab20')  
    num_colors = len(labels)
    colors = [cmap(i / num_colors) for i in range(num_colors)]  # Generate colors

    plt.figure(figsize=(12, 7))
    
    bar_width = 0.5
    index = np.arange(len(labels))
    
    bars = plt.bar(index, values, bar_width, color=colors, edgecolor='black')
    
    plt.xlabel('')  # Remove x-axis label
    plt.ylabel(y_axis_val)
    plt.title(f'{y_axis_val} Distribution')
    plt.xticks(index, labels, rotation=0)  # Ensure x-tick labels are straight
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    
    # Add exact values on top of each bar
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval, int(yval), va='bottom', ha='center', fontsize=10, color='black')
    
    plt.tight_layout()
    
    output_path = os.path.join(output_dir, f'{y_axis_val}_histogram.png')
    plt.savefig(output_path)
    plt.close()

def create_summary_table(data, output_dir):
    df = pd.DataFrame(data)
    output_path = os.path.join(output_dir, 'summary_table.csv')
    df.to_csv(output_path, index=False)

def main():
    base_dir = './gen_outputs'
    output_dir = './gen_graphs'
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    data = {
        'Branch Predictor': [],
        'Lookups Total': [],
        'Taken Mispredicted': [],
        'Not Taken Mispredicted': [],
        'Predicted Branches': [],
        'Predicted Taken Incorrect': [],
        'Predicted Not Taken Incorrect': [],
        'IEW Branch Mispredicts': [],
        'Commit Branch Mispredicts': []
    }
    
    mpp = {
        1: "LocalBP", 
        2: "TournamentBP",
        3: "BiModeBP", 
        4: "MultiperspectivePerceptronTAGE64KB", 
        5: "TAGE"
    }

    for (ind, bps) in mpp.items():
        # print(f'Analyzing BP - {bps}:')
        
        lookups_total, TakenMispredicted, NotTakenMispredicted, predictedBranches, predictedTakenIncorrect, predictedNotTakenIncorrect, iew_branchMispredicts, commit_branchMispredicts = process_directory(base_dir, ind)
        
        # print("Number of BP lookups:", lookups_total)
        # print("Number branches predicted taken but are actually not taken:", TakenMispredicted)
        # print("Number branches predicted 'not taken' but turned out to be taken:", NotTakenMispredicted)
        # print("Number of branches that fetch has predicted taken:", predictedBranches)
        # print("Number of branches that were predicted taken incorrectly:", predictedTakenIncorrect)
        # print("Number of branches that were predicted not taken incorrectly:", predictedNotTakenIncorrect)
        # print("Number of branch mispredicts detected at execute:", iew_branchMispredicts)
        # print("Number of branch mispredicts detected at commit:", commit_branchMispredicts)
        
        data['Branch Predictor'].append(bps)
        data['Lookups Total'].append(lookups_total)
        data['Taken Mispredicted'].append(TakenMispredicted)
        data['Not Taken Mispredicted'].append(NotTakenMispredicted)
        data['Predicted Branches'].append(predictedBranches)
        data['Predicted Taken Incorrect'].append(predictedTakenIncorrect)
        data['Predicted Not Taken Incorrect'].append(predictedNotTakenIncorrect)
        data['IEW Branch Mispredicts'].append(iew_branchMispredicts)
        data['Commit Branch Mispredicts'].append(commit_branchMispredicts)
    
    for metric in ['Lookups Total', 'Taken Mispredicted', 'Not Taken Mispredicted', 'Predicted Branches', 'Predicted Taken Incorrect', 'Predicted Not Taken Incorrect', 'IEW Branch Mispredicts', 'Commit Branch Mispredicts']:
        values = data[metric]
        plot_histograms(values, data['Branch Predictor'], metric, output_dir)
    
    create_summary_table(data, output_dir)

if __name__ == '__main__':
    main()