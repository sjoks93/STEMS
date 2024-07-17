if __name__ == '__main__':
    from common import get_conv_workload, get_quantizer_workload, get_avgpool_workload, get_maxpool_workload, get_add_workload
else:
    from inputs.workload.common import get_conv_workload, get_quantizer_workload, get_avgpool_workload, get_maxpool_workload, get_add_workload

def build_qconfig(graph_type: str, weight_precision: int, feature_precision: int, fl_precision: int = 8,  accumulator_precision: int = 16, num_classes: int = 1000):
    qconfig = []
    if graph_type == 'hardware':
        global_qconfig = {'O': accumulator_precision, 'O_final': feature_precision, 'W': weight_precision, 'I': feature_precision}
        for i in range(64):
            qconfig.append(global_qconfig.copy())
        ##### Add layers #####
        for i in [9, 16, 20, 27, 31, 35, 42, 46, 53, 57]:
            qconfig[i].pop('W')
            qconfig[i].pop('I')
            qconfig[i]['X'] = feature_precision
            qconfig[i]['Y'] = feature_precision
        ##### Special layers #####
        # First layer different
        qconfig[0] = {'O': accumulator_precision, 'O_final': feature_precision, 'W': fl_precision, 'I': fl_precision} # output low precision
        # Last layers different
        qconfig[60] = {'O': accumulator_precision, 'O_final': fl_precision, 'W': weight_precision, 'I': feature_precision} # output high precision
        qconfig[61] = {'O': accumulator_precision, 'O_final': fl_precision, 'W': fl_precision, 'I': fl_precision} # conv1x1 layer
        qconfig[62] = {'O': accumulator_precision, 'O_final': fl_precision, 'W': 0, 'I': fl_precision} # pooling
        qconfig[63] = {'O': accumulator_precision, 'O_final': accumulator_precision, 'W': fl_precision, 'I': fl_precision} # linear layer
    elif graph_type == 'academic':
        global_qconfig = {'O': accumulator_precision, 'O_final': feature_precision, 'W': weight_precision, 'I': feature_precision}
        for i in range(74):
            qconfig.append(global_qconfig.copy())
        ##### Layers that need high output precision (conv before add, conv before residual branch) #####
        for i in [5, 9, 13, 17, 22, 26, 30, 35, 41, 44, 49, 53, 57, 61, 66, ]:
            qconfig[i]['O_final'] = accumulator_precision
        ##### Quantizers (high input precision) #####
        for i in [6, 14, 19, 27, 32, 37, 45, 50, 58, 63]:
            qconfig[i] = {'O': accumulator_precision, 'O_final': feature_precision, 'W': 0, 'I': accumulator_precision}
        ##### Add layers WI->XY (all high precision) #####
        for i in [10, 18, 23, 31, 36, 41, 49, 54, 62, 67]:
            qconfig[i] = {'O': accumulator_precision, 'O_final': accumulator_precision, 'X': accumulator_precision, 'Y': accumulator_precision}
        # Add layers that have small output precision
        for i in [10, 23, 41, 54, 67]:
            qconfig[i]['O_final'] = feature_precision
        ##### Special layers #####
        # First layer different
        qconfig[0] = {'O': accumulator_precision, 'O_final': feature_precision, 'W': fl_precision, 'I': fl_precision}  # output low precision
        # # Last layers different
        qconfig[70] = {'O': accumulator_precision, 'O_final': fl_precision, 'W': weight_precision, 'I': feature_precision}  # output high precision
        qconfig[71] = {'O': accumulator_precision, 'O_final': accumulator_precision, 'W': fl_precision, 'I': fl_precision}  # conv1x1 layer
        qconfig[72] = {'O': accumulator_precision, 'O_final': fl_precision, 'W': 0, 'I': accumulator_precision}  # pooling
        qconfig[73] = {'O': accumulator_precision, 'O_final': accumulator_precision, 'W': fl_precision, 'I': fl_precision}  # linear layer
    else:
        raise NotImplementedError

    # if num_classes == 10 or num_classes == 100:
    #     # HW case
    #     # add layers
    #     qconfig.insert(6, {'O': accumulator_precision, 'O_final': op_precision, 'W': op_precision, 'I': op_precision})
    #     qconfig.insert(13, {'O': accumulator_precision, 'O_final': op_precision, 'W': op_precision, 'I': op_precision})

    return qconfig


def inv_res_block(layer_id, input_shape, output_channel, stride, expand_ratio, qconfig, graph_type):
    workload = {}
    x = input_shape
    y = x
    hidden_dim = int(input_shape[1] * expand_ratio)
    residual_source_id = layer_id - 1
    use_res_connect = stride == 1 and input_shape[1] == output_channel

    if use_res_connect and graph_type == 'academic':
        work, x, layer_id = get_quantizer_workload(layer_id, input_shape=x, qconfig=qconfig)
        workload.update(work)

    if expand_ratio != 1:
        work, x, layer_id = get_conv_workload(layer_id, input_shape=x, out_features=hidden_dim, kernel_size=1, stride=1, padding=0, qconfig=qconfig)
        workload.update(work)

    # DW conv
    work, x, layer_id = get_conv_workload(layer_id, input_shape=x, out_features=hidden_dim, kernel_size=3, stride=stride, padding=1, groups=hidden_dim, qconfig=qconfig)
    workload.update(work)

    # PW Conv
    work, x, layer_id = get_conv_workload(layer_id, input_shape=x, out_features=output_channel, kernel_size=1, stride=1, padding=0, qconfig=qconfig)
    workload.update(work)


    if use_res_connect:
        assert x == y
        work, x, layer_id = get_add_workload(layer_id, input_shape=y, qconfig=qconfig, residual_source_id=residual_source_id)
        workload.update(work)

    return workload, x, layer_id


def get_mbnetv2_workload(filter_multiplier=1.0, graph_type='hardware', weight_precision=8, feature_precision=8, fl_precision=8, accumulator_precision=16, num_classes=1000):
    workload = {}
    qconfig = build_qconfig(graph_type=graph_type, weight_precision=weight_precision, feature_precision=feature_precision, fl_precision=fl_precision, accumulator_precision=accumulator_precision, num_classes=num_classes)

    # Stride 1 for CIFAR-10 and CIFAR-100, stride 2 for ImageNet
    stride = 1 if num_classes == 10 or num_classes == 100 else 2

    inverted_residual_setting = [
        # t, c, n, s
        [1, 16, 1, 1],
        [6, 24, 2, stride],
        [6, 32, 3, stride],
        [6, 64, 4, 2],
        [6, 96, 3, 1],
        [6, 160, 3, 2],
        [6, 320, 1, 1],
    ]

    # building first layer
    input_channel = int(32 * filter_multiplier)
    last_channel = int(1280 * filter_multiplier)

    layer_id = 0

    x = (1, 3, 32, 32) if num_classes == 10 or num_classes == 100 else (1, 3, 224, 224)
    work, x, layer_id = get_conv_workload(layer_id, input_shape=x, out_features=input_channel, kernel_size=3, stride=stride, qconfig=qconfig)
    workload.update(work)

    for t, c, n, s in inverted_residual_setting:
        output_channel = int(c * filter_multiplier)
        for i in range(n):
            stride = s if i == 0 else 1
            work, x, layer_id = inv_res_block(layer_id, x, output_channel, stride, expand_ratio=t, qconfig=qconfig, graph_type=graph_type)
            workload.update(work)

    # building last several layers
    work, x, layer_id = get_conv_workload(layer_id, input_shape=x, out_features=last_channel, kernel_size=1, padding=0, qconfig=qconfig)
    workload.update(work)

    # AVG Pool
    work, x, layer_id = get_avgpool_workload(layer_id, input_shape=x, qconfig=qconfig)
    workload.update(work)

    # Classifier; linear
    work, x, layer_id = get_conv_workload(layer_id, input_shape=x, out_features=1000, kernel_size=1, padding=0, qconfig=qconfig)
    workload.update(work)
    return workload


workload = get_mbnetv2_workload(filter_multiplier=1.0, graph_type='academic', weight_precision=8, feature_precision=8, fl_precision=8, num_classes=1000)
# There is an error with fm=0.0625!

if __name__ == '__main__':
    for k,v in workload.items():
        try:
            op_source = v["operand_source"]["I"][0]
        except IndexError:
            op_source = v["operand_source"]["I"]
        except KeyError:
            op_source = str(v["operand_source"]["X"][0])+"&"+str(v["operand_source"]["Y"][0])

        if v["operator_type"] == 'Conv':
            print(f'{k}: {v["operator_type"]} {v["loop_dim_size"]["FX"]}x{v["loop_dim_size"]["FY"]}. Precision: {v["operand_precision"]}. Op_source: {op_source}')
        else:
            print(f'{k}: {v["operator_type"]}. Precision: {v["operand_precision"]}. Op_source: {op_source}')
    print('ok')
    from common import feature_size
    print(feature_size)
    sorted_feature_size = []
    for v in feature_size.values():
        sorted_feature_size.append(v['I'])
        sorted_feature_size.append(v['O'])

    sorted_feature_size = sorted(sorted_feature_size, reverse=True)
    print(sorted_feature_size)
    print(f'Max: {sorted_feature_size[0]/8/1024} KBytes. 2nd max: Max: {sorted_feature_size[1]/8/1024} KBytes')
