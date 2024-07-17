mapping = {
    "default": {
        "core_allocation": 1,
        "temporal_ordering": [
            # Innermost loop
            ("C", 32),
            ("IY", 4),
            ("IX", 4),
            ("IY", 49),
            ("K", 2),
            ("IY", 4),
            ("IX", 49),
            ("IX", 4),

            # Outermost loop
        ],        
        "spatial_mapping": {
            "D1": ("FX", 3),
            "D2": ("FY", 3),
            "D3": ("K", 32),
        },
        "memory_operand_links": {"O": "O", "W": "I2", "I": "I1", "V": "S"},
    },
    "Add": {
        "core_allocation": 1,
        "spatial_mapping": {
            "D1": ("IX", 1),
            "D2": ("IY", 1),

        },
        "memory_operand_links": {"O": "O", "X": "I2", "Y": "I1"},
    },
}
