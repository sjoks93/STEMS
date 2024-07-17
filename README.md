# STEMS
STEMS is a HW architecture-mapping design space exploration  (DSE) framework for multi-layer SNN mapping. STEMS applies inter-layer optimizations across SNN spatial and temporal dimensions.  STEMS is built on top of Stream and Zigzag DSE frameworks, found [here](https://zigzag-project.github.io/zigzag/). 


## Install required packages:
```
> pip install -r requirements.txt
```

## The first run
```
> cd stream
> python api.py
```

## Example run
python3 main_stream_arguments.py --workload 7PLIF --accelerator Meta_protoype_like_single_core  --schedule_order LYT_gated --time_schedule 1111111 --depth_schedule 0000000 --sp_map True --fuse_barrier True


## Documentation
Documentation for STEMS is underway!
