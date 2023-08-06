from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional

import arrow
from loguru import logger

from snatch.base.status import IntegrationStatus
from snatch.helpers.validator import Validator


@dataclass
class BaseData:
    """Base Data Class.

    The subclasses created using this class will be available
    to Data Scientists.

    Default Properties
    ==================

    * tax_id (str):                 The TaxId prospected.
                                    must be a valid CNPJ, formatted or not.
    * integration_status (str):     The current Integration Status. Current status are:
                                    NOT_FOUND, WAITING, SUCCESS, EXPIRED, ERROR,
                                    CONN_ERROR and TIMEOUT
                                    Please check the `find_current_status` method
                                    for more info.
    * status_reason (str):          The human friendly reason for current status
    * prospect_date (datetime):     The prospect datetime.
    * payload (dict):               Original payload received from prospection.
    * timeit (str)                  Time for retrieving data.
    * datasource_base_url (str)     Data Source Base Url.
    * current_environment (str)     Current AWS Environment. Available environments are:
                                    local, dev, stg, prd. Default: prd.
    * data_type (str)               DataSource Object Name.
    """

    id: Optional[int] = None
    tax_id: Optional[str] = None
    integration_status: Optional[IntegrationStatus] = None
    status_reason: str = ""
    prospect_date: Optional[datetime] = None
    payload: Optional[Dict[str, Any]] = None
    timeit: Optional[str] = None
    datasource_base_url: Optional[str] = None
    current_environment: Optional[str] = None

    @property
    def data_type(self) -> str:
        """Return DataSource Object Name."""
        return self.__class__.__name__

    def find_current_status(self, data):
        """Find current Status for Data.

        Current available status:

        * NOT_FOUND   When backend responds 404 for TaxId
        * WAITING     When backend responds with status "PENDING" or "RUNNING"
        * SUCCESS     When backend responds with status "SUCCESS"
                      and prospect date is lower or equal than max_days_old
        * NO_DATA     When Datasource responds 200, but no Data was returned
        * INCOMPLETE  When Datasource responds 200, but Data prospected is incomplete
        * EXPIRED     When backend responds with status "SUCCESS"
                      and prospect date is greater than max_days_old
        * ERROR       When backend responds a integration error
                      when prospecting the DataSource
        * CONN_ERROR  When backend responds 40x,50x
        * TIMEOUT     When timeout occurs

        :param max_days_old: Max days old for current data, for check expiration.
        :param max_periods_old: Max months old for current data, for check expiration.
        """
        if self.integration_status.is_success:
            days_old = (
                arrow.utcnow().ceil("day") - arrow.get(self.prospect_date).floor("day")
            ).days
            months_old = int(
                (
                    arrow.utcnow().ceil("month")
                    - arrow.get(self.prospect_date).floor("day")
                ).days
                / 30
            )
            expired_by_date = (
                data["max_days_old"] is not None
                and days_old > data["max_days_old"]
                or data["max_days_old"] == 0
            )
            self.integration_status = (
                IntegrationStatus.EXPIRED
                if expired_by_date is True or Validator(data).start() is False
                else self.integration_status
            )
            if self.integration_status == IntegrationStatus.EXPIRED:
                status_reason = (
                    "Data from Datasource is: "
                    + (
                        f"Expired by Date: {days_old} old"
                        if expired_by_date
                        else f"Expired by Period: {months_old} months old"
                    )
                    + ". Requesting new prospect..."
                )
                logger.warning(status_reason)
                self.status_reason = status_reason
        if self.integration_status.need_wait:
            self.integration_status = IntegrationStatus.WAITING
