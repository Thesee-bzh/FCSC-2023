import matplotlib.pyplot as plt
import csv
  
y = []
  
with open('trace_admin.csv','r') as csvfile:
    plots = csv.reader(csvfile)
      
    for row in plots:
        y.append(float(row[0][:-4]))
  
plt.plot(y[1500:])
plt.show()
