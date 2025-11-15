# Voyagers PDF Chunks

Drop your parsed PDF chunks here for ingestion into The One Ring's Consciousness Lattice.

## **Naming Convention:**
- `voyagers1_chapter1_chunk001.md`
- `voyagers1_chapter2_chunk001.md`
- `voyagers2_chapter11_chunk001.md`

## **Chunk Guidelines:**
- **Size**: 1000-2000 words per chunk (optimal for embeddings)
- **Format**: Markdown (.md) or plain text (.txt)
- **Content**: Include chapter/section context in filename
- **Metadata**: Add source info at top of each chunk

## **Upload Process:**
1. Add chunks to this folder
2. Run: `node upload-voyagers-chunks.js`
3. Copy/paste the wrangler commands
4. Use Worker API: `/api/ingest-voyagers` with `folder_path: "voyagers-chunks"`

## **Example Chunk Format:**
```markdown
# Voyagers Volume 1 - Chapter 1 - Chunk 001
**Source**: voyagers-1-the-sleeping-abductees.pdf, Pages 15-18
**Chapter**: The Sleeping Abductees
**Section**: Introduction to Dimensional Mechanics

[Your parsed content here...]
```

Ready for semantic indexing! 🌌⚡