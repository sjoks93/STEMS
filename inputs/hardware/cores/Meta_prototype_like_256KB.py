import os
from zigzag.classes.hardware.architecture.memory_hierarchy import MemoryHierarchy
from zigzag.classes.hardware.architecture.memory_level import MemoryLevel
from zigzag.classes.hardware.architecture.operational_unit import Multiplier
from zigzag.classes.hardware.architecture.operational_array import MultiplierArray
from zigzag.classes.hardware.architecture.memory_instance import MemoryInstance
from zigzag.classes.hardware.architecture.accelerator import Accelerator
from zigzag.classes.hardware.architecture.core import Core


def get_memory_hierarchy(multiplier_array):
    """Memory hierarchy variables"""
    """ size=#bit, bw=(read bw, write bw), cost=(read word energy, write work energy) """
    #RF energy for rd/wr is ~2fJ/bit
    reg_IW1 = MemoryInstance(name="rf_4b_W", size=4, r_bw=4, w_bw=4, r_cost=0.000*4, w_cost=0.000*4, area=0, r_port=1,
                             w_port=1, rw_port=0, latency=1, support_sparsity=False)
    # reg_I1 = MemoryInstance(name="rf_4b_I", size=4, r_bw=4, w_bw=4, r_cost=0.002*4, w_cost=0.000*4, area=0, r_port=1,
    #                          w_port=1, rw_port=0, latency=1, support_sparsity=False)
    reg_O1 = MemoryInstance(name="rf_16b_O", size=16, r_bw=16, w_bw=16, r_cost=0.000*16, w_cost=0.000*16, area=0, r_port=2,
                            w_port=2, rw_port=0, latency=1, support_sparsity=False)

    ##################################### on-chip memory hierarchy building blocks #####################################
    # 8kB SRAM energy for rd/wr is ~100/120 fJ/bit.
    sram_32KB_with_4_8K_64_1r_1w = MemoryInstance(name="sram_32KB", size=8192 * 8 * 4, r_bw=64 * 4, w_bw=64 * 4,
                                                  r_cost=0.1 * 64 * 4, w_cost=0.12 * 64 * 4, area=0, r_port=1, w_port=1,
                                                  rw_port=0, latency=1, min_r_granularity=64, min_w_granularity=64,)

    sram_16KB_with_2_8K_64_1r_1w = MemoryInstance(name="sram_16KB", size=8192 * 8 * 2, r_bw=64 * 2, w_bw=64 * 2,
                                                  r_cost=0.1 * 64 * 2, w_cost=0.12 * 64 * 2, area=0, r_port=1, w_port=1,
                                                  rw_port=0, latency=1, min_r_granularity=64, min_w_granularity=64,)

    # 128kB SRAM energy for rd/wr is ~130/175 fJ/bit.
    sram_1M_with_8_128K_bank_128_1r_1w = MemoryInstance(name="sram_1MB", size=131072 * 8 * 2.1, r_bw=128 * 2,
                                                          w_bw=128 * 2, r_cost=0.13 * 128 * 2, w_cost=0.175 * 128 * 2,
                                                          area=0, r_port=1, w_port=1, rw_port=0, latency=1,
                                                          min_r_granularity=64, min_w_granularity=64)

    #######################################################################################################################


    memory_hierarchy_graph = MemoryHierarchy(operational_array=multiplier_array)

    """
    fh: from high = wr_in_by_high 
    fl: from low = wr_in_by_low 
    th: to high = rd_out_to_high
    tl: to low = rd_out_to_low
    """
    # we don't have unrolled I-Reg to better support G unrolling
    # memory_hierarchy_graph.add_memory(memory_instance=reg_I1, operands=('I1',),
    #                                   port_alloc=({'fh': 'w_port_1', 'tl': 'r_port_1', 'fl': None, 'th': None},),
    #                                   served_dimensions={(1, 0, 0, 0)})
    memory_hierarchy_graph.add_memory(
        memory_instance=reg_IW1,
        operands=("I2",),
        port_alloc=({"fh": "w_port_1", "tl": "r_port_1", "fl": None, "th": None},),
        served_dimensions={(0, 0, 1, 0), (0, 0, 0, 1)},
    )
    memory_hierarchy_graph.add_memory(
        memory_instance=reg_O1,
        operands=("O",),
        port_alloc=(
            {"fh": "w_port_1", "tl": "r_port_1", "fl": "w_port_2", "th": "r_port_2"},
        ),
        served_dimensions={(0, 1, 0, 0)},
    )
    memory_hierarchy_graph.add_memory(
        memory_instance=reg_O1,
        operands=("S",),
        port_alloc=(
            {"fh": "w_port_1", "tl": "r_port_1", "fl": "w_port_2", "th": "r_port_2"},
        ),
        served_dimensions={(0, 1, 0, 0)},
    )
    ##################################### on-chip highest memory hierarchy initialization #####################################

    memory_hierarchy_graph.add_memory(
        memory_instance=sram_32KB_with_4_8K_64_1r_1w,
        operands=("I2",),
        port_alloc=({"fh": "w_port_1", "tl": "r_port_1", "fl": None, "th": None},),
        served_dimensions="all",
    )
    # memory_hierarchy_graph.add_memory(
    #     memory_instance=sram_1M_with_8_128K_bank_128_1r_1w_W,
    #     operands=("I2",),
    #     port_alloc=({"fh": "w_port_1", "tl": "r_port_1", "fl": None, "th": None},),
    #     served_dimensions="all",
    # )

    memory_hierarchy_graph.add_memory(
        memory_instance=sram_16KB_with_2_8K_64_1r_1w,
        operands=("I1",),
        port_alloc=({"fh": "w_port_1", "tl": "r_port_1", "fl": None, "th": None},),
        served_dimensions="all",
    )
    memory_hierarchy_graph.add_memory(
        memory_instance=sram_1M_with_8_128K_bank_128_1r_1w,
        operands=("I1", "I2", "O", "S"),
        port_alloc=(
            {"fh": "w_port_1", "tl": "r_port_1", "fl": None, "th": None},
            {"fh": "w_port_1", "tl": "r_port_1", "fl": None, "th": None},
            {"fh": "w_port_1", "tl": "r_port_1", "fl": "w_port_1", "th": "r_port_1"},
            {"fh": "w_port_1", "tl": "r_port_1", "fl": "w_port_1", "th": "r_port_1"},
        ),
        served_dimensions="all",
    )

    ####################################################################################################################

    # memory_hierarchy_graph.add_memory(memory_instance=dram, operands=('I1', 'I2', 'O'),
    #                                   port_alloc=({'fh': 'rw_port_1', 'tl': 'rw_port_1', 'fl': None, 'th': None},
    #                                               {'fh': 'rw_port_1', 'tl': 'rw_port_1', 'fl': None, 'th': None},
    #                                               {'fh': 'rw_port_1', 'tl': 'rw_port_1', 'fl': 'rw_port_1', 'th': 'rw_port_1'},),
    #                                   served_dimensions='all')

    # from zigzag.visualization.graph.memory_hierarchy import (
    #     visualize_memory_hierarchy_graph,
    # )
    #
    # visualize_memory_hierarchy_graph(memory_hierarchy_graph)
    return memory_hierarchy_graph


def get_operational_array():
    """Multiplier array variables"""
    # Tree size==2 MACs
    # INT4 160 fJ/MAC
    # INT4 70 fJ/MAC
    multiplier_input_precision = [4, 4]
    multiplier_energy = 0.07
    multiplier_area = 1
    dimensions = {
        "D1": 32,
        "D2": 2,
        "D3": 16,
        "D4": 1,
    }  # {'D1': ('K', 32), 'D2': ('C', 2), 'D3': ('OX', 4), 'D4': ('OY', 4),}

    multiplier = Multiplier(
        multiplier_input_precision, multiplier_energy, multiplier_area
    )
    multiplier_array = MultiplierArray(multiplier, dimensions)

    return multiplier_array


def get_dataflows():
    return [{"D1": ("K", 32), "D2": ("C", 2), "D3": ("OY", 16), "D4": ("OX", 1)}]


def get_CN_node_size(factor_loops=list()):
    return [("K", 32), ("C", 2), ("OY", 16), ("OX", 1)] + factor_loops


def get_core(id):
    operational_array = get_operational_array()
    memory_hierarchy = get_memory_hierarchy(operational_array)
    dataflows = get_dataflows()
    core = Core(id, operational_array, memory_hierarchy, dataflows, sparse_speedup=False, sparse_mac=False)
    return core


if __name__ == "__main__":
    print(get_core(1))
