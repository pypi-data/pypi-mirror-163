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
import logging
import os
import pathlib
from typing import List, Optional, Union

from sodasql.common.yaml_helper import YamlHelper
from sodasql.scan.file_system import FileSystemSingleton
from sodasql.scan.parser import Parser
from sodasql.scan.scan import Scan
from sodasql.scan.scan_yml import ScanYml
from sodasql.scan.warehouse_yml import WarehouseYml
from sodasql.scan.warehouse_yml_parser import WarehouseYmlParser, read_warehouse_yml_file
from sodasql.soda_server_client.soda_server_client import SodaServerClient
from sodasql.scan.failed_rows_processor import FailedRowsProcessor


logger = logging.getLogger(__name__)


def build_warehouse_yml_parser(
    warehouse_yml_file: Optional[str] = None, warehouse_yml_dict: Optional[dict] = None
) -> WarehouseYmlParser:
    """
    Build a warehouse yml parser.

    Parameters
    ----------
    warehouse_yml_file : Optional[str], optional (default: None)
        A warehouse yml file.
    warehouse_yml_dict : Optional[dict], optional (default: None)
        A warehouse yml dict.

    Returns
    -------
    out : WarehouseYmlParser
        The warehouse yml parser.
    """
    if not warehouse_yml_dict:
        if isinstance(warehouse_yml_file, pathlib.PurePath):
            warehouse_yml_file_str = str(warehouse_yml_file)
        elif isinstance(warehouse_yml_file, str):
            warehouse_yml_file_str = warehouse_yml_file
        else:
            logger.error(
                "scan_builder.warehouse_yml_file must be an instance of Purepath or str, "
                f"but was {type(warehouse_yml_file)}: {warehouse_yml_file}"
            )

        warehouse_yml_dict = read_warehouse_yml_file(warehouse_yml_file_str)

    warehouse_yml_parser = WarehouseYmlParser(warehouse_yml_dict, warehouse_yml_file)

    return warehouse_yml_parser


def create_soda_server_client(
    warehouse_yml: Optional[WarehouseYml] = None,
) -> SodaServerClient:
    """
    Create a Soda server client.

    Use the API key from the warehouse yml or from environment variables.

    Parameters
    ----------
    warehouse_yml : Optional[WarehouseYml], optional (default: None)
        The warehouse yml.

    Returns
    -------
    out : SodaServerClient
        The soda server client.
    """
    if (
        warehouse_yml is not None
        and warehouse_yml.soda_api_key_id
        and warehouse_yml.soda_api_key_secret
    ):
        host = warehouse_yml.soda_host
        api_key_id = warehouse_yml.soda_api_key_id
        api_key_secret = warehouse_yml.soda_api_key_secret
        port = str(warehouse_yml.soda_port)
        protocol = warehouse_yml.soda_protocol
    else:
        host = os.getenv("SODA_HOST", "cloud.soda.io")
        api_key_id = os.getenv("SODA_SERVER_API_KEY_ID", None)
        api_key_secret = os.getenv("SODA_SERVER_API_KEY_SECRET", None)
        port = os.getenv("SODA_PORT", "443")
        protocol = os.getenv("SODA_PROTOCOL", "https")

    soda_server_client = SodaServerClient(
        host,
        api_key_id=api_key_id,
        api_key_secret=api_key_secret,
        protocol=protocol,
        port=port,
    )
    return soda_server_client


class ScanBuilder:
    """
    Programmatic scan execution based on default dir structure:

    scan_builder = ScanBuilder()
    scan_builder.scan_yml_file = 'tables/my_table.yml'
    # scan_builder will automatically find the warehouse.yml in the parent and same directory as the scan YAML file
    # scan_builder.warehouse_yml_file = '../warehouse.yml'
    scan = scan_builder.build()
    scan_result = scan.execute()
    if scan_result.has_failures():
        print('Scan has test failures, stop the pipeline')

    Programmatic scan execution using dicts:

    scan_builder = ScanBuilder()
    scan_builder.warehouse_dict = {
        'name': 'my_warehouse_name',
        'connection': {
            'type': 'snowflake',
            ...
        }
    })
    scan_builder.scan_dict = {
        ...
    }
    scan = scan_builder.build()
    scan_result = scan.execute()
    if scan_result.has_failures():
        print('Scan has test failures, stop the pipeline')
    """

    def __init__(self):
        self.file_system = FileSystemSingleton.INSTANCE
        self.warehouse_yml_file: Optional[Union[str, pathlib.PurePath]] = None
        self.warehouse_yml_dict: Optional[dict] = None
        self.warehouse_yml: Optional[WarehouseYml] = None
        self.scan_yml_file: Optional[str] = None
        self.time: Optional[str] = None
        self.scan_yml_dict: Optional[dict] = None
        self.scan_yml: Optional[ScanYml] = None
        self.variables: dict = {}
        self.parsers: List[Parser] = []
        self.assert_no_warnings_or_errors = True
        self.soda_server_client: Optional[SodaServerClient] = None
        self.scan_results_json_path: Optional[str] = None
        self.failed_rows_dir_path: Optional[str] = None
        self.failed_rows_processor: Optional[FailedRowsProcessor] = None

    def build(self, offline: bool = False):
        self._build_warehouse_yml()
        self._build_scan_yml()

        for parser in self.parsers:
            parser.assert_no_warnings_or_errors()
        if not self.scan_yml or not self.warehouse_yml:
            return

        from sodasql.scan.warehouse import Warehouse
        warehouse = Warehouse(self.warehouse_yml)

        if not offline:
            self._create_soda_server_client()

        return Scan(warehouse=warehouse,
                    scan_yml=self.scan_yml,
                    variables=self.variables,
                    soda_server_client=self.soda_server_client,
                    time=self.time,
                    scan_results_file=self.scan_results_json_path,
                    failed_rows_processor=self.failed_rows_processor)

    def _build_warehouse_yml(self):
        if not self.warehouse_yml_file and not self.warehouse_yml_dict and not self.warehouse_yml:
            logger.error("No warehouse specified")
        elif not self.warehouse_yml:
            warehouse_yml_parser = build_warehouse_yml_parser(
                self.warehouse_yml_file, self.warehouse_yml_dict
            )
            self.parse_warehouse_yml(warehouse_yml_parser)

    def parse_warehouse_yml(self, warehouse_parser):
        warehouse_parser.log()
        self.parsers.append(warehouse_parser)
        self.warehouse_yml = warehouse_parser.warehouse_yml

    def _build_scan_yml(self):
        if not self.scan_yml_file and not self.scan_yml_dict and not self.scan_yml:
            logger.error(f'No scan file specified')
            return
        elif self.scan_yml_file and not self.scan_yml_dict and not self.scan_yml:
            scan_yml_file_str: Optional[str] = None
            if isinstance(self.scan_yml_file, pathlib.PurePath):
                scan_yml_file_str = str(self.scan_yml_file)
            elif isinstance(self.scan_yml_file, str):
                scan_yml_file_str = self.scan_yml_file

            if not isinstance(scan_yml_file_str, str):
                logger.error(
                    f'scan_builder.scan_yml_file must be str, but was {type(scan_yml_file_str)}: {scan_yml_file_str}')
            elif self.file_system.is_readable_file(scan_yml_file_str):
                scan_yml_str = self.file_system.file_read_as_str(scan_yml_file_str)

                if scan_yml_str:
                    self.scan_yml_dict = YamlHelper.parse_yaml(scan_yml_str, scan_yml_file_str)
                else:
                    logger.error(f'Failed to parse scan yaml file: {scan_yml_file_str}')

        if self.scan_yml_dict and not self.scan_yml:
            from sodasql.scan.scan_yml_parser import ScanYmlParser
            scan_yml_parser = ScanYmlParser(self.scan_yml_dict, self.scan_yml_file)
            scan_yml_parser.log()
            self.parsers.append(scan_yml_parser)
            self.scan_yml = scan_yml_parser.scan_yml

    def _create_soda_server_client(self):
        if not self.soda_server_client:
            soda_server_client = create_soda_server_client(self.warehouse_yml)
            if soda_server_client.api_key_id and soda_server_client.api_key_secret:
                self.soda_server_client = soda_server_client
            else:
                logger.debug("No Soda Cloud account configured")
