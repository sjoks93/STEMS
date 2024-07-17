import os
from zigzag.classes.hardware.architecture.memory_hierarchy import MemoryHierarchy
from zigzag.classes.hardware.architecture.memory_level import MemoryLevel
from zigzag.classes.hardware.architecture.operational_unit import Multiplier
from zigzag.classes.hardware.architecture.operational_array import MultiplierArray
from zigzag.classes.hardware.architecture.memory_instance import MemoryInstance
from zigzag.classes.hardware.architecture.accelerator import Accelerator
from zigzag.classes.hardware.architecture.core import Core

w_size = 4
feature_size = 8
s_size = 1

def memory_hierarchy_dut(multiplier_array):
    """Memory hierarchy variables"""
    """ size=#bit, bw=(read bw, write bw), cost=(read word energy, write work energy) """
    #RF energy for rd/wr is ~2fJ/bit



    reg_W = MemoryInstance(name="rf_W", size=w_size * 32 * 3 * 3, r_bw=w_size * 3 * 3, w_bw=w_size * 32 * 3 * 3, r_cost=0.002*w_size*3*3, w_cost=0.002* w_size * 32*3*3, area=0, r_port=1,
                             w_port=1, rw_port=0, latency=1, support_sparsity=True)

    reg_I = MemoryInstance(name="rf_I", size= s_size * 32, r_bw=s_size, w_bw=s_size * 32, r_cost=0.002*s_size * 32, w_cost=0.002* s_size * 32, area=0, r_port=1,
                             w_port=1, rw_port=0, latency=1, support_sparsity=True)
    
    reg_O = MemoryInstance(name="rf_O", size=(s_size), r_bw=s_size, w_bw=s_size, r_cost=0.002*(s_size), w_cost=0.002*(s_size), area=0, r_port=2,
                            w_port=2, rw_port=0, latency=1, support_sparsity=True)
    reg_S = MemoryInstance(name="rf_S", size=(feature_size), r_bw=feature_size, w_bw=feature_size, r_cost=0.002*(feature_size), w_cost=0.002*(feature_size), area=0, r_port=2,
                            w_port=2, rw_port=0, latency=1, support_sparsity=True)    
    # reg_S = MemoryInstance(name="rf_S", size=feature_size, r_bw=feature_size, w_bw=feature_size, r_cost=0.002*feature_size, w_cost=0.002*feature_size, area=0, r_port=2,
    #                         w_port=2, rw_port=0, latency=1, )
    
    ##################################### on-chip memory hierarchy building blocks #####################################
    # 8kB SRAM energy for rd/wr is ~100/120 fJ/bit.
    # sram_64KB_with_8_8K_64_1r_1w = MemoryInstance(name="sram_64KB", size=8192 * 8 * 8, r_bw=64 * 8, w_bw=64 * 8,
    #                                               r_cost=0.1 * 64 * 8, w_cost=0.12 * 64 * 8, area=0, r_port=1, w_port=1,
    #                                               rw_port=0, latency=1, min_r_granularity=64, min_w_granularity=64,)

    # sram_32KB_with_4_8K_64_1r_1w = MemoryInstance(name="sram_32KB", size=8192 * 8 * 4, r_bw=64 * 4, w_bw=64 * 4,
    #                                               r_cost=0.1 * 64 * 4, w_cost=0.12 * 64 * 4, area=0, r_port=1, w_port=1,
    #                                               rw_port=0, latency=1, min_r_granularity=64, min_w_granularity=64,)
    sram_96KB_with_12_8K_64_1r_1iow = MemoryInstance(name="sram_32KB", size=8192 * 8 * 12, r_bw=64 * 12, w_bw=64 * 12,
                                                  r_cost=0.1 * 64 * 12, w_cost=0.12 * 64 * 12, area=0, r_port=1, w_port=1,
                                                  rw_port=0, latency=1, min_r_granularity=64, min_w_granularity=64,)
    # 128kB SRAM energy for rd/wr is ~130/175 fJ/bit.
    # sram_1M_with_8_128K_bank_128_1r_1w_A = MemoryInstance(name="sram_1MB_A", size=131072 * 8 * 8, r_bw=128 * 8,
    #                                                       w_bw=128 * 8, r_cost=0.13 * 128 * 8, w_cost=0.175 * 128 * 8,
    #                                                       area=0, r_port=1, w_port=1, rw_port=0, latency=1,
    #                                                       min_r_granularity=64, min_w_granularity=64)

    # sram_1M_with_8_128K_bank_128_1r_1w_W = MemoryInstance(name="sram_1MB_W", size=131072 * 8 * 8, r_bw=128 * 8,
    #                                                       w_bw=128 * 8, r_cost=0.13 * 128 * 8, w_cost=0.175 * 128 * 8,
    #                                                       area=0, r_port=1, w_port=1, rw_port=0, latency=1,
    #                                                       min_r_granularity=64, min_w_granularity=64)
    # sram_2M_with_16_128K_bank_128_1r_1w_AW = MemoryInstance(name="sram_2MB_AW", size=2 * 131072 * 8 * 8, r_bw=128 * 8,
    #                                                       w_bw=128 * 8, r_cost= 0.13 * 128 * 8, w_cost= 0.175 * 128 * 8,
    #                                                       area=0, r_port=2, w_port=2, rw_port=0, latency=1,
    #                                                       min_r_granularity=64, min_w_granularity=64)

    #######################################################################################################################

    dram = MemoryInstance(name="dram", size=10000000000, r_bw=64, w_bw=64, r_cost=700, w_cost=750, area=0,
                          r_port=0, w_port=0, rw_port=1, latency=1)

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
                                      served_dimensions="all")
    memory_hierarchy_graph.add_memory(
        memory_instance=reg_W,
        operands=("I2",),
        port_alloc=({"fh": "w_port_1", "tl": "r_port_1", "fl": None, "th": None},),
        served_dimensions={(1, 1, 0)},
    )
    memory_hierarchy_graph.add_memory(
        memory_instance=reg_O,
        operands=("O"),
        port_alloc=(
            {"fh": "w_port_1", "tl": "r_port_1", "fl": "w_port_2", "th": "r_port_2"},
        ),
        served_dimensions={(0, 0, 0)},
    )
    memory_hierarchy_graph.add_memory(
        memory_instance=reg_S,
        operands=("S"),
        port_alloc=(
            {"fh": "w_port_1", "tl": "r_port_1", "fl": "w_port_2", "th": "r_port_2"},
        ),
        served_dimensions={(0, 0, 0)},
    )    
    # memory_hierarchy_graph.add_memory(
    #     memory_instance=reg_S,
    #     operands=("S",),
    #     port_alloc=(
    #         {"fh": "w_port_1", "tl": "r_port_1", "fl": "w_port_2", "th": "r_port_2"},
    #     ),
    #     served_dimensions={(0, 1, 0, 0)},
    # )
    ##################################### on-chip highest memory hierarchy initialization #####################################

    memory_hierarchy_graph.add_memory(
        memory_instance=sram_96KB_with_12_8K_64_1r_1iow,
        operands=("I2", "I1", "S", "O"),
        port_alloc=({"fh": "w_port_1", "tl": "r_port_1", "fl": None, "th": None},
        {"fh": "w_port_1", "tl": "r_port_1", "fl": None, "th": None},
        {"fh": "w_port_1", "tl": "r_port_1", "fl": "w_port_1", "th": "r_port_1"},
        {"fh": "w_port_1", "tl": "r_port_1", "fl": "w_port_1", "th": "r_port_1"},),
        served_dimensions="all",
    )
    # memory_hierarchy_graph.add_memory(
    #     memory_instance=sram_1M_with_8_128K_bank_128_1r_1w_W,
    #     operands=("I2",),
    #     port_alloc=({"fh": "w_port_1", "tl": "r_port_1", "fl": None, "th": None},),
    #     served_dimensions="all",
    # )

    # memory_hierarchy_graph.add_memory(
    #     memory_instance=sram_32KB_with_4_8K_64_1r_1w,
    #     operands=("S", "O"),
    #     port_alloc=(#{"fh": "w_port_1", "tl": "r_port_1", "fl": None, "th": None},
    #                {"fh": "w_port_1", "tl": "r_port_1", "fl": "w_port_1", "th": "r_port_1"},
    #                {"fh": "w_port_1", "tl": "r_port_1", "fl": "w_port_1", "th": "r_port_1"},),
    #     served_dimensions="all",
    # )
    # memory_hierarchy_graph.add_memory(
    #     memory_instance=sram_2M_with_16_128K_bank_128_1r_1w_AW,
    #     operands=("I1", "O", "S", "I2"),
    #     port_alloc=(
    #         {"fh": "w_port_1", "tl": "r_port_1", "fl": None, "th": None},
    #         {"fh": "w_port_1", "tl": "r_port_1", "fl": "w_port_1", "th": "r_port_1"},
    #         {"fh": "w_port_1", "tl": "r_port_1", "fl": "w_port_1", "th": "r_port_1"},
    #         {"fh": "w_port_2", "tl": "r_port_2", "fl": None, "th": None},

    #     ),
    #     served_dimensions="all",
    # )

    ####################################################################################################################

    memory_hierarchy_graph.add_memory(memory_instance=dram, operands=('I1', 'I2', 'O', 'S'),
                                      port_alloc=({'fh': 'rw_port_1', 'tl': 'rw_port_1', 'fl': None, 'th': None},
                                                  {'fh': 'rw_port_1', 'tl': 'rw_port_1', 'fl': None, 'th': None},
                                                  {'fh': 'rw_port_1', 'tl': 'rw_port_1', 'fl': 'rw_port_1', 'th': 'rw_port_1'},
                                                  {'fh': 'rw_port_1', 'tl': 'rw_port_1', 'fl': 'rw_port_1', 'th': 'rw_port_1'},),
                                      served_dimensions='all')

    # from zigzag.visualization.graph.memory_hierarchy import (
    #     visualize_memory_hierarchy_graph,
    # )
    #
    # visualize_memory_hierarchy_graph(memory_hierarchy_graph)
    return memory_hierarchy_graph


def multiplier_array_dut():
    """Multiplier array variables"""
    multiplier_input_precision = [8, 8]
    multiplier_energy = 0.04
    multiplier_area = 1
    dimensions = {
        "D1": 3,
        "D2": 3,
        "D3": 32,
    }  # {'D1': ('K', 32), 'D2': ('C', 2), 'D3': ('OX', 4), 'D4': ('OY', 4),}

    multiplier = Multiplier(
        multiplier_input_precision, multiplier_energy, multiplier_area
    )
    multiplier_array = MultiplierArray(multiplier, dimensions)

    return multiplier_array


def cores_dut():
    multiplier_array1 = multiplier_array_dut()
    memory_hierarchy1 = memory_hierarchy_dut(multiplier_array1)

    core1 = Core(1, multiplier_array1, memory_hierarchy1, sparse_speedup=True)

    return {core1}


cores = cores_dut()
acc_name = os.path.basename(__file__)[:-3]
accelerator = Accelerator(acc_name, cores)