mapping = {
    "default": {
        "core_allocation": 1,
        "temporal_ordering": [
            # Innermost loop
            ("C", 2),            
            ("C", 16),            
            ("FX", 3),
            ("FY", 3),
            ("C", 8),            
            ("OY", 2.5),
            ("OX", 3),
            ("K", 32),
            ("OY", 2),
            ("K", 8),

            # ("OX", 2),
            # ("OY", 2),
            # ("OX", 7),
            # ("OX", 7),
            # ("OY", 7),
            # ("OY", 7),

            # Outermost loop
        ],        
        "spatial_mapping": {
            "D1": ("K", 32),
            "D2": ("C", 2),
            "D3": ("OX", 4),
            "D4": ("OY", 4),
        },
        "memory_operand_links": {"O": "O", "W": "I2", "I": "I1", "V": "S"},
    },
    "Add": {
        "core_allocation": 1,
        "spatial_mapping": {
            "D1": ("G", 32),
            "D2": ("C", 1),
            "D3": ("OX", 1),
            "D4": ("OY", 1),
        },
        "memory_operand_links": {"O": "O", "X": "I2", "Y": "I1"},
    },
}
