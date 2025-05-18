import os
import shutil
import tempfile
import logging
from pathlib import Path
from src.main import apply_rules, ensure_dir

# Setup basic logger to silence output during tests
logging.basicConfig(level=logging.CRITICAL)

def test_apply_move_rule():
    # Setup temporary folder structure
    with tempfile.TemporaryDirectory() as temp_dir:
        downloads_dir = Path(temp_dir) / "Downloads"
        target_dir = Path(temp_dir) / "Documents/PDFs"
        downloads_dir.mkdir(parents=True)
        
        # Create dummy file to be moved
        dummy_file = downloads_dir / "example.pdf"
        dummy_file.write_text("Test PDF content")

        # Define rule to move PDF
        rules = [{
            "match": {
                "extension": ".pdf"
            },
            "action": "move",
            "destination": str(target_dir)
        }]

        apply_rules(str(dummy_file), rules)

        # Assert file moved correctly
        expected_path = target_dir / "example.pdf"
        assert expected_path.exists()
        assert not dummy_file.exists()

def test_apply_delete_rule():
    with tempfile.TemporaryDirectory() as temp_dir:
        test_dir = Path(temp_dir)
        test_file = test_dir / "temp.zip"
        test_file.write_text("ZIP content")

        rules = [{
            "match": {
                "extension": ".zip"
            },
            "action": "delete"
        }]

        apply_rules(str(test_file), rules)
        assert not test_file.exists()
