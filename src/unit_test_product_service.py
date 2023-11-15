import unittest
from product import app
from flask import request

class ProductManagementTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_product_list(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Title', response.data)
        # Add more assertions as needed to validate the product list page

    def test_manage_product_add(self):
        # Test adding a product
        response = self.app.post('/manage_product/0', data={'title': 'New Product - 8', 'author': 'Author 8', 'price': 35}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'New Product - 8', response.data)
        # Add more assertions to validate the addition of the product

    def test_manage_product_edit(self):
        # Assuming you have an existing product with ID 2
        response = self.app.post('/manage_product/2', data={'title': 'Updated Product', 'author': 'Author 2', 'price': 20.09}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'20.09', response.data)
        # Add more assertions to validate the product update

    def test_manage_product_edit_non_existing(self):
        # Test editing a product that does not exist (ID 999)
        response = self.app.post('/edit_product/999', data={'title': 'Updated Product', 'author': 'Author 2', 'price': 29.99}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'999', response.data)
        # Add more assertions to validate the non-existing product update

    def test_delete_product(self):
        # Assuming you have an existing product with ID 7
        response = self.app.get('/delete_product/7', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'New Product 7', response.data)
        # Add more assertions to validate the product deletion

if __name__ == '__main__':
    unittest.main()
