from sqlite_mps import *
from qtn_sim import *
from myCircuitAdapter import *
import time, tracemalloc

def getTimeMemory(simulator, circuit):
    start = time.perf_counter_ns()
    tracemalloc.start()

    simulator(circuit)

    mem = tracemalloc.get_traced_memory()

    tracemalloc.stop()

    end = time.perf_counter_ns()
    timeIt = end - start

    return timeIt, mem[1]


# rdbmsSim=SQLITE_MPS.run_circuit_json(rdbmsJson)
# # x=rdbmsSim.get_statevector_np()
# # print(x)
# npSim = QuantumMPS(n)
# npSim.applyCircuit(myGHZ)
# # print(np.ravel(q.convert_To_One_Tensor()))

n = 2000
myGHZ = GHZCircuit(n)
rdbmsJson = change(n, myGHZ)

print("RDBMS\t")
print(getTimeMemory(SQLITE_MPS.run_circuit_json, rdbmsJson))
print("\nNumpy\t")
print(getTimeMemory(QuantumMPS(n).applyCircuit, myGHZ))


rdbmsTime = []
rdbmsMemory = []

numpyTime = []
numpyMemory = []

x = [i for i in range(1,200)]

for i in x:
    myGHZ = GHZCircuit(i)
    rdbmsJson = change(i, myGHZ)

    rdbms = getTimeMemory(SQLITE_MPS.run_circuit_json, rdbmsJson)
    numpyMps = getTimeMemory(QuantumMPS(i).applyCircuit, myGHZ)

    rdbmsTime.append(rdbms[0])
    rdbmsMemory.append(rdbms[1])

    numpyTime.append(numpyMps[0])
    numpyMemory.append(numpyMps[1])

    print(i)


# plot


t1 = "Execution time"
t2 = "Memory usage"

ylabel1 = "Time (ns)"
ylabel2 = "Memory (bytes)"

fig = plt.figure()
fig.suptitle("RDBMS vs Numpy Tensor Native GHZ")
ax1 = fig.add_subplot(1,2,1)
ax2 = fig.add_subplot(1,2,2)

ax1.set_title(t1)
ax1.set_xlabel("Number of Qubits")
ax1.set_ylabel(ylabel1)

ax2.set_title(t2)
ax2.set_xlabel("Number of Qubits")
ax2.set_ylabel(ylabel2)

ax1.scatter(x,rdbmsTime,label="RDBMS")
ax2.scatter(x,rdbmsMemory,label="RDBMS")

ax1.scatter(x,numpyTime,label="Numpy")
ax2.scatter(x,numpyMemory,label="Numpy")

ax1.legend(loc="upper left")
ax2.legend(loc="upper left")

plt.show()