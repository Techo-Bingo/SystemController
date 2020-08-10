

import numpy
import matplotlib.pyplot as plot
#data = numpy.array([[1312, 99, 553],
#                    [112, 1935, 0]])
data = numpy.array([[1312, 112],
                    [99, 1935],
                    [553, 0]])
color_list = ['red', 'green', 'grey', 'blue', 'magenta']
label_list = ['Used', 'Free', 'Buff/Cache']
x_list = ['Memory', 'Swap']

for i in range(len(label_list)):
    S = numpy.sum(data[:i], axis = 0)
    plot.bar(x_list, data[i], bottom = S, label=label_list[i], color = color_list[i % len(label_list)])
plot.legend(loc="upper left")
plot.show()
