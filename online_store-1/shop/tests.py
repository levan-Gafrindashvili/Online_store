from django.test import TestCase
from .models import YourModel  # Replace with your actual model

class YourModelTestCase(TestCase):
    def setUp(self):
        # Set up any initial data for your tests here
        YourModel.objects.create(name="Test Name", description="Test Description")

    def test_model_creation(self):
        """Test that the model was created successfully."""
        obj = YourModel.objects.get(name="Test Name")
        self.assertEqual(obj.description, "Test Description")

    def test_model_str(self):
        """Test the string representation of the model."""
        obj = YourModel.objects.get(name="Test Name")
        self.assertEqual(str(obj), "Expected String Representation")  # Replace with expected output

# Add more test cases as needed for your application functionality