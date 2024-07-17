from math import ceil
import functools


__all__ = ['get_conv_workload', 'get_quantizer_workload', 'get_avgpool_workload', 'get_maxpool_workload', 'get_add_workload']
feature_size = {}

def get_conv_workload(layer_id, input_shape, out_features, kernel_size, qconfig, stride=1, padding=1, groups=1, name_suffix='', override_source_layer=None):
    # Compute the output size of a convolution based in the input size, kernel size, stride and padding
    output_shape = input_shape[0], out_features, \
        (input_shape[2] + 2 * padding - kernel_size) // stride + 1, \
        (input_shape[3] + 2 * padding - kernel_size) // stride + 1

    # workload = f'conv {kernel_size}x{kernel_size}. input: {input_shape}, output: {output_shape}'
    if override_source_layer:
        operand_source = [override_source_layer]
    else:
        # I usually source layer_id, except for first layer
        operand_source = [layer_id - 1] if layer_id != 0 else []
    workload = {
        'operator_type': 'Conv' + name_suffix,
        'equation': 'O[b][g][k][oy][ox]+=W[g][k][c][fy][fx]*I[b][g][c][iy][ix]',
        'loop_dim_size': {'B': input_shape[0], 'K': ceil(output_shape[1] / groups), 'G': groups, "OX": output_shape[2],
                          "OY": output_shape[3], "C": ceil(input_shape[1] / groups), "FX": kernel_size,
                          "FY": kernel_size},
        'pr_loop_dim_size': {'IX': input_shape[2], 'IY': input_shape[3]},
        'dimension_relations': [f'ix={stride}*ox+fx', f'iy={stride}*oy+fy'],
        'operand_precision': qconfig[layer_id],
        'operand_source': {'W': [], 'I': operand_source},
        'constant_operands': ['W'] if layer_id != 0 else ['W', 'I'],  # also I for the first layer (layer_id==0)
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'},
    }

    global feature_size
    feature_size[layer_id] = {'I': functools.reduce(lambda x, y: x*y, input_shape)*qconfig[layer_id]['I'], 'O': functools.reduce(lambda x, y: x*y, output_shape)*qconfig[layer_id]['O_final']}
    # print(f"Conv: {functools.reduce(lambda x, y: x*y, input_shape)*qconfig[layer_id]['I']}. oup: {functools.reduce(lambda x, y: x*y, output_shape)*qconfig[layer_id]['O']}")
    return {layer_id: workload}, output_shape, layer_id + 1

def get_sconv_workload(layer_id, input_shape, out_features, kernel_size, qconfig, stride=1, padding=1, groups=1, name_suffix='', override_source_layer=None):
    # Compute the output size of a convolution based in the input size, kernel size, stride and padding
    output_shape = input_shape[0], out_features, \
        (input_shape[2] + 2 * padding - kernel_size) // stride + 1, \
        (input_shape[3] + 2 * padding - kernel_size) // stride + 1

    # workload = f'conv {kernel_size}x{kernel_size}. input: {input_shape}, output: {output_shape}'
    if override_source_layer:
        operand_source = [override_source_layer]
    else:
        # I usually source layer_id, except for first layer
        operand_source = [layer_id - 1] if layer_id != 0 else []
    workload = {
        'operator_type': 'Conv' + name_suffix,
        'equation': 'O[b][g][k][oy][ox]+=W[g][k][c][fy][fx]*I[b][g][c][iy][ix]',
        'loop_dim_size': {'B': input_shape[0], 'K': ceil(output_shape[1] / groups), 'G': groups, "OX": output_shape[2],
                          "OY": output_shape[3], "C": ceil(input_shape[1] / groups), "FX": kernel_size,
                          "FY": kernel_size},
        'pr_loop_dim_size': {'IX': input_shape[2], 'IY': input_shape[3]},
        'dimension_relations': [f'ix={stride}*ox+fx', f'iy={stride}*oy+fy'],
        'operand_precision': qconfig[layer_id],
        'operand_source': {'W': [], 'I': operand_source},
        'operand_state': {"V": []},
        'state': True,
        'constant_operands': ['W'] if layer_id != 0 else ['W', 'I'],  # also I for the first layer (layer_id==0)
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2', 'V': 'S'},
    }

    global feature_size
    feature_size[layer_id] = {'I': functools.reduce(lambda x, y: x*y, input_shape)*qconfig[layer_id]['I'], 'O': functools.reduce(lambda x, y: x*y, output_shape)*qconfig[layer_id]['O']}
    # print(f"Conv: {functools.reduce(lambda x, y: x*y, input_shape)*qconfig[layer_id]['I']}. oup: {functools.reduce(lambda x, y: x*y, output_shape)*qconfig[layer_id]['O']}")
    return {layer_id: workload}, output_shape, layer_id + 1

def get_sconv_inputwise_workload(layer_id, input_shape, out_features, kernel_size, qconfig, stride=1, padding=1, groups=1, name_suffix='', override_source_layer=None):
    # Compute the output size of a convolution based in the input size, kernel size, stride and padding
    output_shape = input_shape[0], out_features, \
        (input_shape[2] + 2 * padding - kernel_size) // stride + 1, \
        (input_shape[3] + 2 * padding - kernel_size) // stride + 1

    # workload = f'conv {kernel_size}x{kernel_size}. input: {input_shape}, output: {output_shape}'
    if override_source_layer:
        operand_source = [override_source_layer]
    else:
        # I usually source layer_id, except for first layer
        operand_source = [layer_id - 1] if layer_id != 0 else []
    workload = {
        'operator_type': 'Conv' + name_suffix,
        'equation': 'O[b][g][k][oy][ox]+=W[g][k][c][fy][fx]*I[b][g][c][iy][ix]',
        'loop_dim_size': {'B': input_shape[0], 'K': ceil(output_shape[1] / groups), 'G': groups, "OX": output_shape[2],
                          "OY": output_shape[3], "C": ceil(input_shape[1] / groups), "FX": kernel_size,
                          "FY": kernel_size},
        'pr_loop_dim_size': {'OX': output_shape[2], 'OY': output_shape[3]},
        'dimension_relations': [f'ox=ix/{stride}-fx', f'oy=iy/{stride}-fy'],
        'operand_precision': qconfig[layer_id],
        'operand_source': {'W': [], 'I': operand_source},
        'operand_state': {"V": []},
        'state': True,
        'constant_operands': ['W'] if layer_id != 0 else ['W', 'I'],  # also I for the first layer (layer_id==0)
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2', 'V': 'S'},
    }

    global feature_size
    feature_size[layer_id] = {'I': functools.reduce(lambda x, y: x*y, input_shape)*qconfig[layer_id]['I'], 'O': functools.reduce(lambda x, y: x*y, output_shape)*qconfig[layer_id]['O']}
    # print(f"Conv: {functools.reduce(lambda x, y: x*y, input_shape)*qconfig[layer_id]['I']}. oup: {functools.reduce(lambda x, y: x*y, output_shape)*qconfig[layer_id]['O']}")
    return {layer_id: workload}, output_shape, layer_id + 1



def get_ssconv_workload(layer_id, input_shape, out_features, kernel_size, qconfig, stride=1, padding=1, groups=1, i_rate = 0.05, name_suffix='', override_source_layer=None):
    # Compute the output size of a convolution based in the input size, kernel size, stride and padding
    output_shape = input_shape[0], out_features, \
        (input_shape[2] + 2 * padding - kernel_size) // stride + 1, \
        (input_shape[3] + 2 * padding - kernel_size) // stride + 1

    # workload = f'conv {kernel_size}x{kernel_size}. input: {input_shape}, output: {output_shape}'
    if override_source_layer:
        operand_source = [override_source_layer]
    else:
        # I usually source layer_id, except for first layer
        operand_source = [layer_id - 1] if layer_id != 0 else []
    workload = {
        'operator_type': 'Conv' + name_suffix,
        'equation': 'O[b][g][k][oy][ox]+=W[g][k][c][fy][fx]*I[b][g][c][iy][ix]',
        'loop_dim_size': {'B': input_shape[0], 'K': ceil(output_shape[1] / groups), 'G': groups, "OX": output_shape[2],
                          "OY": output_shape[3], "C": ceil(input_shape[1] / groups), "FX": kernel_size,
                          "FY": kernel_size},
        'pr_loop_dim_size': {'IX': input_shape[2], 'IY': input_shape[3]},
        'dimension_relations': [f'ix={stride}*ox+fx', f'iy={stride}*oy+fy'],
        'operand_precision': qconfig[layer_id],
        'operand_source': {'W': [], 'I': operand_source},
        'operand_state': {"V": []},
        'sparse': True,
        'i_rate': i_rate,
        'state': True,
        'constant_operands': ['W'] if layer_id != 0 else ['W', 'I'],  # also I for the first layer (layer_id==0)
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2', 'V': 'S'},
    }

    global feature_size
    feature_size[layer_id] = {'I': functools.reduce(lambda x, y: x*y, input_shape)*qconfig[layer_id]['I'], 'O': functools.reduce(lambda x, y: x*y, output_shape)*qconfig[layer_id]['O']}
    # print(f"Conv: {functools.reduce(lambda x, y: x*y, input_shape)*qconfig[layer_id]['I']}. oup: {functools.reduce(lambda x, y: x*y, output_shape)*qconfig[layer_id]['O']}")
    return {layer_id: workload}, output_shape, layer_id + 1
def get_quantizer_workload(layer_id, input_shape, qconfig, override_source_layer=None):
    return _get_pool_workload(layer_id=layer_id, input_shape=input_shape, qconfig=qconfig, operator='quantizer', override_source_layer=override_source_layer)

def get_avgpool_workload(layer_id, input_shape, qconfig, override_source_layer=None):
    return _get_pool_workload(layer_id=layer_id, input_shape=input_shape, qconfig=qconfig, operator='avg', override_source_layer=override_source_layer)

def get_maxpool_workload(layer_id, input_shape, qconfig, kernel_size=3, padding=1, stride=2, override_source_layer=None):
    return _get_pool_workload(layer_id=layer_id, input_shape=input_shape, qconfig=qconfig, operator='max', kernel_size=kernel_size, padding=padding, stride=stride, override_source_layer=override_source_layer)

def _get_pool_workload(layer_id, input_shape, qconfig, operator='avg', kernel_size=None, padding=None, stride=1, override_source_layer=None):
    precision = qconfig[layer_id]
    precision['W'] = 0
    operand_source = override_source_layer if override_source_layer else layer_id - 1

    if operator == 'avg':
        operator_tye = 'AveragePool'
        output_shape = input_shape[0], input_shape[1], 1, 1
        filter_size_x, filter_size_y = input_shape[2], input_shape[3]
    elif operator == 'max':
        operator_tye = 'MaxPool'
        output_shape = input_shape[0], input_shape[1], \
            (input_shape[2] + 2 * padding - kernel_size) // stride + 1, \
            (input_shape[3] + 2 * padding - kernel_size) // stride + 1
        filter_size_x, filter_size_y = kernel_size, kernel_size
    elif operator == 'quantizer':
        operator_tye = 'Quantizer'
        output_shape = input_shape
        filter_size_x, filter_size_y = 1, 1
    else:
        raise NotImplementedError

    workload = {
        'operator_type': operator_tye,
        'equation': 'O[b][g][oy][ox]+=W[fx][fy]*I[b][g][iy][ix]',
        'dimension_relations': [f'ix={stride}*ox+fx', f'iy={stride}*oy+fy'],
        'loop_dim_size': {'B': input_shape[0], 'G': input_shape[1], 'OY': output_shape[2], 'OX': output_shape[3],
                          'FX': filter_size_x, 'FY': filter_size_y},
        'operand_precision': precision,
        'operand_source': {'W': [], 'I': [operand_source]},
        'constant_operands': ['W'],
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'},
    }

    global feature_size
    feature_size[layer_id] = {'I': functools.reduce(lambda x, y: x * y, input_shape) * qconfig[layer_id]['I'],
                              'O': functools.reduce(lambda x, y: x * y, output_shape) * qconfig[layer_id]['O_final']}
    # print(f"Pool: {functools.reduce(lambda x, y: x*y, input_shape)*qconfig[layer_id]['I']}. oup: {functools.reduce(lambda x, y: x*y, output_shape)*qconfig[layer_id]['O']}")
    return {layer_id: workload}, output_shape, layer_id + 1

def get_add_workload(layer_id, input_shape, qconfig, residual_source_id, override_source_layer=None):
    # Residual add
    operand_source = input_shape[1] if override_source_layer else layer_id - 1
    workload = {
        'operator_type': 'Add',
        'equation': 'O[b][g][oy][ox]=X[b][g][oy][ox]+Y[b][g][oy][ox]',
        'dimension_relations': [],
        'loop_dim_size': {'B': input_shape[0], 'G': input_shape[1], 'OY': input_shape[2], 'OX': input_shape[3]},
        'operand_precision': qconfig[layer_id],
        'operand_source': {'X': [residual_source_id], 'Y': [operand_source]},
        'constant_operands': [],
        'memory_operand_links': {'O': 'O', 'X': 'I2', 'Y': 'I1'}
    }   
    global feature_size
    feature_size[layer_id] = {'I': functools.reduce(lambda x, y: x * y, input_shape) * qconfig[layer_id]['X'],
                              'O': functools.reduce(lambda x, y: x * y, input_shape) * qconfig[layer_id]['O_final']}
    # print(f"Add: in/out {functools.reduce(lambda x, y: x*y, input_shape)*qconfig[layer_id]['X']}")
    return {layer_id: workload}, input_shape, layer_id + 1

