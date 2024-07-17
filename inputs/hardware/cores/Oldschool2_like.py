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
    reg_I = MemoryInstance(name="rf_2B_I", size=16, r_bw=16, w_bw=16, r_cost=0.002*16, w_cost=0.002*16, area=0, r_port=1,
                             w_port=1, rw_port=0, latency=1, )
    reg_W = MemoryInstance(name="rf_2B_W", size=16, r_bw=16, w_bw=16, r_cost=0.002*16, w_cost=0.002*16, area=0, r_port=1,
                             w_port=1, rw_port=0, latency=1, support_sparsity=True)
    reg_O1 = MemoryInstance(name="rf_2B", size=16, r_bw=16, w_bw=16, r_cost=0.002*16, w_cost=0.002*16, area=0, r_port=2,
                            w_port=2, rw_port=0, latency=1, support_sparsity=True)

    ##################################### on-chip memory hierarchy building blocks #####################################
    # 8kB SRAM energy for rd/wr is ~100/120 fJ/bit.
    sram_64KB_with_8_8K_64_1r_1w = MemoryInstance(name="sram_64KB", size=8192 * 8 * 8, r_bw=64 * 8, w_bw=64 * 8,
                                                  r_cost=0.1 * 64 * 8, w_cost=0.12 * 64 * 8, area=0, r_port=1, w_port=1,
                                                  rw_port=0, latency=1, min_r_granularity=64, min_w_granularity=64,)

    sram_32KB_with_4_8K_64_1r_1w = MemoryInstance(name="sram_32KB", size=8192 * 8 * 4, r_bw=64 * 4, w_bw=64 * 4,
                                                  r_cost=0.1 * 64 * 4, w_cost=0.12 * 64 * 4, area=0, r_port=1, w_port=1,
                                                  rw_port=0, latency=1, min_r_granularity=64, min_w_granularity=64,)

    # 128kB SRAM energy for rd/wr is ~130/175 fJ/bit.
    sram_1M_with_8_128K_bank_128_1r_1w = MemoryInstance(name="sram_1MB", size=131072 * 8 * 8, r_bw=128 * 8,
                                                          w_bw=128 * 8, r_cost=0.13 * 128 * 8, w_cost=0.175 * 128 * 8,
                                                          area=0, r_port=1, w_port=1, rw_port=0, latency=1,
                                                          min_r_granularity=64, min_w_granularity=64)

    # sram_1M_with_8_128K_bank_128_1r_1w_W = MemoryInstance(name="sram_1MB_W", size=131072 * 8 * 8, r_bw=128 * 8,
    #                                                       w_bw=128 * 8, r_cost=0.13 * 128 * 8, w_cost=0.175 * 128 * 8,
    #                                                       area=0, r_port=1, w_port=1, rw_port=0, latency=1,
    #                                                       min_r_granularity=64, min_w_granularity=64)

    #######################################################################################################################

    # dram = MemoryInstance(name="dram", size=10000000000, r_bw=64, w_bw=64, r_cost=700, w_cost=750, area=0,
    #                       r_port=0, w_port=0, rw_port=1, latency=1)

    memory_hierarchy_graph = MemoryHierarchy(operational_array=multiplier_array)


    """
    fh: from high = wr_in_by_high 
    fl: from low = wr_in_by_low 
    th: to high = rd_out_to_high
    tl: to low = rd_out_to_low
    """
    # we don't have unrolled I-Reg to better support G unrolling
    memory_hierarchy_graph.add_memory(memory_instance=reg_I, operands=('I1',),
                                      port_alloc=({'fh': 'w_port_1', 'tl': 'r_port_1', 'fl': None, 'th': None},),
                                      served_dimensions={(1, 0)})
    memory_hierarchy_graph.add_memory(
        memory_instance=reg_W,
        operands=("I2",),
        port_alloc=({"fh": "w_port_1", "tl": "r_port_1", "fl": None, "th": None},),
        served_dimensions={(0, 0)},
    )
    memory_hierarchy_graph.add_memory(
        memory_instance=reg_O1,
        operands=("O",),
        port_alloc=(
            {"fh": "w_port_1", "tl": "r_port_1", "fl": "w_port_2", "th": "r_port_2"},
        ),
        served_dimensions={(0, 1)},
    )
    memory_hierarchy_graph.add_memory(
        memory_instance=reg_O1,
        operands=("S",),
        port_alloc=(
            {"fh": "w_port_1", "tl": "r_port_1", "fl": "w_port_2", "th": "r_port_2"},
        ),
        served_dimensions={(0, 1)},
    )
    ##################################### on-chip highest memory hierarchy initialization #####################################

    memory_hierarchy_graph.add_memory(
        memory_instance=sram_64KB_with_8_8K_64_1r_1w,
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
        memory_instance=sram_32KB_with_4_8K_64_1r_1w,
        operands=("I1", "O", "S"),
        port_alloc=({"fh": "w_port_1", "tl": "r_port_1", "fl": None, "th": None},
            {"fh": "w_port_1", "tl": "r_port_1", "fl": "w_port_1", "th": "r_port_1"},
            {"fh": "w_port_1", "tl": "r_port_1", "fl": "w_port_1", "th": "r_port_1"},),
       
        served_dimensions="all",
    )
    memory_hierarchy_graph.add_memory(
        memory_instance=sram_1M_with_8_128K_bank_128_1r_1w,
        operands=("I1", "O", "S", "I2"),
        port_alloc=(
            {"fh": "w_port_1", "tl": "r_port_1", "fl": None, "th": None},
            {"fh": "w_port_1", "tl": "r_port_1", "fl": "w_port_1", "th": "r_port_1"},
            {"fh": "w_port_1", "tl": "r_port_1", "fl": "w_port_1", "th": "r_port_1"},
            {"fh": "w_port_1", "tl": "r_port_1", "fl": None, "th": None},
        ),
        served_dimensions="all",
    )

    ####################################################################################################################

    # memory_hierarchy_graph.add_memory(memory_instance=dram, operands=('I1', 'I2', 'O', 'S'),
    #                                   port_alloc=({'fh': 'rw_port_1', 'tl': 'rw_port_1', 'fl': None, 'th': None},
    #                                               {'fh': 'rw_port_1', 'tl': 'rw_port_1', 'fl': None, 'th': None},
    #                                               {'fh': 'rw_port_1', 'tl': 'rw_port_1', 'fl': 'rw_port_1', 'th': 'rw_port_1'},
    #                                               {'fh': 'rw_port_1', 'tl': 'rw_port_1', 'fl': 'rw_port_1', 'th': 'rw_port_1'},),
    #                                   served_dimensions='all')

    return memory_hierarchy_graph


def get_operational_array():
    """Multiplier array variables"""
    # Tree size==2 MACs
    # INT8 400 fJ/MAC
    # INT4 150 fJ/MAC
    # INT2 80 fJ/MAC
    multiplier_input_precision = [8, 8]
    multiplier_energy = 0.07#0.03#0.4
    multiplier_area = 1
    dimensions = {
        "D1": 32,
        "D2": 32,
    }  # {'D1': ('K', 32), 'D2': ('C', 2), 'D3': ('OX', 4), 'D4': ('OY', 4),}

    multiplier = Multiplier(
        multiplier_input_precision, multiplier_energy, multiplier_area
    )
    multiplier_array = MultiplierArray(multiplier, dimensions)

    return multiplier_array


def get_dataflows():
    return [{"D1": ("K", 32), "D2": ("C", 32)}]


def get_CN_node_size(factor_loops=list()):
    return [("K", 32), ("C", 32)] + factor_loops


def get_core(id):
    operational_array = get_operational_array()
    memory_hierarchy = get_memory_hierarchy(operational_array)
    dataflows = get_dataflows()
    core = Core(id, operational_array, memory_hierarchy, dataflows, sparse_speedup=True)
    return core


if __name__ == "__main__":
    print(get_core(1))
