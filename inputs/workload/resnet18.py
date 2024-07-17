if __name__ == '__main__':
    from common import get_conv_workload, get_quantizer_workload, get_avgpool_workload, get_maxpool_workload, get_add_workload
else:
    from inputs.workload.common import get_conv_workload, get_quantizer_workload, get_avgpool_workload, get_maxpool_workload, get_add_workload


def build_qconfig(graph_type: str, weight_precision: int, feature_precision: int, fl_precision: int = 8,  accumulator_precision: int = 16):
    qconfig = []
    if graph_type == 'hardware':
        global_qconfig = {'O': accumulator_precision, 'O_final': feature_precision, 'W': weight_precision, 'I': feature_precision}
        for i in range(31):
            qconfig.append(global_qconfig.copy())
        ##### Add layers #####
        for i in [4, 7, 11, 14, 18, 21, 25, 28]:
            qconfig[i].pop('W')
            qconfig[i].pop('I')
            qconfig[i]['X'] = feature_precision
            qconfig[i]['Y'] = feature_precision
        ##### Special layers #####
        # First layers different
        qconfig[0] = {'O': accumulator_precision, 'O_final': feature_precision, 'W': fl_precision, 'I': fl_precision} # output low precision
        # Last layers different
        qconfig[28] = {'O': accumulator_precision, 'O_final': fl_precision, 'X': feature_precision, 'Y': feature_precision} # output high precision
        qconfig[29] = {'O': accumulator_precision, 'O_final': fl_precision, 'W': 0, 'I': fl_precision} # pooling
        qconfig[30] = {'O': accumulator_precision, 'O_final': accumulator_precision, 'W': fl_precision, 'I': fl_precision} # linear layer
    elif graph_type == 'academic':
        global_qconfig = {'O': accumulator_precision, 'O_final': feature_precision, 'W': weight_precision, 'I': feature_precision}
        for i in range(42):
            qconfig.append(global_qconfig.copy())
        ##### Add layers WI->XY (all high precision) #####
        for i in [5, 9, 15, 19, 25, 29, 35, 39]:
            qconfig[i] = {'O': accumulator_precision, 'O_final': accumulator_precision, 'X': accumulator_precision, 'Y': accumulator_precision}
        ##### Layers that need high output precision (conv before add, conv_downsample) #####
        for i in [4, 8, 12, 18, 22, 28, 32, 38, 14, 24, 34]:
            qconfig[i]['O_final'] = accumulator_precision
        ##### Quantizers (high input precision) #####
        for i in [2, 6, 10, 13, 16, 20, 23, 26, 30, 33, 36,]:
            qconfig[i] = {'O': accumulator_precision, 'O_final': feature_precision, 'W': 0, 'I': accumulator_precision}

        ##### Special layers #####
        # First layer different
        qconfig[0] = {'O': accumulator_precision, 'O_final': accumulator_precision, 'W': fl_precision, 'I': fl_precision} # output high precision
        qconfig[1] = {'O': accumulator_precision, 'O_final': accumulator_precision, 'W': 0, 'I': accumulator_precision} # Maxpool; constant precision
        # Last layers different
        qconfig[40] = {'O': accumulator_precision, 'O_final': fl_precision, 'W': 0, 'I': accumulator_precision} # AvgPool; high input precision
        qconfig[41] = {'O': accumulator_precision, 'O_final': accumulator_precision, 'W': fl_precision, 'I': fl_precision} # linear layer
    else:
        raise NotImplementedError

    return qconfig


def basic_block(layer_id, input_shape, output_channel, stride, qconfig, graph_type):
    workload = {}
    x = input_shape
    y = x
    residual_source_id = layer_id - 1
    use_downsample = stride != 1 and input_shape[1] != output_channel

    if graph_type == 'academic': # Scales are not the same in main and residual branch
        work, x, layer_id = get_quantizer_workload(layer_id, input_shape=x, qconfig=qconfig)
        workload.update(work)

    # Conv 1
    work, x, layer_id = get_conv_workload(layer_id, input_shape=x, out_features=output_channel, kernel_size=3, stride=stride, padding=1, qconfig=qconfig)
    workload.update(work)
    # Conv2
    work, x, layer_id = get_conv_workload(layer_id, input_shape=x, out_features=output_channel, kernel_size=3, stride=1, padding=1, qconfig=qconfig)
    workload.update(work)

    # Conv downsample
    if use_downsample:
        override_source_layer = residual_source_id
        if graph_type == 'academic': # Scales are not the same in main and residual branch
            work, y, layer_id = get_quantizer_workload(layer_id, input_shape=y, qconfig=qconfig, override_source_layer=override_source_layer)
            workload.update(work)
            override_source_layer = None

        # Conv downsample
        work, y, layer_id = get_conv_workload(layer_id, input_shape=y, out_features=output_channel, kernel_size=3, stride=stride, padding=1, qconfig=qconfig, override_source_layer=override_source_layer)
        workload.update(work)

    # Residual add
    assert x == y
    work, x, layer_id = get_add_workload(layer_id, input_shape=y, qconfig=qconfig, residual_source_id=residual_source_id)
    workload.update(work)

    return workload, x, layer_id


def get_r18_workload(filter_multiplier=1.0, graph_type='hardware', weight_precision=8, feature_precision=8, fl_precision=8, accumulator_precision=16, num_classes=1000):
    workload = {}
    qconfig = build_qconfig(graph_type=graph_type, weight_precision=weight_precision, feature_precision=feature_precision, fl_precision=fl_precision, accumulator_precision=accumulator_precision)
    if num_classes == 10 or num_classes == 100:
        qconfig.pop(1)

    in_planes = 64
    layers = [2,2,2,2]

    # building first layer
    input_channel = int(in_planes * filter_multiplier)
    layer_id = 0

    # Stem   
    if num_classes == 10 or num_classes == 100:
        x = (1, 3, 32, 32)
        # First layer
        work, x, layer_id = get_conv_workload(layer_id, input_shape=x, out_features=input_channel, kernel_size=3, stride=1, padding=1, qconfig=qconfig)
        workload.update(work)
    else:
        x = (1, 3, 224, 224)
        # First layer
        work, x, layer_id = get_conv_workload(layer_id, input_shape=x, out_features=input_channel, kernel_size=7, stride=2, padding=3, qconfig=qconfig)
        workload.update(work)

        # Max Pool
        work, x, layer_id = get_maxpool_workload(layer_id, input_shape=x, qconfig=qconfig, kernel_size=3, stride=2, padding=1)
        workload.update(work)

    # Basic blocks
    for i in range(len(layers)):
        output_channel = input_channel * (2 ** i)
        stride = 1 if i == 0 else 2
        strides = [stride] + [1] * (layers[i] - 1)
        for stride in strides:
            work, x, layer_id = basic_block(layer_id, x, output_channel, stride, qconfig=qconfig, graph_type=graph_type)
            workload.update(work)


    # AVG Pool
    work, x, layer_id = get_avgpool_workload(layer_id, input_shape=x, qconfig=qconfig)
    workload.update(work)

    # Classifier; linear
    work, x, layer_id = get_conv_workload(layer_id, input_shape=x, out_features=num_classes, kernel_size=1, padding=0, qconfig=qconfig)
    workload.update(work)
    return workload


workload = get_r18_workload(filter_multiplier=1.5, graph_type='academic', weight_precision=8, feature_precision=8, fl_precision=8,)


if __name__ == '__main__':
    for k,v in workload.items():
        if v["operator_type"] == 'Conv':
            print(f'{k}: {v["operator_type"]} {v["loop_dim_size"]["FX"]}x{v["loop_dim_size"]["FY"]}. \t Precision: {v["operand_precision"]}. \t {v["loop_dim_size"]}')
        else:
            print(f'{k}: {v["operator_type"]}. \t Precision: {v["operand_precision"]}. \t {v["loop_dim_size"]}')
        # if v["operator_type"] == 'Conv':
        #     print(f'{k}: {v["operator_type"]} {v["loop_dim_size"]["FX"]}x{v["loop_dim_size"]["FY"]}. \t Precision: {v["operand_precision"]}. \t Operand_source: {v["operand_source"]}. \t Loopdimsize:{v["loop_dim_size"]}')
        # else:
        #     print(f'{k}: {v["operator_type"]}. \t Precision: {v["operand_precision"]}. \t Operand_source: {v["operand_source"]}. \t Loopdimsize:{v["loop_dim_size"]}')
    print('ok')