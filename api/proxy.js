// Vercel Serverless Function: CORS Proxy for Live API Testing
export default async function handler(req, res) {
  // Allow all origins, methods, and headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS, PATCH');
  res.setHeader('Access-Control-Allow-Headers', '*');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  const targetUrl = req.query.url;
  if (!targetUrl) {
    return res.status(400).json({ error: 'Missing target url parameter in query (?url=...)' });
  }

  try {
    const headers = {};
    if (req.headers['content-type']) {
      headers['Content-Type'] = req.headers['content-type'];
    } else {
      headers['Content-Type'] = 'application/json';
    }
    headers['Accept'] = 'application/json';

    if (req.headers['authorization']) {
      headers['Authorization'] = req.headers['authorization'];
    }
    if (req.headers['x-frappe-csrf-token']) {
      headers['X-Frappe-CSRF-Token'] = req.headers['x-frappe-csrf-token'];
    }
    if (req.headers['cookie']) {
      headers['Cookie'] = req.headers['cookie'];
    }

    const fetchOptions = {
      method: req.method,
      headers: headers
    };

    if (req.method !== 'GET' && req.method !== 'HEAD') {
      if (req.body) {
        fetchOptions.body = typeof req.body === 'string' ? req.body : JSON.stringify(req.body);
      }
    }

    const upstreamResponse = await fetch(targetUrl, fetchOptions);
    const responseText = await upstreamResponse.text();

    res.status(upstreamResponse.status);
    const contentType = upstreamResponse.headers.get('content-type');
    if (contentType) {
      res.setHeader('Content-Type', contentType);
    } else {
      res.setHeader('Content-Type', 'application/json');
    }

    return res.send(responseText);
  } catch (error) {
    return res.status(502).json({
      error: 'Proxy execution failed',
      details: error.message
    });
  }
}

