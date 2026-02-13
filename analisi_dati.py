'''
acc x
acc y
acc z
gyro x
gyro y
gyro z
temp ((sen55+scd40)/2)
temp sen55
temp internal (cpu)
temp probe
'''
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def main():

    columns = [
        'extra_1', 'result', 'table', 'start', 'stop', 
        'time', 'value', 'field', 'measurement', 'domain', 'sensor_id'
    ]
    
    lines  = pd.read_csv(
        'log_monitoraggio_25-07-2022.csv',
        names=columns,
        parse_dates=['time'],
        comment='#',
        skipinitialspace=True,
        dtype={'value': float}
    )


    acc_x_lines = lines[lines['table'] == '0']
    acc_y_lines = lines[lines['table'] == '1']
    acc_z_lines = lines[lines['table'] == '2']
    gyro_x_lines = lines[lines['table'] == '3']
    gyro_y_lines = lines[lines['table'] == '4']
    gyro_z_lines = lines[lines['table'] == '5']
    temp_lines = lines[lines['table'] == '6']
    temp_sen55_lines = lines[lines['table'] == '7']
    temp_cpu_lines = lines[lines['table'] == '8']
    temp_probe_lines = lines[lines['table'] == '9']

    print(acc_x_lines[['time']])

    fig, acc_x = plt.subplots()
    acc_x.plot(acc_x_lines['time'], acc_x_lines['value'])
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()