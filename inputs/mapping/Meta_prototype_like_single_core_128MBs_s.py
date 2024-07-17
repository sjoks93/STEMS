mapping = {
    "default": {
        "core_allocation": [0,],
    },
    "Conv": {
        "core_allocation": [0,],
    },
    "Gemm": {
        "core_allocation": [0,],
    },
    "Pool": {
        "core_allocation": 0,
    },
    "MaxPool": {
        "core_allocation": 0,
    },
    "AveragePool": {
        "core_allocation": 0,
    },
    "GlobalAveragePool": {
        "core_allocation": 0,
    },
    "Add": {
        "core_allocation": 0,
        "spatial_mapping": {
            "D1": ("K", 32),
            "D2": ("C", 1),
            "D3": ("OX", 1),
            "D4": ("OY", 1),
        },        
    },
}