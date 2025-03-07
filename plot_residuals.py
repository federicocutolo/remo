import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
def plot_residuals(sample):
    print(os.getcwd())
    rows = range(3, 1700000)
    cols = range(1, 5)
    df = pd.read_csv(f'samples/sample_{sample:04d}/output/L2_convergence_NS_NLTE.dat', 
                     delim_whitespace=True, skiprows=lambda x: x not in rows, 
                     usecols=cols)
    data = df.to_numpy()
    plt.figure()
    plt.plot(data)
    plt.grid(linestyle = ':', linewidth = 0.8)
    plt.xlabel(r'$iter$')
    plt.ylabel(r'$E$')
    labels = [r'res_1', 'res_2', 'res_3', 'res_4']
    plt.legend(labels, loc=1)
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 plot_residuals.py <sample_number>")
    else:
        sample_number = int(sys.argv[1])
        plot_residuals(sample_number)
