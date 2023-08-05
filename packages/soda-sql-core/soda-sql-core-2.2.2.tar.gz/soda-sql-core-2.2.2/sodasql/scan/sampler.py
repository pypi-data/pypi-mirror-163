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

import json
import logging
import re
import tempfile
from datetime import datetime
from typing import List

from deprecated import deprecated

from sodasql.scan.metric import Metric
from sodasql.scan.samples_yml import SamplesYml
from sodasql.scan.scan import Scan
from sodasql.scan.scan_column import ScanColumn
from sodasql.scan.test_result import TestResult

logger = logging.getLogger(__name__)


class Sampler:

    def __init__(self, scan: Scan):
        self.scan = scan
        self.scan_reference = self.scan.scan_reference
        self.scan_folder_name = (f'{self._fileify(self.scan.warehouse.name)}' +
                                 f'-{self._fileify(self.scan.scan_yml.table_name)}' +
                                 (f'-{self._fileify(self.scan.time)}' if isinstance(self.scan.time, str) else '') +
                                 (f'-{self.scan.time.strftime("%Y%m%d%H%M%S")}' if isinstance(self.scan.time,
                                                                                              datetime) else '') +
                                 f'-{datetime.now().strftime("%Y%m%d%H%M%S")}')

    def _fileify(self, name: str):
        return re.sub(r'[^A-Za-z0-9_.]*', '', name).lower()

    def get_samples(self, samples_yml: SamplesYml, measurement, test_results: List[TestResult]):
        """
        Builds and executes SQL to save a sample for the given measurement
        Args:
            samples_yml: For column metric samples, samples_yml will have the defaults from the scan samples
                         already resolved.
        """
        column_name = measurement.column_name
        scan_column: ScanColumn = self.scan.scan_columns[column_name.lower()] if column_name else None
        tests = [test_result.test for test_result in test_results]

        # rows_total is the total number of rows from which the sample is taken
        rows_total = measurement.value
        sample_name = None
        where_clause = None
        tablesample = None
        limit = None
        test_ids = None

        if measurement.metric == Metric.ROW_COUNT:
            sample_name = 'dataset'
            tablesample = samples_yml.table_tablesample
            limit = samples_yml.table_limit
        elif measurement.metric == Metric.MISSING_COUNT:
            sample_name = 'missing'
            where_clause = scan_column.missing_condition
            tablesample = samples_yml.failed_tablesample
            limit = samples_yml.failed_limit

            def is_missing_test(test):
                return test.metrics == [Metric.MISSING_COUNT] or test.metrics == [Metric.MISSING_PERCENTAGE]

            test_ids = [test.id for test in tests if is_missing_test(test) and test.column == column_name]
        elif measurement.metric == Metric.VALUES_COUNT:
            sample_name = 'values'
            where_clause = f'NOT ({scan_column.missing_condition})'
            tablesample = samples_yml.passed_tablesample
            limit = samples_yml.passed_limit
        elif measurement.metric == Metric.INVALID_COUNT:
            sample_name = 'invalid'
            where_clause = f'NOT ({scan_column.missing_condition}) AND NOT ({scan_column.valid_condition})'
            tablesample = samples_yml.failed_tablesample
            limit = samples_yml.failed_limit

            def is_invalid_test(test):
                return test.metrics == [Metric.INVALID_COUNT] or test.metrics == [Metric.INVALID_PERCENTAGE]

            test_ids = [test.id for test in tests if is_invalid_test(test) and test.column == column_name]
        elif measurement.metric == Metric.VALID_COUNT:
            sample_name = 'valid'
            where_clause = f'NOT ({scan_column.missing_condition}) AND ({scan_column.valid_condition})'
            tablesample = samples_yml.passed_tablesample
            limit = samples_yml.passed_limit

        sql = (f"SELECT * \n"
               f"FROM {self.scan.qualified_table_name}")

        if where_clause:
            sql += f" \nWHERE {where_clause} "

        if tablesample is not None:
            sql += f" \nTABLESAMPLE {tablesample};"
        else:
            if self.scan.warehouse.dialect.type == 'sqlserver':
                sql += f" ORDER BY 1 OFFSET 0 ROWS FETCH NEXT {limit} ROWS ONLY"
            else:
                sql += f" \nLIMIT {limit};"

        sample_description = (f'{self.scan.scan_yml.table_name}.sample'
                              if sample_name == 'dataset' else f'{self.scan.scan_yml.table_name}.{column_name}.{sample_name}')

        logger.debug(f'Sending sample {sample_description}')

        sample_columns, sample_rows, total_row_count = self._get_query_results_with_limit(sql, limit or 5)

        return {'sample_name': sample_name,
                'column_name': column_name,
                'test_ids': test_ids,
                'sample_columns': sample_columns,
                'sample_rows': sample_rows,
                'sample_description': sample_description,
                'total_row_count': rows_total}

    def send_samples_to_soda_cloud(self, samples_context):

        sample_name = samples_context.get('sample_name')
        column_name = samples_context.get('column_name')
        test_ids = samples_context.get('test_ids')
        sample_columns = samples_context.get('sample_columns')
        sample_description = samples_context.get('sample_description')
        total_row_count = samples_context.get('total_row_count')
        sample_rows = samples_context.get('sample_rows')
        stored_row_count = len(sample_rows)

        scan_folder_name = (f'{self._fileify(self.scan.warehouse.name)}' +
                            f'-{self._fileify(self.scan.scan_yml.table_name)}' +
                            (f'-{self._fileify(self.scan.time)}' if isinstance(self.scan.time, str) else '') +
                            (f'-{self.scan.time.strftime("%Y%m%d%H%M%S")}' if isinstance(self.scan.time,
                                                                                         datetime) else '') +
                            f'-{datetime.now().strftime("%Y%m%d%H%M%S")}')
        try:

            with tempfile.TemporaryFile() as temp_file:
                for row in sample_rows:
                    temp_file.write(bytearray(json.dumps(row), 'utf-8'))
                    temp_file.write(b'\n')

                temp_file_size_in_bytes = temp_file.tell()
                temp_file.seek(0)

                file_path = (f'{scan_folder_name}/' +
                             (f'{self._fileify(column_name)}_' if column_name else '') +
                             f'{sample_name}.jsonl')

                file_id = self.scan.soda_server_client.scan_upload(self.scan.scan_reference,
                                                                   file_path,
                                                                   temp_file,
                                                                   temp_file_size_in_bytes)

                self.scan.soda_server_client.scan_file(
                    scan_reference=self.scan.scan_reference,
                    sample_type=sample_name + 'Sample',
                    stored=stored_row_count,
                    total=total_row_count,
                    source_columns=sample_columns,
                    file_id=file_id,
                    column_name=column_name,
                    test_ids=test_ids)

                logger.debug(f'Sent sample {sample_description} ({stored_row_count}/{total_row_count}) to Soda Cloud')
        except Exception as e:
            logger.exception(f'Soda cloud error: Could not upload samples: {e}')
            raise e

    def create_file_path_failed_rows_sql_metric(self, column_name: str, metric_name: str):
        return (f'{self.scan_folder_name}/' +
                (f'{self._fileify(column_name)}_' if column_name else '') +
                'failed_rows_' +
                f'{self._fileify(metric_name)}' +
                '.jsonl')

    def __serialize_file_upload_value(self, value):
        if value is None \
            or isinstance(value, str) \
            or isinstance(value, int) \
            or isinstance(value, float):
            return value
        return str(value)

    def __get_sample_columns(self, cursor):
        return [
            {'name': d[0],
             'type': self.scan.warehouse.dialect.get_type_name(d)}
            for d in cursor.description
        ]

    def _get_query_results_with_limit(self, sql: str, limit: int):
        cursor = self.scan.warehouse.connection.cursor()
        try:
            logger.debug(f'Executing SQL query: \n{sql}')
            start = datetime.now()
            cursor.execute(sql)
            sample_columns = self.__get_sample_columns(cursor)
            stored_rows = total_rows = 0
            row = cursor.fetchone()
            sample_rows = []
            while row is not None:
                sample_values = []
                if stored_rows < limit:
                    for i in range(0, len(row)):
                        sample_values.append(self.__serialize_file_upload_value(row[i]))
                    stored_rows += 1
                total_rows += 1
                sample_rows.append(sample_values)
                row = cursor.fetchone()

            delta = datetime.now() - start
            logger.debug(f'SQL took {str(delta)}')

        finally:
            cursor.close()

        return sample_columns, sample_rows, total_rows

    def save_sample_to_local_file_with_limit(self, sql, temp_file, limit: int):
        cursor = self.scan.warehouse.connection.cursor()
        try:
            logger.debug(f'Executing SQL query: \n{sql}')
            start = datetime.now()
            cursor.execute(sql)
            sample_columns = self.__get_sample_columns(cursor)

            stored_rows = total_rows = 0
            row = cursor.fetchone()
            while row is not None:
                if stored_rows < limit:
                    sample_values = []
                    for i in range(0, len(row)):
                        sample_values.append(self.__serialize_file_upload_value(row[i]))
                    temp_file.write(bytearray(json.dumps(sample_values), 'utf-8'))
                    temp_file.write(b'\n')
                    stored_rows += 1
                total_rows += 1
                row = cursor.fetchone()

            delta = datetime.now() - start
            logger.debug(f'SQL took {str(delta)}')

        finally:
            cursor.close()

        return stored_rows, sample_columns, total_rows
