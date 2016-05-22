#!/usr/bin/env python

# Copyright 2015, Google, Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Command-line application that demonstrates basic BigQuery API usage.
This sample queries a public shakespeare dataset and displays the 10 of
Shakespeare's works with the greatest number of distinct words.
This sample is used on this page:
    https://cloud.google.com/bigquery/bigquery-api-quickstart
For more information, see the README.md under /bigquery.
"""
# [START all]
import argparse
import textwrap

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.client import GoogleCredentials


def main(project_id):
    # [START build_service]
    # Grab the application's default credentials from the environment.
    credentials = GoogleCredentials.get_application_default()
    # Construct the service object for interacting with the BigQuery API.
    bigquery_service = build('bigquery', 'v2', credentials=credentials)
    # [END build_service]

    try:
        # [START run_query]
        query_request = bigquery_service.jobs()
        query_data = {
            'query': (
                """
                SELECT language, 100*sum(merged="true")/count(*), "% of prs merged of", count(*)
                FROM (
                    SELECT 
                        repo_name, 
                        JSON_EXTRACT(payload, '$.action') as action, 
                        JSON_EXTRACT(payload, '$.pull_request.merged') as merged, 
                        JSON_EXTRACT(payload, '$.repo.language') as language, 
                        payload
                    FROM [githubarchive:month.201604]
                    WHERE type = "PullRequestEvent"
                    LIMIT 1000
                )
                WHERE action = '"closed"'
                GROUP BY language
                ;"""
            )
        }

        query_response = query_request.query(
            projectId=project_id,
            body=query_data
        ).execute()
        # [END run_query]

        # [START print_results]
        print('Query Results:')
        for row in query_response['rows']:
            print('\t'.join(field['v'] for field in row['f']))
        # [END print_results]

    except HttpError as err:
        print('Error: {}'.format(err.content))
        raise err


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('project_id', help='Your Google Cloud Project ID.')

    args = parser.parse_args()

    main(args.project_id)
# [END all]