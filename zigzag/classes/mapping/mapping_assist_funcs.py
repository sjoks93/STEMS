from typing import Dict, List
from typing import TYPE_CHECKING
from math import prod, ceil, floor

from copy import deepcopy
import numpy as np
from zigzag.utils import pickle_deepcopy



if TYPE_CHECKING:
    from zigzag.classes.workload.layer_node import LayerNode

## Collect information of each single loop tuple in mapping.
# Applied range: from the lowest architectural level to the current level.

class InputLoop:
    def __init__(self, T, C, Y, X, FX, FY):
        self.T = T
        self.C = C
        self.Y = Y
        self.X = X
        self.FX = FX
        self.FY = FY

    def equal(self, loop):
        if loop.T == self.T and loop.C == self.C and loop.Y == self.Y and loop.X == self.X and loop.FX == self.FX and loop.FY == self.FY:
            return True
        else:
            return False
        
    def getCost(self):
        return self.rate, self.count, self.total
    
    def setCost(self, rate, count, total):
        self.rate = rate
        self.count = count
        self.total = total
    
    def __str__(self):
        return str(self.T) + str(self.C) + str(self.Y) + str(self.X) + str(self.FX) + str(self.FY)

    def __repr__(self):
        return str(self.T) + str(self.C) + str(self.Y) + str(self.X) + str(self.FX) + str(self.FY)
class Loop:

    ## The class constructor
    # @param loop
    # @param MAC_op
    # @param data_elem
    def __init__(self, loop: tuple, MAC_op: int, data_elem: int):
        self.loop = loop
        self.MAC_op = MAC_op
        self.data_elem = data_elem
        self.reuse = MAC_op / data_elem

    def __str__(self):
        return str(self.loop)

    def __repr__(self):
        return str(self.loop)

## This function decouples the pr loops into data size (r loops) and data reuse (ir loops).
# It also provides a transferred mapping dictionary in which the pr loops are replaced by r and ir loops.



# def find_zero_tiless(layer_node: "LayerNode", tile_size_per_lvl: Dict, lv: int):
#     if(layer_node.input_path is None):
#         return [1, 1, 1, 1]
#     else:
#         return [0.031375125, 0.031375125, 0.062625, 1] #[Reg<->ALU, BUF<->REG, DRAM<->BUF, <->DRAM]
    
def count_zeros(inner_loop_dims, layer_node):

    return 1, 1
    # if layer_node.input_path is None:
    #     return 1, 1
    # else:
    #     input_tile = layer_node.input_tile
    # t_in, c_in, y_in, x_in, fx, fy = inner_loop_dims
    # t, c, y, x = input_tile.shape
    # stride = layer_node.stride
    # kernel = layer_node.filter_size
    # kernel_loop = int(kernel[0]/fx), int(kernel[1]/fy)
    # t_out, c_out, y_out, x_out = ceil(t/t_in), ceil(c/c_in), ceil(y/(stride[1] * y_in)), ceil(x/(stride[0] * x_in))
    # total_tiles = t_out * c_out * x_out * y_out * kernel_loop[0] * kernel_loop[1]
    # if total_tiles == 1:
    #     return 1, 1
    # zero_tiles = 0  

    # for t_o in range(t_out):
    #     t_range_start = t_o * t_in
    #     t_range_end = (t_o + 1) * t_in
    #     for c_o in range(c_out):
    #         c_range_start = c_o * c_in 
    #         c_range_end = (c_o + 1) * c_in            
    #         for y_o in range(y_out):
    #             for k_y in range(kernel_loop[1]):
    #                 y_range_start = int(max(y_in * y_o * stride[1] - (fy-1)/2 + k_y, 0))
    #                 y_range_end = int(min(y_in * (y_o + 1) * stride[1] + (fy-1)/2 - (stride[1] - 1) + k_y, y))
    #                 for x_o in range(x_out):
    #                     for k_x in range(kernel_loop[0]):
    #                         x_range_start = int(max(x_in * x_o * stride[0] - fx/2 + k_x, 0))
    #                         x_range_end = int(min(x_in * (x_o+1) * stride[0] + fx/2 - (stride[0] - 1) + k_x, x))
    #                         subarray = input_tile[t_range_start:t_range_end, c_range_start:c_range_end, 
    #                                 y_range_start:y_range_end, x_range_start:x_range_end]
    #                         if not np.any(subarray):
    #                             zero_tiles += 1
    # non_zero_tiles = total_tiles - zero_tiles
    # return non_zero_tiles, total_tiles

def get_input_rate(input_tile):
    return np.count_nonzero(input_tile)/input_tile.size

def find_zero_tiles(layer_node: "LayerNode", tile_size_per_lvl: Dict, kernel_tilesize_perlvl: Dict,lv: int):
    
    non_zero_tiles = []
    total_tiles = []
    rate_tiles = []
    if layer_node.input_path is None: 
        return np.ones(lv+1)    
    inner_loop = {}
    kernel_loop = {}

    for i in range(lv):
        non_zero_tiles.append(0)
        total_tiles.append(1)
        rate_tiles.append(1)
        # for op in tile_size_per_lvl:
        #     inner_loop[op] = int(prod(tile_size_per_lvl[op][:i+1]))
        # for op in kernel_tilesize_perlvl:
        #     kernel_loop[op] = int(prod(kernel_tilesize_perlvl[op][:i+1]))
        # c_in = inner_loop['C']
        # x_in = inner_loop['X']
        # y_in = inner_loop['Y']
        # t_in = inner_loop['T']
        # fx_in = kernel_loop['FX']
        # fy_in = kernel_loop['FY']
        # loop = InputLoop(t_in, c_in, y_in, x_in, fx_in, fy_in)
        # found = False
        # for inner in layer_node.input_tile_history:
        #     if inner.equal(loop):
        #         found = True
        #         loop = inner
        #         break
        # if found:
        #     rate_tiles[i], non_zero_tiles[i], total_tiles[i] = loop.getCost()
        # else:
        #     non_zero_tiles[i], total_tiles[i] = count_zeros([loop.T, loop.C, loop.Y, loop.X, loop.FX, loop.FY], layer_node)
        #     rate_tiles [i] = non_zero_tiles[i] / total_tiles[i]
        #     loop.setCost(rate_tiles[i], non_zero_tiles[i], total_tiles[i])
        #     layer_node.input_tile_history.append(loop)
    rate_tiles.append(1)
    # print(rate_tiles)
    return rate_tiles

    

def decouple_pr_loop(mapping_dict: Dict, layer_node: "LayerNode", s_operand: str = None):

    operand_loop_dim = {
        op: layer_node.operand_loop_dim[op] for op in mapping_dict.keys() if layer_node.operand_loop_dim.__contains__(op)
    }
    r_ir_operand_loop_LUT = {
        op: relevance["r"] + relevance["ir"]
        for (op, relevance) in operand_loop_dim.items()
    }
    pr_operand_loop_LUT = {
        op: relevance["pr"]
        for (op, relevance) in operand_loop_dim.items()
        if relevance["pr"] != {}
    }
    pr_operand_list = list(pr_operand_loop_LUT.keys())
    pr_orig = pr_operand_list.copy()
    if s_operand is None:
        pass
    else:
        pr_operand_list = [s_operand]

    mapping_dict_reform = pickle_deepcopy(mapping_dict)

    # current and below level pr data size
    cabl_pr_data_size = {}
    # current and below level pr data reuse
    cabl_pr_data_reuse = {}

    # each single pr loop data size
    per_pr_data_size = {}
    # each single pr loop data reuse
    per_pr_data_reuse = {}
    for i, operand in enumerate(pr_operand_list):

        # initialize current and below level pr loop size
        cabl_pr_lp_size = {
            pr_data_dim: {
                pr_loop_dim: 1
                for pr_loop_dim in pr_operand_loop_LUT[pr_orig[i]][pr_data_dim]
            }
            for pr_data_dim in pr_operand_loop_LUT[pr_orig[i]].keys()
        }

        # initialize current and below level pr data size
        cabl_pr_data_size[operand] = {
            pr_data_dim: [[] for _ in range(len(mapping_dict[operand]))]
            for pr_data_dim in pr_operand_loop_LUT[pr_orig[i]].keys()
        }
        # initialize current and below level pr data reuse
        cabl_pr_data_reuse[operand] = {
            pr_data_dim: [[] for _ in range(len(mapping_dict[operand]))]
            for pr_data_dim in pr_operand_loop_LUT[pr_orig[i]].keys()
        }

        # initialize per pr loop data size
        per_pr_data_size[operand] = {
            pr_data_dim: [[] for _ in range(len(mapping_dict[operand]))]
            for pr_data_dim in pr_operand_loop_LUT[pr_orig[i]].keys()
        }

        # initialize per pr loop data reuse
        per_pr_data_reuse[operand] = {
            pr_data_dim: [[] for _ in range(len(mapping_dict[operand]))]
            for pr_data_dim in pr_operand_loop_LUT[pr_orig[i]].keys()
        }

        # update the cabl_pr_lp_size by multiply pr loop size across architectural level
        for level, loop_list in enumerate(mapping_dict[operand]):
            for loop_type, loop_size in loop_list:
                if loop_type in r_ir_operand_loop_LUT[pr_orig[i]]:
                    continue
                for pr_data_dim in pr_operand_loop_LUT[pr_orig[i]].keys():
                    if any(
                        lp_type == loop_type
                        for lp_type in pr_operand_loop_LUT[pr_orig[i]][pr_data_dim]
                    ):
                        cabl_pr_lp_size[pr_data_dim][loop_type] *= loop_size

                        # compute pr related data dimension size and data dimension reuse at current and below joint levels
                        # based on pr_funcs (dynamic functions extracted in LayerNode). Each pr loop is decoupled into r and ir loops.
                        pr_loop_combined_to_r = layer_node.calc_tensor_dim(
                            cabl_pr_lp_size[pr_data_dim], pr_data_dim
                        )
                        pr_loop_combined_to_ir = (
                            prod(cabl_pr_lp_size[pr_data_dim].values())
                            / pr_loop_combined_to_r
                        )
                        cabl_pr_data_size[operand][pr_data_dim][level].append(
                            pr_loop_combined_to_r
                        )
                        cabl_pr_data_reuse[operand][pr_data_dim][level].append(
                            pr_loop_combined_to_ir
                        )

        # compute pr related data dimension size and data dimension reuse at each level for each pr loop
        # based on cabl_pr_data_size/cabl_pr_data_reuse """
        for pr_data_dim in cabl_pr_data_size[operand].keys():
            data_size_list = cabl_pr_data_size[operand][pr_data_dim]
            data_reuse_list = cabl_pr_data_reuse[operand][pr_data_dim]
            previous_data_size = 1
            previous_data_data_reuse = 1
            for level, va_list in enumerate(data_size_list):
                for idx in range(len(va_list)):
                    per_pr_data_size[operand][pr_data_dim][level].append(
                        data_size_list[level][idx] / previous_data_size
                    )
                    per_pr_data_reuse[operand][pr_data_dim][level].append(
                        data_reuse_list[level][idx] / previous_data_data_reuse
                    )
                    previous_data_size = data_size_list[level][idx]
                    previous_data_data_reuse = data_reuse_list[level][idx]

        mapping_dict_reform[operand] = replace_pr_loop_in_mapping(
            mapping_dict[operand],
            per_pr_data_size[operand],
            per_pr_data_reuse[operand],
            pr_operand_loop_LUT[pr_orig[i]],
            r_ir_operand_loop_LUT[pr_orig[i]],
        )
    # return mapping_dict_reform, cabl_pr_data_size, cabl_pr_data_reuse, per_pr_data_size, per_pr_data_reuse
    return mapping_dict_reform

## This function replaces all pr loops in a mapping of a single operand with r and ir loops.
# @param single_operand_mapping
# @param per_pr_data_size
# @param per_pr_data_reuse
# @param pr_operand_loop_LUT
# @param r_ir_operand_loop_LUT
def replace_pr_loop_in_mapping(
    single_operand_mapping: Dict,
    per_pr_data_size: Dict,
    per_pr_data_reuse: Dict,
    pr_operand_loop_LUT: Dict,
    r_ir_operand_loop_LUT: List,
):
    mapping_new = pickle_deepcopy(single_operand_mapping)
    for level, loop_list in enumerate(single_operand_mapping):
        # Introduce the current level pr loop index to distinguish different pr loops at the same architectural level
        cl_pr_lp_idx_local = {
            pr_data_dim: 0 for pr_data_dim in pr_operand_loop_LUT.keys()
        }
        cl_pr_lp_idx_global = 0
        for idx, (loop_type, loop_size) in enumerate(loop_list):
            if loop_type in r_ir_operand_loop_LUT:
                continue
            for pr_data_dim in pr_operand_loop_LUT.keys():
                if any(
                    lp_type == loop_type for lp_type in pr_operand_loop_LUT[pr_data_dim]
                ):
                    # replace the pr loop in the mapping by r loop
                    pr_idx_local = cl_pr_lp_idx_local[pr_data_dim]
                    pr_idx_global = cl_pr_lp_idx_global
                    mapping_new[level][idx + pr_idx_global] = (
                        pr_data_dim + "_r",
                        per_pr_data_size[pr_data_dim][level][pr_idx_local],
                    )
                    # insert ir loop after the r loop 
                    # NOTE: Here we insert the ir loop after/above the r loop, which indicates that we ignore the input FIFO effect
                    # during current level feeds data to below level. We could also insert the ir loop before/below the r loop,
                    # which leads to more energy-efficient mapping if the innermost ir loop merging down is enabled.
                    mapping_new[level].insert(
                        idx + pr_idx_global + 1,
                        (
                            pr_data_dim + "_ir",
                            per_pr_data_reuse[pr_data_dim][level][pr_idx_local],
                        ),
                    )
                    # update the pr loop index
                    cl_pr_lp_idx_local[pr_data_dim] += 1
                    cl_pr_lp_idx_global += 1
    return mapping_new


# This function generates detailed information for each single loop item for each operand.
def calc_data_size_MAC_count_per_loop(
    mapping_dict_reform: Dict, operand_loop_dim_reform: Dict
):
    detailed_mapping_dict = deepcopy(mapping_dict_reform)
    for operand, mapping_list in mapping_dict_reform.items():
        MAC_count = 1
        data_elem = 1
        for level, loop_list in enumerate(mapping_dict_reform[operand]):
            for idx, (loop_type, loop_size) in enumerate(loop_list):
                MAC_count *= loop_size
                if loop_type in operand_loop_dim_reform[operand]["r"]:
                    data_elem *= loop_size
                detailed_mapping_dict[operand][level][idx] = Loop(
                    (loop_type, loop_size), round(MAC_count), round(data_elem)
                )
    return detailed_mapping_dict
