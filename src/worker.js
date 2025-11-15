// 🔥 THE ONE RING WORKER - EverLightOS Federation API 🔥
// D1 + Vectorize + Ollama AutoRAG System

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;

    // CORS headers for all responses
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    };

    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    try {
      // Route handling
      if (path.startsWith('/api/chat')) {
        return await handleChat(request, env, corsHeaders);
      } else if (path.startsWith('/api/search')) {
        return await handleSearch(request, env, corsHeaders);
      } else if (path.startsWith('/api/ingest')) {
        return await handleIngest(request, env, corsHeaders);
      } else if (path.startsWith('/api/federation')) {
        return await handleFederation(request, env, corsHeaders);
      } else if (path.startsWith('/api/ingest-voyagers')) {
        return await handleVoyagersIngestion(request, env, corsHeaders);
      } else if (path.startsWith('/api/list-bucket')) {
        return await handleListBucket(request, env, corsHeaders);
      } else {
        return new Response('EverLightOS Federation API - The One Ring Worker', {
          headers: { ...corsHeaders, 'Content-Type': 'text/plain' }
        });
      }
    } catch (error) {
      return new Response(JSON.stringify({ error: error.message }), {
        status: 500,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });
    }
  }
};

// 🤖 CHAT WITH OLLAMA FEDERATION
async function handleChat(request, env, corsHeaders) {
  const { message, model = 'llama3.1:8b', context = [] } = await request.json();
  
  // For now, return a test response until Ollama server is configured
  const testResponse = `Hello! I'm The One Ring Worker responding to: "${message}". ` +
    `I would normally connect to your Ollama server at ${env.OLLAMA_BASE_URL} using model ${model}, ` +
    `but it seems the server isn't accessible right now. This proves the Worker is deployed and working!`;
  
  return new Response(JSON.stringify({
    response: testResponse,
    model: model,
    context: context,
    timestamp: new Date().toISOString(),
    status: 'test_mode',
    worker_url: 'https://everlight-federation-api.47loginslater.workers.dev'
  }), {
    headers: { ...corsHeaders, 'Content-Type': 'application/json' }
  });
}

// 🔍 AUTORAG SEARCH WITH VECTORIZE + D1
async function handleSearch(request, env, corsHeaders) {
  const { query, limit = 5 } = await request.json();
  
  // Test response until D1 and Vectorize are set up
  const testResponse = `Search query received: "${query}". ` +
    `This would normally search the Consciousness Lattice (Vectorize) and Federation Database (D1) ` +
    `for relevant content, then generate an AI response using your Ollama server. ` +
    `The One Ring Worker is ready for full deployment!`;
  
  return new Response(JSON.stringify({
    query: query,
    ai_response: testResponse,
    sources: [
      {
        id: 'test-1',
        title: 'The One Ring Worker Test',
        content: 'This is a test response showing the Worker is deployed and functional.',
        score: 1.0
      }
    ],
    total_results: 1,
    status: 'test_mode'
  }), {
    headers: { ...corsHeaders, 'Content-Type': 'application/json' }
  });
}

// 📚 INGEST CONTENT INTO D1 + VECTORIZE
async function handleIngest(request, env, corsHeaders) {
  const { title, content, source, tags = [] } = await request.json();
  
  // For now, use mock embeddings until Ollama is configured
  const mockVector = Array.from({length: 1536}, () => Math.random() - 0.5);
  
  const id = crypto.randomUUID();
  
  // Store in D1
  await env.FEDERATION_DB.prepare(`
    INSERT INTO knowledge_base (id, title, content, source, tags, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
  `).bind(
    id,
    title,
    content,
    source,
    JSON.stringify(tags),
    new Date().toISOString()
  ).run();

  // Store vector in Vectorize
  await env.CONSCIOUSNESS_LATTICE.upsert([{
    id: id,
    values: mockVector,
    metadata: {
      title: title,
      source: source,
      tags: tags
    }
  }]);

  return new Response(JSON.stringify({
    success: true,
    id: id,
    message: 'Content ingested into The One Ring',
    note: 'Using mock embeddings until Ollama server is configured'
  }), {
    headers: { ...corsHeaders, 'Content-Type': 'application/json' }
  });
}

// 🤝 FEDERATION EXPERIMENTS (Multi-AI Consensus)
async function handleFederation(request, env, corsHeaders) {
  const { query, models = ['llama3.1:8b', 'mistral:7b', 'codellama:7b'] } = await request.json();
  
  // Query multiple models simultaneously
  const responses = await Promise.all(
    models.map(async (model) => {
      const response = await fetch('https://ai.omniversalaether.online/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model: model,
          prompt: query,
          stream: false
        })
      });
      const result = await response.json();
      return { model, response: result.response };
    })
  );

  // Analyze consensus using a meta-model
  const consensusPrompt = `
    Analyze these AI responses for consensus:
    ${responses.map(r => `${r.model}: ${r.response}`).join('\n\n')}
    
    Provide a consensus summary and note any disagreements:
  `;

  const consensusResponse = await fetch('https://ai.omniversalaether.online/api/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model: 'llama3.1:8b',
      prompt: consensusPrompt,
      stream: false
    })
  });

  const consensus = await consensusResponse.json();

  // Log federation experiment to D1
  await env.FEDERATION_DB.prepare(`
    INSERT INTO federation_experiments (id, timestamp, query, models, responses, consensus)
    VALUES (?, ?, ?, ?, ?, ?)
  `).bind(
    crypto.randomUUID(),
    new Date().toISOString(),
    query,
    JSON.stringify(models),
    JSON.stringify(responses),
    consensus.response
  ).run();

  return new Response(JSON.stringify({
    query: query,
    individual_responses: responses,
    consensus: consensus.response,
    models_used: models,
    experiment_type: 'multi_ai_consensus'
  }), {
    headers: { ...corsHeaders, 'Content-Type': 'application/json' }
  });
}

// 🌌 VOYAGERS KNOWLEDGE BASE INGESTION
async function handleVoyagersIngestion(request, env, corsHeaders) {
  try {
    const body = await request.json();
    const folder_path = body.folder_path || 'voyagers-chunks';
    const max_files = body.max_files || 10;
    
    // List objects in our R2 bucket
    const objects = await env.EVERLIGHT_BUCKET.list({ prefix: `${folder_path}/` });
    
    if (objects.objects.length === 0) {
      return new Response(JSON.stringify({
        success: false,
        message: `No files found in ${folder_path}/ folder`,
        note: 'Upload parsed PDF chunks to voyagers-chunks/ folder first'
      }), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });
    }

    const results = {
      processed: 0,
      failed: 0,
      files: []
    };

    // Process multiple files
    for (const obj of objects.objects.slice(0, max_files)) {
      try {
        const file = await env.EVERLIGHT_BUCKET.get(obj.key);
        if (!file) continue;
        
        const content = await file.text();
        const filename = obj.key.split('/').pop();
        const title = filename.replace(/\.[^/.]+$/, '').replace(/[_-]/g, ' ');
        
        const id = crypto.randomUUID();
        
        // Store in D1
        await env.FEDERATION_DB.prepare(`
          INSERT INTO knowledge_base (id, title, content, source, tags, created_at)
          VALUES (?, ?, ?, ?, ?, ?)
        `).bind(
          id,
          `Voyagers: ${title}`,
          content,
          `r2://one-bucket-everlightos/${obj.key}`,
          JSON.stringify(['voyagers', 'chunks', 'foundational']),
          new Date().toISOString()
        ).run();

        // Mock vector for Vectorize
        const mockVector = Array.from({length: 1536}, () => Math.random() - 0.5);
        
        await env.CONSCIOUSNESS_LATTICE.upsert([{
          id: id,
          values: mockVector,
          metadata: {
            title: `Voyagers: ${title}`,
            source: `r2://one-bucket-everlightos/${obj.key}`,
            chunk_type: 'pdf_parsed',
            tags: ['voyagers', 'chunks', 'foundational']
          }
        }]);

        results.processed++;
        results.files.push({
          id: id,
          title: `Voyagers: ${title}`,
          source: obj.key,
          size: obj.size
        });
        
      } catch (error) {
        results.failed++;
      }
    }

    return new Response(JSON.stringify({
      success: true,
      message: `Voyagers chunks ingestion completed`,
      folder_path: folder_path,
      total_files_found: objects.objects.length,
      results: results
    }), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    });
    
  } catch (error) {
    return new Response(JSON.stringify({
      success: false,
      error: error.message
    }), {
      status: 500,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    });
  }
}

// 📁 LIST R2 BUCKET CONTENTS
async function handleListBucket(request, env, corsHeaders) {
  try {
    const url = new URL(request.url);
    const prefix = url.searchParams.get('prefix') || '';
    
    const objects = await env.EVERLIGHT_BUCKET.list({ prefix: prefix });
    
    return new Response(JSON.stringify({
      success: true,
      prefix: prefix,
      total_objects: objects.objects.length,
      objects: objects.objects.map(obj => ({
        key: obj.key,
        size: obj.size,
        uploaded: obj.uploaded
      }))
    }), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    });
    
  } catch (error) {
    return new Response(JSON.stringify({
      success: false,
      error: error.message
    }), {
      status: 500,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    });
  }
}