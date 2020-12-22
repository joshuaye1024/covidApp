# -*- coding: utf-8 -*-
# 2020-12-22
# Josh Ye with help from Owen Gallagher

from typing import Tuple
import logging
from logging import Logger
from trileaf_db.db_client import DBClient
from trileaf_db import db_api as api
import pandas as pd

log: Logger = logging.getLogger(__name__)

#TODO: Check if region code is valid; if not, raise an exception. Possibly a custom one. Log as error.
#TODO: Check date formats between 1. workbench file 2. covid api dataframe 3. function argument integer
#TODO: copy all table names for the insert once trileaf api updated. ez.
#TODO: Use logger to check if there are any missing columns after import.
class CovidDataImport:

    def insert_covid_region(self, dbclient: DBClient, region_id: str) -> bool:
        """Insert new covid region. Separate from inserting the statistics for the region, which is given in the next method.

        Returns:
            True if the region was inserted.
        """

        #query is an SQL insert statement, so return type is int.
        inserts: int = dbclient.query(
            sql='insert into {t_cr}({id}) values (%s)'.format(
                t_cr=api.TABLE_COVID_REGIONS,
                id=api.COVID_REGIONS_ID
            ),
            args=region_id
        )

        if inserts > 0:
            log.info('added region {} to the database'.format(region_id))
            return True

        else:
            log.warning('region {} not added to db'.format(region_id))
            return False


    def insert_covid_region_stats(self,
                                  dbclient: DBClient,
                                  region_id: str,
                                  region_stats: pd.DataFrame) -> int:
        """Insert new covid region stats.

        Args:
            dbclient = DBClient instance.

            region_id = covid region code (US state/territory abbreviation).

            region_stats = DataFrame of covid stats, where each row corresponds to a datetime.

        Returns:
            inserted = number of new rows inserted into the covid_region_stats table. Ideally, this
            is equal to region_stats.shape[0].
        """

        # check if region already in database
        # exists will be [[1]] if found in db, [] if not
        exists: Tuple = dbclient.query(
            sql='select 1 from {t_cr} where {id}=%s'.format(
                t_cr=api.TABLE_COVID_REGIONS,
                id=api.COVID_REGIONS_ID
            ),
            args=region_id
        )

        if len(exists) == 0:
            # region is new; add to database
            self.insert_covid_region(dbclient, region_id)

        # else, region already in database
        log.debug('region {} in database'.format(region_id))

        inserts: int = dbclient.multiquery(
            sql='insert into {t_crs}({id},{dt},{pos},{etc}) values (%s,%s,%s)'.format(
                t_crs=api.TABLE_COVID_REGION_STATS,
                id=api.COVID_REG_STAT_REGION_ID,
                dt=api.COVID_REG_STAT_DATETIME,
                pos=api.COVID_REG_STAT_POSITIVES,
                etc='...'
            ),
            # assumes columns in region_stats align with the order of the column names
            # enumerated above
            args=region_stats
        )

        # as an alternative to dbclient.multiquery, dbclient.query with each row in
        # region_stats.itertuples() is what I did for data_collector

        return inserts

        def get_latest_date(self,
                            dbclient: DBClient,
                            region_id: str,)->str:
            # get latest date in database
            latest: str = dbclient.query(
                sql='SELECT MAX({dt}) FROM {t_cs}'.format(
                    t_cs=api.TABLE_COVID_REGION_STATS,
                    dt=api.COVID_REG_STAT_DATETIME
                )
            )

            return latest

