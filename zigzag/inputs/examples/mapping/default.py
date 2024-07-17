mapping = {
    "default": {
        "core_allocation": 1,
        # "temporal_ordering": [
        # #     # Innermost loop
        # #     ("FX", 3),
        # #     ("FY", 3),
        # #     ("K",  8),
        # #     ("OY", 1000),
        # #     ("OX", 1000),
        #     ("FY", 3),
        #     ("FX", 3),
        #     ("OY", 180),
        #     ("OX", 360),

        # #     ("C", 8),
        # #     #("K", 7),
        # #     # ("OY", 7),

        # #     # Outermost loop
        # ],        
        "spatial_mapping": {
            "D1": ("K", 32),
            "D2": ("C", 32),

        },
        "memory_operand_links": {"O": "O", "W": "I2", "I": "I1", "V": "S"},
    },
    "Add": {
        "core_allocation": 1,
        "spatial_mapping": {
            "D1": ("G", 32),
            "D2": ("C", 32),
        },
        "memory_operand_links": {"O": "O", "X": "I2", "Y": "I1"},
    },
}
