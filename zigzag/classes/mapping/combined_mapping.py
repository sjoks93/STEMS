from typing import Dict
from math import prod
import copy
from zigzag.classes.workload.layer_node import LayerNode
from zigzag.classes.mapping.spatial.spatial_mapping import SpatialMapping
from zigzag.classes.mapping.temporal.temporal_mapping import TemporalMapping
from zigzag.classes.hardware.architecture.accelerator import Accelerator
import zigzag.classes.mapping.mapping_assist_funcs as mapping_assist_funcs

## The standard four-way data moving attribute of a memory interface.
class FourWayDataMoving:

    ## The class constructor
    # @param rd_out_to_low
    # @param wr_in_by_low
    # @param rd_out_to_high
    # @param wr_in_by_high
    def __init__(self, rd_out_to_low, wr_in_by_low, rd_out_to_high, wr_in_by_high):
        self.rd_out_to_low = rd_out_to_low
        self.wr_in_by_low = wr_in_by_low
        self.rd_out_to_high = rd_out_to_high
        self.wr_in_by_high = wr_in_by_high
        """ format used in the original ZigZag version """
        self.info_list = [
            (self.rd_out_to_low, self.wr_in_by_low),
            (self.rd_out_to_high, self.wr_in_by_high),
        ]

    def update_single_dir_data(self, dir: str, new_value):
        setattr(self, dir, new_value)
        self.info_list = [
            (self.rd_out_to_low, self.wr_in_by_low),
            (self.rd_out_to_high, self.wr_in_by_high),
        ]

    ## Return the total amount of times this memory interface is read from to the level above.
    # If scaling is the energy cost per read, this returns the total read energy.
    def get_total_read_outs_to_above(self, scaling: float = 1):
        return scaling * self.rd_out_to_high

    ## Return the total amount of times this memory interface is read from to the level below.
    # If scaling is the energy cost per read, this returns the total read energy.
    def get_total_read_outs_to_below(self, scaling: float = 1):
        return scaling * self.rd_out_to_low

    ## Return the total amount of times this memory interface is written to from the level above.
    # If scaling is the energy cost per write, this returns the total read energy.
    def get_total_write_ins_from_above(self, scaling: float = 1):
        return scaling * self.wr_in_by_high

    ## Return the total amount of times this memory interface is written to from the level below.
    # If scaling is the energy cost per write, this returns the total read energy.
    def get_total_write_ins_from_below(self, scaling: float = 1):
        return scaling * self.wr_in_by_low

    def __add__(self, other):
        return FourWayDataMoving(
            self.rd_out_to_low + other.rd_out_to_low,
            self.wr_in_by_low + other.wr_in_by_low,
            self.rd_out_to_high + other.rd_out_to_high,
            self.wr_in_by_high + other.wr_in_by_high,
        )

    def __mul__(self, other):
        return FourWayDataMoving(
            self.rd_out_to_low * other,
            self.wr_in_by_low * other,
            self.rd_out_to_high * other,
            self.wr_in_by_high * other,
        )

    def __iter__(self):
        for e in ["rd_out_to_low", "wr_in_by_low", "rd_out_to_high", "wr_in_by_high"]:
            yield e

    def __repr__(self):
        return f"4waydatamoving (rd /\\: {self.rd_out_to_high}, wr V: {self.wr_in_by_high}, rd V: {self.rd_out_to_low}, wr /\\: {self.wr_in_by_low})"

    def __jsonrepr__(self):
        return repr(self)

    def __getitem__(self, item):
        if hasattr(self, item):
            return getattr(self, item)
        else:
            raise KeyError()


## Collect the memory access pattern for each unit memory (memory that only hold one operand at one level).
class DataMovePattern:

    ## The class construcotr
    # @param operand
    # @param mem_level
    def __init__(self, operand, mem_level):
        self.name = operand + str(mem_level)
        self.data_elem_move_count = FourWayDataMoving(0, 0, 0, 0)
        self.data_precision = FourWayDataMoving(0, 0, 0, 0)
        self.req_mem_bw_aver = FourWayDataMoving(0, 0, 0, 0)
        self.req_mem_bw_inst = FourWayDataMoving(0, 0, 0, 0)
        self.data_trans_period = FourWayDataMoving(0, 0, 0, 0)
        self.data_trans_period_count = FourWayDataMoving(0, 0, 0, 0)
        self.data_trans_amount_per_period = FourWayDataMoving(0, 0, 0, 0)
        self.inst_data_trans_window = FourWayDataMoving(0, 0, 0, 0)

    # For every memory, there are 4 data transfer link in the hierarchy: 
    # rd_out_to_low, wr_in_by_low, rd_out_to_high, wr_in_by_high

    def set_data_elem_move_count(
        self, rd_out_to_low, wr_in_by_low, rd_out_to_high, wr_in_by_high
    ):
        self.data_elem_move_count = FourWayDataMoving(
            rd_out_to_low, wr_in_by_low, rd_out_to_high, wr_in_by_high
        )

    def set_data_precision(
        self, rd_out_to_low, wr_in_by_low, rd_out_to_high, wr_in_by_high
    ):
        self.data_precision = FourWayDataMoving(
            rd_out_to_low, wr_in_by_low, rd_out_to_high, wr_in_by_high
        )

    def set_req_mem_bw_aver(
        self, rd_out_to_low, wr_in_by_low, rd_out_to_high, wr_in_by_high
    ):
        self.req_mem_bw_aver = FourWayDataMoving(
            rd_out_to_low, wr_in_by_low, rd_out_to_high, wr_in_by_high
        )

    def set_req_mem_bw_inst(
        self, rd_out_to_low, wr_in_by_low, rd_out_to_high, wr_in_by_high
    ):
        self.req_mem_bw_inst = FourWayDataMoving(
            rd_out_to_low, wr_in_by_low, rd_out_to_high, wr_in_by_high
        )

    def set_data_trans_period(
        self, rd_out_to_low, wr_in_by_low, rd_out_to_high, wr_in_by_high
    ):
        # data_trans_period: every how many cycle, the memory link need to be activated for a certain duration
        self.data_trans_period = FourWayDataMoving(
            rd_out_to_low, wr_in_by_low, rd_out_to_high, wr_in_by_high
        )

    def set_data_trans_period_count(
        self, rd_out_to_low, wr_in_by_low, rd_out_to_high, wr_in_by_high
    ):
        # data_trans_period_count: to finish all the for-loop computation, how many such ideal_period is required
        self.data_trans_period_count = FourWayDataMoving(
            rd_out_to_low, wr_in_by_low, rd_out_to_high, wr_in_by_high
        )

    def set_data_trans_amount_per_period(
        self, rd_out_to_low, wr_in_by_low, rd_out_to_high, wr_in_by_high
    ):
        # data_trans_amount_per_period: data amount that being transferred for each single period
        self.data_trans_amount_per_period = FourWayDataMoving(
            rd_out_to_low, wr_in_by_low, rd_out_to_high, wr_in_by_high
        )

    def set_inst_data_trans_window(
        self, rd_out_to_low, wr_in_by_low, rd_out_to_high, wr_in_by_high
    ):
        # inst_data_trans_window: the allowed memory updating window, assuming the served memory level
        # is non-double buffered (thus need to avoid the data overwriting issue
        self.inst_data_trans_window = FourWayDataMoving(
            rd_out_to_low, wr_in_by_low, rd_out_to_high, wr_in_by_high
        )

    ## update a single direction value for all data move attributes
    def update_single_dir_data(self, direction, new_value):
        self.data_elem_move_count.update_single_dir_data(direction, new_value)
        self.data_precision.update_single_dir_data(direction, new_value)
        self.req_mem_bw_aver.update_single_dir_data(direction, new_value)
        self.req_mem_bw_inst.update_single_dir_data(direction, new_value)
        self.data_trans_period.update_single_dir_data(direction, new_value)
        self.data_trans_period_count.update_single_dir_data(direction, new_value)
        self.data_trans_amount_per_period.update_single_dir_data(direction, new_value)
        self.inst_data_trans_window.update_single_dir_data(direction, new_value)

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)


## Collect information of a complete mapping (spatial and temporal)
# 
# NOTE: Mapping is HW-unaware, i.e. Mapping doesn't take in HW information
# like memory bw, access cost, size and so on.
class Mapping:

    ## The class construcotr
    # @param accelerator
    # @param spatial mapping
    # @param temporal mapping
    # @param layer_node
    # @param access_same_data_considered_as_no_access
    def __init__(
        self,
        accelerator: Accelerator,
        spatial_mapping: Dict or SpatialMapping,
        temporal_mapping: Dict or TemporalMapping,
        layer_node: LayerNode,
        access_same_data_considered_as_no_access: bool = False,
    ):
        # Mapping object can be initialized with separate spatial and temporal mappings
        self.accelerator = accelerator
        if type(spatial_mapping) is SpatialMapping:
            self.spatial_mapping = spatial_mapping
        else:
            self.spatial_mapping = SpatialMapping(spatial_mapping, layer_node)
        if type(temporal_mapping) is TemporalMapping:
            self.temporal_mapping = temporal_mapping
        else:
            self.temporal_mapping = TemporalMapping(temporal_mapping, layer_node)
        self.layer_node = layer_node
        self.operand_list = layer_node.operand_list
        self.access_same_data_considered_as_no_access = (
            access_same_data_considered_as_no_access
        )
        self.mem_level = self.temporal_mapping.mem_level
        # Initialize unit_mem_data_movement, which collects all the important data movement info 
        # related to each unit memory, such as data access count, data precision, required memory BW to 
        # prevent stall, data transfer rate, etc.
        self.unit_mem_data_movement = {
            op: [[] for _ in range(self.mem_level[op])] for op in self.operand_list
        }

        # Combine spatial and temporal mapping dictionary into "joint_mapping_dict" in order to 
        # enable decoupling pr loops into r and ir loops in one go
        self.combine_spatial_temporal_mapping_dict()

        # Decouple pr loops into r and ir loops, preparing for later mapping info extraction
        self.combined_mapping_dict_1s1t_reform = mapping_assist_funcs.decouple_pr_loop(
            self.combined_mapping_dict_1s1t, layer_node
        )
        self.combined_mapping_dict_1s2t_reform = mapping_assist_funcs.decouple_pr_loop(
            self.combined_mapping_dict_1s2t, layer_node
        )

        # Distinguish final output from partial output: "psum_flag"
        self.distinguish_output()

        # Generate a dictionary that collect data precision for each operand at each arch level
        self.gen_data_precision_dict()

        # Generate r/ir loop size list at each level for each operand
        self.gen_r_ir_loop_list()

        # Calculate data size at each memory level, including total data size and 
        # unrolled data size (data at each unrolled memory unit). Unit used: # element 
        self.calc_data_size()

        # Calculate the effective data size at each unrolled memory unit.
        # Effective data size: the unrolled data size divided by all top r loops at that level.
        # Unit used: # element
        self.calc_effective_data_size()

        # Calculate data access count at each memory level. Unit used: # element 
        # NOTE: this data access is not memory word access!
        self.calc_data_access()

        # Calculate required memory bandwidth and the periodic data transfer pattern
        self.calc_req_mem_bw_and_data_transfer_rate()

        # Ignore the data traffic between the top level memory and the external world
        self.disable_data_traffic_external()

    ## Combine spatial and temporal mapping dictionary into combined_mapping_dict by
    # inserting spatial loops above temporal loops at each level.
    #
    # - combined_mapping_dict_1s1t: corresponding level's smap and tmap are merged together.
    # Each level's data size is the total data size.
    # - combined_mapping_dict_1s2t: each level's smap is merged to level+1's tmap.
    # Each level's data size is the unrolled data size.
    def combine_spatial_temporal_mapping_dict(self):

        # Initialization
        combined_mapping_dict_1s1t = {
            op: [[] for _ in range(self.spatial_mapping.arch_level[op])]
            for op in self.operand_list
        }
        combined_mapping_dict_1s2t = {
            op: [[] for _ in range(self.spatial_mapping.arch_level[op] + 1)]
            for op in self.operand_list
        }
        su_dict_seed = self.spatial_mapping.mapping_dict_origin
        # Add an empty innermost level and an empty outermost level
        tm_dict_seed = {
            op: [[]] + tm_list + [[]]
            for op, tm_list in self.temporal_mapping.mapping_dic_stationary.items()
        }

        # Combining
        for operand in self.operand_list:
            for level, current_level_su_loops in enumerate(su_dict_seed[operand]):
                current_level_tm_loops = tm_dict_seed[operand][level]
                above_level_tm_loops = tm_dict_seed[operand][level + 1]
                combined_mapping_dict_1s1t[operand][level] = (
                    current_level_tm_loops + current_level_su_loops
                )
                combined_mapping_dict_1s2t[operand][level + 1] = (
                    above_level_tm_loops + current_level_su_loops
                )

        self.combined_mapping_dict_1s1t = combined_mapping_dict_1s1t
        self.combined_mapping_dict_1s2t = combined_mapping_dict_1s2t

    ## This function generates an list "psum_flag" that identify whether an output memory
    # level holds partial or final output.
    # E.g., psum_flag = [True, True, False] means that there are 3 memory levels for output and only the outermost
    # memory level hold the final output, the 1st and 2nd memory levels need to store partial output for some time.
    # For indexing convenience, we add an extra False to the end of the psum_flag list.
    def distinguish_output(self):
        output_operand = self.layer_node.output_operand
        output_loop_dim_relevancy = self.layer_node.operand_loop_dim_reform[
            output_operand
        ]
        # output_ir_flag indicate whether at an architectural level, there is output's ir loop in it.
        # True for yes, there is.
        output_arch_level = self.spatial_mapping.arch_level[output_operand]
        output_ir_flag = [False] * output_arch_level
        for level, current_level_loops in enumerate(
            self.combined_mapping_dict_1s1t_reform[output_operand]
        ):
            for loop_type, loop_dim in current_level_loops:
                if loop_type in output_loop_dim_relevancy["ir"] and loop_dim > 1:
                    output_ir_flag[level] = True
                    break
        # reversely check from current level to the top level whether there is ir loop shows up in the middle, 
        # False means final output is present at current level
        psum_flag_H2L = [
            any(output_ir_flag[lv:output_arch_level])
            for lv in reversed(range(output_arch_level))
        ]
        psum_flag_L2H = list(reversed(psum_flag_H2L))
        self.psum_flag = psum_flag_L2H[1:] + [
            False
        ]  # add an extra False on top for later indexing convenience

    ## This function generates a dictionary that collect data precision for each operand at each arch level
    def gen_data_precision_dict(self):
        input_operands = self.layer_node.input_operands
        output_operand = self.layer_node.output_operand
        operands = self.layer_node.operand_list
        if(self.layer_node.state):
            data_precision_dict = {
                op: [self.layer_node.operand_precision[op]] * (self.mem_level[op] + 1)
                for op in operands
            }
        else:
            data_precision_dict = {
                op: [self.layer_node.operand_precision[op]] * (self.mem_level[op] + 1)
                for op in input_operands
            }
            data_precision_dict[output_operand] = []
            
            for i in range(self.mem_level[output_operand] + 1):
                if i == 0 or self.psum_flag[i-1]:
                    data_precision_dict[output_operand].append(
                        self.layer_node.operand_precision[output_operand]
                    )
                else:
                    data_precision_dict[output_operand].append(
                        self.layer_node.operand_precision[output_operand + "_final"]
                    )
        self.data_precision_dict = data_precision_dict

    ## Given the combined mapping, generate r/ir loop size list at each level for each operand
    def gen_r_ir_loop_list(self):
        combined_mapping = self.combined_mapping_dict_1s1t_reform
        combined_mapping2 = self.combined_mapping_dict_1s2t_reform
        relevancy_table = self.layer_node.operand_loop_dim_reform
        r_loop_size_per_level = {
            op: [
                prod(
                    [
                        lp_dim
                        for lp_type, lp_dim in combined_mapping[op][lv]
                        if lp_type in relevancy_table[op]["r"]
                    ]
                )
                for lv in range(self.spatial_mapping.arch_level[op])
            ]
            for op in self.operand_list
        }
        if self.layer_node.state:
            output_operand = self.layer_node.state_operand
        else:
            output_operand = self.layer_node.output_operand
        lv_range = self.spatial_mapping.arch_level[output_operand]
        r_loop_size_per_level_output = {
            lp_type: [
                    prod([
                        lp_dim for lo_type, lp_dim in combined_mapping[output_operand][lv] if lo_type == lp_type]) 
                        for lv in range(lv_range)
                    ]
            for lp_type in relevancy_table[output_operand]["r"]
        }
        ir_loop_size_per_level_output = {
            lp_type: [
                    prod([
                        lp_dim for lo_type, lp_dim in combined_mapping[output_operand][lv] if lo_type == lp_type]) 
                        for lv in range(lv_range)
                    ]
            for lp_type in relevancy_table[output_operand]["ir"]
        }
        if relevancy_table.__contains__(self.layer_node.weight_operand):
            pr_loop_size_per_level_output = {
                lp_type: [
                        prod([
                            lp_dim for lo_type, lp_dim in combined_mapping[output_operand][lv] if lo_type == lp_type]) 
                            for lv in range(lv_range)
                        ]
                for lp_type in relevancy_table[self.layer_node.weight_operand]["r"]
            }
        else:
            pr_loop_size_per_level_output = {}            
        input_tilesize_perlvl = {}
        input_tilesize_perlvl['C'] = []
        input_tilesize_perlvl['X'] = []
        input_tilesize_perlvl['Y'] = []
        input_tilesize_perlvl['T'] = []
        kernel_tilesize_perlvl = {}
        kernel_tilesize_perlvl['FX'] = []
        kernel_tilesize_perlvl['FY'] = []
        for lv in range(lv_range):
            if(ir_loop_size_per_level_output.__contains__('C')):
                input_tilesize_perlvl['C'].append(ir_loop_size_per_level_output['C'][lv])
            else:
                input_tilesize_perlvl['C'].append(1)
            if self.layer_node.state:
                if(ir_loop_size_per_level_output.__contains__('T')):
                    input_tilesize_perlvl['T'].append(ir_loop_size_per_level_output['T'][lv])
                else:
                    input_tilesize_perlvl['T'].append(1) 
            else:
                if(r_loop_size_per_level_output.__contains__('T')):
                    input_tilesize_perlvl['T'].append(r_loop_size_per_level_output['T'][lv])
                else:
                    input_tilesize_perlvl['T'].append(1)                 
            if(pr_loop_size_per_level_output.__contains__('FX')):
                kernel_tilesize_perlvl['FX'].append(pr_loop_size_per_level_output['FX'][lv])
            else:
                kernel_tilesize_perlvl['FX'].append(1)
            if(pr_loop_size_per_level_output.__contains__('FY')):
                kernel_tilesize_perlvl['FY'].append(pr_loop_size_per_level_output['FY'][lv])
            else:
                kernel_tilesize_perlvl['FY'].append(1)
            if(r_loop_size_per_level_output.__contains__('OX')):
                input_tilesize_perlvl['X'].append(r_loop_size_per_level_output['OX'][lv])
            else:
                input_tilesize_perlvl['X'].append(1)

            if(r_loop_size_per_level_output.__contains__('OY')):
                input_tilesize_perlvl['Y'].append(r_loop_size_per_level_output['OY'][lv])
            else:
                input_tilesize_perlvl['Y'].append(1)            
        self.output_tile_rate = mapping_assist_funcs.find_zero_tiles(self.layer_node, input_tilesize_perlvl, kernel_tilesize_perlvl, lv_range)

        r_loop_size_per_level2 = {
            op: [
                prod(
                    [
                        lp_dim
                        for lp_type, lp_dim in combined_mapping2[op][lv]
                        if lp_type in relevancy_table[op]["r"]
                    ]
                )
                for lv in range(self.spatial_mapping.arch_level[op])
            ]
            for op in self.operand_list
        }
        ir_loop_size_per_level = {
            op: [
                prod(
                    [
                        lp_dim
                        for lp_type, lp_dim in combined_mapping[op][lv]
                        if lp_type in relevancy_table[op]["ir"]
                    ]
                )
                for lv in range(self.spatial_mapping.arch_level[op])
            ]
            for op in self.operand_list
        }
        ir_loop_size_per_level2 = {
            op: [
                prod(
                    [
                        lp_dim
                        for lp_type, lp_dim in combined_mapping2[op][lv]
                        if lp_type in relevancy_table[op]["ir"]
                    ]
                )
                for lv in range(self.spatial_mapping.arch_level[op])
            ]
            for op in self.operand_list
        }

        # current and below levels (cabl) r loop size
        r_loop_size_cabl = {
            op: [
                round(prod(r_loop_size_per_level[op][0 : lv + 1]))
                for lv in range(self.spatial_mapping.arch_level[op])
            ]
            for op in self.operand_list
        }
        r_loop_size_cabl2 = {
            op: [
                round(prod(r_loop_size_per_level2[op][0 : lv + 1]))
                for lv in range(self.spatial_mapping.arch_level[op])
            ]
            for op in self.operand_list
        }
        # current and below levels (cabl) ir loop size
        ir_loop_size_cabl = {
            op: [
                prod(ir_loop_size_per_level[op][0 : lv + 1])
                for lv in range(self.spatial_mapping.arch_level[op])
            ]
            for op in self.operand_list
        }
        # current and below levels (cabl) ir loop size
        ir_loop_size_cabl2 = {
            op: [
                prod(ir_loop_size_per_level2[op][0 : lv + 1])
                for lv in range(self.spatial_mapping.arch_level[op])
            ]
            for op in self.operand_list
        }
        # current and above levels (caal) ir loop size, only for output operand for calculating psum backflow access count
        output_operand = self.layer_node.output_operand
        O_ir_loop_size_caal = [
            prod(
                ir_loop_size_per_level[output_operand][
                    lv : self.spatial_mapping.arch_level[output_operand]
                ]
            )
            for lv in range(self.spatial_mapping.arch_level[output_operand])
        ]
        if(self.layer_node.state):
            self.S_ir_loop_size_caal = [
                prod(
                    ir_loop_size_per_level[self.layer_node.state_operand][
                        lv : self.spatial_mapping.arch_level[self.layer_node.state_operand]
                    ]
                )
                for lv in range(self.spatial_mapping.arch_level[self.layer_node.state_operand])
            ]   
            self.S_ir_loop_size_caal.extend([1, 1])
         
        # append two extra 1 to the list to facilitate the psum bcakflow access calculation later
        # We can see it as adding two output memory levels on top with no data reuse.
        O_ir_loop_size_caal.extend([1, 1])
        self.r_loop_size_per_level = r_loop_size_per_level
        self.r_loop_size_per_level2 = r_loop_size_per_level2
        self.ir_loop_size_per_level = ir_loop_size_per_level
        self.r_loop_size_cabl = r_loop_size_cabl
        self.r_loop_size_cabl2 = r_loop_size_cabl2
        self.ir_loop_size_cabl = ir_loop_size_cabl
        self.ir_loop_size_cabl2 = ir_loop_size_cabl2
        self.O_ir_loop_size_caal = O_ir_loop_size_caal  

    ## Based on the r loop size list, calculate the data size held by each architectural level.
    def calc_data_size(self):
        # data_elem_per_level_unrolled: data size held inside of each unrolled unit at each architectural level
        # data_elem_per_level: total data size at each architectural level (= data_elem_per_level_unrolled * unique unit count)
        data_elem_per_level_unrolled = {
            op: [
                round(self.r_loop_size_cabl2[op][lv])
                for lv in range(self.spatial_mapping.arch_level[op])
            ]
            for op in self.operand_list
        }
        data_bit_per_level_unrolled = {
            op: [
                round(self.r_loop_size_cabl2[op][lv]) * self.data_precision_dict[op][lv]
                for lv in range(self.spatial_mapping.arch_level[op])
            ]
            for op in self.operand_list
        }

        data_elem_per_level = {
            op: [
                round(data_elem_unrolled * self.spatial_mapping.unit_unique[op][lv])
                for lv, data_elem_unrolled in enumerate(
                    data_elem_per_level_unrolled[op]
                )
            ]
            for op in self.operand_list
        }

        data_bit_per_level = {
            op: [
                round(data_elem_unrolled * self.spatial_mapping.unit_unique[op][lv])
                * self.data_precision_dict[op][lv]
                for lv, data_elem_unrolled in enumerate(
                    data_elem_per_level_unrolled[op]
                )
            ]
            for op in self.operand_list
        }
        self.data_elem_per_level_unrolled = data_elem_per_level_unrolled
        self.data_bit_per_level_unrolled = data_bit_per_level_unrolled
        self.data_elem_per_level = data_elem_per_level
        self.data_bit_per_level = data_bit_per_level

    ## Calculate the effective data size for getting the allowed memory updating window in latency calculation.
    # The effective data size is calculated by using data_elem_per_level_unrolled divided by the top r loops.
    def calc_effective_data_size(self):
        effective_data_elem = {
            op: [
                data_elem_unrolled // self.temporal_mapping.top_r_loop_size[op][lv]
                for lv, data_elem_unrolled in enumerate(
                    self.data_elem_per_level_unrolled[op]
                )
            ]
            for op in self.operand_list
        }

        effective_data_bit = {
            op: [
                data_bit_unrolled // self.temporal_mapping.top_r_loop_size[op][lv]
                for lv, data_bit_unrolled in enumerate(
                    self.data_bit_per_level_unrolled[op]
                )
            ]
            for op in self.operand_list
        }
        self.effective_data_elem = effective_data_elem
        self.effective_data_bit = effective_data_bit

    ## Based on the ir loop size list and the total MAC Op count, calculate the data access
    # at each memory level in a bottom-up way.
    def calc_data_access(self):
        total_MAC_count = self.layer_node.total_MAC_count

        # data_access_raw doesn't distinguish read and write, doesn't distinguish input operands from output operand 
        # data_access_raw: each memory levels' spatial loops and temporal loops are put together (combined_mapping_dict_1s1t)
        # data_access_raw2: each memory levels' spatial loops are put to memory level + 1s' temporal loops location (combined_mapping_dict_1s2t)
        data_access_raw = {
            op: [
                round(total_MAC_count / self.ir_loop_size_cabl[op][lv])
                for lv in range(self.spatial_mapping.arch_level[op])
            ]
            for op in self.operand_list
        }
        data_access_raw2 = {
            op: [
                round(total_MAC_count / self.ir_loop_size_cabl2[op][lv])
                for lv in range(self.spatial_mapping.arch_level[op])
            ]
            for op in self.operand_list
        }
        self.data_access_raw = data_access_raw
        self.data_access_raw2 = data_access_raw2

        # Distinguish read and write, unify input operands and output operand
        # For input operands
        for operand in self.layer_node.input_operands:
            for mem_level in range(self.mem_level[operand]):
                unit_mem_data_movement = DataMovePattern(operand, mem_level)

                # data access count
                if (
                    self.access_same_data_considered_as_no_access
                    and mem_level == 0
                    and self.accelerator.get_core(
                        self.layer_node.get_core_allocation()
                    ).mem_r_bw_dict[self.layer_node.memory_operand_links[operand]][
                        mem_level
                    ]
                    >= self.data_bit_per_level[operand][mem_level]
                    // self.spatial_mapping.unit_unique[operand][mem_level + 1]
                ):
                    # If we need access the same input data multiple times from the innermost memory level and the data size is smaller than the memory read bw,
                    # take into account only one-time access cost (assume the data can stay at the output pins of the memory as long as it is needed).
                    rd_out_to_low = (
                        data_access_raw[operand][mem_level]
                        // self.temporal_mapping.MAC_level_data_stationary_cycle[
                            operand
                        ]
                    )
                else:
                    rd_out_to_low = data_access_raw[operand][mem_level]
                wr_in_by_low = 0
                rd_out_to_high = 0
                wr_in_by_high = data_access_raw2[operand][mem_level + 1]
                unit_mem_data_movement.set_data_elem_move_count(
                    rd_out_to_low, wr_in_by_low, rd_out_to_high, wr_in_by_high
                )
                # data precision
                rd_out_to_low_pre = self.layer_node.operand_precision[operand]
                wr_in_by_low_pre = 0
                rd_out_to_high_pre = 0
                wr_in_by_high_pre = self.layer_node.operand_precision[operand]
                unit_mem_data_movement.set_data_precision(
                    rd_out_to_low_pre,
                    wr_in_by_low_pre,
                    rd_out_to_high_pre,
                    wr_in_by_high_pre,
                )

                self.unit_mem_data_movement[operand][mem_level] = unit_mem_data_movement

        # For output operand
        output_operand = self.layer_node.output_operand
        output_size = self.layer_node.operand_size_elem["O"]
        if(self.layer_node.state):
            for mem_level in range(self.mem_level[output_operand]):
                unit_mem_data_movement = DataMovePattern(output_operand, mem_level)

                # Note that the index for data_access_raw is arch_level, which is one level more than mem_level. 
                # the first arch_level means the operational array level (e.g. MAC array level); 
                # the first mem_level means the innermost memory level (e.g. register file level.

                # data access count
                wr_in_by_low = data_access_raw[output_operand][mem_level]
                rd_out_to_low = self.layer_node.operand_size_elem[output_operand] * (
                    self.O_ir_loop_size_caal[mem_level + 1] - 1
                )

                rd_out_to_high = data_access_raw2[output_operand][mem_level + 1]
                wr_in_by_high = self.layer_node.operand_size_elem[output_operand] * (
                    self.O_ir_loop_size_caal[mem_level + 2] - 1
                )
                """ data precision """

                if(rd_out_to_low == 0 and mem_level != 0):
                    rd_out_to_low = output_size
                wr_in_by_low_pre = self.layer_node.operand_precision[output_operand]
                rd_out_to_low_pre = self.layer_node.operand_precision[output_operand]


                if(wr_in_by_high == 0 and mem_level != self.mem_level[output_operand] - 1):
                    wr_in_by_high = output_size
                wr_in_by_high_pre = self.layer_node.operand_precision[output_operand]
                rd_out_to_high_pre = self.layer_node.operand_precision[output_operand]

                if(mem_level == self.mem_level[output_operand] - 1):
                    rd_out_to_high = 0
                    wr_in_by_high = 0
   
                if(mem_level != self.mem_level[output_operand] - 1):
                    rd_out_to_high = output_size
                else:
                    rd_out_to_high = 0
                wr_in_by_low = output_size
                rd_out_to_low = 0
                wr_in_by_high = 0

                unit_mem_data_movement.set_data_elem_move_count(
                    rd_out_to_low, wr_in_by_low, rd_out_to_high, wr_in_by_high
                )
                unit_mem_data_movement.set_data_precision(
                    rd_out_to_low_pre,
                    wr_in_by_low_pre,
                    rd_out_to_high_pre,
                    wr_in_by_high_pre,
                )    

                self.unit_mem_data_movement[output_operand][
                    mem_level
                ] = unit_mem_data_movement

            state_operand = self.layer_node.state_operand
            for mem_level in range(self.mem_level[state_operand]):
                unit_mem_data_movement = DataMovePattern(state_operand, mem_level)

                # Note that the index for data_access_raw is arch_level, which is one level more than mem_level. 
                # the first arch_level means the operational array level (e.g. MAC array level); 
                # the first mem_level means the innermost memory level (e.g. register file level.

                # data access count
                wr_in_by_low = data_access_raw[state_operand][mem_level]
                rd_out_to_low = self.layer_node.operand_size_elem[state_operand] * (
                    self.S_ir_loop_size_caal[mem_level + 1] - 1
                )

                rd_out_to_high = data_access_raw2[state_operand][mem_level + 1]
                wr_in_by_high = self.layer_node.operand_size_elem[state_operand] * (
                    self.S_ir_loop_size_caal[mem_level + 2] - 1
                )
                """ data precision """

                if(rd_out_to_low == 0 and mem_level != 0):
                    rd_out_to_low = output_size
                wr_in_by_low_pre = self.layer_node.operand_precision[state_operand]
                rd_out_to_low_pre = self.layer_node.operand_precision[state_operand]

                """partial output data precision"""
                if(wr_in_by_high == 0 and mem_level != self.mem_level[state_operand] - 1):
                    wr_in_by_high = output_size
                wr_in_by_high_pre = self.layer_node.operand_precision[state_operand]
                rd_out_to_high_pre = self.layer_node.operand_precision[state_operand]

                if(mem_level == self.mem_level[state_operand] - 1):
                    rd_out_to_high = 0
                    wr_in_by_high = 0
                unit_mem_data_movement_S = DataMovePattern(state_operand, mem_level)
                unit_mem_data_movement_S.set_data_elem_move_count(
                    rd_out_to_low, wr_in_by_low, rd_out_to_high, wr_in_by_high
                )

                prec_state = self.layer_node.operand_precision[state_operand]
                unit_mem_data_movement_S.set_data_precision(
                    prec_state,
                    prec_state,
                    prec_state,
                    prec_state,
                )    
                self.unit_mem_data_movement[state_operand][mem_level] = unit_mem_data_movement_S
        else:
            for mem_level in range(self.mem_level[output_operand]):
                unit_mem_data_movement = DataMovePattern(output_operand, mem_level)

                # Note that the index for data_access_raw is arch_level, which is one level more than mem_level. 
                # the first arch_level means the operational array level (e.g. MAC array level); 
                # the first mem_level means the innermost memory level (e.g. register file level.

                # data access count
                wr_in_by_low = data_access_raw[output_operand][mem_level]
                rd_out_to_low = self.layer_node.operand_size_elem[output_operand] * (
                    self.O_ir_loop_size_caal[mem_level + 1] - 1
                )

                rd_out_to_high = data_access_raw2[output_operand][mem_level + 1]
                wr_in_by_high = self.layer_node.operand_size_elem[output_operand] * (
                    self.O_ir_loop_size_caal[mem_level + 2] - 1
                )

                unit_mem_data_movement.set_data_elem_move_count(
                    rd_out_to_low, wr_in_by_low, rd_out_to_high, wr_in_by_high
                )

                # data precision
                if rd_out_to_low != 0:
                    # partial output data precision
                    wr_in_by_low_pre = self.layer_node.operand_precision[output_operand]
                    rd_out_to_low_pre = self.layer_node.operand_precision[output_operand]
                else:
                    # final output data precision
                    wr_in_by_low_pre = self.layer_node.operand_precision[
                        output_operand + "_final"
                    ]
                    rd_out_to_low_pre = 0
                if wr_in_by_high != 0:
                    # partial output data precision
                    wr_in_by_high_pre = self.layer_node.operand_precision[output_operand]
                    rd_out_to_high_pre = self.layer_node.operand_precision[output_operand]
                else:
                    # final output data precision
                    wr_in_by_high_pre = 0
                    rd_out_to_high_pre = self.layer_node.operand_precision[
                        output_operand + "_final"
                    ]

                unit_mem_data_movement.set_data_precision(
                    rd_out_to_low_pre,
                    wr_in_by_low_pre,
                    rd_out_to_high_pre,
                    wr_in_by_high_pre,
                )

                self.unit_mem_data_movement[output_operand][
                    mem_level
                ] = unit_mem_data_movement

        

    def calc_req_mem_bw_and_data_transfer_rate(self):
        """
        This function calculates the average & instant required memory bw and the periodic data transfer pattern.
        """
        if self.access_same_data_considered_as_no_access:
            # For input operands, add operational array level's 'MAC_level_data_stationary_cycle' cycle in the below to align with the list length of data_each_level
            cycle_each_level = {
                op: [self.temporal_mapping.MAC_level_data_stationary_cycle[op]]
                + self.temporal_mapping.cycle_cabl_level[op]
                for op in self.layer_node.input_operands
            }
            # For output operands, add operational array level's 1 cycle in the below to align with the list length of data_each_level
            cycle_each_level[self.layer_node.output_operand] = [
                1
            ] + self.temporal_mapping.cycle_cabl_level[self.layer_node.output_operand]
            if self.layer_node.state:
                cycle_each_level[self.layer_node.state_operand] = [
                    1
                ] + self.temporal_mapping.cycle_cabl_level[self.layer_node.state_operand]

        else:
            cycle_each_level = {
                op: [1] + self.temporal_mapping.cycle_cabl_level[op]
                for op in self.operand_list
            }

        data_each_level_unrolled = self.data_elem_per_level_unrolled

        # Add the mem BW boost factor 1 on the top (the memory BW boost factor from outside to top memory) 
        # to align with the list length of data_each_level
        mem_bw_boost_factor = {
            op: self.spatial_mapping.mem_bw_boost[op] + [1] for op in self.operand_list
        }
        """ req_mem_bw_raw doesn't distinguish read and write, doesn't distinguish input operands from output operand """
        """ "_L/_H" indicates for each data transfer link (DTL), the lower/higher memory level's required BW, 
        e.g. for the DTL of Global Buffer (Weight) talking to spatially unrolled Weight Reg File, 
        each Weight Reg File's required write BW is indicated by "_L", 
        while Global Buffer (Weight)'s required read BW is indicate by "_H" """

        # if(self.layer_node.state):
        #     for lv in range(self.spatial_mapping.arch_level[output_operand]):
                
        #         data_each_level_unrolled[output_operand][lv] 
        req_mem_bw_L_raw = {
            op: [
                data_each_level_unrolled[op][lv] / cycle_each_level[op][lv]
                for lv in range(self.spatial_mapping.arch_level[op])
            ]
            for op in self.operand_list
        }
        # if(self.layer_node.state):
        #     req_mem_bw_L_raw[self.layer_node.output_operand] = [1/self.temporal_mapping.output_ir_loops for lv in range(self.spatial_mapping.arch_level[self.layer_node.output_operand])]
        req_mem_bw_H_raw = {
            op: [
                req_mem_bw_L_raw[op][lv] * mem_bw_boost_factor[op][lv]
                for lv in range(self.spatial_mapping.arch_level[op])
            ]
            for op in self.operand_list
        }

        """
        Calculates the average required memory bw.
        """
        """ Distinguish read and write, unify input operands and output operand """
        """ For input operands """
        for operand in self.layer_node.input_operands:
            for mem_level in range(self.mem_level[operand]):
                # average required memory BW
                rd_out_to_low_bw = req_mem_bw_H_raw[operand][mem_level]
                wr_in_by_low_bw = 0
                rd_out_to_high_bw = 0
                wr_in_by_high_bw = req_mem_bw_L_raw[operand][mem_level + 1]
                self.unit_mem_data_movement[operand][mem_level].set_req_mem_bw_aver(
                    rd_out_to_low_bw,
                    wr_in_by_low_bw,
                    rd_out_to_high_bw,
                    wr_in_by_high_bw,
                )

                """ data transfer period """
                rd_out_to_low_pd = cycle_each_level[operand][mem_level]
                wr_in_by_low_pd = 0
                rd_out_to_high_pd = 0
                wr_in_by_high_pd = cycle_each_level[operand][mem_level + 1]
                self.unit_mem_data_movement[operand][mem_level].set_data_trans_period(
                    rd_out_to_low_pd,
                    wr_in_by_low_pd,
                    rd_out_to_high_pd,
                    wr_in_by_high_pd,
                )
                # data transfer period count
                rd_out_to_low_pc = (
                    self.temporal_mapping.total_cycle
                    // cycle_each_level[operand][mem_level]
                )
                wr_in_by_low_pc = 0
                rd_out_to_high_pc = 0
                wr_in_by_high_pc = (
                    self.temporal_mapping.total_cycle
                    // cycle_each_level[operand][mem_level + 1]
                )
                self.unit_mem_data_movement[operand][
                    mem_level
                ].set_data_trans_period_count(
                    rd_out_to_low_pc,
                    wr_in_by_low_pc,
                    rd_out_to_high_pc,
                    wr_in_by_high_pc,
                )
             
                # per-period data transfer amount
                rd_out_to_low_da = (
                    data_each_level_unrolled[operand][mem_level]
                    * mem_bw_boost_factor[operand][mem_level]
                )
                wr_in_by_low_da = 0
                rd_out_to_high_da = 0
                wr_in_by_high_da = data_each_level_unrolled[operand][mem_level + 1]


                self.unit_mem_data_movement[operand][
                    mem_level
                ].set_data_trans_amount_per_period(
                    rd_out_to_low_da,
                    wr_in_by_low_da,
                    rd_out_to_high_da,
                    wr_in_by_high_da,
                )

        # For output operand 
        output_operand = self.layer_node.output_operand
        output_size = self.layer_node.operand_size_elem["O"]
        for mem_level in range(self.mem_level[output_operand]):
            wr_in_by_low_bw = req_mem_bw_H_raw[output_operand][mem_level]
            rd_out_to_high_bw = req_mem_bw_L_raw[output_operand][mem_level + 1]
            wr_in_by_low_pd = cycle_each_level[output_operand][mem_level]
            rd_out_to_high_pd = cycle_each_level[output_operand][mem_level + 1]
            wr_in_by_low_pc = (
                self.temporal_mapping.total_cycle
                // cycle_each_level[output_operand][mem_level]
            )
            rd_out_to_high_pc = (
                self.temporal_mapping.total_cycle
                // cycle_each_level[output_operand][mem_level + 1]
            )
            wr_in_by_low_da = (
                data_each_level_unrolled[output_operand][mem_level]
                * mem_bw_boost_factor[output_operand][mem_level]
            )
            rd_out_to_high_da = data_each_level_unrolled[output_operand][mem_level + 1]
            if(self.layer_node.state):
                self.unit_mem_data_movement[output_operand][mem_level].set_req_mem_bw_aver(
                    0, wr_in_by_low_bw, rd_out_to_high_bw, 0
                )
                """ data transfer period """
                self.unit_mem_data_movement[output_operand][
                    mem_level
                ].set_data_trans_period(
                    0, wr_in_by_low_pd, rd_out_to_high_pd, 0
                )
                """ data transfer period count """
                self.unit_mem_data_movement[output_operand][
                    mem_level
                ].set_data_trans_period_count(
                    0, wr_in_by_low_pc, rd_out_to_high_pc, 0
                )
                """ per-period data transfer amount """
                self.unit_mem_data_movement[output_operand][
                    mem_level
                ].set_data_trans_amount_per_period(
                    0, wr_in_by_low_da, rd_out_to_high_da, 0
                )
                
            else:

                if self.psum_flag[mem_level]:
                    rd_out_to_low_bw = wr_in_by_low_bw
                    rd_out_to_low_pd = wr_in_by_low_pd
                    rd_out_to_low_pc = wr_in_by_low_pc
                    rd_out_to_low_da = wr_in_by_low_da
                else:
                    rd_out_to_low_bw = 0
                    rd_out_to_low_pd = 0
                    rd_out_to_low_pc = 0
                    rd_out_to_low_da = 0

                if self.psum_flag[mem_level + 1]:
                    wr_in_by_high_bw = rd_out_to_high_bw
                    wr_in_by_high_pd = rd_out_to_high_pd
                    wr_in_by_high_pc = rd_out_to_high_pc
                    wr_in_by_high_da = rd_out_to_high_da
                else:
                    wr_in_by_high_bw = 0
                    wr_in_by_high_pd = 0
                    wr_in_by_high_pc = 0
                    wr_in_by_high_da = 0       

                """ average required memory BW """
                self.unit_mem_data_movement[output_operand][mem_level].set_req_mem_bw_aver(
                    rd_out_to_low_bw, wr_in_by_low_bw, rd_out_to_high_bw, wr_in_by_high_bw
                )
                """ data transfer period """
                self.unit_mem_data_movement[output_operand][
                    mem_level
                ].set_data_trans_period(
                    rd_out_to_low_pd, wr_in_by_low_pd, rd_out_to_high_pd, wr_in_by_high_pd
                )
                """ data transfer period count """
                self.unit_mem_data_movement[output_operand][
                    mem_level
                ].set_data_trans_period_count(
                    rd_out_to_low_pc, wr_in_by_low_pc, rd_out_to_high_pc, wr_in_by_high_pc
                )                   
                """ per-period data transfer amount """
                self.unit_mem_data_movement[output_operand][
                    mem_level
                ].set_data_trans_amount_per_period(
                    rd_out_to_low_da, wr_in_by_low_da, rd_out_to_high_da, wr_in_by_high_da
                )
        if(self.layer_node.state):
            state_operand = self.layer_node.state_operand
            for mem_level in range(self.mem_level[state_operand]):
                wr_in_by_low_bw = req_mem_bw_H_raw[state_operand][mem_level]
                rd_out_to_high_bw = req_mem_bw_L_raw[state_operand][mem_level + 1]
                wr_in_by_low_pd = cycle_each_level[state_operand][mem_level]
                rd_out_to_high_pd = cycle_each_level[state_operand][mem_level + 1]
                wr_in_by_low_pc = (
                    self.temporal_mapping.total_cycle
                    // cycle_each_level[state_operand][mem_level]
                )
                rd_out_to_high_pc = (
                    self.temporal_mapping.total_cycle
                    // cycle_each_level[state_operand][mem_level + 1]
                )
                wr_in_by_low_da = (
                    data_each_level_unrolled[state_operand][mem_level]
                    * mem_bw_boost_factor[state_operand][mem_level]
                )
                rd_out_to_high_da = data_each_level_unrolled[state_operand][mem_level + 1]

                self.unit_mem_data_movement[state_operand][mem_level].set_req_mem_bw_aver(
                    wr_in_by_low_bw, wr_in_by_low_bw, rd_out_to_high_bw, rd_out_to_high_bw
                )
                """ data transfer period """
                self.unit_mem_data_movement[state_operand][
                    mem_level
                ].set_data_trans_period(
                    wr_in_by_low_pd, wr_in_by_low_pd, rd_out_to_high_pd, rd_out_to_high_pd
                )
                """ data transfer period count """
                self.unit_mem_data_movement[state_operand][
                    mem_level
                ].set_data_trans_period_count(
                    wr_in_by_low_pc, wr_in_by_low_pc, rd_out_to_high_pc, rd_out_to_high_pc
                )               
                """ per-period data transfer amount """
                self.unit_mem_data_movement[state_operand][
                    mem_level
                ].set_data_trans_amount_per_period(
                    wr_in_by_low_da, wr_in_by_low_da, rd_out_to_high_da, rd_out_to_high_da
                )
                    
                    

        """
        Calculate the instant memory updating behavior.
        """
        top_ir_loop_size = copy.deepcopy(self.temporal_mapping.top_ir_loop_size)
        for operand in self.operand_list:
            for level, data_movement_item in enumerate(
                self.unit_mem_data_movement[operand]
            ):
                req_mem_bw_aver = data_movement_item.req_mem_bw_aver
                # calculate "instant required memory BW" based on "average required memory BW"
                rd_out_to_low_bw = (
                    req_mem_bw_aver.rd_out_to_low * top_ir_loop_size[operand][level]
                )
                wr_in_by_low_bw = (
                    req_mem_bw_aver.wr_in_by_low * top_ir_loop_size[operand][level]
                )
                rd_out_to_high_bw = (
                    req_mem_bw_aver.rd_out_to_high
                    * top_ir_loop_size[operand][level + 1]
                )
                wr_in_by_high_bw = (
                    req_mem_bw_aver.wr_in_by_high * top_ir_loop_size[operand][level + 1]
                )
                data_movement_item.set_req_mem_bw_inst(
                    rd_out_to_low_bw,
                    wr_in_by_low_bw,
                    rd_out_to_high_bw,
                    wr_in_by_high_bw,
                )

                data_trans_period = data_movement_item.data_trans_period
                # calculate "instant data transferring window", assuming non-double buffered memory
                rd_out_to_low_wd = (
                    data_trans_period.rd_out_to_low // top_ir_loop_size[operand][level]
                )
                wr_in_by_low_wd = (
                    data_trans_period.wr_in_by_low // top_ir_loop_size[operand][level]
                )
                rd_out_to_high_wd = (
                    data_trans_period.rd_out_to_high
                    // top_ir_loop_size[operand][level + 1]
                )
                wr_in_by_high_wd = (
                    data_trans_period.wr_in_by_high
                    // top_ir_loop_size[operand][level + 1]
                )
                data_movement_item.set_inst_data_trans_window(
                    rd_out_to_low_wd,
                    wr_in_by_low_wd,
                    rd_out_to_high_wd,
                    wr_in_by_high_wd,
                )

    ## This function set all the data traffic between the top level memory and the external world to 0
    # in unit_mem_data_movement.
    def disable_data_traffic_external(self):
        for operand in self.operand_list:
            mem_level = self.mem_level[operand] - 1
            self.unit_mem_data_movement[operand][mem_level].update_single_dir_data(
                "rd_out_to_high", 0
            )
            self.unit_mem_data_movement[operand][mem_level].update_single_dir_data(
                "wr_in_by_high", 0
            )
