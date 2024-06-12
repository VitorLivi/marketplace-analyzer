#!/bin/sh

JOBS_PWD=$(cd ../jobs && pwd)

crontab -l | { cat; echo "
  0 0 * * 0 python $JOBS_PWD/measure_week_data_job'
  0 0 1 */1 * python $JOBS_PWD/measure_month_data_job'
"; } | crontab -
