from stream.classes.workload.computation_node import ComputationNode


class SimdNode(ComputationNode):
    def __init__(
        self,
        node_id,
        node_attrs,
        node_name,
        node_input_names,
        node_output_names,
        op_type,
    ):
        super().__init__(
            node_id, node_attrs, node_name, node_input_names, node_output_names, op_type
        )
