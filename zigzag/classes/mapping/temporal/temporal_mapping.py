from typing import Dict
from math import prod
from zigzag.classes.workload.layer_node import LayerNode
from zigzag.utils import pickle_deepcopy

## Class that collect all the info related to temporal mapping.
class TemporalMapping:

    ## The class constructor
    # @param temporal_mapping_dict
    # @param layer_node
    def __init__(self, temporal_mapping_dict: Dict, layer_node: LayerNode):
        self.mapping_dic_origin = temporal_mapping_dict
        self.layer_node = layer_node
        self.operand_list = layer_node.operand_list

        # Extract memory hierarchy level count for each operand from temporal mapping definition
        self.mem_level = {op: len(tmap) for (op, tmap) in temporal_mapping_dict.items()}
        # print(temporal_mapping_dict)
        # For each memory level, if the innermost/bottom loop is ir loop, merge it down to the below level
        self.innermost_stationary_loop_merge_down()

        # Calculate the current and below level (cabl) iteration cycle for each memory level, 
        # i.e., each memory level refreshes once, how many cycles it covers
        self.calc_cycle_cabl_level()

        # Calculate the current and below loop (cabl) iteration cycle for each loop,
        # i.e., each loop iterates once, how many cycles it covers '''
        # self.calc_cycle_cabl_loop()

        # Calculate the top-ir loop size at each memory level, which will be used 
        # to compute instant required memory BW in combined_mapping.py """
        self.calc_top_r_and_ir_loop()

        self.calc_output_ir_loop()
        self.calc_output_r_stationary_loop()
        # print("eyooo")
        # print(self.cycle_cabl_level)
        # print(self.top_r_loop_size)
        # print(self.top_ir_loop_size)

    def __str__(self):
        return str(self.mapping_dic_stationary)

    def __repr__(self):
        return str(self)

    ## JSON representation of this object to save it to a json file.
    def __jsonrepr__(self):
        return {"temporal_mapping": self.mapping_dic_stationary}

    ## Iteratively merging down the ir loops which located at the bottom position of each memory level.
    # Also calculate the MAC level data stationary cycle, i,e., the innermost memory level's bottom ir loops.
    def innermost_stationary_loop_merge_down(self):
        # Initialization
        mapping_current = pickle_deepcopy(self.mapping_dic_origin)
        mapping_previous = pickle_deepcopy(self.mapping_dic_origin)
        done = False

        while not done:
            mapping_st = {
                op: [[] for _ in range(self.mem_level[op])] for op in self.operand_list
            }
            MAC_level_st = {op: 1 for op in self.operand_list}
            for operand in self.mem_level.keys():
                for level, current_level_loops in enumerate(mapping_previous[operand]):
                    if not current_level_loops:
                        mapping_st[operand][level] = pickle_deepcopy(
                            current_level_loops
                        )
                    else:
                        for loop_type, loop_dim in current_level_loops:
                            if (
                                loop_type
                                in self.layer_node.operand_loop_dim[operand]["ir"]
                            ):
                                if level == 0:
                                    MAC_level_st[operand] *= loop_dim
                                    mapping_st[operand][level].append(
                                        (loop_type, loop_dim)
                                    )
                                    mapping_current[operand][level].remove(
                                        (loop_type, loop_dim)
                                    )
                                else:
                                    mapping_st[operand][level - 1].append(
                                        (loop_type, loop_dim)
                                    )
                                    mapping_current[operand][level].remove(
                                        (loop_type, loop_dim)
                                    )
                            else:
                                mapping_st[operand][level].extend(
                                    mapping_current[operand][level]
                                )
                                break
            if mapping_st != mapping_previous:
                mapping_previous = pickle_deepcopy(mapping_st)
                mapping_current = pickle_deepcopy(mapping_st)
                continue
            else:
                done = True

        self.mapping_dic_stationary = mapping_st
        self.MAC_level_data_stationary_cycle = MAC_level_st

    ## Calculate the iteration cycles that each memory level covers
    def calc_cycle_cabl_level(self):
        # iteration_each_level only counts for the current level for-loops
        iteration_each_level = {
            op: [
                prod(
                    [loop_dim for (_, loop_dim) in self.mapping_dic_stationary[op][lv]]
                )
                for lv in range(self.mem_level[op])
            ]
            for op in self.operand_list
        }
        # cycle_per_level count for current and below levels' for-loops
        cycle_cabl_level = {
            op: [
                prod(iteration_each_level[op][0 : lv + 1])
                for lv in range(self.mem_level[op])
            ]
            for op in self.operand_list
        }

        # ASSERT: The total cycle count must be the same for all operand
        total_cycle = [cycle_cabl_level[op][-1] for op in self.operand_list]
        assert all(
            x == total_cycle[0] for x in total_cycle
        ), f"The total cycle count is not the same for all operand {total_cycle}, please correct the temporal mapping."

        self.cycle_cabl_level = cycle_cabl_level
        self.total_cycle = total_cycle[0]

    def calc_output_ir_loop(self):

        prod = 1
        counter = 0
        last_counter = 0
        last_level = 0
        prod_perlev = [1 for level in self.mapping_dic_stationary[self.layer_node.output_operand]]
        for level, current_level_loops in enumerate(self.mapping_dic_stationary[self.layer_node.output_operand]):
            if not current_level_loops:
                continue
            else:
                for loop_type, loop_dim in current_level_loops:
                    counter += 1
                    if loop_type in self.layer_node.operand_loop_dim[self.layer_node.output_operand]["ir"]:
                        prod *= loop_dim
                        prod_perlev[level] *= loop_dim
                        last_counter = counter
                        last_level = level
        self.last_ir_counter = last_counter
        self.output_ir_loops = prod
        self.top_ir_prod = prod_perlev[last_level]
        self.ir_prod_perlevel = prod_perlev

    def calc_output_r_stationary_loop(self):

        prod = 1
        counter = 0
        for level, current_level_loops in enumerate(self.mapping_dic_stationary[self.layer_node.output_operand]):
            if not current_level_loops:
                continue
            else:
                for loop_type, loop_dim in current_level_loops:
                    counter += 1
                    if(counter == self.last_ir_counter):
                        break
                    if loop_type in self.layer_node.operand_loop_dim[self.layer_node.output_operand]["r"]:
                        prod *= loop_dim
        self.output_r_stationary_loops = prod


    #def calc_output_size_per_level(self):



    def calc_top_r_and_ir_loop(self):
        # top_ir_loop_size: For each memory level, from top to bottom, the product of top few irrelevant loops.
        # top_ir is used for later required instant memory bandwidth calculation.
    
        # Initialization
        # self.mem_level[op] + 1 to add the placeholder for operational array level
        top_r_loop_size = {
            op: [1 for _ in range(self.mem_level[op] + 1)] for op in self.operand_list
        }

        top_ir_loop_size = {
            op: [1 for _ in range(self.mem_level[op] + 1)] for op in self.operand_list
        }

        # Check and extract the top ir loops
        for operand in self.operand_list:
            for level, current_level_loops in enumerate(
                self.mapping_dic_stationary[operand]
            ):
                if not current_level_loops:
                    continue
                else:
                    for loop_type, loop_dim in reversed(current_level_loops):
                        if loop_type in self.layer_node.operand_loop_dim[operand]["r"]:
                            top_r_loop_size[operand][level + 1] *= loop_dim
                        else:
                            break
                    for loop_type, loop_dim in reversed(current_level_loops):
                        if loop_type in self.layer_node.operand_loop_dim[operand]["ir"]:
                            top_ir_loop_size[operand][level + 1] *= loop_dim
                            #if(operand == self.layer_node.output_operand):
                        else:
                            break
        self.top_r_loop_size = top_r_loop_size
        self.top_ir_loop_size = top_ir_loop_size
