#!/usr/bin/env python3
"""
tutorial_poc.py - HTTP API Testing Script for OmniParse
This script demonstrates how to test the OmniParse FastAPI endpoints
using HTTP requests.

Endpoints:
- /parse_document - Parse documents (PDF, PPT, DOC, PPTX, DOCX)
- /parse_image - Parse/process images (JPEG, PNG, BMP, TIFF, HEIC)
- /parse_media - Parse audio/video files
- /parse_website - Parse web pages

Usage:
    python tutorial_poc.py --host localhost --port 8000 --test all
"""

import argparse
import base64
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, Optional

import requests


class OmniParseAPIClient:
    """Client for testing OmniParse API endpoints."""

    def __init__(self, host: str = "localhost", port: int = 8000):
        self.base_url = f"http://{host}:{port}"
        self.host = host
        self.port = port

    def test_health(self) -> Dict[str, Any]:
        """Test the root endpoint to verify server is running."""
        try:
            response = requests.get(f"{self.base_url}/", timeout=5)
            return {
                "success": True,
                "status_code": response.status_code,
                "data": response.json() if response.text else {"message": "Server is running"},
            }
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}

    def parse_document(self, file_path: str) -> Dict[str, Any]:
        """Parse a document file (PDF, PPT, DOC, PPTX, DOCX).

        Args:
            file_path: Path to the document file

        Returns:
            Response from the API containing parsed text and metadata
        """
        if not os.path.exists(file_path):
            return {"success": False, "error": f"File not found: {file_path}"}

        try:
            with open(file_path, "rb") as f:
                files = {"file": (os.path.basename(file_path), f, "application/pdf")}
                response = requests.post(
                    f"{self.base_url}/parse_document",
                    files=files,
                    timeout=300,
                )
                return {
                    "success": True,
                    "status_code": response.status_code,
                    "data": response.json(),
                }
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}

    def parse_document_pdf(self, file_path: str) -> Dict[str, Any]:
        """Parse a PDF document specifically."""
        return self._parse_file_endpoint("/parse_document/pdf", file_path)

    def parse_document_ppt(self, file_path: str) -> Dict[str, Any]:
        """Parse a PPT document specifically."""
        return self._parse_file_endpoint("/parse_document/ppt", file_path)

    def parse_document_docs(self, file_path: str) -> Dict[str, Any]:
        """Parse a DOC document specifically."""
        return self._parse_file_endpoint("/parse_document/docs", file_path)

    def _parse_file_endpoint(self, endpoint: str, file_path: str) -> Dict[str, Any]:
        """Helper to parse files via specific endpoints."""
        if not os.path.exists(file_path):
            return {"success": False, "error": f"File not found: {file_path}"}

        try:
            with open(file_path, "rb") as f:
                files = {"file": (os.path.basename(file_path), f)}
                response = requests.post(
                    f"{self.base_url}{endpoint}",
                    files=files,
                    timeout=300,
                )
                return {
                    "success": True,
                    "status_code": response.status_code,
                    "data": response.json(),
                }
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}

    def parse_image(self, file_path: str) -> Dict[str, Any]:
        """Parse an image file (JPEG, PNG, BMP, TIFF, HEIC).

        Args:
            file_path: Path to the image file

        Returns:
            Response from the API containing parsed text and metadata
        """
        if not os.path.exists(file_path):
            return {"success": False, "error": f"File not found: {file_path}"}

        try:
            with open(file_path, "rb") as f:
                files = {"file": (os.path.basename(file_path), f)}
                response = requests.post(
                    f"{self.base_url}/parse_image/image",
                    files=files,
                    timeout=300,
                )
                return {
                    "success": True,
                    "status_code": response.status_code,
                    "data": response.json(),
                }
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}

    def process_image(
        self, file_path: str, task: str = "Caption"
    ) -> Dict[str, Any]:
        """Process an image with a specific task.

        Args:
            file_path: Path to the image file
            task: The processing task (Caption, Detailed Caption, OCR, etc.)

        Returns:
            Response from the API containing processed results
        """
        if not os.path.exists(file_path):
            return {"success": False, "error": f"File not found: {file_path}"}

        try:
            with open(file_path, "rb") as f:
                files = {"image": (os.path.basename(file_path), f)}
                data = {"task": task}
                response = requests.post(
                    f"{self.base_url}/parse_image/process_image",
                    files=files,
                    data=data,
                    timeout=300,
                )
                return {
                    "success": True,
                    "status_code": response.status_code,
                    "data": response.json(),
                }
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}

    def parse_media_audio(self, file_path: str) -> Dict[str, Any]:
        """Parse an audio file (MP3, WAV, AAC).

        Args:
            file_path: Path to the audio file

        Returns:
            Response from the API containing transcribed text
        """
        if not os.path.exists(file_path):
            return {"success": False, "error": f"File not found: {file_path}"}

        try:
            with open(file_path, "rb") as f:
                files = {"file": (os.path.basename(file_path), f)}
                response = requests.post(
                    f"{self.base_url}/parse_media/audio",
                    files=files,
                    timeout=600,
                )
                return {
                    "success": True,
                    "status_code": response.status_code,
                    "data": response.json(),
                }
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}

    def parse_media_video(self, file_path: str) -> Dict[str, Any]:
        """Parse a video file (MP4, MKV, AVI, MOV).

        Args:
            file_path: Path to the video file

        Returns:
            Response from the API containing transcribed text
        """
        if not os.path.exists(file_path):
            return {"success": False, "error": f"File not found: {file_path}"}

        try:
            with open(file_path, "rb") as f:
                files = {"file": (os.path.basename(file_path), f)}
                response = requests.post(
                    f"{self.base_url}/parse_media/video",
                    files=files,
                    timeout=600,
                )
                return {
                    "success": True,
                    "status_code": response.status_code,
                    "data": response.json(),
                }
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}

    def parse_website(self, url: str) -> Dict[str, Any]:
        """Parse a web page.

        Args:
            url: The URL of the web page to parse

        Returns:
            Response from the API containing parsed content
        """
        try:
            response = requests.post(
                f"{self.base_url}/parse_website/parse",
                params={"url": url},
                headers={"accept": "application/json"},
                timeout=60,
            )
            return {
                "success": True,
                "status_code": response.status_code,
                "data": response.json(),
            }
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}

    def print_response(self, response: Dict[str, Any], max_text_length: int = 500):
        """Pretty print an API response."""
        if not response.get("success"):
            print(f"[ERROR] {response.get('error', 'Unknown error')}")
            return

        print(f"[INFO] Status: {response.get('status_code', 'N/A')}")
        data = response.get("data", {})

        # Print text (truncated if long)
        text = data.get("text", "")
        if text:
            print(f"\n[TEXT] (length: {len(text)})")
            print("-" * 50)
            print(text[:max_text_length] + "..." if len(text) > max_text_length else text)
            print("-" * 50)

        # Print metadata if present
        if "metadata" in data:
            print(f"\n[METADATA]")
            print(json.dumps(data["metadata"], indent=2))

        # Print images info if present
        if "images" in data:
            print(f"\n[IMAGES] ({len(data['images'])} images)")
            for i, img in enumerate(data["images"]):
                print(f"  Image {i+1}: {img.get('filename', 'N/A')} - size: {len(img.get('image', ''))} chars")

        # Print full JSON if requested
        print(f"\n[FULL JSON]")
        print(json.dumps(data, indent=2))


def create_sample_files(output_dir: str) -> Dict[str, str]:
    """Create sample files for testing (if they don't exist)."""
    os.makedirs(output_dir, exist_ok=True)
    sample_files = {}

    # Create a sample text file (to convert to PDF for testing)
    sample_text = """
    Sample Document for OmniParse Testing
    ======================================

    This is a sample document created to test the OmniParse API.
    It contains multiple sections to demonstrate the parsing capabilities.

    Section 1: Introduction
    ------------------------
    OmniParse is a powerful document parsing platform that supports
    multiple file formats including PDF, PPT, DOC, and more.

    Section 2: Features
    ------------------
    - Multi-format document support
    - OCR for scanned documents
    - Table extraction
    - Image extraction and captioning
    - Semantic chunking

    Section 3: Conclusion
    --------------------
    This is the end of the sample document. Thank you for testing OmniParse!
    """
    text_file = os.path.join(output_dir, "sample_document.txt")
    with open(text_file, "w") as f:
        f.write(sample_text)
    sample_files["txt"] = text_file

    return sample_files


def run_tests(client: OmniParseAPIClient, test_type: str = "all") -> Dict[str, bool]:
    """Run API tests based on the specified type.

    Args:
        client: OmniParseAPIClient instance
        test_type: Type of tests to run ("all", "health", "document", "image", "media", "website")

    Returns:
        Dictionary of test results
    """
    results = {}

    print("=" * 60)
    print("OmniParse API Test Suite")
    print("=" * 60)
    print(f"Base URL: {client.base_url}")
    print(f"Test Type: {test_type}")
    print("=" * 60)

    # Test 1: Health check (always run)
    print("\n[TEST 1] Health Check")
    result = client.test_health()
    results["health"] = result.get("success", False)
    client.print_response(result)
    time.sleep(1)

    if test_type in ("all", "health"):
        return results

    # Test 2: Document parsing
    if test_type in ("all", "document"):
        print("\n[TEST 2] Document Parsing")
        # Create sample document
        sample_files = create_sample_files("/tmp/omniparse_test")
        if "txt" in sample_files:
            # Note: For actual testing, you should provide real PDF/DOC files
            print("[INFO] Creating sample document...")
            print(f"[INFO] Sample file created at: {sample_files['txt']}")
            print("[INFO] Note: For real testing, convert this to PDF/DOC format")

            # Example: Parse document from file
            # result = client.parse_document("/path/to/real/document.pdf")
            # results["parse_document"] = result.get("success", False)
            # client.print_response(result)
        results["parse_document"] = False  # Placeholder
        time.sleep(1)

    # Test 3: Image parsing
    if test_type in ("all", "image"):
        print("\n[TEST 3] Image Parsing")
        print("[INFO] Image parsing tests require actual image files")
        print("[INFO] Example command: client.parse_image('/path/to/image.jpg')")
        results["parse_image"] = False  # Placeholder
        time.sleep(1)

    # Test 4: Media parsing
    if test_type in ("all", "media"):
        print("\n[TEST 4] Media Parsing")
        print("[INFO] Media parsing tests require actual audio/video files")
        print("[INFO] Example command: client.parse_media_audio('/path/to/audio.mp3')")
        results["parse_media"] = False  # Placeholder
        time.sleep(1)

    # Test 5: Website parsing
    if test_type in ("all", "website"):
        print("\n[TEST 5] Website Parsing")
        # Example: Parse a website
        # result = client.parse_website("https://example.com")
        # results["parse_website"] = result.get("success", False)
        # client.print_response(result)

        # Test with a real URL (commented out for safety)
        test_url = "https://example.com"
        print(f"[INFO] Testing with URL: {test_url}")
        result = client.parse_website(test_url)
        results["parse_website"] = result.get("success", False)
        client.print_response(result)

    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    for test_name, passed in results.items():
        status = "[PASS]" if passed else "[FAIL]"
        print(f"  {status} {test_name}")
    print("=" * 60)

    return results


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="OmniParse API Testing Script"
    )
    parser.add_argument(
        "--host",
        default="localhost",
        help="API host (default: localhost)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="API port (default: 8000)",
    )
    parser.add_argument(
        "--test",
        choices=["all", "health", "document", "image", "media", "website"],
        default="all",
        help="Type of tests to run (default: all)",
    )
    parser.add_argument(
        "--file",
        help="Path to file for document/image parsing",
    )
    parser.add_argument(
        "--url",
        help="URL for website parsing",
    )
    parser.add_argument(
        "--task",
        default="Caption",
        help="Task for image processing (default: Caption)",
    )
    parser.add_argument(
        "--output",
        choices=["summary", "json"],
        default="summary",
        help="Output format (default: summary)",
    )

    args = parser.parse_args()

    # Create client
    client = OmniParseAPIClient(host=args.host, port=args.port)

    # If file or URL provided, run specific test
    if args.file:
        # Determine file type by extension
        ext = os.path.splitext(args.file)[1].lower()
        if ext in (".pdf", ".ppt", ".doc", ".pptx", ".docx"):
            result = client.parse_document(args.file)
        elif ext in (".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff"):
            result = client.process_image(args.file, args.task)
        elif ext in (".mp3", ".wav", ".aac"):
            result = client.parse_media_audio(args.file)
        elif ext in (".mp4", ".mkv", ".avi", ".mov"):
            result = client.parse_media_video(args.file)
        else:
            print(f"Unsupported file type: {ext}")
            sys.exit(1)

        if args.output == "json":
            print(json.dumps(result, indent=2))
        else:
            client.print_response(result)

    elif args.url:
        result = client.parse_website(args.url)
        if args.output == "json":
            print(json.dumps(result, indent=2))
        else:
            client.print_response(result)

    else:
        # Run full test suite
        results = run_tests(client, args.test)

        if args.output == "json":
            print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
