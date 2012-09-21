from test_base import TestBase


class TestBamboo(TestBase):

    def setUp(self):
        TestBase.setUp(self)
        self.fake_id = '31546146'

    def _store_csv(self):
        response = self.bamboo.store_csv_file(self.CSV_FILE)
        self.dataset_id = response['id']
        return response

    def test_get_url(self):
        self.assertTrue(isinstance(self.bamboo.get_url(), basestring))

    def test_get_dataset_url(self):
        self.assertTrue(isinstance(self.bamboo.get_dataset_url(self.fake_id), basestring))
        self.assertTrue('datasets' in self.bamboo.get_dataset_url(self.fake_id))

    def test_get_dataset_summary_url(self):
        self.assertTrue(isinstance(self.bamboo.get_dataset_summary_url(self.fake_id), basestring))
        self.assertTrue('summary' in self.bamboo.get_dataset_summary_url(self.fake_id))

    def test_get_dataset_info_url(self):
        self.assertTrue(isinstance(self.bamboo.get_dataset_info_url(self.fake_id), basestring))
        self.assertTrue('info' in self.bamboo.get_dataset_info_url(self.fake_id))

    def test_get_dataset_calculations_url(self):
        self.assertTrue(isinstance(self.bamboo.get_dataset_calculations_url(self.fake_id), basestring))
        self.assertTrue('calculations' in self.bamboo.get_dataset_calculations_url(self.fake_id))

    def test_store_csv_file(self):
        response = self._store_csv()
        self.assertTrue('id' in response)

    def test_delete_dataset(self):
        self._store_csv()
        response = self.bamboo.delete_dataset(self.dataset_id)
        self.assertTrue('success' in response)
        self.dataset_id = None

    def test_store_calculation(self):
        self._store_csv()
        name = 'amount_gps_alt'
        formula = 'amount+gps_alt'
        response = self.bamboo.store_calculation(self.dataset_id, name, formula)
        self.assertTrue('name' in response)
        self.assertEqual(response['name'], name)
        self.assertTrue('formula' in response)
        self.assertEqual(response['formula'], formula)

    def test_count_submissions(self):
        self._store_csv()
        count = self.bamboo.count_submissions(self.dataset_id, 'amount')
        count = int(count)
        self.assertTrue(isinstance(count, int))
        self.assertEqual(count, self.NUM_ROWS)

    def test_count_submissions_dimension(self):
        self._store_csv()
        count = self.bamboo.count_submissions(self.dataset_id, 'rating')
        count = int(count)
        self.assertTrue(isinstance(count, int))
        self.assertEqual(count, self.NUM_ROWS)

    def test_count_submissions_mean(self):
        self._store_csv()
        mean = self.bamboo.count_submissions(self.dataset_id, 'amount', 'mean')
        mean = float(mean)
        self.assertTrue(isinstance(mean, float))

    def test_count_submissions_mean_dimension(self):
        self._store_csv()
        mean = self.bamboo.count_submissions(self.dataset_id, 'rating', 'mean')
        mean = float(mean)
        self.assertTrue(isinstance(mean, float))
        self.assertEqual(mean, self.NUM_ROWS)

    def test_query(self):
        self._store_csv()
        response = self.bamboo.query(self.dataset_id)
        self.assertTrue(isinstance(response, list))
        self.assertEqual(len(response), self.NUM_ROWS)

    def test_query_summary(self):
        self._store_csv()
        response = self.bamboo.query(self.dataset_id, as_summary=True)
        self.assertTrue(isinstance(response, dict))
        self.assertEqual(len(response), self.NUM_COLS)
