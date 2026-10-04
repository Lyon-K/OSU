import matplotlib.pyplot as plt
import csv

def plot(filename, color, label):
    x = []
    y = []
    with open(filename,'r') as csvfile:
        plots = csv.reader(csvfile, delimiter = ',')
        for row in plots:
            x.append(float(row[0]))
            y.append(float(row[1]))
    plt.plot(x, y, color = color, label = label)


plot('C:/OSU/ECE375/hw4/files/tek0009CH1.csv', 'r', "No buttons pressed")
plot('C:/OSU/ECE375/hw4/files/tek0010CH1.csv', 'g', "PD4 pressed")
plot('C:/OSU/ECE375/hw4/files/tek0011CH1.csv', 'b', "PD5 pressed")
# plot('tek0003CH2.csv', 'y', "all buttons pressed")
plt.xlabel('TIME (s)')
plt.ylabel('Voltage (V)')
plt.title("Lab 1's Graph of voltage against time")
plt.legend()