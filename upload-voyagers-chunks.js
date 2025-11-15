#!/usr/bin/env node
// 🌌 Voyagers Chunks Upload Script
// Uploads parsed PDF chunks to R2 bucket for ingestion

const fs = require('fs');
const path = require('path');

async function uploadChunks() {
  const chunksDir = './Energetic-Synthesis/voyagers-chunks';
  
  if (!fs.existsSync(chunksDir)) {
    console.log('❌ voyagers-chunks directory not found');
    console.log('📁 Create: Energetic-Synthesis/voyagers-chunks/');
    return;
  }

  const files = fs.readdirSync(chunksDir).filter(f => f.endsWith('.md') || f.endsWith('.txt'));
  
  if (files.length === 0) {
    console.log('📝 No chunk files found. Add your parsed PDF chunks to:');
    console.log('   Energetic-Synthesis/voyagers-chunks/');
    console.log('');
    console.log('💡 Suggested naming:');
    console.log('   voyagers1_chapter1_chunk001.md');
    console.log('   voyagers1_chapter1_chunk002.md');
    console.log('   voyagers2_chapter11_chunk001.md');
    return;
  }

  console.log(`🚀 Found ${files.length} chunk files to upload`);
  console.log('');
  
  // Generate wrangler commands
  console.log('📋 Run these commands to upload:');
  console.log('');
  
  files.forEach(file => {
    const localPath = path.join(chunksDir, file).replace(/\\/g, '/');
    const remotePath = `voyagers-chunks/${file}`;
    console.log(`wrangler r2 object put one-bucket-everlightos/${remotePath} --file="${localPath}"`);
  });
  
  console.log('');
  console.log('🔧 Or run the batch upload:');
  console.log('node upload-voyagers-chunks.js --upload');
}

// Check if --upload flag is provided
if (process.argv.includes('--upload')) {
  console.log('🚀 Batch upload not implemented yet - use individual wrangler commands above');
} else {
  uploadChunks();
}