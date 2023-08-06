#
# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project.
#

from enum import Enum
from typing import Any, Dict, List, Union

from dataclasses import dataclass, field


class Verb(Enum):
    Aggregate = "aggregate"
    Bin = "bin"
    Binarize = "binarize"
    Boolean = "boolean"
    Chain = "chain"
    Concat = "concat"
    Convert = "convert"
    Dedupe = "dedupe"
    Derive = "derive"
    Difference = "difference"
    Erase = "erase"
    Fetch = "fetch"
    Fill = "fill"
    Filter = "filter"
    FilterAggregateLookup = "filter-aggregate-lookup"
    Fold = "fold"
    Groupby = "groupby"
    Impute = "impute"
    Intersect = "intersect"
    Join = "join"
    Lookup = "lookup"
    Merge = "merge"
    MultiBinarize = "multi-binarize"
    OneHot = "onehot"
    Orderby = "orderby"
    Pivot = "pivot"
    Recode = "recode"
    Rename = "rename"
    Rollup = "rollup"
    Sample = "sample"
    Select = "select"
    Spread = "spread"
    Unfold = "unfold"
    Ungroup = "ungroup"
    Unhot = "unhot"
    Union = "union"
    Unorder = "unorder"
    Unroll = "unroll"
    Window = "window"


compound_verbs = {Verb.Chain, Verb.FilterAggregateLookup, Verb.MultiBinarize}


class Bin:
    min: Union[float, str]
    count: int


class Category:
    name: str
    count: int


@dataclass
class DataType(Enum):
    Array = "array"
    Boolean = "boolean"
    Date = "date"
    Number = "number"
    String = "string"
    Text = "text"
    Object = "object"
    Undefined = "undefined"
    Unknown = "unknown"


@dataclass
class Step:
    verb: Verb
    input: Union[str, Dict[str, str]]
    output: Union[str, Dict[str, str]]
    args: Dict[str, Any] = field(default_factory=dict)


class JoinStrategy(Enum):
    Inner = "inner"
    LeftOuter = "left outer"
    RightOuter = "right outer"
    FullOuter = "full outer"
    AntiJoin = "anti join"
    SemiJoin = "semi join"
    Cross = "cross"


@dataclass
class InputColumnArgs:
    column: str


class FieldAggregateOperation(Enum):
    Any = "any"
    Count = "count"
    CountDistinct = "distinct"
    Valid = "valid"
    Invalid = "invalid"
    Max = "max"
    Min = "min"
    Sum = "sum"
    Product = "product"
    Mean = "mean"
    Mode = "mode"
    Median = "median"
    StDev = "stdev"
    StDevPopulation = "stdevp"
    Variance = "variance"
    ArraryAgg = "array_agg"
    ArrayAggDistinct = "array_agg_distinct"


class BinStrategy(Enum):
    Auto = "auto"
    FixedCount = "fixed count"
    FixedWidth = "fixed width"


class FilterCompareType(Enum):
    Value = "value"
    Column = "column"


class NumericComparisonOperator(Enum):
    Equals = "="
    NotEqual = "!="
    LessThan = "<"
    LessThanOrEqual = "<="
    GreaterThan = ">"
    GreaterThanOrEqual = ">="
    IsEmpty = "is empty"
    IsNotEmpty = "is not empty"


class StringComparisonOperator(Enum):
    Equals = "equals"
    NotEqual = "is not equal"
    Contains = "contains"
    StartsWith = "starts with"
    EndsWith = "ends with"
    IsEmpty = "is empty"
    IsNotEmpty = "is not empty"
    RegularExpression = "regex"


class BooleanComparisonOperator(Enum):
    Equals = "equals"
    NotEqual = "is not equal"
    IsTrue = "is true"
    IsFalse = "is false"
    IsEmpty = "is empty"
    IsNotEmpty = "is not empty"


@dataclass
class Criterion:
    value: Any
    type: FilterCompareType
    operator: Union[
        NumericComparisonOperator, StringComparisonOperator, BooleanComparisonOperator
    ]


class BooleanLogicalOperator(Enum):
    OR = "or"
    AND = "and"
    NOR = "nor"
    NAND = "nand"
    XOR = "xor"
    XNOR = "xnor"


@dataclass
class FilterArgs(InputColumnArgs):
    criteria: List[Criterion]
    logical: BooleanLogicalOperator = BooleanLogicalOperator.OR


class SetOp(Enum):
    Concat = "concat"
    Union = "union"
    Intersect = "intersect"
    Except = "except"


class MathOperator(Enum):
    Add = "+"
    Subtract = "-"
    Multiply = "*"
    Divide = "/"
    Concatenate = "concat"


class SortDirection(Enum):
    Ascending = "asc"
    Descending = "desc"


class ParseType(Enum):
    Boolean = "boolean"
    Date = "date"
    Integer = "int"
    Decimal = "float"
    String = "string"


class MergeStrategy(Enum):
    FirstOneWins = "first one wins"
    LastOneWins = "last one wins"
    Concat = "concat"
    CreateArray = "array"


class WindowFunction(Enum):
    RowNumber = "row_number"
    Rank = "rank"
    PercentRank = "percent_rank"
    CumulativeDistribution = "cume_dist"
    FirstValue = "first_value"
    LastValue = "last_value"
    FillDown = "fill_down"
    FillUp = "fill_up"


@dataclass
class OrderByInstruction:
    column: str
    direction: SortDirection
