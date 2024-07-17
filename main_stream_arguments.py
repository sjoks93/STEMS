from zigzag.classes.stages import *
from stream.classes.stages import *
import os
import sys
import pickle
import pandas as pd
from stream.utils import load_scme, save_scme

from inputs.workload.resnet18 import get_r18_workload
from inputs.workload.resnet18_s import get_r18_workload_s
from inputs.workload.resnet18_s_sparse import get_r18_workload_s_sparse
from inputs.workload.mobilenetv2 import get_mbnetv2_workload
import argparse
# Initialize the logger
import logging as _logging


# = "RED_LIF"

_logging_level = _logging.INFO
_logging_format = (
    "%(asctime)s - %(name)s.%(funcName)s +%(lineno)s - %(levelname)s - %(message)s"
)
_logging.basicConfig(level=_logging_level, format=_logging_format)

parser = argparse.ArgumentParser(description="Setup Stream inputs")
parser.add_argument('--accelerator', type=str, required=False, default='Meta_prototype_like_single_core', help='Accelerator name')
parser.add_argument('--workload', type=str, required=True, help='Workload name')
parser.add_argument('--schedule_order', type=str, required=True, help='Schedule mode')
parser.add_argument('--time_schedule', type=str, required=False, default="00000000", help='time_schedule')
parser.add_argument('--depth_schedule', type=str, required=False, default="00000000", help='time_schedule')
parser.add_argument('--sp_map', type=bool, required=False, default=False, help='map all op on comp core')
parser.add_argument('--fuse_barrier', type=bool, required=False, default=False)
parser.add_argument('--time_factor', type=int, required=False, default=1)
#parser.add_argument('--w_rf', type=int, required=True, help='Schedule mode')
#parser.add_argument('--w_lb', type=int, required=True, help='Schedule mode')
# parser.add_argument('--a_lb', type=int, required=True, help='Schedule mode')
# parser.add_argument('--gb_bn', type=int, required=True, help='Schedule mode')
# parser.add_argument('--gb_bw', type=int, required=True, help='Schedule mode')
# parser.add_argument('--sparse_w', type=int, required=True, help='Schedule mode')
# parser.add_argument('--sparse_sop', type=int, required=True, help='Schedule mode')
# parser.add_argument('--best_schedule', type=int, required=True, help='Schedule mode')

#parser.add_argument('--ff', type=int, required=True, help='Schedule mode')



args = parser.parse_args()
# sparse_w = (args.sparse_w == 1)
# sparse_sop = (args.sparse_sop == 1)
# best_schedule = (args.best_schedule == 1)

# accelerator_params = [args.w_rf, args.w_lb, args.a_lb, args.gb_bn, args.gb_bw, sparse_w, sparse_sop]
# print(accelerator_params, best_schedule)
####### Settings #######
# Directory of this file
root_dir = os.path.dirname(os.path.abspath(__file__))
dse_dir = os.path.join(root_dir, 'outputs', 'dse')
########################
# CN_define_mode = 2  
# hint_loops = [("OY", 7), ("OX", "all"), ("K", "all"), ("C", "all"), ("FX", "all"), ("FY", "all"), ("G", "all")]#, ("OX", 2)]  
CN_define_mode = 1

# hint_loops =[     
#               [('T', 1), ('OY', 64)], 
#               [('T', 1), ('OY', 64)], 
#               [('T', 1), ('OY', 32)], 
#               [('T', 1), ('OY', 16)], 
#               [('T', 1), ('OY', 8)],
#               [('T', 1), ('OY', 4)],
#               [('T', 1), ('OY', 2)],]
              #, [], [], [], [], [], []]
#fuse_loops = [0, 0, 0, 0, 0, 0, 0, 0] 
#fuse_loops = [0, 0, 1, 1, 1, 1, 1]
#hint_loops = [('T', 16), ('OY', 1)]
#hint_loops = [('T', 1), ('OX', 1)]
#hint_loops = [[('OY', 128), ('T', 16)], [('OY', 64), ('T', 16)]]
#hint_loops = [('T', 16), ('OY', 8)]
####### Parse arguments #######
accelerator = f"inputs.hardware.socs.{args.accelerator}"
if args.sp_map:
    mapping = f"inputs.mapping.{args.accelerator}_s"
    fig_name = ""
else:
    mapping = f"inputs.mapping.{args.accelerator}"
    fig_name = "-sep_cores"
model = args.workload
schedule_order = args.schedule_order
best_schedule =  False
hint_loops = []
flag_tbf = False
flag_stf = False
barrier = 0
fuse_loops = []



if args.workload == "5PLIF" or args.workload == "7PLIF" or args.workload == "7PLIF_test":
    workload = "inputs.workload.SEW-RESNET."+args.workload
    T = 16
    OX = 128 
    for i in range (7):
        if args.time_schedule[i] == '0':
            time = T
        else:
            time = 1
        if args.depth_schedule[i] == '0':
            space = 1
        else:
            space = OX
        if args.time_schedule[i] == '1' and args.depth_schedule [i] == '1':
            flag_tbf = True
            if flag_stf:
                barrier += 1
                flag_stf = False
        elif args.time_schedule[i] == '0' and args.depth_schedule [i] == '1':
            flag_stf = True
            if flag_tbf:
                barrier += 1
                flag_tbf = False
        else:
            flag_stf = False
            flag_tbf = False
        # space = OX
        # time = args.time_factor
        fuse_loops.append(barrier)
        hint_loops.append([('OX', space), ('AX', space), ('T', time)])
        OX = OX/2
    if not args.fuse_barrier:
        fuse_loops = [0, 0, 0, 0, 0, 0, 0]
else:
    workload = "inputs.workload."+args.workload
    T = 12
    OX1 = [320, 160, 160, 80, 40, 20, 10, 5]
    OX0 = [40, 40, 40, 40, 40, 20, 10, 5]
    for i in range(8):
        if args.time_schedule[i] == '0':
            time = T
            space = OX1[i]
        else:
            time = 1      
            space = OX1[i]  
        if args.depth_schedule[i] == '0':
            space = 1
        if args.time_schedule[i] == '1' and args.depth_schedule [i] == '1':
            flag_tbf = True
            if flag_stf:
                barrier += 1
                flag_stf = False
        elif args.time_schedule[i] == '0' and args.depth_schedule [i] == '1':
            flag_stf = True
            if flag_tbf:
                barrier += 1
                flag_tbf = False
        else:
            flag_stf = False
            flag_tbf = False
        fuse_loops.append(barrier)            
        hint_loops.append([('OX', space), ('AX', space), ('T', time)])
    if not args.fuse_barrier:
        fuse_loops = [0, 0, 0, 0, 0, 0, 0, 0]

print(hint_loops)
print(fuse_loops)
if sum(fuse_loops) == 0:
    fuse_str = ""
else:
    fuse_str = "-"+str(sum(fuse_loops)) + "-"
time_str = str(int(16/args.time_factor))
# if args.workload == "5PLIF":
#     workload = "inputs.workload.SEW-RESNET."+args.workload
#     if best_schedule:
#         hint_loops = [[('T', 16), ('OX', 16)], 
#               [('T', 16), ('OX', 8)],
#               [('T', 1), ('OX', 8)],
#               [('T', 1), ('OX', 4)],
#               [('T', 1), ('OX', 1)],
#               [('T', 1), ('OX', 1)],
#               [('T', 1), ('OX', 1)],]
#         hint_loops_str = "ST-TB-F"
#     else:
#         hint_loops = [('T', 16), ('OX', 1)] 
#         hint_loops_str = "ST-LBL"

# elif args.workload == "7PLIF":
#     workload = "inputs.workload.SEW-RESNET."+args.workload
#     if best_schedule:
#         hint_loops = [[('T', 1), ('OX', 128)], 
#               [('T', 1), ('OX', 64)],
#               [('T', 1), ('OX', 32)],
#               [('T', 1), ('OX', 16)],
#               [('T', 1), ('OX', 1)],
#               [('T', 1), ('OX', 1)],
#               [('T', 1), ('OX', 1)],]
#         hint_loops_str = "TB-F"
#     else:
#         hint_loops_str = "ST-LBL"
#         hint_loops = [('T', 16), ('OX', 1)]
# else:
#     if best_schedule:
#         hint_loops = [[('T', 1), ('OX', 320)], 
#               [('T', 1), ('OX', 160)],
#               [('T', 1), ('OX', 80)],
#               [('T', 1), ('OX', 40)],
#               [('T', 1), ('OX', 1)],
#               [('T', 1), ('OX', 1)],
#               [('T', 1), ('OX', 1)],]
#         hint_loops_str = "TB-F"
#     else:
#         hint_loops = [('T', 12), ('OX', 1)]
#         hint_loops_str = "ST-LBL"
#     workload = "inputs.workload."+args.workload
model = args.workload
#hint_loops_str = "ST-TB"#hint_loops#[0:4]

accelerator_params = None

file_name_prefix = f"{args.accelerator}-{model}"
cme_pickle_filename = os.path.join(dse_dir, f"{file_name_prefix}-saved_cn_hw_cost.pickle")
scme_pickle_filename = os.path.join(dse_dir, f"{file_name_prefix}-scme.pickle")
plot_file_name = f"{file_name_prefix}-{args.time_schedule}-{args.depth_schedule}{fig_name}{fuse_str}"
#plot_file_name = f"{file_name_prefix}-{time_str}-DF{fig_name}{fuse_str}"
nb_ga_individuals = 16
nb_ga_generations = 16
plot_full_schedule = True
plot_data_transfer = True
visualize_node_hw_performances_path = (
    f"outputs/dse/{plot_file_name}_visualization.png"
)
###############################
if os.path.exists(os.path.join(dse_dir, f"{plot_file_name}-energybreakdown.pickle")):
    print(plot_file_name, " already exists")
    sys.exit()
####### Execute Stream #######
mainstage = MainStage(
[  # Initializes the MainStage as entry point
    AcceleratorParserStage,  # Parses the accelerator
    # StreamONNXModelParserStage,  # Parses the ONNX Model into the workload
    UserDefinedModelParserStage,  # Parses the user-defined Model into the workload
    GenerateCNWorkloadHybridStage,
    IntraCoreMappingStage,
    InterCoreMappingStage,
],
accelerator=accelerator,  # required by AcceleratorParserStage
accelerator_params=accelerator_params,
workload_path=workload,  # required by ModelParserStage
mapping_path=mapping,  # required by ModelParserStage
loma_lpf_limit=6,  # required by LomaStage
loma_show_progress_bar=False,
nb_ga_individuals=nb_ga_individuals,  # number of individuals in each genetic algorithm generation
nb_ga_generations=nb_ga_generations,  # number of genetic algorithm generations
node_hw_performances_path=cme_pickle_filename,
# saved node_hw_performances to skip re-computation
plot_hof=True,
# Save schedule and memory usage plot of each individual in the Genetic Algorithm hall of fame
plot_file_name=plot_file_name,
plot_full_schedule=plot_full_schedule,
plot_data_transfer=plot_data_transfer,
cn_define_mode=CN_define_mode,
hint_loops=hint_loops, # Empty for LBL
fuse_loops=fuse_loops,
scheduler_candidate_selection=schedule_order,
operands_to_prefetch=[],
visualize_node_hw_performances_path=visualize_node_hw_performances_path,
)

# Launch the MainStage
scme, _ = mainstage.run()
scme = scme[0]

# # Pickle the best SCME for later re-plotting
# pickle_path = f"outputs/dse/{file_name_prefix}_best_scme.pickle"
# with open(pickle_path, "wb") as fp:
#     pickle.dump(scme, fp)

# Ploting Results
plot_full_schedule = True
draw_dependencies = True
plot_data_transfer = True
section_start_percent = (0, 50, 98)
percent_shown = (2, 2, 2)
fuse_loops_sum = sum(fuse_loops)
fig_path = f"outputs/dse/timeline-{plot_file_name}.png"


from stream.visualization.schedule import (
    plot_timeline_brokenaxes,
    visualize_timeline_plotly,
)
plot_timeline_brokenaxes(
    scme,
    draw_dependencies,
    section_start_percent,
    percent_shown,
    plot_data_transfer,
    fig_path=fig_path,
)

energy_from_stream = scme.energy / 1e9
print(f"Energy: {energy_from_stream} mJ")






from stream.visualization.memory_usage import plot_memory_usage
# Plotting results using Plotly
visualize_timeline_plotly(
    scme,
    draw_dependencies=True,
    draw_communication=True,
    fig_path=os.path.join(dse_dir, f"{plot_file_name}-schedule.html"),
)

max_usage = plot_memory_usage(scme, (0,),(100,), fig_path=os.path.join(dse_dir, f"{plot_file_name}-memory.png"), show_dram=True)
# import os
# os.remove(cme_pickle_filename)
# os.remove(scme_pickle_filename)
# print(f"total_cn_onchip_energy: {scme.total_cn_onchip_energy / 1e9} mJ")
# print(f"total_cn_offchip_memory_energy: {scme.total_cn_offchip_memory_energy / 1e9} mJ")
##############################

####### Parse CN CME #######
# Get the energy from the pickle file
# with open(cme_pickle_filename, 'rb') as fp:
#     pickled_data = pickle.load(fp)

# def compensate_mac(workload, mac_energy):
#     # Tree size==2 MACs
#     # INT8 400 fJ/MAC
#     # INT4 150 fJ/MAC
#     # INT2 80 fJ/MAC
#     estimate_mac = lambda b: round(55 / 12 * b ** 2 + 7.5 * b + 140 / 3)  # 4.58333 x**2 + 7.5 x + 46.6667; LeastSquares fit
#     factor = None

#     if workload['operator_type'] == 'Add':
#         operand_a = 'X'
#         operand_b = 'Y'
#     else:
#         operand_a = 'W'
#         operand_b = 'I'



#     if workload['operand_precision'][operand_a] == 16 and workload['operand_precision'][operand_b] == 16:
#         factor = estimate_mac(16) / 400
#     if workload['operand_precision'][operand_a] == 8 and workload['operand_precision'][operand_b] == 8:
#         factor = 400 / 400
#     if workload['operand_precision'][operand_a] == 4 and workload['operand_precision'][operand_b] == 4:
#         factor = 150 / 400
#     if workload['operand_precision'][operand_a] == 2 and workload['operand_precision'][operand_b] == 2:
#         factor = 80 / 400
#     #### Uneven ones;
#     if workload['operand_precision'][operand_a] == 0:
#         # typically pooling type; assume 50 fj per Pool or Quantize
#         factor = 50 / 400
#     if workload['operand_precision'][operand_a] == 4 and workload['operand_precision'][operand_b] == 8:
#         factor = estimate_mac(6) / 400
#     if workload['operand_precision'][operand_a] == 2 and workload['operand_precision'][operand_b] == 8:
#         factor = estimate_mac(5) / 400
#     if workload['operand_precision'][operand_a] == 2 and workload['operand_precision'][operand_b] == 4:
#         factor = estimate_mac(3) / 400

#     ### Accumulate operation
#     if workload['operand_precision'][operand_b] == 1:
#         factor = workload['operand_precision'][operand_a]/16

#     if factor is None:
#         raise ValueError(f"Unknown precision combination: {workload['operand_precision']}")

#     return mac_energy * factor

# reduced_mac_energy = 0
# v_size = 0
# o_size_r = 0
# o_size_w = 0
# data = scme.cn_offchip_energy_breakdown
# for computation_node, core_cme in pickled_data.items():
#     layer_id = computation_node.id[0]
#     for core, cme in core_cme.items():
#         # TODO: compensate MAC energy!
#         MAC_energy = compensate_mac(workload[layer_id], cme.MAC_energy)
#         reduced_mac_energy += cme.MAC_energy - MAC_energy
#         data.append({'layer_id': layer_id, 'operand': '', 'component': 'MAC', 'energy': MAC_energy})
#         for operand, energy_per_memory_level in cme.energy_breakdown.items():
#             memory_operand = cme.layer_op_to_mem_op[operand]
#             for mem_level, energy in zip(cme.mem_hierarchy_dict[memory_operand], energy_per_memory_level):
#                 data.append({'layer_id': layer_id,
#                              'operand': operand,
#                              'component': mem_level.name,
#                              'energy': energy
#                              })
#                 # if layer_id == 0 and operand == 'O':
#                 #     print(energy)
# # dram_rwcost =  700/64 + 750/64 + 0.13 + 0.175 
# # dram_rcost = 700/64 + 0.175
# # dram_wcost = 750/64 + 0.13
# # print(o_size_r, o_size_w)
# # estimate_V_dram_energy = v_size * dram_rwcost
# # estimate_O_dram_energy = o_size_r * dram_rcost + o_size_w * dram_wcost

# # print(estimate_V_dram_energy/1e9)
# # print(estimate_O_dram_energy/1e9)
# columns = ['layer_id', 'operand', 'component', 'energy']
# df = pd.DataFrame(data, columns=columns)
# df2 = pd.DataFrame([{'layer_id': -1, 'operand': '', 'component': 'other', 'energy': float(scme.energy - df['energy'].sum() - reduced_mac_energy)}], columns=columns)
# df = pd.concat([df, df2], ignore_index=True)

####### Parse SCME into text-based energy breakdown #######
def recalculate_compute_energy(workload, energy, model):
    operand_a, operand_b = 'W', 'I'

    # Scale the compute energy for each operator type
    # match workload['operator_type']:
    #     case 'Add':
    #         # Let's assume these layers are cheaper than INT8 MAC. E.g., 1/5th of the cost
    #         # Will still be scaled by precision later on.
    #         factor = 1/5
    #         operand_a, operand_b = 'X', 'Y'
    #     case 'MaxPool' | 'AveragePool' | 'Quantizer':
    #         # Let's assume these layers are cheaper than INT8 MAC. E.g., 1/8th of the cost
    #         factor = 1/8
    #     case 'Conv':
    #         factor = 1
    #     case _:
    #         raise ValueError(f"Unknown operator_type: {workload['operator_type']}")
    #if(workload < 13 and workload != 4 and workload != 7 and workload != 11):
    if model == "5PLIF" or model == "7PLIF" or model == "7PLIF_test":
        if(workload == 0):
            factor = 16/7
        else:
            factor = 1
    else:
        if(workload < 13 and workload != 4 and workload != 7 and workload != 11):
            factor = 16/7
        else:
            factor = 1
    
    #print('recalculated', workload, energy, factor)
    energy *= factor

    # Scale the compute energy for various precision levels
    # Tree size==2 MACs
    # INT8 400 fJ/MAC
    # INT4 150 fJ/MAC
    # INT2 80 fJ/MAC
    #estimate_mac = lambda b: round(55 / 12 * b ** 2 + 7.5 * b + 140 / 3)  # 4.58333 x**2 + 7.5 x + 46.6667; LeastSquares fit

#     ### Accumulate operation
    # if workload['operand_precision'][operand_b] == 1:
    #     factor = workload['operand_precision'][operand_a]/16
    # else:
    #     match (workload['operand_precision'][operand_a], workload['operand_precision'][operand_b]):
    #         case (16, 16):
    #             factor = estimate_mac(16) / 400
    #         case (8, 8):
    #             factor = 1
    #         case (4, 4):
    #             factor = 150 / 400
    #         case (2, 2):
    #             factor = 80 / 400
    #         ### Uneven ones;
    #         case (0, _): # Typically a Pool or Quantize layer; lets keep energy constant for each precision
    #             factor = 1
    #         case (4, 8):
    #             factor = estimate_mac(6) / 400
    #         case (2, 8):
    #             factor = estimate_mac(5) / 400
    #         case (2, 4):
    #             factor = estimate_mac(3) / 400
    #         case _:
    #             raise ValueError(f"Unknown precision combination: {workload['operand_precision']}")

    #energy *= factor
    return energy

### Parse the energy breakdown.
data = []
for _, costs in scme.energy_breakdown.items():
    for cost in costs:
        if cost.component == 'MAC':
            tensor = cost.tensor[0]
            operand = ''
            energy = recalculate_compute_energy(tensor.id[0], cost.energy, model)
        else:
            tensor = cost.tensor
            operand = tensor.layer_operand
            energy = cost.energy

        data.append({'layer_id': tensor.id[0], 'operand': operand, 'component': cost.component, 'energy': energy})

columns = ['layer_id', 'operand', 'component', 'energy']
df = pd.DataFrame(data, columns=columns)

df_dram = df[df['component']=='dram']
#df_V = df_dram[df_dram['operand']=='V']['energy']
usage_data = []
usage_data.append({'time_schedule': args.time_schedule, 'depth_schedule': args.depth_schedule, 'max_usage': max_usage})
df_data = pd.DataFrame(usage_data, columns=['time_schedule', 'depth_schedule', 'max_usage'])
df_data.to_pickle(os.path.join(dse_dir, f"{plot_file_name}-maxusage.pickle"))
# df_dram_O = df_dram[df_dram['operand']=='O']
# print(df_dram_O['energy'])
# print(df_dram_O['layer_id'])
df_dram_O = df_dram[df_dram['operand']=='V']
# print(df_dram_O['energy'])
# print(df_dram_O['layer_id'])
print(f"Energy from DRAM V: {df_dram[(df_dram['operand']=='V')]['energy'].sum()/1e9} mJ")
#print(f"Energy from DRAM O: {df_dram[(df_dram['operand'] in ['O', 'I', 'X', 'Y']) & (df_dram['component']=='dram')]['energy'].sum()/1e9} mJ")
print(f"Energy from DRAM W: {df_dram[(df_dram['operand']=='W')]['energy'].sum()/1e9} mJ")

print(f"Energy from df: {df['energy'].sum()/1e9} mJ")
print(f"DRAM: {df[df['component']=='dram']['energy'].sum()/1e9} mJ")
print(f"Remainder: {df[df['component']!='dram']['energy'].sum()/1e9} mJ")

df.to_pickle(os.path.join(dse_dir, f"{plot_file_name}-energybreakdown.pickle"))
#save_scme(scme, scme_pickle_filename)

###########################
