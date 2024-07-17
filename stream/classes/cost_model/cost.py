from collections import namedtuple

# tensor contains layer id and operand...
# need something like component; offchip comm or core2core
Cost = namedtuple("Cost", ["tensor", "component", "energy"])

