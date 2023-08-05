#  Copyright 2020 Soda
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#   http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from sodasql.scan.dialect import Dialect
from sodasql.scan.group_value import GroupValue
from sodasql.scan.scan import Scan
from sodasql.scan.scan_column import ScanColumn

from sodasql.soda_server_client.monitor_measurement import MonitorMeasurement


class MonitorMetricType:
    ROW_COUNT = 'rowCount'
    MISSING_VALUES_COUNT = 'missingValuesCount'
    MISSING_VALUES_PERCENTAGE = 'missingValuesPercentage'
    VALID_VALUES_COUNT = 'validValuesCount'
    VALID_VALUES_PERCENTAGE = 'validValuesPercentage'
    INVALID_VALUES_COUNT = 'invalidValuesCount'
    INVALID_VALUES_PERCENTAGE = 'invalidValuesPercentage'
    MINIMUM_VALUE = 'minimumValue'
    MAXIMUM_VALUE = 'maximumValue'
    UNIQUE_VALUES_COUNT = 'uniqueValuesCount'
    DISTINCT_VALUES_COUNT = 'distinctValuesCount'
    UNIQUENESS_PERCENTAGE = 'uniquenessPercentage'
    MINIMUM_LENGTH = 'minimumLength'
    MAXIMUM_LENGTH = 'maximumLength'
    AVERAGE_LENGTH = 'averageLength'
    AVERAGE = 'average'
    STANDARD_DEVIATION = 'standardDeviation'
    SUM = 'sum'
    VARIANCE = 'variance'


@dataclass
class MonitorMetric:
    scan: Scan
    metric_id: str
    metric_type: str
    column_name: str
    group_by_column_names: List[str]
    metric_sql: str = None
    sql: str = None

    def build_sql(self,
                  qualified_group_column_names,
                  filter_condition,
                  qualified_table_name):

        scan_column: Optional[ScanColumn] = \
            self.scan.scan_columns.get(self.column_name.lower()) \
            if self.column_name and self.scan.scan_columns \
            else None

        dialect: Dialect = self.scan.warehouse.dialect

        metric_select_fields = []
        select_fields = []

        if qualified_group_column_names:
            metric_select_fields.extend(qualified_group_column_names)
            select_fields.extend(qualified_group_column_names)

        if self.metric_type == MonitorMetricType.ROW_COUNT:
            metric_select_fields.append(dialect.sql_expr_count_all())
        elif scan_column:
            select_fields.append(scan_column.qualified_column_name)
            if self.metric_type == MonitorMetricType.MISSING_VALUES_COUNT:
                metric_select_fields.append(dialect.sql_expr_count_conditional(scan_column.missing_condition, scan_column.column_name))
            elif self.metric_type == MonitorMetricType.MISSING_VALUES_PERCENTAGE:
                metric_select_fields.append(dialect.sql_expr_count_all())
                metric_select_fields.append(dialect.sql_expr_count_conditional(scan_column.missing_condition, scan_column.column_name))
            elif self.metric_type == MonitorMetricType.VALID_VALUES_COUNT:
                metric_select_fields.append(
                    dialect.sql_expr_count_conditional(scan_column.non_missing_and_valid_condition, scan_column.column_name))
            elif self.metric_type in [MonitorMetricType.VALID_VALUES_PERCENTAGE,
                                      MonitorMetricType.INVALID_VALUES_COUNT,
                                      MonitorMetricType.INVALID_VALUES_PERCENTAGE]:
                metric_select_fields.append(dialect.sql_expr_count_conditional(scan_column.non_missing_condition, scan_column.column_name))
                metric_select_fields.append(
                    dialect.sql_expr_count_conditional(scan_column.non_missing_and_valid_condition, scan_column.column_name))
            elif self.metric_type == MonitorMetricType.UNIQUENESS_PERCENTAGE:
                metric_select_fields.append(
                    dialect.sql_expr_count_conditional(scan_column.non_missing_and_valid_condition, scan_column.column_name))
                metric_select_fields.append(dialect.sql_expr_count(dialect.sql_expr_distinct(
                    dialect.sql_expr_conditional(scan_column.non_missing_and_valid_condition,
                                                 scan_column.qualified_column_name))))
            elif self.metric_type == MonitorMetricType.MINIMUM_VALUE:
                metric_select_fields.append(dialect.sql_expr_min(scan_column.numeric_expr))
            elif self.metric_type == MonitorMetricType.MAXIMUM_VALUE:
                metric_select_fields.append(dialect.sql_expr_max(scan_column.numeric_expr))
            elif self.metric_type == MonitorMetricType.AVERAGE:
                metric_select_fields.append(dialect.sql_expr_avg(scan_column.numeric_expr))
            elif self.metric_type == MonitorMetricType.SUM:
                metric_select_fields.append(dialect.sql_expr_sum(scan_column.numeric_expr))
            else:
                raise RuntimeError(f'Unsupported metric type: {self.metric_type}')

        metric_fields = ", \n       ".join(metric_select_fields)
        self.metric_sql = (f'SELECT {metric_fields} \n'
                           f'FROM {qualified_table_name}')

        self.sql = (f'SELECT * \n'
                    f'FROM {qualified_table_name}')

        if filter_condition:
            self.metric_sql += f' \nWHERE {filter_condition}'
            self.sql += f' \nWHERE {filter_condition}'

        if qualified_group_column_names:
            self.metric_sql += f' \nGROUP BY {", ".join(qualified_group_column_names)}'
            self.sql += f' \nGROUP BY {", ".join(qualified_group_column_names)}'

    def execute(self) -> MonitorMeasurement:
        if not self.group_by_column_names:
            start = datetime.now()
            row = self.scan.warehouse.sql_fetchone(self.metric_sql)
            query_milliseconds = int(((datetime.now() - start).total_seconds()) * 1000)
            value = self.get_value(row)
            return MonitorMeasurement(
                metric=self.metric_type,
                metric_id=self.metric_id,
                sql=self.metric_sql,
                column_name=self.column_name,
                value=value,
                query_milliseconds=query_milliseconds)
        else:
            start = datetime.now()
            rows = self.scan.warehouse.sql_fetchall(self.metric_sql)
            query_milliseconds = int(((datetime.now() - start).total_seconds()) * 1000)

            group_values = []
            for row in rows:
                results = list(row)
                group_columns_count = len(self.group_by_column_names)
                group = results[:group_columns_count]
                results = results[group_columns_count:]
                value = self.get_value(results)
                group_values.append(GroupValue(group=group, value=value))

            return MonitorMeasurement(
                metric=self.metric_type,
                metric_id=self.metric_id,
                sql=self.metric_sql,
                column_name=self.column_name,
                group_values=group_values,
                query_milliseconds=query_milliseconds)

    def get_value(self, results):
        value = None
        if self.metric_type == MonitorMetricType.MISSING_VALUES_PERCENTAGE:
            row_count = int(results[0])
            missing_count = int(results[1])
            value = None
            if row_count > 0:
                value = float(missing_count) * 100 / row_count

        elif self.metric_type in [MonitorMetricType.MISSING_VALUES_PERCENTAGE,
                                  MonitorMetricType.INVALID_VALUES_COUNT,
                                  MonitorMetricType.INVALID_VALUES_PERCENTAGE]:
            values_count = int(results[0])
            valid_count = int(results[1])
            invalid_count = values_count - valid_count
            value = None

            if self.metric_type == MonitorMetricType.VALID_VALUES_PERCENTAGE and values_count > 0:
                value = float(valid_count) * 100 / values_count
            elif self.metric_type == MonitorMetricType.INVALID_VALUES_COUNT:
                value = invalid_count
            elif self.metric_type == MonitorMetricType.INVALID_VALUES_PERCENTAGE and values_count > 0:
                value = float(invalid_count) * 100 / values_count

        elif self.metric_type == MonitorMetricType.UNIQUENESS_PERCENTAGE:
            valid_count = int(results[0])
            distinct_count = int(results[1])
            if valid_count > 1:
                value = (distinct_count - 1) * 100 / (valid_count - 1)
        else:
            value = results[0]
            if not (value is None or isinstance(value, int) or isinstance(value, float)):
                value = float(value)
        return value
