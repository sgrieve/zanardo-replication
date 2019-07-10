import matplotlib.pyplot as plt
import tokunaga_fns as toku
from glob import glob
import csv
import numpy as np
from sklearn.linear_model import LinearRegression

file_list = glob('/Users/stuart/zanardo-replication/data/TokunagaData_*_*.csv')

precip = {}

with open('/Users/stuart/zanardo-replication/supplement/precip_lookup.csv') as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)
    next(reader, None)
    for row in reader:
        precip[int(row[0]) - 1] = float(row[1])

Cs = {}

for q in range(50):
    Cs[q] = []

for filename in file_list:

    toku_data, strahler_data, _ = toku.read_toku_data(filename)

    basin_id = int(filename.split('TokunagaData_buffer_')[1][:-6])

    r_sq, a, c = toku.fit_a_and_c(toku_data, strahler_data)
    threshold = 0.8
    if r_sq > threshold:
        Cs[basin_id].append(c)

x = []
y = []

for key, value in Cs.items():
    if value:
        x.append(np.mean(value))
        y.append(precip[key])

plt.scatter(x, y, s=25, alpha=0.6, c='k', linewidth=0)

x = np.array(x).reshape(len(x), 1)
y = np.array(y).reshape(len(y), 1)

model = LinearRegression()
model.fit(x, y)

x_new = np.linspace(1.8, 3.5, 100)
y_new = model.predict(x_new[:, np.newaxis])

residuals = np.array(y) - model.predict(x)
ss_res = np.sum(residuals**2)
ss_tot = np.sum((y - np.mean(y))**2)
r_squared = 1 - (ss_res / ss_tot)

print(r_squared)

plt.plot(x_new, y_new, 'r--')

plt.title('Confidence threshold: {}'.format(threshold))
# plt.xlim(0, 7)
plt.xlabel('c')
plt.ylabel('Mean annual precipitation ($mm yr^{-1}$)')

plt.show()

# plt.savefig('precip_c_{}.png'.format(threshold))
