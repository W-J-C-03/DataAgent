from typing import TypedDict

from app.entities.column_info import ColumnInfo
from app.entities.metric_info import MetricInfo
from app.entities.value_info import ValueInfo

class MetricInfoState(TypedDict):
    name: str
    description: str
    relevant_columns: list[str]
    alias: list[str]

class ColumnInfoState(TypedDict):
    name: str
    type: str
    role: str
    examples: list
    description: str
    alias: list[str]
    table_id: str

class TableInfoState(TypedDict):
    name: str
    role: str
    description: str
    columns: list[ColumnInfoState]

class DateInfoState(TypedDict):
    date: str
    weekday: str
    quarter: str

class DBInfoState(TypedDict):
    dialect: str
    version: str
class DataAgentState(TypedDict):
    query: str
    keywords: list[str]

    retrieved_column_infos: list[ColumnInfo] # 字段信息
    retrieved_metric_infos: list[MetricInfo] # 指标信息
    retrieved_value_infos: list[ValueInfo] # 取值信息

    # 需要过滤的字段
    table_infos: list[TableInfoState]
    metric_infos: list[MetricInfoState]

    # 需要额外增加的字段
    date_info: DateInfoState
    db_info: DBInfoState

    sql: str
    error: str # 检验是否出现错误，为了条件边设置