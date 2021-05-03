from tvb.simulator.models.stefanescu_jirsa import ReducedSetHindmarshRose
from tvb.simulator.lab import *
import warnings
import numpy as np
import argparse
import pandas as pd
import time
import logging


def tvb_simulation(file, go):
    my_rng = np.random.RandomState(seed=42)
    oscillator = ReducedSetHindmarshRose()
    white_matter = connectivity.Connectivity.from_file(file)
    oscillator.variables_of_interest = ["xi"]
    white_matter.speed = np.array([speed])
    white_matter_coupling = coupling.Linear(a=go)
    # if the sampling hz is 81920, dt = 0.01220703125
    # if the sampling hz is 208, dt = 4.8076923076923
    heunint = integrators.HeunStochastic(dt= 0.01220703125, noise=noise.Additive(nsig=np.array([1.0]), ntau=0.0,
                                                                                random_stream=my_rng))
    monitors_Bold = (monitors.Bold(hrf_kernel = equations.Gamma(), period = 2000.0), 
                    monitors.TemporalAverage(period=1.0),
                    monitors.ProgressLogger(period = 1e3))
    sim = simulator.Simulator(model=oscillator, connectivity=white_matter, coupling=white_matter_coupling,
                              integrator=heunint, monitors=monitors_Bold, simulation_length=(10**4))
    sim.configure()

    (bold_time, bold_data), (tavg_time, tavg_data), _ = sim.run()

    #plt.figure(figsize=(10,5))
    #plt.plot(bold_time * ( 10**(-3) ), bold_data[:,0,:,0], alpha = 0.3)
    #plt.title("BOLD signals of limbic areas")
    #plt.xlabel("Time (s)")
    #plt.grid(True)
    #plt.show()
    return bold_data




speed = 10.

bash obtain the input
parser = argparse.ArgumentParser(description='pass a float')
parser.add_argument('float',type=float, help='the number')
args = parser.parse_args()
y = args.float

if __name__ == "__main__":
    #test_file = '/home/wayne/0306A.zip'
    test_file = '/home/yxw190015/go/'
    #test_file = 'C:/onedrive/OneDrive - The University of Texas at Dallas/AUS-76-DATASET/ALL_Structure_category/Joelle_normalized/AD/dd/0306A.zip'
    start_time = time.time()
    raw = tvb_simulation(test_file, np.array([y]))
    end_time = time.time()
    logging.warning('Duration: {}'.format(end_time - start_time))


