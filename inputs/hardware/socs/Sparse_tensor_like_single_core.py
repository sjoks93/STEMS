from inputs.hardware.cores.Sparse_tensor_like import (
    get_core as get_sparse_tensor,
)
from inputs.hardware.cores.pooling import get_core as get_pooling_core
from inputs.hardware.cores.simd import get_core as get_simd_core
from inputs.hardware.cores.offchip import get_offchip_core
from inputs.hardware.nocs.mesh_2d import get_2d_mesh
from stream.classes.hardware.architecture.accelerator import Accelerator

cores = [get_sparse_tensor(id) for id in range(1)]  # 1 core
pooling_core = get_pooling_core(id=1)
simd_core = get_simd_core(id=2)
offchip_core_id = 3
offchip_core = get_offchip_core(id=offchip_core_id)

cores_graph = get_2d_mesh(cores, 1, 1, 32, 0, pooling_core, simd_core, offchip_core)

accelerator = Accelerator(
    "Sparse-tensor-like-single-core", cores_graph, offchip_core_id=offchip_core_id
)
