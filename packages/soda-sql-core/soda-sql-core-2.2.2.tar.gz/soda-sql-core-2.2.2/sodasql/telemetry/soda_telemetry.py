import logging
import platform
from typing import Optional

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.semconv.resource import ResourceAttributes
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    SimpleSpanProcessor,
)

from sodasql.__version__ import SODA_SQL_VERSION
from sodasql.common.config_helper import ConfigHelper
from sodasql.scan.dialect import Dialect
from sodasql.telemetry.memory_span_exporter import MemorySpanExporter
from sodasql.telemetry.soda_exporter import SodaConsoleSpanExporter, SodaOTLPSpanExporter

logger = logging.getLogger(__name__)


class SodaTelemetry:
    """Main entry point for Open Telemetry tracing.

    For more info about what and why visit https://github.com/sodadata/soda-sql/issues/543.

    The main goal of this class is to concentrate as much tracing data and logic as reasonable.
    This code design means that compromises have been made on code design in order to facilitate maximum
    transparency and avoid scattering tracing code around the codebase.

    With that being said, some tracing is still present in other files, e.g.:
    - `/core/sodasql/cli/cli.py` - CLI arguments and options tracing
    - `/core/sodasql/scan/warehouse.py` - safe datasource type and hash tracing

    This list is not necessarily exhaustive, search for `from sodasql.telemetry.soda_telemetry import SodaTelemetry` imports OR
    `set_attribute` method usage to obtain the full list.
    """

    ENDPOINT = 'https://collect.soda.io/v1/traces'
    __instance = None
    soda_config = ConfigHelper.get_instance()

    @staticmethod
    def get_instance(test_mode: bool = False):
        if test_mode:
            SodaTelemetry.__instance = None

        if SodaTelemetry.__instance is None:
            SodaTelemetry(test_mode=test_mode)
        return SodaTelemetry.__instance

    def __init__(self, test_mode: bool):
        if SodaTelemetry.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            SodaTelemetry.__instance = self

        self.__send = self.soda_config.send_anonymous_usage_stats or test_mode

        if self.__send:
            logger.info("Setting up usage telemetry.")

            self.__provider = TracerProvider(
                resource=Resource.create(
                    {
                        'os.architecture': platform.architecture(),
                        'python.version': platform.python_version(),
                        'python.implementation': platform.python_implementation(),
                        ResourceAttributes.OS_TYPE: platform.system(),
                        ResourceAttributes.OS_VERSION: platform.version(),
                        'platform': platform.platform(),
                        ResourceAttributes.SERVICE_VERSION: SODA_SQL_VERSION,
                        ResourceAttributes.SERVICE_NAME: 'soda',
                        ResourceAttributes.SERVICE_NAMESPACE: 'soda-sql',
                    }
                )
            )

            if test_mode:
                self.__setup_for_test()
            else:
                self.__setup()
        else:
            logger.info("Skipping usage telemetry setup.")

    def __setup(self):
        """Set up Open Telemetry processors and exporters for normal use.
        """
        local_debug_mode = self.soda_config.get_value('tracing_local_debug_mode')

        if local_debug_mode or logger.getEffectiveLevel() == logging.DEBUG:
            self.__provider.add_span_processor(BatchSpanProcessor(SodaConsoleSpanExporter()))

        if not local_debug_mode:
            otlp_exporter = SodaOTLPSpanExporter(endpoint=self.ENDPOINT)
            otlp_processor = BatchSpanProcessor(otlp_exporter)
            self.__provider.add_span_processor(otlp_processor)

        trace.set_tracer_provider(self.__provider)

    def __setup_for_test(self):
        """Set up Open Telemetry processors and exporters for usage in tests.
        """
        self.__provider.add_span_processor(SimpleSpanProcessor(MemorySpanExporter.get_instance()))

        trace.set_tracer_provider(self.__provider)

    def set_attribute(self, key: str, value: str) -> None:
        """Set attribute value in the current span.
        """
        if self.__send:
            current_span = trace.get_current_span()
            current_span.set_attribute(key, value)

    @staticmethod
    def obtain_datasource_hash(dialect: Dialect):
        return dialect.generate_hash_safe()

    @property
    def user_cookie_id(self) -> str:
        return self.soda_config.get_value('user_cookie_id')
