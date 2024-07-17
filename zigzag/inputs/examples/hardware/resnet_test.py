workload = {
    4: {  # Addition of layer 1 (residual path) and layer 3 (main path)
        "operator_type": "Add",
        "equation": "O[b][g][oy][ox]=X[b][g][oy][ox]+Y[b][g][oy][ox]",
        "dimension_relations": [],
        "loop_dim_size": {"B": 1, "G": 64, "OY": 56, "OX": 56},
        "operand_precision": {"O": 16, "O_final": 8, "X": 8, "Y": 8},
        "operand_source": {"X": [1], "Y": [3]},
        "constant_operands": [],
        "operand_source_dimension_mapping": {
            "X": {"OX": "OX", "OY": "OY", "G": "K"},
            "Y": {"OX": "OX", "OY": "OY", "G": "K"},
        },
    }
}