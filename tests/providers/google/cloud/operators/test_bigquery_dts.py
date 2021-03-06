#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
import unittest

import mock

from airflow.providers.google.cloud.operators.bigquery_dts import (
    BigQueryCreateDataTransferOperator,
    BigQueryDataTransferServiceStartTransferRunsOperator,
    BigQueryDeleteDataTransferConfigOperator,
)

PROJECT_ID = "id"


TRANSFER_CONFIG = {
    "data_source_id": "google_cloud_storage",
    "destination_dataset_id": "example_dataset",
    "params": {},
    "display_name": "example-transfer",
    "disabled": False,
    "data_refresh_window_days": 0,
    "schedule": "first sunday of quarter 00:00",
}

TRANSFER_CONFIG_ID = "id1234"

NAME = "projects/123abc/locations/321cba/transferConfig/1a2b3c"


class BigQueryCreateDataTransferOperatorTestCase(unittest.TestCase):
    @mock.patch("airflow.providers.google.cloud.operators.bigquery_dts.BiqQueryDataTransferServiceHook")
    @mock.patch("airflow.providers.google.cloud.operators.bigquery_dts.get_object_id")
    def test_execute(self, mock_name, mock_hook):
        mock_name.return_value = TRANSFER_CONFIG_ID
        mock_xcom = mock.MagicMock()
        op = BigQueryCreateDataTransferOperator(
            transfer_config=TRANSFER_CONFIG, project_id=PROJECT_ID, task_id="id"
        )
        op.xcom_push = mock_xcom
        op.execute(None)
        mock_hook.return_value.create_transfer_config.assert_called_once_with(
            authorization_code=None,
            metadata=None,
            transfer_config=TRANSFER_CONFIG,
            project_id=PROJECT_ID,
            retry=None,
            timeout=None,
        )


class BigQueryDeleteDataTransferConfigOperatorTestCase(unittest.TestCase):
    @mock.patch("airflow.providers.google.cloud.operators.bigquery_dts.BiqQueryDataTransferServiceHook")
    def test_execute(self, mock_hook):
        op = BigQueryDeleteDataTransferConfigOperator(
            transfer_config_id=TRANSFER_CONFIG_ID, task_id="id", project_id=PROJECT_ID
        )
        op.execute(None)
        mock_hook.return_value.delete_transfer_config.assert_called_once_with(
            metadata=None,
            transfer_config_id=TRANSFER_CONFIG_ID,
            project_id=PROJECT_ID,
            retry=None,
            timeout=None,
        )


class BigQueryDataTransferServiceStartTransferRunsOperatorTestCase(unittest.TestCase):
    @mock.patch("airflow.providers.google.cloud.operators.bigquery_dts.BiqQueryDataTransferServiceHook")
    def test_execute(self, mock_hook):
        op = BigQueryDataTransferServiceStartTransferRunsOperator(
            transfer_config_id=TRANSFER_CONFIG_ID, task_id="id", project_id=PROJECT_ID
        )
        op.execute(None)
        mock_hook.return_value.start_manual_transfer_runs.assert_called_once_with(
            transfer_config_id=TRANSFER_CONFIG_ID,
            project_id=PROJECT_ID,
            requested_time_range=None,
            requested_run_time=None,
            metadata=None,
            retry=None,
            timeout=None,
        )
