workload = {
    9: {  
        "operator_type": "Conv",
        "equation": "O[t][b][k][oy][ox]+=W[k][c][fy][fx]*I[t][b][c][iy][ix]",
        "dimension_relations": ["ix=1*ox+1*fx", "iy=1*oy+1*fy"],
        "loop_dim_size": {
            "T": 16,
            "B": 1,
            "K": 64,
            "C": 64,
            "OY": 32,
            "OX": 32,
            "FY": 3,
            "FX": 3,
        },
        "operand_precision": {"V": 12, "O": 1, "W": 4, "I": 1},
        "operand_source": {"W": [], "I": []},
        "constant_operands": ["W", "I"],
        "state": True,
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2', 'V': 'S'},
        'weight_operand': "W",
        'time_operand': "T",
        "input_path": 'data/SEW_7PLIF/7PLIF_max_t_5.npy',
        # acc_count = 603,979,776
        "cut_block": 2,

    },  
}
