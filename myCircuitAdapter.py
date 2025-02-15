import json
from qtn_sim import *

file=open("./circuit.json")
circuit=json.load(file)



def change(n, circuit: QCircuit):
    
    gateList = []


    for (gate, indices) in circuit.gateList:
        gateList.append({
            "qubits":indices,
            "gate":gate.id
        })

    json = {
        "number_of_qubits": n,
        "gates": gateList
    }

    return json