


workload = {
    0: {  
        "operator_type": "Conv",
        "equation": "O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][iy][ix]",
        "dimension_relations": ["ix=2*ox+1*fx", "iy=2*oy+1*fy"],
        "loop_dim_size": {
            "B": 1,
            "K": 32,
            "C": 6,
            "OY": 180,
            "OX": 320,
            "FY": 3,
            "FX": 3,
        },
        "operand_precision": {"O": 16, "O_final": 4, "W": 4, "I": 4},
        "operand_source": {"W": [], "I": []},
        "constant_operands": ["I", "W"],
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'},
        'weight_operand': "W",
        "input_path": 'max_0.npy',
        #"i_rate": 0.6075499131944444,
    },
    1: {  
        "operator_type": "Conv",
        "equation": "O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][iy][ix]",
        "dimension_relations": ["ix=1*ox+1*fx", "iy=1*oy+1*fy"],
        "loop_dim_size": {
            "B": 1,
            "K": 64,
            "C": 32,
            "OY": 180,
            "OX": 320,
            "FY": 3,
            "FX": 3,
        },
        "operand_precision": {"O": 16, "O_final": 4, "W": 4, "I": 4},
        "operand_source": {"W": [], "I": [0]},
        "constant_operands": ["W"],
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'},
        'weight_operand': "W",
        "input_path": 'max_1.npy',
        #"i_rate": 0.6562131076388888,
       

    },    
    2: {  
        "operator_type": "Conv",
        "equation": "O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][iy][ix]",
        "dimension_relations": ["ix=2*ox+1*fx", "iy=2*oy+1*fy"],
        "loop_dim_size": {
            "B": 1,
            "K": 64,
            "C": 64,
            "OY": 90,
            "OX": 160,
            "FY": 3,
            "FX": 3,
        },
        "operand_precision": {"O": 16, "O_final": 4, "W": 4, "I": 4},
        "operand_source": {"W": [], "I": [1]},
        "constant_operands": ["W"],
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'},
        'weight_operand': "W",
        "input_path": 'max_2.npy',
        #"i_rate": 0.364794
    },  
    3: {  
        "operator_type": "Conv",
        "equation": "O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][iy][ix]",
        "dimension_relations": ["ix=2*ox+1*fx", "iy=2*oy+1*fy"],
        "loop_dim_size": {
            "B": 1,
            "K": 64,
            "C": 32,
            "OY": 90,
            "OX": 160,
            "FY": 3,
            "FX": 3,
        },
        "operand_precision": {"O": 16, "O_final": 4, "W": 4, "I": 4},
        "operand_source": {"W": [], "I": [0]},
        "constant_operands": ["W"],
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'},
        'weight_operand': "W",
        "input_path": 'max_1.npy',
        #"i_rate": 0.6562
    },
    4: {  
        "operator_type": "Add",
        "equation": "O[b][g][oy][ox]+=X[b][g][oy][ox]+Y[b][g][oy][ox]",
       "dimension_relations": [],
        "loop_dim_size": {
            "B": 1,
            "G": 64,
            "OY": 90,
            "OX": 160,
        },
        "operand_precision": {"O": 16, "O_final": 4, "X": 4, "Y": 4},
        "operand_source": {"X": [2], "Y": [3]},
        "constant_operands": [],
        'memory_operand_links': {'O': 'O', 'X': 'I2', 'Y': 'I1'}
    },
    5: {  
        "operator_type": "Conv",
        "equation": "O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][iy][ix]",
        "dimension_relations": ["ix=1*ox+1*fx", "iy=1*oy+1*fy"],
        "loop_dim_size": {
            "B": 1,
            "K": 64,
            "C": 64,
            "OY": 90,
            "OX": 160,
            "FY": 3,
            "FX": 3,
        },
        "operand_precision": {"O": 16, "O_final": 4, "W": 4, "I": 4},
        "operand_source": {"W": [], "I": [4]},
        "constant_operands": ["W"],
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'},
        'weight_operand': "W",
        "input_path": 'max_3.npy',
        #"i_rate": 0.71646
    }, 
    6: {  
        "operator_type": "Conv",
        "equation": "O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][iy][ix]",
        "dimension_relations": ["ix=1*ox+1*fx", "iy=1*oy+1*fy"],
        "loop_dim_size": {
            "B": 1,
            "K": 64,
            "C": 64,
            "OY": 90,
            "OX": 160,
            "FY": 3,
            "FX": 3,
        },
        "operand_precision": {"O": 16, "O_final": 4, "W": 4, "I": 4},
        "operand_source": {"W": [], "I": [5]},
        "constant_operands": ["W"],
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'},
        'weight_operand': "W",
        "input_path": 'max_4.npy',
        #"i_rate": 0.39674
    },                    
    7: {  
        "operator_type": "Add",
        "equation": "O[b][g][oy][ox]+=X[b][g][oy][ox]+Y[b][g][oy][ox]",
        "dimension_relations": [],
        "loop_dim_size": {
            "B": 1,
            "G": 64,
            "OY": 90,
            "OX": 160,
        },
        "operand_precision": {"O": 4, "O_final": 4, "X": 4, "Y": 4},
        "operand_source": {"X": [4], "Y": [6]},
        "constant_operands": [],
        'memory_operand_links': {'O': 'O', 'X': 'I2', 'Y': 'I1'}

    },
    8: {  
        "operator_type": "Conv",
        "equation": "O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][iy][ix]",
        "dimension_relations": ["ix=1*ox+1*fx", "iy=1*oy+1*fy"],
        "loop_dim_size": {
            "B": 1,
            "K": 128,
            "C": 64,
            "OY": 90,
            "OX": 160,
            "FY": 3,
            "FX": 3,
        },
        "operand_precision": {"O": 16, "O_final": 4, "W": 4, "I": 4},
        "operand_source": {"W": [], "I": [7]},
        "constant_operands": ["W"],
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'},
        'weight_operand': "W",
        "input_path": 'max_5.npy',        
        #"i_rate": 0.822366
    },  
    9: {  
        "operator_type": "Conv",
        "equation": "O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][iy][ix]",
        "dimension_relations": ["ix=1*ox+1*fx", "iy=1*oy+1*fy"],
        "loop_dim_size": {
            "B": 1,
            "K": 128,
            "C": 128,
            "OY": 90,
            "OX": 160,
            "FY": 3,
            "FX": 3,
        },
        "operand_precision": {"O": 16, "O_final": 4, "W": 4, "I": 4},
        "operand_source": {"W": [], "I": [8]},
        "constant_operands": ["W"],
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'},
        'weight_operand': "W",
        "input_path": 'max_6.npy',
        #"i_rate": 0.26089
    },   
    10: {  
        "operator_type": "Conv",
        "equation": "O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][iy][ix]",
        "dimension_relations": ["ix=1*ox+1*fx", "iy=1*oy+1*fy"],
        "loop_dim_size": {
            "B": 1,
            "K": 128,
            "C": 64,
            "OY": 90,
            "OX": 160,
            "FY": 3,
            "FX": 3,
        },
        "operand_precision": {"O": 16, "O_final": 4, "W": 4, "I": 4},
        "operand_source": {"W": [], "I": [7]},
        "constant_operands": ["W"],
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'},
        'weight_operand': "W",
        "input_path": 'max_5.npy',
        #"i_rate": 0.822367
    },    
    11: {  
        "operator_type": "Add",
        "equation": "O[b][g][oy][ox]+=X[b][g][oy][ox]+Y[b][g][oy][ox]",
        "dimension_relations": [],
        "loop_dim_size": {
            "B": 1,
            "G": 128,
            "OY": 90,
            "OX": 160,
        },
        "operand_precision": {"O": 4, "O_final": 4, "X": 4, "Y": 4},
        "operand_source": {"X": [9], "Y": [10]},
        "constant_operands": [],
        'memory_operand_links': {'O': 'O', 'X': 'I2', 'Y': 'I1'},
        
    },    
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
        "operand_precision": {"V": 16, "O": 1, "W": 4, "I": 4},
        #"operand_precision": {"O_final": 8, "O": 16, "W": 8, "I": 8},
        "operand_source": {"W": [], "I": [11]},
        "operand_state": {"V": []},
        "constant_operands": ["W"],
        "state": True,
        #"sparse": False,
        ##"i_rate": 0.05,
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2', 'V': 'S'},
        'weight_operand': "W",
        "input_path": 'max_7.npy',
        #"i_rate": 0.295345
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
        "operand_precision": {"V": 12, "O": 1, "W": 4, "I": 1},
        #"operand_precision": {"O_final": 8, "O": 16, "W": 8, "I": 8},
        "operand_source": {"W": [], "I": [12]},
        "operand_state": {"V": []},
        "constant_operands": ["W"],
        "state": True,
        #"sparse": False,
        ##"i_rate": 0.05,
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2', 'V': 'S'},
        'weight_operand': "W",
        "input_path": 'max_8.npy',
        #"i_rate": 0.103109
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
        "operand_precision": {"V": 12, "O": 1, "W": 4, "I": 1},
        #"operand_precision": {"O_final": 8, "O": 16, "W": 8, "I": 8},
        "operand_source": {"W": [], "I": [13]},
        "operand_state": {"V": []},
        "constant_operands": ["W"],
        "state": True,
        #"sparse": False,
        ##"i_rate": 0.05,
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2', 'V': 'S'},
        'weight_operand': "W",
        "input_path": 'max_9.npy',
        #"i_rate": 0.10533288

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
        "operand_precision": {"V": 12, "O": 1, "W": 4, "I": 1},
        #"operand_precision": {"O_final": 8, "O": 16, "W": 8, "I": 8},
        "operand_source": {"W": [], "I": [14]},
        "operand_state": {"V": []},
        "constant_operands": ["W"],
        "state": True,
        #"sparse": False,
        ##"i_rate": 0.05,
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2', 'V': 'S'},
        'weight_operand': "W",
        "input_path": 'max_10.npy',
        #"i_rate": 0.871419
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
        "operand_precision": {"V": 12, "O": 1, "W": 4, "I": 1},
        #"operand_precision": {"O_final": 8, "O": 16, "W": 8, "I": 8},
        "operand_source": {"W": [], "I": [15]},
        "operand_state": {"V": []},
        "constant_operands": ["W"],
        "state": True,
        #"sparse": False,
        ##"i_rate": 0.05,
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2', 'V': 'S'},
        'weight_operand': "W",
        "input_path": 'max_11.npy',
        #"i_rate": 0.084635

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