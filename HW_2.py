from xml.dom import minidom
import sys
import time
import csv
import matrixops
import copy

xml = minidom.parse(sys.argv[1])
data = xml.getElementsByTagName('net')
num_of_vertex = len(data)

d = [float('Inf')] * num_of_vertex
for i in range(num_of_vertex):
    d[i] = [float('Inf')] * num_of_vertex
for i in range(num_of_vertex):
    d[i][i] = 0


def div(a, b):
    if b == 0:
        return float('Inf')
    else:
        return a / b

data = xml.getElementsByTagName('diode')
for s in data:
    u = int(s.attributes['net_from'].value)
    v = int(s.attributes['net_to'].value)
    d[u-1][v-1] = div(1.,
                      div(1.,
                          d[u-1][v-1]) +
                      div(1.,
                          float(s.attributes['resistance'].value)))
    d[v-1][u-1] = div(1.,
                      div(1.,
                          d[v-1][u-1]) +
                      div(1., float(s.attributes
                                    ['reverse_resistance'].value)))

data = xml.getElementsByTagName('resistor')
for s in data:
    u = int(s.attributes['net_from'].value)
    v = int(s.attributes['net_to'].value)
    d[u-1][v-1] = div(1.,
                      div(1.,
                          d[u-1][v-1]) +
                      div(1.,
                          float(s.attributes['resistance'].value)))
    d[v-1][u-1] = div(1.,
                      div(1.,
                          d[v-1][u-1]) +
                      div(1.,
                          float(s.attributes['resistance'].value)))

data = xml.getElementsByTagName('capactor')
for s in data:
    u = int(s.attributes['net_from'].value)
    v = int(s.attributes['net_to'].value)
    d[u-1][v-1] = div(1.,
                      div(1.,
                          d[u-1][v-1]) +
                      div(1., float(s.attributes['resistance'].value)))
    d[v-1][u-1] = div(1.,
                      div(1.,
                          d[v-1][u-1]) +
                      div(1., float(s.attributes['resistance'].value)))

d_c = copy.deepcopy(d);

sp_time = time.clock()
for k in range(num_of_vertex):
    for i in range(num_of_vertex):
        for j in range(num_of_vertex):
            d[i][j] = div(1., div(1., d[i][j]) +
                          div(1., d[i][k] + d[k][j]))
ep_time = time.clock()
t_python = 1000. * (ep_time - sp_time)

sc_time = time.clock()
res = matrixops.F_W(d_c);
ec_time = time.clock()
t_c = 1000. * (ec_time - sc_time)

print('%.6f' % (t_python / t_c))

f = open(sys.argv[2], 'w')
for r in d:
    for el in r:
        f.write('%.6f,' % el)
    f.write('\n')
f.close


