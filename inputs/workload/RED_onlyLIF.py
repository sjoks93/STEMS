


workload = {    
   12: {  
        "operator_type": "Conv",
        "equation": "O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][iy][ix]",
        "dimension_relations": ["ix=ox+2*fx", "iy=oy+2*fy"],
        "loop_dim_size": {
            "B": 1,
            "K": 256,
            "C": 128,
            "OY": 45,
            "OX": 80,
            "FY": 3,
            "FX": 3,
            #"C": "16"
        },
        "operand_precision": {"V": 8, "O": 1, "W": 4, "I": 1},
        #"operand_precision": {"O_final": 8, "O": 16, "W": 8, "I": 8},
        "operand_source": {"W": [], "I": []},
        "operand_state": {"V": []},
        "constant_operands": ["W", "I"],
        "state": True,
        #"sparse": False,
        #"i_rate": 0.05,
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2', 'V': 'S'},
        "input_path": 'max_7.npy',
    },
   13: {  
        "operator_type": "Conv",
        "equation": "O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][iy][ix]",
        "dimension_relations": ["ix=ox+2*fx", "iy=oy+2*fy"],
        "loop_dim_size": {
            "B": 1,
            "K": 256,
            "C": 256,
            "OY": 23,
            "OX": 40,
            "FY": 3,
            "FX": 3,
            #"C": "16"
        },
        "operand_precision": {"V": 8, "O": 1, "W": 4, "I": 1},
        #"operand_precision": {"O_final": 8, "O": 16, "W": 8, "I": 8},
        "operand_source": {"W": [], "I": [12]},
        "operand_state": {"V": []},
        "constant_operands": ["W"],
        "state": True,
        #"sparse": False,
        #"i_rate": 0.05,
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2', 'V': 'S'},
        "input_path": 'max_8.npy',
    },
   14: {  
        "operator_type": "Conv",
        "equation": "O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][iy][ix]",
        "dimension_relations": ["ix=ox+2*fx", "iy=oy+2*fy"],
        "loop_dim_size": {
            "B": 1,
            "K": 256,
            "C": 256,
            "OY": 12,
            "OX": 20,
            "FY": 3,
            "FX": 3,
            #"C": "16"
        },
        "operand_precision": {"V": 8, "O": 1, "W": 4, "I": 1},
        #"operand_precision": {"O_final": 8, "O": 16, "W": 8, "I": 8},
        "operand_source": {"W": [], "I": [13]},
        "operand_state": {"V": []},
        "constant_operands": ["W"],
        "state": True,
        #"sparse": False,
        #"i_rate": 0.05,
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2', 'V': 'S'},
        "input_path": 'max_9.npy',

    },
   15: {  
        "operator_type": "Conv",
        "equation": "O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][iy][ix]",
        "dimension_relations": ["ix=ox+2*fx", "iy=oy+2*fy"],
        "loop_dim_size": {
            "B": 1,
            "K": 256,
            "C": 256,
            "OY": 6,
            "OX": 10,
            "FY": 3,
            "FX": 3,
            #"C": "16"
        },
        "operand_precision": {"V": 8, "O": 1, "W": 4, "I": 1},
        #"operand_precision": {"O_final": 8, "O": 16, "W": 8, "I": 8},
        "operand_source": {"W": [], "I": [14]},
        "operand_state": {"V": []},
        "constant_operands": ["W"],
        "state": True,
        #"sparse": False,
        #"i_rate": 0.05,
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2', 'V': 'S'},
        "input_path": 'max_10.npy',
    },
   16: {  
        "operator_type": "Conv",
        "equation": "O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][iy][ix]",
        "dimension_relations": ["ix=ox+2*fx", "iy=oy+2*fy"],
        "loop_dim_size": {
            "B": 1,
            "K": 256,
            "C": 256,
            "OY": 5,
            "OX": 3,
            "FY": 3,
            "FX": 3,
            #"C": "16"
        },
        "operand_precision": {"V": 8, "O": 1, "W": 4, "I": 1},
        #"operand_precision": {"O_final": 8, "O": 16, "W": 8, "I": 8},
        "operand_source": {"W": [], "I": [15]},
        "operand_state": {"V": []},
        "constant_operands": ["W"],
        "state": True,
        #"sparse": False,
        #"i_rate": 0.05,
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2', 'V': 'S'},
        "input_path": 'max_11.npy',

    },                
     
}
''''
I:(6, 360, 640)
0:(32, 180, 320)
1:(64, 180, 320)
2:(64, 90, 160)
3:(64, 90, 160)
7:(64, 90, 160)
5:(128, 90, 160)
6:(128, 90, 160)
7:(256, 45, 80)
(256, 23, 40)
(256, 12, 20)
(256, 6, 10)
(256, 3, 5)
'''''