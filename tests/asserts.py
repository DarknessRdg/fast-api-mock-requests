class APIAssertMixin:
    def assertSuccess(self, response, status):
        received = response.status_code
        self.assertTrue(200 <= received <= 299, f'{received} is not 2xx')
        self.assertEqual(response.status_code, status)
