import math

from stream.classes.cost_model.cost import Cost
from stream.classes.cost_model.cost_model import StreamCostModelEvaluation
from stream.classes.workload.computation_node import ComputationNode
from stream.utils import get_too_large_operands
from zigzag.utils import pickle_deepcopy


class FitnessEvaluator:
    def __init__(
        self, workload=None, accelerator=None, node_hw_performances=None
    ) -> None:
        self.workload = workload
        self.accelerator = accelerator
        self.node_hw_performances = node_hw_performances
        # self.num_cores = len(inputs.accelerator.cores)

    def get_fitness(self):
        raise NotImplementedError


class StandardFitnessEvaluator(FitnessEvaluator):
    """The standard fitness evaluator considers latency, max buffer occupancy and energy equally."""

    def __init__(
        self,
        workload,
        accelerator,
        node_hw_performances,
        layer_groups_flexible,
        scheduler_candidate_selection,
        operands_to_prefetch,
    ) -> None:
        super().__init__(workload, accelerator, node_hw_performances)

        self.weights = (-1.0, -1.0)
        self.metrics = ["energy", "latency"]

        self.layer_groups_flexible = layer_groups_flexible
        self.scheduler_candidate_selection = scheduler_candidate_selection
        self.operands_to_prefetch = operands_to_prefetch

    def get_fitness(self, core_allocations: list, return_scme=False):
        """Get the fitness of the given core_allocations

        Args:
            core_allocations (list): core_allocations
        """
        self.set_node_core_allocations(core_allocations)
        scme = StreamCostModelEvaluation(
            pickle_deepcopy(self.workload),
            pickle_deepcopy(self.accelerator),
            self.scheduler_candidate_selection,
            self.operands_to_prefetch,
        )
        scme.run()
        energy = scme.energy
        latency = scme.latency
        if not return_scme:
            return energy, latency
        print(scme)
        return energy, latency, scme

    def set_node_core_allocations(self, core_allocations):
        """Sets the core allocation of all nodes in self.workload according to core_allocations.
        This will only set the energy, runtime and core_allocation of the nodes which are flexible in their core allocation.
        We assume the energy, runtime and core_allocation of the other nodes are already set.

        Args:
            core_allocations (list): list of the node-core allocations
        """
        for i, core_allocation in enumerate(core_allocations):
            core = self.accelerator.get_core(core_allocation)
            (layer_id, group_id) = self.layer_groups_flexible[i]
            # Find all nodes of this coarse id and set their core_allocation, energy and runtime
            nodes = (
                node
                for node in self.workload.nodes()
                if isinstance(node, ComputationNode)
                and node.id[0] == layer_id
                and node.group == group_id
            )
            for node in nodes:
                try:
                    equivalent_unique_node = next(
                        (n for n in self.node_hw_performances.keys() if node == n)
                    )
                except StopIteration:
                    raise ValueError(
                        f"The given node_hw_performances doesn't have run information for node={node}"
                    )
                try:
                    cme = self.node_hw_performances[equivalent_unique_node][core]
                except KeyError:
                    raise KeyError(
                        f"The given node_hw_performances doesn't have information for core_allocation={core_allocation} of node={node}"
                    )


                latency = cme.latency_total1
                too_large_operands = get_too_large_operands(cme, self.accelerator, core_id=core_allocation)

                #### OLD:
                onchip_energy_old = (cme.energy_total)  # Initialize the on-chip energy as total energy
                # If there is a too_large_operand, we separate the off-chip energy.
                offchip_energy_old = 0
                for too_large_operand in too_large_operands:
                    layer_operand = cme.mem_op_to_layer_op[too_large_operand]
                    layer_operand_offchip_energy = cme.energy_breakdown[layer_operand][-1]
                    offchip_energy_old += layer_operand_offchip_energy
                    onchip_energy_old -= layer_operand_offchip_energy
                ################

                mac_tensors = list(equivalent_unique_node.operand_tensors.values())
                offchip_energy = []
                onchip_energy = [Cost(tensor=mac_tensors, component="MAC", energy=cme.MAC_energy)]
                for layer_operand, energy_list in cme.energy_breakdown.items():
                    tensor = equivalent_unique_node.operand_tensors[layer_operand]
                    memory_operand = cme.layer_op_to_mem_op[layer_operand]
                    memory_levels = cme.mem_hierarchy_dict[memory_operand]
                    if memory_operand in too_large_operands:
                        component = memory_levels[-1].name
                        offchip_energy.append(Cost(tensor=tensor, component=component, energy=energy_list[-1]))
                        remaining_energy_list = energy_list[:-1]
                    else:
                        remaining_energy_list = energy_list

                    for i, energy in enumerate(remaining_energy_list):
                        onchip_energy.append(Cost(tensor=tensor, component=memory_levels[i].name, energy=energy))

                assert math.isclose(onchip_energy_old, sum([c.energy for c in onchip_energy]))
                assert math.isclose(offchip_energy_old, sum([c.energy for c in offchip_energy]))

                node.set_onchip_energy(onchip_energy)
                node.set_offchip_energy(offchip_energy)
                node.set_runtime(latency)
                node.set_core_allocation(core_allocation)
                node.set_too_large_operands(too_large_operands)


# from stream.classes.cost_model.cost_model import StreamCostModelEvaluation
# from stream.classes.workload.computation_node import ComputationNode
# from zigzag.utils import pickle_deepcopy

# from stream.utils import get_too_large_operands


# class FitnessEvaluator:
#     def __init__(
#         self, workload=None, accelerator=None, node_hw_performances=None
#     ) -> None:
#         self.workload = workload
#         self.accelerator = accelerator
#         self.node_hw_performances = node_hw_performances
#         # self.num_cores = len(inputs.accelerator.cores)

#     def get_fitness(self):
#         raise NotImplementedError


# class StandardFitnessEvaluator(FitnessEvaluator):
#     """The standard fitness evaluator considers latency, max buffer occupancy and energy equally."""

#     def __init__(
#         self,
#         workload,
#         accelerator,
#         node_hw_performances,
#         layer_groups_flexible,
#         scheduler_candidate_selection,
#         operands_to_prefetch,
#     ) -> None:
#         super().__init__(workload, accelerator, node_hw_performances)

#         self.weights = (-1.0, -1.0)
#         self.metrics = ["energy", "latency"]

#         self.layer_groups_flexible = layer_groups_flexible
#         self.scheduler_candidate_selection = scheduler_candidate_selection
#         self.operands_to_prefetch = operands_to_prefetch

#     def get_fitness(self, core_allocations: list, return_scme=False):
#         """Get the fitness of the given core_allocations

#         Args:
#             core_allocations (list): core_allocations
#         """
#         self.set_node_core_allocations(core_allocations)
#         scme = StreamCostModelEvaluation(
#             pickle_deepcopy(self.workload),
#             pickle_deepcopy(self.accelerator),
#             self.scheduler_candidate_selection,
#             self.operands_to_prefetch,
#         )
#         scme.run()
#         energy = scme.energy
#         latency = scme.latency
#         if not return_scme:
#             return energy, latency
#         return energy, latency, scme

#     def set_node_core_allocations(self, core_allocations):
#         """Sets the core allocation of all nodes in self.workload according to core_allocations.
#         This will only set the energy, runtime and core_allocation of the nodes which are flexible in their core allocation.
#         We assume the energy, runtime and core_allocation of the other nodes are already set.

#         Args:
#             core_allocations (list): list of the node-core allocations
#         """
#         for i, core_allocation in enumerate(core_allocations):
#             core = self.accelerator.get_core(core_allocation)
#             (layer_id, group_id) = self.layer_groups_flexible[i]
#             # Find all nodes of this coarse id and set their core_allocation, energy and runtime
#             nodes = (
#                 node
#                 for node in self.workload.nodes()
#                 if isinstance(node, ComputationNode)
#                 and node.id[0] == layer_id
#                 and node.group == group_id
#             )
#             for node in nodes:
#                 try:
#                     equivalent_unique_node = next(
#                         (n for n in self.node_hw_performances.keys() if node == n)
#                     )
#                 except StopIteration:
#                     raise ValueError(
#                         f"The given node_hw_performances doesn't have run information for node={node}"
#                     )
#                 try:
#                     cme = self.node_hw_performances[equivalent_unique_node][core]
#                 except KeyError:
#                     raise KeyError(
#                         f"The given node_hw_performances doesn't have information for core_allocation={core_allocation} of node={node}"
#                     )
#                 onchip_energy = (
#                     cme.energy_total
#                 )  # Initialize on-chip energy as total energy
#                 latency = cme.latency_total1
#                 too_large_operands = get_too_large_operands(
#                     cme, self.accelerator, core_id=core_allocation
#                 )
#                 # If there is a too_large_operand, we separate the off-chip energy.
#                 offchip_energy = 0
#                 for too_large_operand in too_large_operands:
#                     layer_operand = next(
#                         (
#                             k
#                             for (k, v) in cme.layer.memory_operand_links.items()
#                             if v == too_large_operand
#                         )
#                     )
#                     layer_operand_offchip_energy = cme.energy_breakdown[layer_operand][
#                         -1
#                     ]
#                     offchip_energy += layer_operand_offchip_energy
#                     onchip_energy -= layer_operand_offchip_energy
#                 node.set_onchip_energy(onchip_energy)
#                 node.set_offchip_energy(offchip_energy)
#                 node.set_runtime(latency)
#                 node.set_core_allocation(core_allocation)
#                 node.set_too_large_operands(too_large_operands)
