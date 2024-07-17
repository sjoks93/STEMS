
# total_acc =     8,785,428,480
# total_mac =   105,239,347,200
# total_op =    114,012,775,680

workload = {
    0: {  
        "operator_type": "Conv",
        "equation": "O[b][t][k][oy][ox]+=W[k][c][fy][fx]*I[b][t][c][iy][ix]",
        "dimension_relations": ["ix=2*ox+1*fx", "iy=2*oy+1*fy"],
        "loop_dim_size": {
            "B": 1,
            "K": 32,
            "C": 6,
            "OY": 180,
            "OX": 320,
            "FY": 7,
            "FX": 7,
            "T": 12,
        },
        "operand_precision": {"O": 12, "O_final": 4, "W": 4, "I": 4},
        "operand_source": {"W": [], "I": []},
        "constant_operands": ["I", "W"],
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'},
        'time_operand': "T",
        'weight_operand' : "W",
        #"input_path": 'data/RED/max_t_0.npy',
        "cut_block": 0,

        #"i_rate": 0.6075499131944444,
       #mac_count = 6,502,809,600
    },
    1: {  
        "operator_type": "Conv",
        "equation": "O[b][t][k][oy][ox]+=W[k][c][fy][fx]*I[b][t][c][iy][ix]",
        "dimension_relations": ["ix=1*ox+1*fx", "iy=1*oy+1*fy"],
        "loop_dim_size": {
            "B": 1,
            "K": 64,
            "C": 32,
            "OY": 180,
            "OX": 320,
            "FY": 3,
            "FX": 3,
            "T": 12,
        },
        "operand_precision": {"O": 12, "O_final": 4, "W": 4, "I": 4},
        "operand_source": {"W": [], "I": [0]},
        "constant_operands": ["W"],
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'},
        'time_operand': "T",
        'weight_operand' : "W",
        #"input_path": 'data/RED/max_t_1.npy',
        #"i_rate": 0.6562131076388888,
        #mac_count = 12,740,198,400
        "cut_block": 0,
       

    },    
    2: {  
        "operator_type": "Conv",
        "equation": "O[b][t][k][oy][ox]+=W[k][c][fy][fx]*I[b][t][c][iy][ix]",
        "dimension_relations": ["ix=2*ox+1*fx", "iy=2*oy+1*fy"],
        "loop_dim_size": {
            "B": 1,
            "K": 64,
            "C": 64,
            "OY": 90,
            "OX": 160,
            "FY": 3,
            "FX": 3,
            "T": 12,
        },
        "operand_precision": {"O": 12, "O_final": 4, "W": 4, "I": 4},
        "operand_source": {"W": [], "I": [1]},
        "constant_operands": ["W"],
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'},
        'time_operand': "T",
        'weight_operand' : "W",
        #"input_path": 'data/RED/max_t_2.npy',
        "cut_block": 0,
        #"i_rate": 0.364794
        # mac_count = 6,370,099,200
    },  
    3: {  
        "operator_type": "Conv",
        "equation": "O[b][t][k][oy][ox]+=W[k][c][fy][fx]*I[b][t][c][iy][ix]",
        "dimension_relations": ["ix=2*ox+1*fx", "iy=2*oy+1*fy"],
        "loop_dim_size": {
            "B": 1,
            "K": 64,
            "C": 32,
            "OY": 90,
            "OX": 160,
            "FY": 3,
            "FX": 3,
            "T": 12,
        },
        "operand_precision": {"O": 12, "O_final": 4, "W": 4, "I": 4},
        "operand_source": {"W": [], "I": [0]},
        "constant_operands": ["W"],
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'},
        'time_operand': "T",
        'weight_operand' : "W",
        #"input_path": 'data/RED/max_t_1.npy',
        "cut_block": 0,
        #"i_rate": 0.6562
        # mac count: 3,185,049,600
    },
    4: {  
        "operator_type": "Add",
        "equation": "O[b][t][k][ay][ax]+=X[b][t][k][ay][ax]+Y[b][t][k][ay][ax]",
       "dimension_relations": [],
        "loop_dim_size": {
            "B": 1,
            "K": 64,
            "AY": 90,
            "AX": 160,
            "T": 12,
        },
        'time_opreand': "T",
        "operand_precision": {"O": 4, "O_final": 4, "X": 4, "Y": 4},
        "operand_source": {"X": [2], "Y": [3]},
        "constant_operands": [],
        'memory_operand_links': {'O': 'O', 'X': 'I2', 'Y': 'I1'},
        "cut_block": 0,
        # acc count: 11,059,200
    },
    5: {  
        "operator_type": "Conv",
        "equation": "O[b][t][k][oy][ox]+=W[k][c][fy][fx]*I[b][t][c][iy][ix]",
        "dimension_relations": ["ix=1*ox+1*fx", "iy=1*oy+1*fy"],
        "loop_dim_size": {
            "B": 1,
            "K": 64,
            "C": 64,
            "OY": 90,
            "OX": 160,
            "FY": 3,
            "FX": 3,
            "T": 12,
        },
        "operand_precision": {"O": 12, "O_final": 4, "W": 4, "I": 4},
        "operand_source": {"W": [], "I": [4]},
        "constant_operands": ["W"],
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'},
        'time_operand': "T",
        'weight_operand' : "W",
        #"input_path": 'data/RED/max_t_3.npy',
        "cut_block": 1,
        #"i_rate": 0.71646
        # mac_count: 6,370,099,200
    }, 
    6: {  
        "operator_type": "Conv",
        "equation": "O[b][t][k][oy][ox]+=W[k][c][fy][fx]*I[b][t][c][iy][ix]",
        "dimension_relations": ["ix=1*ox+1*fx", "iy=1*oy+1*fy"],
        "loop_dim_size": {
            "B": 1,
            "K": 64,
            "C": 64,
            "OY": 90,
            "OX": 160,
            "FY": 3,
            "FX": 3,
            "T": 12,
        },
        "operand_precision": {"O": 12, "O_final": 4, "W": 4, "I": 4},
        "operand_source": {"W": [], "I": [5]},
        "constant_operands": ["W"],
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'},
        'time_operand': "T",
        'weight_operand' : "W",
        #"input_path": 'data/RED/max_t_4.npy',
        "cut_block": 1,
        #"i_rate": 0.39674
         # mac_count: 6,370,099,200
       
    },                    
    7: {  
        "operator_type": "Add",
        "equation": "O[b][t][k][ay][ax]+=X[b][t][k][ay][ax]+Y[b][t][k][ay][ax]",
        "dimension_relations": [],
        "loop_dim_size": {
            "B": 1,
            "K": 64,
            "AY": 90,
            "AX": 160,
            "T": 12,
        },
        'time_opreand': "T",
        "operand_precision": {"O": 4, "O_final": 4, "X": 4, "Y": 4},
        "operand_source": {"X": [4], "Y": [6]},
        "constant_operands": [],
        'memory_operand_links': {'O': 'O', 'X': 'I2', 'Y': 'I1'},
        "cut_block": 1,
        # acc count: 11,059,200

    },
    8: {  
        "operator_type": "Conv",
        "equation": "O[b][t][k][oy][ox]+=W[k][c][fy][fx]*I[b][t][c][iy][ix]",
        "dimension_relations": ["ix=1*ox+1*fx", "iy=1*oy+1*fy"],
        "loop_dim_size": {
            "B": 1,
            "K": 128,
            "C": 64,
            "OY": 90,
            "OX": 160,
            "FY": 3,
            "FX": 3,
            "T": 12,
        },
        "operand_precision": {"O": 12, "O_final": 4, "W": 4, "I": 4},
        "operand_source": {"W": [], "I": [7]},
        "constant_operands": ["W"],
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'},
        'time_operand': "T",
        'weight_operand' : "W",
        #"input_path": 'data/RED/max_t_5.npy',        
        "cut_block": 2,
        #"i_rate": 0.822366
        # mac_count: 12,740,198,400
    },  
    9: {  
        "operator_type": "Conv",
        "equation": "O[b][t][k][oy][ox]+=W[k][c][fy][fx]*I[b][t][c][iy][ix]",
        "dimension_relations": ["ix=1*ox+1*fx", "iy=1*oy+1*fy"],
        "loop_dim_size": {
            "B": 1,
            "K": 128,
            "C": 128,
            "OY": 90,
            "OX": 160,
            "FY": 3,
            "FX": 3,
            "T": 12,
        },
        "operand_precision": {"O": 12, "O_final": 4, "W": 4, "I": 4},
        "operand_source": {"W": [], "I": [8]},
        "constant_operands": ["W"],
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'},
        'time_operand': "T",
        'weight_operand' : "W",
        #"input_path": 'data/RED/max_t_6.npy',
        "cut_block": 2,
        #"i_rate": 0.26089
        # mac_count: 25,480,396,800
    },   
    10: {  
        "operator_type": "Conv",
        "equation": "O[b][t][k][oy][ox]+=W[k][c][fy][fx]*I[b][t][c][iy][ix]",
        "dimension_relations": ["ix=1*ox+1*fx", "iy=1*oy+1*fy"],
        "loop_dim_size": {
            "B": 1,
            "K": 128,
            "C": 64,
            "OY": 90,
            "OX": 160,
            "FY": 3,
            "FX": 3,
            "T": 12,
        },
        "operand_precision": {"O": 12, "O_final": 4, "W": 4, "I": 4},
        "operand_source": {"W": [], "I": [7]},
        "constant_operands": ["W"],
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'},
        'time_operand': "T",
        'weight_operand' : "W",
        #"input_path": 'data/RED/max_t_5.npy',
        "cut_block": 2,
        #"i_rate": 0.822367
        # mac_count: 12,740,198,400
    },    
    11: {  
        "operator_type": "Add",
        "equation": "O[b][t][k][ay][ax]+=X[b][t][k][ay][ax]+Y[b][t][k][ay][ax]",
        "dimension_relations": [],
        "loop_dim_size": {
            "B": 1,
            "K": 128,
            "AY": 90,
            "AX": 160,
            "T": 12,
        },
        'time_opreand': "T",
        "operand_precision": {"O": 4, "O_final": 4, "X": 4, "Y": 4},
        "operand_source": {"X": [9], "Y": [10]},
        "constant_operands": [],
        'memory_operand_links': {'O': 'O', 'X': 'I2', 'Y': 'I1'},
        "cut_block": 2,
        # acc_count: 22,118,400
        
    },    
   12: {  
        "operator_type": "Conv",
        "equation": "O[b][t][k][oy][ox]+=W[k][c][fy][fx]*I[b][t][c][iy][ix]",
        "dimension_relations": ["ix=2*ox+1*fx", "iy=2*oy+1*fy"],
        "loop_dim_size": {
            "B": 1,
            "K": 256,
            "C": 128,
            "OY": 45,
            "OX": 80,
            "FY": 3,
            "FX": 3,
            "T": 12,
            #"C": "16"
        },
        "operand_precision": {"V": 12, "O": 1, "W": 4, "I": 4},
        #"operand_precision": {"O_final": 8, "O": 16, "W": 8, "I": 8},
        "operand_source": {"W": [], "I": [11]},
        "state_operand": "V",
        "constant_operands": ["W"],
        "state": True,
        #"sparse": False,
        #"i_rate": 0.05,
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2', 'V': 'S'},
        'time_operand': "T",
        'weight_operand' : "W",
        #"input_path": 'data/RED/max_t_7.npy',
        "cut_block": 3,
        #"i_rate": 0.295345
        # mac_count: 12,740,198,400
    },
   13: {  
        "operator_type": "Conv",
        "equation": "O[b][t][k][oy][ox]+=W[k][c][fy][fx]*I[b][t][c][iy][ix]",
        "dimension_relations": ["ix=2*ox+1*fx", "iy=2*oy+1*fy"],
        "loop_dim_size": {
            "B": 1,
            "K": 256,
            "C": 256,
            "OY": 23,
            "OX": 40,
            "FY": 3,
            "FX": 3,
            "T": 12,
            #"C": "16"
        },
        "operand_precision": {"V": 12, "O": 1, "W": 4, "I": 1},
        #"operand_precision": {"O_final": 8, "O": 16, "W": 8, "I": 8},
        "operand_source": {"W": [], "I": [12]},
        "state_operand": "V",
        "constant_operands": ["W"],
        "state": True,
        #"sparse": False,
        #"i_rate": 0.05,
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2', 'V': 'S'},
        'time_operand': "T",
        'weight_operand' : "W",
        #"input_path": 'data/RED/max_t_8.npy',
        "cut_block": 4,
        #"i_rate": 0.103109
        # acc_count: 6,511,656,960
    },
   14: {  
        "operator_type": "Conv",
        "equation": "O[b][t][k][oy][ox]+=W[k][c][fy][fx]*I[b][t][c][iy][ix]",
        "dimension_relations": ["ix=2*ox+fx", "iy=2*oy+fy"],
        "loop_dim_size": {
            "B": 1,
            "K": 256,
            "C": 256,
            "OY": 12,
            "OX": 20,
            "FY": 3,
            "FX": 3,
            "T": 12,
            #"C": "16"
        },
        "operand_precision": {"V": 12, "O": 1, "W": 4, "I": 1},
        #"operand_precision": {"O_final": 8, "O": 16, "W": 8, "I": 8},
        "operand_source": {"W": [], "I": [13]},
        "state_operand": "V",
        "constant_operands": ["W"],
        "state": True,
        #"sparse": False,
        #"i_rate": 0.05,
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2', 'V': 'S'},
        'time_operand': "T",
        'weight_operand' : "W",
        #"input_path": 'data/RED/max_t_9.npy',
        "cut_block": 5,
        #"i_rate": 0.10533288
        # acc_count: 1,698,693,120

    },
   15: {  
        "operator_type": "Conv",
        "equation": "O[b][t][k][oy][ox]+=W[k][c][fy][fx]*I[b][t][c][iy][ix]",
        "dimension_relations": ["ix=2*ox+fx", "iy=2*oy+fy"],
        "loop_dim_size": {
            "B": 1,
            "K": 256,
            "C": 256,
            "OY": 6,
            "OX": 10,
            "FY": 3,
            "FX": 3,
            "T": 12,
            #"C": "16"
        },
        "operand_precision": {"V": 12, "O": 1, "W": 4, "I": 1},
        #"operand_precision": {"O_final": 8, "O": 16, "W": 8, "I": 8},
        "operand_source": {"W": [], "I": [14]},
        "state_operand": "V",
        "constant_operands": ["W"],
        "state": True,
        #"sparse": False,
        #"i_rate": 0.05,
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2', 'V': 'S'},
        'time_operand': "T",
        'weight_operand' : "W",
        #"input_path": 'data/RED/max_t_10.npy',
        "cut_block": 6,
        #"i_rate": 0.0871419
        # acc_count: 424,673,280
    },
   16: {  
        "operator_type": "Conv",
        "equation": "O[b][t][k][oy][ox]+=W[k][c][fy][fx]*I[b][t][c][iy][ix]",
        "dimension_relations": ["ix=2*ox+fx", "iy=2*oy+fy"],
        "loop_dim_size": {
            "B": 1,
            "K": 256,
            "C": 256,
            "OY": 3,
            "OX": 5,
            "FY": 3,
            "FX": 3,
            "T": 12,
            #"C": "16"
        },
        "operand_precision": {"V": 12, "O": 1, "W": 4, "I": 1},
        #"operand_precision": {"O_final": 8, "O": 16, "W": 8, "I": 8},
        "operand_source": {"W": [], "I": [15]},
        "state_operand": "V",
        "constant_operands": ["W"],
        "state": True,
        #"sparse": False,
        #"i_rate": 0.05,
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2', 'V': 'S'},
        'time_operand': "T",
        'weight_operand' : "W",
        #"input_path": 'data/RED/max_t_11.npy',
        "cut_block": 7,
        #"i_rate": 0.084635
        #acc count: 106,168,320

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