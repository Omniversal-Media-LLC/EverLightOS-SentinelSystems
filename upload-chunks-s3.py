#!/usr/bin/env python3
"""
🌌 Voyagers Chunks Upload Script
Upload parsed PDF chunks directly to R2 bucket using S3 API
"""

import os
import boto3
from pathlib import Path

# R2 Credentials from voyagers_bucket.ipynb
R2_ACCOUNT_TOKEN = "al8MwwLFOO6DrwbO9EHMQcCDnL8NCOzkXrdh-9C0"
ACCESS_KEY_ID = "4e9c907256870519705b21852e420159"
SECRET_ACCESS_KEY = "50cf0118fb03a9e3f3df4c4a14843f25bc4df56e279af38df2f8fb1261e60d77"
R2_ENDPOINT = "https://2fb52a67d12e6d214c516ace666abd61.r2.cloudflarestorage.com"
BUCKET_NAME = "one-bucket-everlightos"

def upload_voyagers_chunks():
    """Upload all chunks from Energetic-Synthesis/voyagers-chunks/ to R2"""
    
    chunks_dir = Path("./Energetic-Synthesis/voyagers-chunks")
    
    if not chunks_dir.exists():
        print("❌ voyagers-chunks directory not found")
        return
    
    # Find all markdown and text files
    chunk_files = list(chunks_dir.glob("*.md")) + list(chunks_dir.glob("*.txt"))
    
    if not chunk_files:
        print("📝 No chunk files found in voyagers-chunks/")
        print("💡 Add your parsed PDF chunks as .md or .txt files")
        return
    
    print(f"🚀 Found {len(chunk_files)} chunk files to upload")
    
    # Initialize S3 client for R2
    s3_client = boto3.client(
        's3',
        endpoint_url=R2_ENDPOINT,
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=SECRET_ACCESS_KEY,
        region_name='auto'
    )
    
    uploaded = 0
    failed = 0
    
    for chunk_file in chunk_files:
        try:
            # Upload to voyagers-chunks/ prefix in bucket
            key = f"voyagers-chunks/{chunk_file.name}"
            
            print(f"📤 Uploading {chunk_file.name}...")
            
            s3_client.upload_file(
                str(chunk_file),
                BUCKET_NAME,
                key,
                ExtraArgs={'ContentType': 'text/markdown' if chunk_file.suffix == '.md' else 'text/plain'}
            )
            
            uploaded += 1
            print(f"✅ {chunk_file.name} uploaded successfully")
            
        except Exception as e:
            failed += 1
            print(f"❌ Failed to upload {chunk_file.name}: {e}")
    
    print(f"\n🎉 Upload complete: {uploaded} successful, {failed} failed")
    
    if uploaded > 0:
        print(f"\n🧠 Next step - Ingest into Consciousness Lattice:")
        print(f'curl -X POST "https://everlight-federation-api.47loginslater.workers.dev/api/ingest-voyagers" \\')
        print(f'  -H "Content-Type: application/json" \\')
        print(f'  -d \'{{"folder_path": "voyagers-chunks", "max_files": {uploaded}}}\'')

if __name__ == "__main__":
    upload_voyagers_chunks()