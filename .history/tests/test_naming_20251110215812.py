"""Tests for filename generation and sanitization."""
import unittest
from pathlib import Path
from app.naming import FilenameGenerator


class TestFilenameGenerator(unittest.TestCase):
    """Test filename generation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.generator = FilenameGenerator(
            template="{artist} - {title}",
            unsafe_chars="/\\?*:\"<>|"
        )
        self.output_dir = Path("/tmp/test_output")
        self.output_dir.mkdir(exist_ok=True)
    
    def test_sanitize_unsafe_chars(self):
        """Test that unsafe characters are removed."""
        result = self.generator.sanitize("Artist/Name: Title?")
        self.assertNotIn("/", result)
        self.assertNotIn(":", result)
        self.assertNotIn("?", result)
    
    def test_generate_from_tags(self):
        """Test filename generation from tags."""
        tags = {"artist": "Test Artist", "title": "Test Title"}
        original = Path("/tmp/test.flac")
        output = self.generator.generate(tags, original, self.output_dir)
        
        self.assertEqual(output.name, "Test Artist - Test Title.aiff")
        self.assertTrue(output.name.endswith(".aiff"))
    
    def test_fallback_to_filename(self):
        """Test fallback to original filename when tags missing."""
        tags = {}  # No tags
        original = Path("/tmp/my_song.flac")
        output = self.generator.generate(tags, original, self.output_dir)
        
        # Should use original filename stem
        self.assertIn("my_song", output.name)
    
    def test_collision_handling(self):
        """Test collision handling with (2), (3), etc."""
        tags = {"artist": "Artist", "title": "Title"}
        original = Path("/tmp/test.flac")
        
        # Create first file
        first = self.generator.generate(tags, original, self.output_dir, overwrite=False)
        first.touch()
        
        # Generate again - should get (2)
        second = self.generator.generate(tags, original, self.output_dir, overwrite=False)
        self.assertIn("(2)", second.name)


if __name__ == "__main__":
    unittest.main()

