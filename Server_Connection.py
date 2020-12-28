# -*- coding: utf-8 -*-
# 2020-12-22
# Josh Ye with help from Owen Gallagher

from typing import Tuple
import logging
from logging import Logger
import trileaf_db.db_client as db_client
from trileaf_db import db_api as api
import pandas as pd
import Main

log: Logger = logging.getLogger(__name__)

#TODO: Check if region code is valid; if not, raise an exception. Possibly a custom one. Log as error.
#TODO: Check date formats between 1. workbench file 2. covid api dataframe 3. function argument integer
#TODO: copy all table names for the insert once trileaf api updated. ez.
#TODO: Use logger to check if there are any missing columns after import.
class CovidDataImport:

    def insert_covid_region(self, dbclient: db_client.DBClient, region_id: str) -> bool:
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
                                  dbclient: db_client.DBClient,
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
            sql='insert into {t_crs}({id}, {date}, {pos}, '
                '{neg}, {pend}, {prob}, '
                '{res_tot}, {res_src}, {hosp_curr}, '
                '{hosp_tot}, {icu_curr}, {icu_tot}, '
                '{vent_curr}, {vent_tot}, {rec}, {qual}, '
                '{lastup}, {death}, {tot_test_vir}, {pos_vir}, '
                '{neg_vir}, {pos_case_vir}, {conf_death}, {prob_death}, '
                '{tot_enc_vir}, {tot_peep_vir}, {tot_ant}, {pos_ant}, '
                '{neg_ant}, {tot_peep_ant}, {pos_peep_ant}, {neg_peep_ant}, '
                '{tot_test_anti}, {tot_peep_anti}, {pos_peep_anti}, '
                '{pos_anti}, {pos_incr}, {tot_res_incr}, {death_incr}, '
                '{hosp_incr}) values (%s,%s,%s)'.format(
                t_crs=api.TABLE_COVID_REGION_STATS,
                id=api.COVID_STATS_REGION_ID,
                date=api.COVID_STATS_DATETIME,
                pos=api.COVID_STATS_POSITIVES,
                neg=api.COVID_STATS_NEGATIVES,
                pend=api.COVID_STATS_PENDING,
                prob=api.COVID_STATS_PROB_CASES,
                res_tot=api.COVID_STATS_TOTAL_TEST_RES,
                res_src=api.COVID_STATS_TEST_RES_SRC,
                hosp_curr=api.COVID_STATS_CURR_HOSPITALIZED,
                hosp_tot=api.COVID_STATS_TOTAL_HOSPITALIZED,
                icu_curr=api.COVID_STATS_CURR_ICU,
                icu_tot=api.COVID_STATS_TOTAL_ICU,
                vent_curr=api.COVID_STATS_CURR_VENT,
                vent_tot=api.COVID_STATS_TOTAL_VENT,
                rec=api.COVID_STATS_RECOVERED,
                qual=api.COVID_STATS_DATA_QUALITY,
                lastup=api.COVID_STATS_LAST_UPDATE,
                death=api.COVID_STATS_DEATHS,
                tot_test_vir=api.COVID_STATS_TOTAL_TESTS_VIRAL,
                pos_vir=api.COVID_STATS_POSITIVES_VIRAL,
                neg_vir=api.COVID_STATS_NEGATIVES_VIRAL,
                pos_case_vir=api.COVID_STATS_POS_CASES_VIRAL,
                conf_death=api.COVID_STATS_DEATHS_CONFIRMED,
                prob_death=api.COVID_STATS_DEATHS_PROBABLE,
                tot_enc_vir=api.COVID_STATS_TOTAL_TEST_ENCOUNTERS_VIRAL,
                tot_peep_vir=api.COVID_STATS_TOTAL_TESTS_PEOPLE_VIRAL,
                tot_ant=api.COVID_STATS_TOTAL_TESTS_ANTIBODY,
                pos_ant=api.COVID_STATS_POSITIVES_ANTIBODY,
                neg_ant=api.COVID_STATS_NEGATIVES_ANTIBODY,
                tot_peep_ant=api.COVID_STATS_TOTAL_TESTS_PEOPLE_ANTIBODY,
                pos_peep_ant=api.COVID_STATS_POSITIVES_PEOPLE_ANTIBODY,
                neg_peep_ant=api.COVID_STATS_NEGATIVES_PEOPLE_ANTIBODY,
                tot_test_anti=api.COVID_STATS_TOTAL_TESTS_ANTIGEN,
                tot_peep_anti=api.COVID_STATS_TOTAL_TESTS_PEOPLE_ANTIGEN,
                pos_peep_anti=api.COVID_STATS_POSITIVES_PEOPLE_ANTIGEN,
                pos_anti=api.COVID_STATS_POSITIVES_ANTIGEN,
                pos_incr=api.COVID_STATS_POSITIVE_INCREASE,
                tot_res_incr=api.COVID_STATS_TOTAL_TEST_RES_INCREASE,
                death_incr=api.COVID_STATS_DEATHS_INCREASE,
                hosp_incr=api.COVID_STATS_HOSPITALIZED_INCREASE
            ),
            # assumes columns in region_stats align with the order of the column names
            # enumerated above
            args=region_stats
        )

        # as an alternative to dbclient.multiquery, dbclient.query with each row in
        # region_stats.itertuples() is what I did for data_collector

        return inserts

    def get_latest_date(self,
                        dbclient: db_client.DBClient,
                        region_id: str,):
        # get latest date in database
        latest: str = dbclient.query(
            sql='SELECT MAX({dt}) FROM {t_cs}'.format(
                t_cs=api.TABLE_COVID_REGION_STATS,
                dt=api.COVID_REG_STAT_DATETIME
            )
        )

        return latest

    def main(self):
        # load db credentials from ./res/secrets/db_credentials.txt
        db_client.init()

        # create connection client
        dbclient: db_client.DBClient = db_client.DBClient()

        if dbclient.connected():
            # fetch historical region stats from covid api
            # this doesn't show how to skip older data that's already collected

            date =self.get_latest_date()

            region_code: str = 'xx'
            region_stats: pd.DataFrame = Main.getCovidData(date, region_code)

            inserts: int = self.insert_covid_region_stats(
                dbclient,
                region_code,
                region_stats
            )

            log.info('inserted {} new rows for region {}'.format(
                inserts,
                region_code
            ))

        else:
            log.error('failed to connect to trileaf database')

