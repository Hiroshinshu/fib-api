import unittest
from flask import Flask
from fib_server import app

class FibonacciAPITestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
    
    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Enter https://hmsample.f5.si/fib?n=<number> to get the nth fibonacci number.', response.data)

    def test_fib_default(self):
        # デフォルト値が1であることの確認
        response = self.app.get('/fib')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['result'], 1)

    def test_fib_positive_integer(self):
        # 10番目のフィボナッチ数は55であることの確認
        response = self.app.get('/fib?n=10')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['result'], 55)

    def test_fib_zero(self):
        # 0番目のフィボナッチ数は1であることの確認
        response = self.app.get('/fib?n=0')
        self.assertEqual(response.json['status'], 400)
        self.assertEqual(response.json['message'], "n must be a positive integer.")

    def test_fib_negative_integer(self):
        # 負の整数が入力された場合のエラーメッセージの確認
        response = self.app.get('/fib?n=-5')
        self.assertEqual(response.json['status'], 400)
        self.assertEqual(response.json['message'], "n must be a positive integer.")

    def test_fib_non_integer(self):
        # 整数以外が入力された場合のエラーメッセージの確認
        response = self.app.get('/fib?n=abc')
        self.assertEqual(response.json['status'], 400)
        self.assertEqual(response.json['message'], "n must be an integer.")

if __name__ == '__main__':
    unittest.main()
