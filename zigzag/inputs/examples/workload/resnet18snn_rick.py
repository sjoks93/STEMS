workload = {
    0: {  # conv1, stride 2
        "operator_type": "Conv",
        "equation": "O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][iy][ix]",
        "dimension_relations": ["ox=ix-1*fx", "oy=iy-1*fy"],
        "loop_dim_size": {
            "B": 1,
            "K": 64,
            "C": 32,
            "IY": 784,
            "IX": 784,
            "FY": 3,
            "FX": 3,
            #"C": "16"
        },
        "operand_precision": {"V": 8, "O": 1, "W": 4, "I": 1},
        #"operand_precision": {"O_final": 8, "O": 16, "W": 8, "I": 8},
        "operand_source": {"W": [], "I": []},
        "operand_state": {"V": []},
        "constant_operands": ["I", "W"],
        "state": True,
        "sparse": False,
        "i_rate": 0.05,
    },
}
