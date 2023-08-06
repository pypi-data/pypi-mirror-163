#
# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project.
#

from datashaper.engine.verbs.verb_input import VerbInput
from datashaper.table_store import TableContainer


def sample(input: VerbInput, size: int = None, proportion: int = None):
    input_table = input.get_input()
    output = input_table.sample(n=size, frac=proportion)
    return TableContainer(table=output)
