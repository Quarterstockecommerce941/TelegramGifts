import os
import time
import unittest
from TelegramGifts import TelegramGifts

class TestTelegramGiftsAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize the library once for all tests
        cls.gifts = TelegramGifts(ttl_seconds=60)
        
    def test_public_methods_exist(self):
        """Ensure core public methods are exposed"""
        methods = [m for m in dir(self.gifts) if not m.startswith('_')]
        self.assertIn("get_gift", methods)
        self.assertIn("get_model_details", methods)
        self.assertIn("get_attribute_price", methods)
        self.assertIn("download_image", methods)

    def test_get_gift_happy_path(self):
        """Test fetching a valid gift returns correct dictionary structure"""
        info = self.gifts.get_gift("Artisan Brick")
        self.assertIsNotNone(info)
        self.assertEqual(info['short_name'], 'artisan_brick')
        self.assertIn('prices', info)
        self.assertIn('custom_emoji_id', info)
        
    def test_get_model_details(self):
        """Test fetching specific model details returns enriched data"""
        model = self.gifts.get_model_details("artisan_brick", "Pro Gamer")
        self.assertIsNotNone(model)
        self.assertEqual(model['name'], 'pro_gamer')
        self.assertIn('price_ton', model)
        self.assertIn('links', model)
        
    def test_get_attribute_price(self):
        """Test fetching a specific attribute price returns a float"""
        price = self.gifts.get_attribute_price("artisan_brick", "backdrops", "Black")
        self.assertIsInstance(price, float)
        self.assertGreater(price, 0)
        
    def test_edge_cases(self):
        """Ensure invalid inputs return None safely without crashing"""
        self.assertIsNone(self.gifts.get_gift(""))
        self.assertIsNone(self.gifts.get_gift("FakeGift999"))
        self.assertIsNone(self.gifts.get_gift(None))
        
    def test_caching_performance(self):
        """Test that the cache prevents redundant network calls"""
        start_t = time.time()
        self.gifts.get_gift("Diamond Ring") # Fetch fresh data
        t1 = time.time() - start_t
        
        start_t = time.time()
        self.gifts.get_gift("Diamond Ring") # Fetch from cache
        t2 = time.time() - start_t
        
        # Memory fetch should be extremely fast (near 0 seconds)
        self.assertLess(t2, 0.05)
        
    def test_download_image(self):
        """Test that downloading assets writes valid non-empty files to disk"""
        dl_path = self.gifts.download_image("artisan_brick", "webp")
        self.assertTrue(os.path.exists(dl_path))
        self.assertGreater(os.path.getsize(dl_path), 0)

if __name__ == '__main__':
    unittest.main()
