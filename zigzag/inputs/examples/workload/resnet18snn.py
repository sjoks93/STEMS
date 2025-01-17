workload = {
    0: {  
        "operator_type": "Conv",
        "equation": "O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][iy][ix]",
        "dimension_relations": ["ix=2*ox+1*fx", "iy=2*oy+1*fy"],
        "loop_dim_size": {
            "B": 1,
            "K": 265,
            "C": 256,
            "OY": 1000,
            "OX": 1000,
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
        "input_path": 'test.npy',
    },

    # 1: {  # conv1, stride 2
    #     "operator_type": "Conv",
    #     "equation": "O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][iy][ix]",
    #     "dimension_relations": ["ix=2*ox+1*fx", "iy=2*oy+1*fy"],
    #     "loop_dim_size": {
    #         "B": 1,
    #         "K": 32,
    #         "C": 64,
    #         "OY": 784,
    #         "OX": 784,
    #         "FY": 7,
    #         "FX": 7,
    #         #"C": "16"
    #     },
    #     "operand_precision": {"V": 8, "O": 1, "W": 4, "I": 1},
    #     #"operand_precision": {"O_final": 8, "O": 16, "W": 8, "I": 8},
    #     "operand_source": {"W": [], "I": []},
    #     "operand_state": {"V": []},
    #     "constant_operands": ["I", "W"],
    #     "state": True,
    #     "sparse": False,
    #     "i_rate": 0.05,
    # },    
}
