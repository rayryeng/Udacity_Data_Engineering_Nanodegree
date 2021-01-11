from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 # Define your operators params (with defaults) here
                 # Example:
                 # conn_id = your-connection-name
                 redshift_conn_id="",
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        # Map params here
        # Example:
        # self.conn_id = conn_id

        # EDIT - Create instance variables
        self.redshift_conn_id = redshift_conn_id
        # NEW - SQL quality checks
        dq_checks = [
            {'check_sql': "SELECT COUNT(*) FROM users WHERE userid is null",
             'expected_result': 0},
            {'check_sql': "SELECT COUNT(*) FROM songs WHERE songid is null",
             'expected_result': 0}
        ]
        self.dq_checks = dq_checks

    def execute(self, context):
        self.log.info('DataQualityOperator has been implemented')

        # EDIT - implement data quality operator
        redshift_hook = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        self.log.info("Running data quality test")

        error_count = 0
        # For each data quality check...
        # Checking the user IDs and song IDs to see if there are no NULL entries
        for check in self.dq_checks:
            sql = check.get('check_sql')
            exp_result = check.get('expected_result')

            records = redshift_hook.get_records(sql)[0]

            if exp_result != records[0]:
                error_count += 1
                failing_tests.append(sql)

        if error_count > 0:
            self.log.info('Tests failed')
            self.log.info(failing_tests)
            raise ValueError('Data quality check failed')