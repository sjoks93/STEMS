import importlib

from zigzag.classes.io.accelerator.parser import AcceleratorParser
from zigzag.classes.stages.Stage import Stage
from zigzag.classes.workload.dnn_workload import DNNWorkload
from zigzag.utils import pickle_deepcopy

import logging
logger = logging.getLogger(__name__)

## Description missing
class AcceleratorParserStage(Stage):
    def __init__(self, list_of_callables, *, accelerator, accelerator_params = None, **kwargs):
        super().__init__(list_of_callables, **kwargs)
        self.accelerator_parser = AcceleratorParser(accelerator, accelerator_params)

    def run(self):
        self.accelerator_parser.run()
        accelerator = self.accelerator_parser.get_accelerator()
        sub_stage = self.list_of_callables[0](self.list_of_callables[1:], accelerator=accelerator, **self.kwargs)
        for cme, extra_info in sub_stage.run():
            yield cme, extra_info


## @ingroup Stages
## Parse the input workload residing in workload_path.
## The "workload" dict is converted to a NetworkX graph.
## @param workload
## @param mapping
def parse_workload_from_path_or_from_module(workload, mapping):
    if isinstance(workload, str):  # load from path
        module = importlib.import_module(workload)
        workload = module.workload

    if isinstance(mapping, str):  # load from path
        module = importlib.import_module(mapping)
        mapping = module.mapping

    # make a copy here to prevent later it is being changed in the following stages
    workload_copy = pickle_deepcopy(workload)
    workload = DNNWorkload(workload_copy, mapping)
    logger.info(
        f"Created workload graph with {workload.number_of_nodes()} nodes and {workload.number_of_edges()} edges.")

    return workload

## Description missing
class WorkloadParserStage(Stage):
    def __init__(self, list_of_callables, *, workload, mapping, **kwargs):
        super().__init__(list_of_callables, **kwargs)
        self.workload = workload
        self.mapping = mapping

    def run(self):
        workload = parse_workload_from_path_or_from_module(self.workload, self.mapping)
        sub_stage = self.list_of_callables[0](self.list_of_callables[1:], workload=workload, **self.kwargs)
        for cme, extra_info in sub_stage.run():
            yield cme, extra_info

