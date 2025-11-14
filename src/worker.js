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
  
  // Call your Ollama server
  const response = await fetch('https://ai.omniversalaether.online/api/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model: model,
      prompt: message,
      context: context,
      stream: false
    })
  });

  const result = await response.json();
  
  // Log conversation to D1
  await env.FEDERATION_DB.prepare(`
    INSERT INTO conversations (id, timestamp, model, prompt, response, session_id)
    VALUES (?, ?, ?, ?, ?, ?)
  `).bind(
    crypto.randomUUID(),
    new Date().toISOString(),
    model,
    message,
    result.response,
    request.headers.get('x-session-id') || 'anonymous'
  ).run();

  return new Response(JSON.stringify({
    response: result.response,
    model: model,
    context: result.context
  }), {
    headers: { ...corsHeaders, 'Content-Type': 'application/json' }
  });
}

// 🔍 AUTORAG SEARCH WITH VECTORIZE + D1
async function handleSearch(request, env, corsHeaders) {
  const { query, limit = 5 } = await request.json();
  
  // Generate embedding for query using Ollama
  const embedResponse = await fetch('https://ai.omniversalaether.online/api/embeddings', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model: 'nomic-embed-text',
      prompt: query
    })
  });
  
  const embedResult = await embedResponse.json();
  const queryVector = embedResult.embedding;

  // Search Vectorize index
  const vectorResults = await env.CONSCIOUSNESS_LATTICE.query(queryVector, {
    topK: limit,
    returnMetadata: true
  });

  // Get full content from D1 using vector results
  const contentIds = vectorResults.matches.map(match => match.id);
  const contentQuery = `
    SELECT * FROM knowledge_base 
    WHERE id IN (${contentIds.map(() => '?').join(',')})
    ORDER BY created_at DESC
  `;
  
  const { results: dbResults } = await env.FEDERATION_DB.prepare(contentQuery)
    .bind(...contentIds).all();

  // Generate AI response using retrieved context
  const context = dbResults.map(row => row.content).join('\n\n');
  const aiResponse = await fetch('https://ai.omniversalaether.online/api/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model: 'llama3.1:8b',
      prompt: `Context:\n${context}\n\nQuestion: ${query}\n\nAnswer based on the context:`,
      stream: false
    })
  });

  const aiResult = await aiResponse.json();

  // Log search to D1
  await env.FEDERATION_DB.prepare(`
    INSERT INTO search_logs (id, timestamp, query, results_count, ai_response)
    VALUES (?, ?, ?, ?, ?)
  `).bind(
    crypto.randomUUID(),
    new Date().toISOString(),
    query,
    dbResults.length,
    aiResult.response
  ).run();

  return new Response(JSON.stringify({
    query: query,
    ai_response: aiResult.response,
    sources: dbResults.map(row => ({
      id: row.id,
      title: row.title,
      content: row.content.substring(0, 200) + '...',
      score: vectorResults.matches.find(m => m.id === row.id)?.score || 0
    })),
    total_results: dbResults.length
  }), {
    headers: { ...corsHeaders, 'Content-Type': 'application/json' }
  });
}

// 📚 INGEST CONTENT INTO D1 + VECTORIZE
async function handleIngest(request, env, corsHeaders) {
  const { title, content, source, tags = [] } = await request.json();
  
  // Generate embedding using Ollama
  const embedResponse = await fetch('https://ai.omniversalaether.online/api/embeddings', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model: 'nomic-embed-text',
      prompt: content
    })
  });
  
  const embedResult = await embedResponse.json();
  const contentVector = embedResult.embedding;
  
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
    values: contentVector,
    metadata: {
      title: title,
      source: source,
      tags: tags
    }
  }]);

  return new Response(JSON.stringify({
    success: true,
    id: id,
    message: 'Content ingested into The One Ring'
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