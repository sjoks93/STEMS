
# total_acc =   26,096,259,072
# total_mac =       33,554,432
# total =       26,129,813,504

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
        "operand_precision": {"V": 12, "O": 1, "W": 4, "I": 4},
        "operand_source": {"W": [], "I": []},
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2', 'V': 'S'},
        'weight_operand': "W",
        "constant_operands": ["I", "W"],
        "state": True,
        'time_operand': "T",
        "input_path": 'data/SEW_7PLIF/7PLIF_max_t_0.npy',
        "cut_block": 0,
        #"i_rate": 0.29,
        #mac count = 33,554,432
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
        "operand_precision": {"V": 12, "O": 1, "W": 4, "I": 1},
        "operand_source": {"W": [], "I": [0]},
        "constant_operands": ["W"],
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2', 'V': 'S'},
        'weight_operand': "W",
        'time_operand': "T",
        "state": True,
        "input_path": 'data/SEW_7PLIF/7PLIF_max_t_1.npy',
        "cut_block": 0,
        #"i_rate": 0.124,
        # acc_count = 9,663,676,416
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
        "operand_precision": {"V": 12, "O": 1, "W": 4, "I": 1},
        "operand_source": {"W": [], "I": [1]},
        "constant_operands": ["W"],
        "state": True,
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2', 'V': 'S'},
        'weight_operand': "W",
        'time_operand': "T",
        "input_path": 'data/SEW_7PLIF/7PLIF_max_t_2.npy',
        #"i_rate": 0.19,
        "cut_block": 0,

        # acc_count = 9,663,676,416


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
        'memory_operand_links': {'O': 'O', 'X': 'I2', 'Y': 'I1'},
        "cut_block": 0,
        # acc_count = 16,777,216
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
        "cut_block": 0,

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
        "operand_precision": {"V": 12, "O": 1, "W": 4, "I": 1},
        "operand_source": {"W": [], "I": [4]},
        "constant_operands": ["W"],
        "state": True,
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2', 'V': 'S'},
        'weight_operand': "W",
        'time_operand': "T",
        "input_path": 'data/SEW_7PLIF/7PLIF_max_t_3.npy',
        "cut_block": 1,
        
        # acc_count = 2,415,919,104

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
        "operand_precision": {"V": 12, "O": 1, "W": 4, "I": 1},
        "operand_source": {"W": [], "I": [5]},
        "constant_operands": ["W"],
        "state": True,
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2', 'V': 'S'},
        'weight_operand': "W",
        'time_operand': "T",
        "input_path": 'data/SEW_7PLIF/7PLIF_max_t_4.npy',
        # acc_count = 2,415,919,104
        "cut_block": 1,

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
        'memory_operand_links': {'O': 'O', 'X': 'I2', 'Y': 'I1'},
        "cut_block": 1,
        # acc_count = 4,194,304
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
        "cut_block": 1,

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
        "operand_precision": {"V": 12, "O": 1, "W": 4, "I": 1},
        "operand_source": {"W": [], "I": [8]},
        "constant_operands": ["W"],
        "state": True,
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2', 'V': 'S'},
        'weight_operand': "W",
        'time_operand': "T",
        "input_path": 'data/SEW_7PLIF/7PLIF_max_t_5.npy',
        # acc_count = 603,979,776
        "cut_block": 2,

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
        "operand_precision": {"V": 12, "O": 1, "W": 4, "I": 1},
        "operand_source": {"W": [], "I": [9]},
        "constant_operands": ["W"],
        "state": True,
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2', 'V': 'S'},
        'weight_operand': "W",
        'time_operand': "T",
        "input_path": 'data/SEW_7PLIF/7PLIF_max_t_6.npy',
        # acc_count = 603,979,776
        "cut_block": 2,

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
        'memory_operand_links': {'O': 'O', 'X': 'I2', 'Y': 'I1'},
        "cut_block": 2,
        #acc count = 1,048,576
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
        "cut_block": 2,

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
        "input_path": 'data/SEW_7PLIF/7PLIF_max_t_7.npy',
        "cut_block": 3,
        #acc count = 150,994,944
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
        "input_path": 'data/SEW_7PLIF/7PLIF_max_t_8.npy',
        "cut_block": 3,
        #acc count = 150,994,944
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
        'memory_operand_links': {'O': 'O', 'X': 'I2', 'Y': 'I1'},
        "cut_block": 3,
        #acc_count = 262,144
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
        "cut_block": 3,

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
        "input_path": 'data/SEW_7PLIF/7PLIF_max_t_9.npy',
        "cut_block": 4,
        #acc count = 8,388,608
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
        "input_path": 'data/SEW_7PLIF/7PLIF_max_t_10.npy',
        "cut_block": 4,
        #acc count = 150,994,944

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
        "input_path": 'data/SEW_7PLIF/7PLIF_max_t_11.npy',
        #acc count = 150,994,944
        "cut_block": 4,

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
        'memory_operand_links': {'O': 'O', 'X': 'I2', 'Y': 'I1'},
        "cut_block": 4,
        #add count = 65,536
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
        "cut_block": 4,

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
        "input_path": 'data/SEW_7PLIF/7PLIF_max_t_12.npy',
        #acc count = 37,748,736
        "cut_block": 5,

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
        "input_path": 'data/SEW_7PLIF/7PLIF_max_t_13.npy',
        "cut_block": 5,
    # acc count = 37,748,736
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
        'memory_operand_links': {'O': 'O', 'X': 'I2', 'Y': 'I1'},
        "cut_block": 5,
        #acc count: 16,384
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
        "cut_block": 5,

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
        "input_path": 'data/SEW_7PLIF/7PLIF_max_t_14.npy',
        #acc count = 9,437,184
        "cut_block": 6,

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
        "input_path": 'data/SEW_7PLIF/7PLIF_max_t_15.npy',
        #acc count = 9,437,184
        "cut_block": 6,

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
        'memory_operand_links': {'O': 'O', 'X': 'I2', 'Y': 'I1'},
        "cut_block": 6,
        #acc count: 4096
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
        "cut_block": 6,

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