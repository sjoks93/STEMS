


workload = {
    0: {  
        "operator_type": "Conv",
        "equation": "O[t][b][k][oy][ox]+=W[k][c][fy][fx]*I[t][b][c][iy][ix]",
        "dimension_relations": ["ix=1*ox+1*fx", "iy=1*oy+1*fy"],
        "loop_dim_size": {
            "T": 16,
            "B": 1,
            "K": 64,
            "C": 2,
            "OY": 128,
            "OX": 128,
            "FY": 1,
            "FX": 1,
        },
        "operand_precision": {"O": 12, "O_final": 1, "W": 4, "I": 4},
        "operand_source": {"W": [], "I": []},
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'},
        'weight_operand': "W",
        "constant_operands": ["I", "W"],
        "state": False,
        'time_operand': "T",
        "input_path": 'data/sew_4PLIF/4PLIF_max_t_0.npy',

    },
    1: {  
        "operator_type": "Conv",
        "equation": "O[t][b][k][oy][ox]+=W[k][c][fy][fx]*I[t][b][c][iy][ix]",
        "dimension_relations": ["ix=1*ox+1*fx", "iy=1*oy+1*fy"],
        "loop_dim_size": {
            "T": 16,
            "B": 1,
            "K": 64,
            "C": 64,
            "OY": 128,
            "OX": 128,
            "FY": 3,
            "FX": 3,
        },
        "operand_precision": {"O": 12, "O_final": 1, "W": 4, "I": 1},
        "operand_source": {"W": [], "I": [0]},
        "constant_operands": ["W"],
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'},
        'weight_operand': "W",
        'time_operand': "T",
        "state": False,
        "input_path": 'data/sew_4PLIF/4PLIF_max_t_1.npy',

    },    
    2: {  
        "operator_type": "Conv",
        "equation": "O[t][b][k][oy][ox]+=W[k][c][fy][fx]*I[t][b][c][iy][ix]",
        "dimension_relations": ["ix=1*ox+1*fx", "iy=1*oy+1*fy"],
        "loop_dim_size": {
            "T": 16,
            "B": 1,
            "K": 64,
            "C": 64,
            "OY": 128,
            "OX": 128,
            "FY": 3,
            "FX": 3,
        },
        "operand_precision": {"O": 12, "O_final": 1, "W": 4, "I": 1},
        "operand_source": {"W": [], "I": [1]},
        "constant_operands": ["W"],
        "state": False,
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'},
        'weight_operand': "W",
        'time_operand': "T",
        "input_path": 'data/sew_4PLIF/4PLIF_max_t_2.npy',

    },      
    3: {  
        "operator_type": "Add",
        "equation": "O[t][b][g][oy][ox]+=X[t][b][g][oy][ox]+Y[t][b][g][oy][ox]",
       "dimension_relations": [],
        "loop_dim_size": {
            "T": 16,
            "B": 1,
            "G": 64,
            "OY": 128,
            "OX": 128,
        },
        'time_opreand': "T",
        "operand_precision": {"O": 1, "O_final": 1, "X": 1, "Y": 1},
        "operand_source": {"X": [2], "Y": [1]},
        "constant_operands": [],
        'memory_operand_links': {'O': 'O', 'X': 'I2', 'Y': 'I1'}
    },
    4: {  
        "operator_type": "MaxPool",
        "equation": "O[t][b][g][oy][ox]+=W[fx][fy]*I[t][b][g][iy][ix]",
        "dimension_relations": ["ix=2*ox+1*fx", "iy=2*oy+1*fy"],
        "loop_dim_size": {"T": 16, "B": 1, "G": 64, "OY": 64, "OX": 64, "FX": 3, "FY": 3},
        "operand_precision": {"O": 1, "O_final": 1, "I": 1, "W": 0},
        "operand_source": {"W": [], "I": [3]},
        "constant_operands": ["W"],
        'time_operand': "T",
        "operand_source_dimension_mapping": {"I": {"IX": "OX", "IY": "OY", "G": "K"}},
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'},

    },

    5: {  
        "operator_type": "Conv",
        "equation": "O[t][b][k][oy][ox]+=W[k][c][fy][fx]*I[t][b][c][iy][ix]",
        "dimension_relations": ["ix=1*ox+1*fx", "iy=1*oy+1*fy"],
        "loop_dim_size": {
            "T": 16,
            "B": 1,
            "K": 64,
            "C": 64,
            "OY": 64,
            "OX": 64,
            "FY": 3,
            "FX": 3,
        },
        "operand_precision": {"O": 12, "O_final": 1, "W": 4, "I": 1},
        "operand_source": {"W": [], "I": [4]},
        "constant_operands": ["W"],
        "state": False,
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'},
        'weight_operand': "W",
        'time_operand': "T",
        "input_path": 'data/sew_4PLIF/4PLIF_max_t_3.npy',

    },    
    6: {  
        "operator_type": "Conv",
        "equation": "O[t][b][k][oy][ox]+=W[k][c][fy][fx]*I[t][b][c][iy][ix]",
        "dimension_relations": ["ix=1*ox+1*fx", "iy=1*oy+1*fy"],
        "loop_dim_size": {
            "T": 16,
            "B": 1,
            "K": 64,
            "C": 64,
            "OY": 64,
            "OX": 64,
            "FY": 3,
            "FX": 3,
        },
        "operand_precision": {"O": 12, "O_final": 1, "W": 4, "I": 1},
        "operand_source": {"W": [], "I": [5]},
        "constant_operands": ["W"],
        "state": False,
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'},
        'weight_operand': "W",
        'time_operand': "T",
        "input_path": 'data/sew_4PLIF/4PLIF_max_t_4.npy',

    },      
    7: {  
        "operator_type": "Add",
        "equation": "O[t][b][g][oy][ox]+=X[t][b][g][oy][ox]+Y[t][b][g][oy][ox]",
       "dimension_relations": [],
        "loop_dim_size": {
            "T": 16,
            "B": 1,
            "G": 64,
            "OY": 64,
            "OX": 64,
        },
        'time_opreand': "T",
        "operand_precision": {"O": 1, "O_final": 1, "X": 1, "Y": 1},
        "operand_source": {"X": [6], "Y": [5]},
        "constant_operands": [],
        'memory_operand_links': {'O': 'O', 'X': 'I2', 'Y': 'I1'}
    },
    8: {  
        "operator_type": "MaxPool",
        "equation": "O[t][b][g][oy][ox]+=W[fx][fy]*I[t][b][g][iy][ix]",
        "dimension_relations": ["ix=2*ox+1*fx", "iy=2*oy+1*fy"],
        "loop_dim_size": {"T": 16, "B": 1, "G": 64, "OY": 32, "OX": 32, "FX": 3, "FY": 3},
        "operand_precision": {"O": 1, "O_final": 1, "I": 1, "W": 0},
        "operand_source": {"W": [], "I": [7]},
        "constant_operands": ["W"],
        'time_operand': "T",
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'},
        "operand_source_dimension_mapping": {"I": {"IX": "OX", "IY": "OY", "G": "K"}},

    },

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
        "operand_precision": {"O": 12, "O_final": 1, "W": 4, "I": 1},
        "operand_source": {"W": [], "I": [8]},
        "constant_operands": ["W"],
        "state": False,
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'},
        'weight_operand': "W",
        'time_operand': "T",
        "input_path": 'data/sew_4PLIF/4PLIF_max_t_5.npy',

    },    
    10: {  
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
        "operand_precision": {"O": 12, "O_final": 1, "W": 4, "I": 1},
        "operand_source": {"W": [], "I": [9]},
        "constant_operands": ["W"],
        "state": False,
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'},
        'weight_operand': "W",
        'time_operand': "T",
        "input_path": 'data/sew_4PLIF/4PLIF_max_t_6.npy',

    },      
    11: {  
        "operator_type": "Add",
        "equation": "O[t][b][g][oy][ox]+=X[t][b][g][oy][ox]+Y[t][b][g][oy][ox]",
       "dimension_relations": [],
        "loop_dim_size": {
            "T": 16,
            "B": 1,
            "G": 64,
            "OY": 32,
            "OX": 32,
        },
        'time_opreand': "T",
        "operand_precision": {"O": 1, "O_final": 1, "X": 1, "Y": 1},
        "operand_source": {"X": [10], "Y": [9]},
        "constant_operands": [],
        'memory_operand_links': {'O': 'O', 'X': 'I2', 'Y': 'I1'}
    },
    12: {  
        "operator_type": "MaxPool",
        "equation": "O[t][b][g][oy][ox]+=W[fx][fy]*I[t][b][g][iy][ix]",
        "dimension_relations": ["ix=2*ox+1*fx", "iy=2*oy+1*fy"],
        "loop_dim_size": {"T": 16, "B": 1, "G": 64, "OY": 16, "OX": 16, "FX": 3, "FY": 3},
        "operand_precision": {"O": 1, "O_final": 1, "I": 1, "W": 0},
        "operand_source": {"W": [], "I": [11]},
        "constant_operands": ["W"],
        'time_operand': "T",
        "operand_source_dimension_mapping": {"I": {"IX": "OX", "IY": "OY", "G": "K"}},
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'},

    },

    13: {  
        "operator_type": "Conv",
        "equation": "O[t][b][k][oy][ox]+=W[k][c][fy][fx]*I[t][b][c][iy][ix]",
        "dimension_relations": ["ix=1*ox+1*fx", "iy=1*oy+1*fy"],
        "loop_dim_size": {
            "T": 16,
            "B": 1,
            "K": 64,
            "C": 64,
            "OY": 16,
            "OX": 16,
            "FY": 3,
            "FX": 3,
        },
        "operand_precision": {"V": 12, "O": 1, "W": 4, "I": 1},
        "operand_source": {"W": [], "I": [12]},
        "constant_operands": ["W"],
        "state": True,
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2', 'V': 'S'},
        'weight_operand': "W",
        'time_operand': "T",
        "input_path": 'data/sew_4PLIF/4PLIF_max_t_7.npy',

    },    
    14: {  
        "operator_type": "Conv",
        "equation": "O[t][b][k][oy][ox]+=W[k][c][fy][fx]*I[t][b][c][iy][ix]",
        "dimension_relations": ["ix=1*ox+1*fx", "iy=1*oy+1*fy"],
        "loop_dim_size": {
            "T": 16,
            "B": 1,
            "K": 64,
            "C": 64,
            "OY": 16,
            "OX": 16,
            "FY": 3,
            "FX": 3,
        },
        "operand_precision": {"V": 12, "O": 1, "W": 4, "I": 1},
        "operand_source": {"W": [], "I": [13]},
        "constant_operands": ["W"],
        "state": True,
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2', 'V': 'S'},
        'weight_operand': "W",
        'time_operand': "T",
        "input_path": 'data/sew_4PLIF/4PLIF_max_t_8.npy',

    },      
    15: {  
        "operator_type": "Add",
        "equation": "O[t][b][g][oy][ox]+=X[t][b][g][oy][ox]+Y[t][b][g][oy][ox]",
       "dimension_relations": [],
        "loop_dim_size": {
            "T": 16,
            "B": 1,
            "G": 64,
            "OY": 16,
            "OX": 16,
        },
        'time_opreand': "T",
        "operand_precision": {"O": 1, "O_final": 1, "X": 1, "Y": 1},
        "operand_source": {"X": [14], "Y": [13]},
        "constant_operands": [],
        'memory_operand_links': {'O': 'O', 'X': 'I2', 'Y': 'I1'}
    },
    16: {  
        "operator_type": "MaxPool",
        "equation": "O[t][b][g][oy][ox]+=W[fx][fy]*I[t][b][g][iy][ix]",
        "dimension_relations": ["ix=2*ox+1*fx", "iy=2*oy+1*fy"],
        "loop_dim_size": {"T": 16, "B": 1, "G": 64, "OY": 8, "OX": 8, "FX": 3, "FY": 3},
        "operand_precision": {"O": 1, "O_final": 1, "I": 1, "W": 0},
        "operand_source": {"W": [], "I": [15]},
        "constant_operands": ["W"],
        'time_operand': "T",
        "operand_source_dimension_mapping": {"I": {"IX": "OX", "IY": "OY", "G": "K"}},
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'},

    },

    17: {  
        "operator_type": "Conv",
        "equation": "O[t][b][k][oy][ox]+=W[k][c][fy][fx]*I[t][b][c][iy][ix]",
        "dimension_relations": ["ix=1*ox+1*fx", "iy=1*oy+1*fy"],
        "loop_dim_size": {
            "T": 16,
            "B": 1,
            "K": 128,
            "C": 64,
            "OY": 8,
            "OX": 8,
            "FY": 1,
            "FX": 1,
        },
        "operand_precision": {"V": 12, "O": 1, "W": 4, "I": 1},
        "operand_source": {"W": [], "I": [16]},
        "constant_operands": ["W"],
        "state": True,
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2', 'V': 'S'},
        'weight_operand': "W",
        'time_operand': "T",
        "input_path": 'data/sew_4PLIF/4PLIF_max_t_9.npy',
    }, 
    18: {  
        "operator_type": "Conv",
        "equation": "O[t][b][k][oy][ox]+=W[k][c][fy][fx]*I[t][b][c][iy][ix]",
        "dimension_relations": ["ix=1*ox+1*fx", "iy=1*oy+1*fy"],
        "loop_dim_size": {
            "T": 16,
            "B": 1,
            "K": 128,
            "C": 128,
            "OY": 8,
            "OX": 8,
            "FY": 3,
            "FX": 3,
        },
        "operand_precision": {"V": 12, "O": 1, "W": 4, "I": 1},
        "operand_source": {"W": [], "I": [17]},
        "constant_operands": ["W"],
        "state": True,
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2', 'V': 'S'},
        'weight_operand': "W",
        'time_operand': "T",
        "input_path": 'data/sew_4PLIF/4PLIF_max_t_10.npy',

    },    
    19: {  
        "operator_type": "Conv",
        "equation": "O[t][b][k][oy][ox]+=W[k][c][fy][fx]*I[t][b][c][iy][ix]",
        "dimension_relations": ["ix=1*ox+1*fx", "iy=1*oy+1*fy"],
        "loop_dim_size": {
            "T": 16,
            "B": 1,
            "K": 128,
            "C": 128,
            "OY": 8,
            "OX": 8,
            "FY": 3,
            "FX": 3,
        },
        "operand_precision": {"V": 12, "O": 1, "W": 4, "I": 1},
        "operand_source": {"W": [], "I": [18]},
        "constant_operands": ["W"],
        "state": True,
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2', 'V': 'S'},
        'weight_operand': "W",
        'time_operand': "T",
        "input_path": 'data/sew_4PLIF/4PLIF_max_t_11.npy',

    },      
    20: {  
        "operator_type": "Add",
        "equation": "O[t][b][g][oy][ox]+=X[t][b][g][oy][ox]+Y[t][b][g][oy][ox]",
       "dimension_relations": [],
        "loop_dim_size": {
            "T": 16,
            "B": 1,
            "G": 128,
            "OY": 8,
            "OX": 8,
        },
        'time_opreand': "T",
        "operand_precision": {"O": 1, "O_final": 1, "X": 1, "Y": 1},
        "operand_source": {"X": [19], "Y": [18]},
        "constant_operands": [],
        'memory_operand_links': {'O': 'O', 'X': 'I2', 'Y': 'I1'}
    },
    21: {  
        "operator_type": "MaxPool",
        "equation": "O[t][b][g][oy][ox]+=W[fx][fy]*I[t][b][g][iy][ix]",
        "dimension_relations": ["ix=2*ox+1*fx", "iy=2*oy+1*fy"],
        "loop_dim_size": {"T": 16, "B": 1, "G": 128, "OY": 4, "OX": 4, "FX": 3, "FY": 3},
        "operand_precision": {"O": 1, "O_final": 1, "I": 1, "W": 0},
        "operand_source": {"W": [], "I": [20]},
        "constant_operands": ["W"],
        'time_operand': "T",
        "operand_source_dimension_mapping": {"I": {"IX": "OX", "IY": "OY", "G": "K"}},
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'},

    },

    22: {  
        "operator_type": "Conv",
        "equation": "O[t][b][k][oy][ox]+=W[k][c][fy][fx]*I[t][b][c][iy][ix]",
        "dimension_relations": ["ix=1*ox+1*fx", "iy=1*oy+1*fy"],
        "loop_dim_size": {
            "T": 16,
            "B": 1,
            "K": 128,
            "C": 128,
            "OY": 4,
            "OX": 4,
            "FY": 3,
            "FX": 3,
        },
        "operand_precision": {"V": 12, "O": 1, "W": 4, "I": 1},
        "operand_source": {"W": [], "I": [21]},
        "constant_operands": ["W"],
        "state": True,
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2', 'V': 'S'},
        'weight_operand': "W",
        'time_operand': "T",
        "input_path": 'data/sew_4PLIF/4PLIF_max_t_12.npy',

    },    
    23: {  
        "operator_type": "Conv",
        "equation": "O[t][b][k][oy][ox]+=W[k][c][fy][fx]*I[t][b][c][iy][ix]",
        "dimension_relations": ["ix=1*ox+1*fx", "iy=1*oy+1*fy"],
        "loop_dim_size": {
            "T": 16,
            "B": 1,
            "K": 128,
            "C": 128,
            "OY": 4,
            "OX": 4,
            "FY": 3,
            "FX": 3,
        },
        "operand_precision": {"V": 12, "O": 1, "W": 4, "I": 1},
        "operand_source": {"W": [], "I": [22]},
        "constant_operands": ["W"],
        "state": True,
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2', 'V': 'S'},
        'weight_operand': "W",
        'time_operand': "T",
        "input_path": 'data/sew_4PLIF/4PLIF_max_t_13.npy',

    },      
    24: {  
        "operator_type": "Add",
        "equation": "O[t][b][g][oy][ox]+=X[t][b][g][oy][ox]+Y[t][b][g][oy][ox]",
       "dimension_relations": [],
        "loop_dim_size": {
            "T": 16,
            "B": 1,
            "G": 128,
            "OY": 4,
            "OX": 4,
        },
        'time_opreand': "T",
        "operand_precision": {"O": 1, "O_final": 1, "X": 1, "Y": 1},
        "operand_source": {"X": [23], "Y": [22]},
        "constant_operands": [],
        'memory_operand_links': {'O': 'O', 'X': 'I2', 'Y': 'I1'}
    },
    25: {  
        "operator_type": "MaxPool",
        "equation": "O[t][b][g][oy][ox]+=W[fx][fy]*I[t][b][g][iy][ix]",
        "dimension_relations": ["ix=2*ox+1*fx", "iy=2*oy+1*fy"],
        "loop_dim_size": {"T": 16, "B": 1, "G": 128, "OY": 2, "OX": 2, "FX": 3, "FY": 3},
        "operand_precision": {"O": 1, "O_final": 1, "I": 1, "W": 0},
        "operand_source": {"W": [], "I": [24]},
        "constant_operands": ["W"],
        'time_operand': "T",
        "operand_source_dimension_mapping": {"I": {"IX": "OX", "IY": "OY", "G": "K"}},
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'},

    },
    26: {  
        "operator_type": "Conv",
        "equation": "O[t][b][k][oy][ox]+=W[k][c][fy][fx]*I[t][b][c][iy][ix]",
        "dimension_relations": ["ix=1*ox+1*fx", "iy=1*oy+1*fy"],
        "loop_dim_size": {
            "T": 16,
            "B": 1,
            "K": 128,
            "C": 128,
            "OY": 2,
            "OX": 2,
            "FY": 3,
            "FX": 3,
        },
        "operand_precision": {"V": 12, "O": 1, "W": 4, "I": 1},
        "operand_source": {"W": [], "I": [25]},
        "constant_operands": ["W"],
        "state": True,
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2', 'V': 'S'},
        'weight_operand': "W",
        'time_operand': "T",
        "input_path": 'data/sew_4PLIF/4PLIF_max_t_14.npy',

    },    
    27: {  
        "operator_type": "Conv",
        "equation": "O[t][b][k][oy][ox]+=W[k][c][fy][fx]*I[t][b][c][iy][ix]",
        "dimension_relations": ["ix=1*ox+1*fx", "iy=1*oy+1*fy"],
        "loop_dim_size": {
            "T": 16,
            "B": 1,
            "K": 128,
            "C": 128,
            "OY": 2,
            "OX": 2,
            "FY": 3,
            "FX": 3,
        },
        "operand_precision": {"V": 12, "O": 1, "W": 4, "I": 1},
        "operand_source": {"W": [], "I": [26]},
        "constant_operands": ["W"],
        "state": True,
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2', 'V': 'S'},
        'weight_operand': "W",
        'time_operand': "T",
        "input_path": 'data/sew_4PLIF/4PLIF_max_t_15.npy',

    },      
    28: {  
        "operator_type": "Add",
        "equation": "O[t][b][g][oy][ox]+=X[t][b][g][oy][ox]+Y[t][b][g][oy][ox]",
       "dimension_relations": [],
        "loop_dim_size": {
            "T": 16,
            "B": 1,
            "G": 128,
            "OY": 2,
            "OX": 2,
        },
        'time_opreand': "T",
        "operand_precision": {"O": 1, "O_final": 1, "X": 1, "Y": 1},
        "operand_source": {"X": [27], "Y": [26]},
        "constant_operands": [],
        'memory_operand_links': {'O': 'O', 'X': 'I2', 'Y': 'I1'}
    },
    29: {  
        "operator_type": "MaxPool",
        "equation": "O[t][b][g][oy][ox]+=W[fx][fy]*I[t][b][g][iy][ix]",
        "dimension_relations": ["ix=2*ox+1*fx", "iy=2*oy+1*fy"],
        "loop_dim_size": {"T": 16, "B": 1, "G": 128, "OY": 1, "OX": 1, "FX": 3, "FY": 3},
        "operand_precision": {"O": 1, "O_final": 1, "I": 1, "W": 0},
        "operand_source": {"W": [], "I": [28]},
        "constant_operands": ["W"],
        'time_operand': "T",
        "operand_source_dimension_mapping": {"I": {"IX": "OX", "IY": "OY", "G": "K"}},
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'},

    },
    # 30: {  
    #     "operator_type": "Conv",
    #     "equation": "O[t][b][k][oy][ox]+=W[k][c][fy][fx]*I[t][b][c][iy][ix]",
    #     "dimension_relations": ["ix=1*ox+1*fx", "iy=1*oy+1*fy"],
    #     "loop_dim_size": {
    #         "B": 1,
    #         "K": 10,
    #         "C": 128,
    #         "OY": 1,
    #         "OX": 1,
    #         "FY": 1,
    #         "FX": 1,
    #     },
    #     "operand_precision": {"V": 12, "O": 12, "W": 4, "I": 1},
    #     "operand_source": {"W": [], "I": [29]},
    #     "constant_operands": ["W"],
    #     "state": True,
    #     'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'},
    #     "input_path": 'max_t_1.npy',

    # },  
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