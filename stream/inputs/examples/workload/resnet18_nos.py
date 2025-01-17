workload = {
    0: {  # conv1, stride 2
        'operator_type': 'Conv',
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][iy][ix]',
        'dimension_relations': ['ix=2*ox+1*fx', 'iy=2*oy+1*fy'],
        'loop_dim_size': {'B': 1, 'K': 64, 'C': 3, 'OY': 112, 'OX': 112, 'FY': 7, 'FX': 7},
        'operand_precision': {'O': 8, 'O_final': 1, 'W': 4, 'I': 1},
        'operand_source': {'W': [], 'I': []},
        'constant_operands': ['I', 'W'],
        'memory_operand_links': {'O': 'O', 'W': 'I2', 'I': 'I1' },
        'padding': {'IY': (3, 2), 'IX': (3, 2)}
    }
    ,
    1: {  # max pool, stride 2
        'operator_type': 'MaxPool',
        'equation': 'O[b][g][oy][ox]+=W[fx][fy]*I[b][g][iy][ix]',
        'dimension_relations': ['ix=2*ox+1*fx', 'iy=2*oy+1*fy'],
        'loop_dim_size': {'B': 1, 'G': 64, 'OY': 56, 'OX': 56, 'FX': 3, 'FY': 3},
        'operand_precision': {'O': 1, 'O_final': 1, 'W': 0, 'I': 1, 'O_final': 1},
        'operand_source': {'W': [], 'I': [0]},
        'constant_operands': ['W'],
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'G': 'K'}},
        'memory_operand_links': {'O': 'O', 'W': 'I2', 'I': 'I1' },
        'padding': {'IY': (1, 0), 'IX': (1, 0)}
    }
    ,
    2: {  # conv2_1
        'operator_type': 'Conv',
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][iy][ix]',
        'dimension_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B': 1, 'K': 64, 'C': 64, 'OY': 56, 'OX': 56, 'FY': 3, 'FX': 3, },
        'operand_precision': {'O': 8, 'O_final': 1, 'W': 4, 'I': 1},
        'operand_source': {'W': [], 'I': [1]},
        'constant_operands': ['W'],
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'G'}},
        'memory_operand_links': {'O': 'O', 'W': 'I2', 'I': 'I1' },
        'padding': {'IY': (1, 1), 'IX': (1, 1)}
    }
    ,
    3: {  # conv2_2
        'operator_type': 'Conv',
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][iy][ix]',
        'dimension_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B': 1, 'K': 64, 'C': 64, 'OY': 56, 'OX': 56, 'FY': 3, 'FX': 3, },
        'operand_precision': {'O': 8, 'O_final': 1, 'W': 4, 'I': 1},
        'operand_source': {'W': [], 'I': [2]},
        'constant_operands': ['W'],
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'K'}},
        'memory_operand_links': {'O': 'O', 'W': 'I2', 'I': 'I1' },
        'padding': {'IY': (1, 1), 'IX': (1, 1)}
    }
    ,
    4: {  # Addition of layer 1 (residual path) and layer 3 (main path)
        'operator_type': 'Add',
        'equation': 'O[b][g][oy][ox]=X[b][g][oy][ox]+Y[b][g][oy][ox]',
        'dimension_relations': [],
        'loop_dim_size': {'B': 1, 'G': 64, 'OY': 56, 'OX': 56},
        'operand_precision': {'O': 2, 'X': 1, 'Y': 1, 'O_final': 1},
        'operand_source': {'X': [1], 'Y': [3]},
        'constant_operands': [],
        'operand_source_dimension_mapping': {'X': {'OX': 'OX', 'OY': 'OY', 'G': 'K'}, 'Y': {'OX': 'OX', 'OY': 'OY', 'G': 'K'}},
        'memory_operand_links': {'O': 'O', 'X': 'I2', 'Y': 'I1'}
    }
    ,
    5: {  # conv2_3
        'operator_type': 'Conv',
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][iy][ix]',
        'dimension_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B': 1, 'K': 64, 'C': 64, 'OY': 56, 'OX': 56, 'FY': 3, 'FX': 3},
        'operand_precision': {'O': 8, 'O_final': 1, 'W': 4, 'I': 1},
        'operand_source': {'W': [], 'I': [4]},
        'constant_operands': ['W'],
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'G'}},
        'memory_operand_links': {'O': 'O', 'W': 'I2', 'I': 'I1' },
        'padding': {'IY': (1, 1), 'IX': (1, 1)}
    }
    ,
    6: {  # conv2_4
        'operator_type': 'Conv',
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][iy][ix]',
        'dimension_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B': 1, 'K': 64, 'C': 64, 'OY': 56, 'OX': 56, 'FY': 3, 'FX': 3},
        'operand_precision': {'O': 8, 'O_final': 1, 'W': 4, 'I': 1},
        'operand_source': {'W': [], 'I': [5]},
        'constant_operands': ['W'],
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'K'}},
        'memory_operand_links': {'O': 'O', 'W': 'I2', 'I': 'I1' },
        'padding': {'IY': (1, 1), 'IX': (1, 1)}
    },
    7: {  # Addition of layer 4 (residual connection) and layer 6 (main path)
        'operator_type': 'Add',
        'equation': 'O[b][g][oy][ox]=X[b][g][oy][ox]+Y[b][g][oy][ox]',
        'dimension_relations': [],
        'loop_dim_size': {'B': 1, 'G': 64, 'OY': 56, 'OX': 56},
        'operand_precision': {'O': 2, 'X': 1, 'Y': 1, 'O_final': 1},
        'operand_source': {'X': [4], 'Y': [6]},
        'constant_operands': [],
        'operand_source_dimension_mapping': {'X': {'OX': 'OX', 'OY': 'OY', 'G': 'G'}, 'Y': {'OX': 'OX', 'OY': 'OY', 'G': 'K'}},
        'memory_operand_links': {'O': 'O', 'X': 'I2', 'Y': 'I1'}
    }
    ,
    8: {  # conv3_1, stride 2
        'operator_type': 'Conv',
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][iy][ix]',
        'dimension_relations': ['ix=2*ox+1*fx', 'iy=2*oy+1*fy'],
        'loop_dim_size': {'B': 1, 'K': 128, 'C': 64, 'OY': 28, 'OX': 28, 'FY': 3, 'FX': 3},
        'operand_precision': {'O': 8, 'O_final': 1, 'W': 4, 'I': 1},
        'operand_source': {'W': [], 'I': [7]},
        'constant_operands': ['W'],
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'G'}},
        'memory_operand_links': {'O': 'O', 'W': 'I2', 'I': 'I1' },
        'padding': {'IY': (1, 0), 'IX': (1, 0)}
    }
    ,
    9: {  # conv3_2
        'operator_type': 'Conv',
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][iy][ix]',
        'dimension_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B': 1, 'K': 128, 'C': 128, 'OY': 28, 'OX': 28, 'FY': 3, 'FX': 3},
        'operand_precision': {'O': 8, 'O_final': 1, 'W': 4, 'I': 1},
        'operand_source': {'W': [], 'I': [8]},
        'constant_operands': ['W'],
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'K'}},
        'memory_operand_links': {'O': 'O', 'W': 'I2', 'I': 'I1' },
        'padding': {'IY': (1, 1), 'IX': (1, 1)}
    },
    10: {  # conv downsample of layer 7
        'operator_type': 'Conv_downsample',
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][iy][ix]',
        'dimension_relations': ['ix=2*ox+1*fx', 'iy=2*oy+1*fy'],
        'loop_dim_size': {'B': 1, 'K': 128, 'C': 64, 'OY': 28, 'OX': 28, 'FY': 3, 'FX': 3},
        'operand_precision': {'O': 8, 'O_final': 1, 'W': 4, 'I': 1},
        'operand_source': {'W': [], 'I': [7]},
        'constant_operands': ['W'],
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'G'}},
        'memory_operand_links': {'O': 'O', 'W': 'I2', 'I': 'I1' },
        'padding': {'IY': (1, 0), 'IX': (1, 0)}
    }
    ,
    11: {  # Addition of layer 10 (residual connection) and layer 9 (main path)
        'operator_type': 'Add',
        'equation': 'O[b][g][oy][ox]=X[b][g][oy][ox]+Y[b][g][oy][ox]',
        'dimension_relations': [],
        'loop_dim_size': {'B': 1, 'G': 128, 'OY': 28, 'OX': 28},
        'operand_precision': {'O': 2, 'X': 1, 'Y': 1, 'O_final': 1},
        'operand_source': {'X': [10], 'Y': [9]},
        'constant_operands': [],
        'operand_source_dimension_mapping': {'X': {'OX': 'OX', 'OY': 'OY', 'G': 'K'}, 'Y': {'OX': 'OX', 'OY': 'OY', 'G': 'K'}},
        'memory_operand_links': {'O': 'O', 'X': 'I2', 'Y': 'I1'}
    }
    ,
    12: {  # conv3_3
        'operator_type': 'Conv',
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][iy][ix]',
        'dimension_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B': 1, 'K': 128, 'C': 128, 'OY': 28, 'OX': 28, 'FY': 3, 'FX': 3},
        'operand_precision': {'O': 8, 'O_final': 1, 'W': 4, 'I': 1},
        'operand_source': {'W': [], 'I': [11]},
        'constant_operands': ['W'],
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'G'}},
        'memory_operand_links': {'O': 'O', 'W': 'I2', 'I': 'I1' },
        'padding': {'IY': (1, 1), 'IX': (1, 1)}
    }
    ,
    13: {  # conv3_4
        'operator_type': 'Conv',
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][iy][ix]',
        'dimension_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B': 1, 'K': 128, 'C': 128, 'OY': 28, 'OX': 28, 'FY': 3, 'FX': 3},
        'operand_precision': {'O': 8, 'O_final': 1, 'W': 4, 'I': 1},
        'operand_source': {'W': [], 'I': [12]},
        'constant_operands': ['W'],
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'K'}},
        'memory_operand_links': {'O': 'O', 'W': 'I2', 'I': 'I1' },
        'padding': {'IY': (1, 1), 'IX': (1, 1)}
    },
    14: {  # Addition of layer 11 (residual connection) and layer 13 (main path)
        'operator_type': 'Add',
        'equation': 'O[b][g][oy][ox]=X[b][g][oy][ox]+Y[b][g][oy][ox]',
        'dimension_relations': [],
        'loop_dim_size': {'B': 1, 'G': 128, 'OY': 28, 'OX': 28},
        'operand_precision': {'O': 2, 'X': 1, 'Y': 1, 'O_final': 1},
        'operand_source': {'X': [11], 'Y': [13]},
        'constant_operands': [],
        'operand_source_dimension_mapping': {'X': {'OX': 'OX', 'OY': 'OY', 'G': 'G'}, 'Y': {'OX': 'OX', 'OY': 'OY', 'G': 'K'}},
        'memory_operand_links': {'O': 'O', 'X': 'I2', 'Y': 'I1'}
    }
    ,
    15: {  # conv4_1, stride 2
        'operator_type': 'Conv',
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][iy][ix]',
        'dimension_relations': ['ix=2*ox+1*fx', 'iy=2*oy+1*fy'],
        'loop_dim_size': {'B': 1, 'K': 256, 'C': 128, 'OY': 14, 'OX': 14, 'FY': 3, 'FX': 3},
        'operand_precision': {'O': 8, 'O_final': 1, 'W': 4, 'I': 1},
        'operand_source': {'W': [], 'I': [14]},
        'constant_operands': ['W'],
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'G'}},
        'memory_operand_links': {'O': 'O', 'W': 'I2', 'I': 'I1' },
        'padding': {'IY': (1, 0), 'IX': (1, 0)}
    }
    ,
    16: {  # conv4_2
        'operator_type': 'Conv',
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][iy][ix]',
        'dimension_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B': 1, 'K': 256, 'C': 256, 'OY': 14, 'OX': 14, 'FY': 3, 'FX': 3},
        'operand_precision': {'O': 8, 'O_final': 1, 'W': 4, 'I': 1},
        'operand_source': {'W': [], 'I': [15]},
        'constant_operands': ['W'],
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'K'}},
        'memory_operand_links': {'O': 'O', 'W': 'I2', 'I': 'I1' },
        'padding': {'IY': (1, 1), 'IX': (1, 1)}
    },
    17: {  # conv downsample of layer 14
        'operator_type': 'Conv_downsample',
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][iy][ix]',
        'dimension_relations': ['ix=2*ox+1*fx', 'iy=2*oy+1*fy'],
        'loop_dim_size': {'B': 1, 'K': 256, 'C': 128, 'OY': 14, 'OX': 14, 'FY': 3, 'FX': 3},
        'operand_precision': {'O': 8, 'O_final': 1, 'W': 4, 'I': 1},
        'operand_source': {'W': [], 'I': [14]},
        'constant_operands': ['W'],
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'G'}},
        'memory_operand_links': {'O': 'O', 'W': 'I2', 'I': 'I1' },
        'padding': {'IY': (1, 0), 'IX': (1, 0)}
    }
    ,
    18: {  # Addition of layer 17 (residual connection) and layer 16 (main path)
        'operator_type': 'Add',
        'equation': 'O[b][g][oy][ox]=X[b][g][oy][ox]+Y[b][g][oy][ox]',
        'dimension_relations': [],
        'loop_dim_size': {'B': 1, 'G': 256, 'OY': 14, 'OX': 14},
        'operand_precision': {'O': 2, 'X': 1, 'Y': 1, 'O_final': 1},
        'operand_source': {'X': [17], 'Y': [16]},
        'constant_operands': [],
        'operand_source_dimension_mapping': {'X': {'OX': 'OX', 'OY': 'OY', 'G': 'K'}, 'Y': {'OX': 'OX', 'OY': 'OY', 'G': 'K'}},
        'memory_operand_links': {'O': 'O', 'X': 'I2', 'Y': 'I1'}
    }
    ,
    19: {  # conv4_3
        'operator_type': 'Conv',
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][iy][ix]',
        'dimension_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B': 1, 'K': 256, 'C': 256, 'OY': 14, 'OX': 14, 'FY': 3, 'FX': 3},
        'operand_precision': {'O': 8, 'O_final': 1, 'W': 4, 'I': 1},
        'operand_source': {'W': [], 'I': [18]},
        'constant_operands': ['W'],
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'G'}},
        'memory_operand_links': {'O': 'O', 'W': 'I2', 'I': 'I1' },
        'padding': {'IY': (1, 1), 'IX': (1, 1)}
    }
    ,
    20: {  # conv4_4
        'operator_type': 'Conv',
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][iy][ix]',
        'dimension_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B': 1, 'K': 256, 'C': 256, 'OY': 14, 'OX': 14, 'FY': 3, 'FX': 3},
        'operand_precision': {'O': 8, 'O_final': 1, 'W': 4, 'I': 1},
        'operand_source': {'W': [], 'I': [19]},
        'constant_operands': ['W'],
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'K'}},
        'memory_operand_links': {'O': 'O', 'W': 'I2', 'I': 'I1' },
        'padding': {'IY': (1, 1), 'IX': (1, 1)}
    },
    21: {  # Addition of layer 18 (residual connection) and layer 20 (main path)
        'operator_type': 'Add',
        'equation': 'O[b][g][oy][ox]=X[b][g][oy][ox]+Y[b][g][oy][ox]',
        'dimension_relations': [],
        'loop_dim_size': {'B': 1, 'G': 256, 'OY': 14, 'OX': 14},
        'operand_precision': {'O': 2, 'X': 1, 'Y': 1, 'O_final': 1},
        'operand_source': {'X': [18], 'Y': [20]},
        'constant_operands': [],
        'operand_source_dimension_mapping': {'X': {'OX': 'OX', 'OY': 'OY', 'G': 'G'}, 'Y': {'OX': 'OX', 'OY': 'OY', 'G': 'K'}},
        'memory_operand_links': {'O': 'O', 'X': 'I2', 'Y': 'I1'}
    }
    ,
    22: {  # conv5_1, stride 2
        'operator_type': 'Conv',
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][iy][ix]',
        'dimension_relations': ['ix=2*ox+1*fx', 'iy=2*oy+1*fy'],
        'loop_dim_size': {'B': 1, 'K': 512, 'C': 256, 'OY': 7, 'OX': 7, 'FY': 3, 'FX': 3},
        'operand_precision': {'O': 8, 'O_final': 1, 'W': 4, 'I': 1},
        'operand_source': {'W': [], 'I': [21]},
        'constant_operands': ['W'],
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'G'}},
        'memory_operand_links': {'O': 'O', 'W': 'I2', 'I': 'I1' },
        'padding': {'IY': (1, 0), 'IX': (1, 0)}
    }
    ,
    23: {  # conv5_2
        'operator_type': 'Conv',
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][iy][ix]',
        'dimension_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B': 1, 'K': 512, 'C': 512, 'OY': 7, 'OX': 7, 'FY': 3, 'FX': 3},
        'operand_precision': {'O': 8, 'O_final': 1, 'W': 4, 'I': 1},
        'operand_source': {'W': [], 'I': [22]},
        'constant_operands': ['W'],
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'K'}},
        'memory_operand_links': {'O': 'O', 'W': 'I2', 'I': 'I1' },
        'padding': {'IY': (1, 1), 'IX': (1, 1)}
    },
    24: {  # conv downsample of layer 21
        'operator_type': 'Conv_downsample',
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][iy][ix]',
        'dimension_relations': ['ix=2*ox+1*fx', 'iy=2*oy+1*fy'],
        'loop_dim_size': {'B': 1, 'K': 512, 'C': 256, 'OY': 7, 'OX': 7, 'FY': 3, 'FX': 3},
        'operand_precision': {'O': 8, 'O_final': 1, 'W': 4, 'I': 1},
        'operand_source': {'W': [], 'I': [21]},
        'constant_operands': ['W'],
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'G'}},
        'memory_operand_links': {'O': 'O', 'W': 'I2', 'I': 'I1' },
        'padding': {'IY': (1, 0), 'IX': (1, 0)}
    }
    ,
    25: {  # Addition of layer 24 (residual connection) and layer 23 (main path)
        'operator_type': 'Add',
        'equation': 'O[b][g][oy][ox]=X[b][g][oy][ox]+Y[b][g][oy][ox]',
        'dimension_relations': [],
        'loop_dim_size': {'B': 1, 'G': 512, 'OY': 7, 'OX': 7},
        'operand_precision': {'O': 2, 'X': 1, 'Y': 1, 'O_final': 1},
        'operand_source': {'X': [24], 'Y': [23]},
        'constant_operands': [],
        'operand_source_dimension_mapping': {'X': {'OX': 'OX', 'OY': 'OY', 'G': 'G'}, 'Y': {'OX': 'OX', 'OY': 'OY', 'G': 'K'}},
        'memory_operand_links': {'O': 'O', 'X': 'I2', 'Y': 'I1'}
    }
    ,
    26: {  # conv5_3
        'operator_type': 'Conv',
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][iy][ix]',
        'dimension_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B': 1, 'K': 512, 'C': 512, 'OY': 7, 'OX': 7, 'FY': 3, 'FX': 3},
        'operand_precision': {'O': 8, 'O_final': 1, 'W': 4, 'I': 1},
        'operand_source': {'W': [], 'I': [25]},
        'constant_operands': ['W'],
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'G'}},
        'memory_operand_links': {'O': 'O', 'W': 'I2', 'I': 'I1' },
        'padding': {'IY': (1, 1), 'IX': (1, 1)}
    }
    ,
    27: {  # conv4_4
        'operator_type': 'Conv',
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][iy][ix]',
        'dimension_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B': 1, 'K': 512, 'C': 512, 'OY': 7, 'OX': 7, 'FY': 3, 'FX': 3},
        'operand_precision': {'O': 8, 'O_final': 1, 'W': 4, 'I': 1},
        'operand_source': {'W': [], 'I': [26]},
        'constant_operands': ['W'],
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'K'}},
        'memory_operand_links': {'O': 'O', 'W': 'I2', 'I': 'I1' },
        'padding': {'IY': (1, 1), 'IX': (1, 1)}
    },
    28: {  # Addition of layer 25 (residual connection) and layer 27 (main path)
        'operator_type': 'Add',
        'equation': 'O[b][g][oy][ox]=X[b][g][oy][ox]+Y[b][g][oy][ox]',
        'dimension_relations': [],
        'loop_dim_size': {'B': 1, 'G': 512, 'OY': 7, 'OX': 7},
        'operand_precision': {'O': 2, 'X': 1, 'Y': 1, 'O_final': 2},
        'operand_source': {'X': [25], 'Y': [27]},
        'constant_operands': [],
        'operand_source_dimension_mapping': {'X': {'OX': 'OX', 'OY': 'OY', 'G': 'G'}, 'Y': {'OX': 'OX', 'OY': 'OY', 'G': 'K'}},
        'memory_operand_links': {'O': 'O', 'X': 'I2', 'Y': 'I1'}
    },
    29: {  # aver pool
        'operator_type': 'Pooling',
        'equation': 'O[b][g][oy][ox]+=W[fx][fy]*I[b][g][iy][ix]',
        'dimension_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B': 1, 'G': 512, 'OY': 1, 'OX': 1, 'FX': 7, 'FY': 7},
        'operand_precision': {'O': 2, 'W': 0, 'I': 2, 'O_final': 2},
        'operand_source': {'W': [], 'I': [28]},
        'constant_operands': ['W'],
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'G': 'K'}},
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'}
    },
    30: {  # fc
        'operator_type': 'Conv',
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][iy][ix]',
        'dimension_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B': 1, 'K': 1000, 'C': 512, 'OY': 1, 'OX': 1, 'FY': 1, 'FX': 1},
        'operand_precision': {'O': 8, 'O_final': 1, 'W': 4, 'I': 1},
        'operand_source': {'W': [], 'I': [29]},
        'constant_operands': ['W'],
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'G'}},
        'memory_operand_links': {'O': 'O', 'W': 'I2', 'I': 'I1' },
    },
}
