// Golf Scorecard Analyzer - Proxy Server (Google Cloud Vision OCR + Gemini JSON Structuring)
// - Uses Google Cloud Vision to OCR the scorecard image
// - Uses Gemini (text model) to convert OCR text into the JSON structure your front-end expects
//
// Required env (recommended via .env):
//   GEMINI_API_KEY=...
//   GOOGLE_APPLICATION_CREDENTIALS=C:\\path\\to\\service-account.json
//     OR
//   GOOGLE_CLOUD_SERVICE_ACCOUNT_JSON={...service account json...}   (raw JSON string)
//
// Optional:
//   PORT=3000

require('dotenv').config();

const express = require('express');
const cors = require('cors');

const { GoogleGenerativeAI } = require('@google/generative-ai');
const vision = require('@google-cloud/vision');

const app = express();
const PORT = process.env.PORT || 3000;

// ===== CONFIG =====
const GEMINI_MODEL = process.env.GEMINI_TEXT_MODEL || 'gemini-2.0-flash';

// Middleware
app.use(cors());
app.use(express.json({ limit: '20mb' }));

// Gemini init (text-only usage)
const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY || '');

// Vision client init helper
function createVisionClient() {
  // 1) Preferred: GOOGLE_APPLICATION_CREDENTIALS points to a JSON file
  if (process.env.GOOGLE_APPLICATION_CREDENTIALS) {
    return new vision.ImageAnnotatorClient();
  }

  // 2) Alternative: service account JSON stored in env as raw JSON string
  if (process.env.GOOGLE_CLOUD_SERVICE_ACCOUNT_JSON) {
    let raw = process.env.GOOGLE_CLOUD_SERVICE_ACCOUNT_JSON.trim();

    // If someone accidentally wrapped it in quotes, try to recover.
    if ((raw.startsWith('"') && raw.endsWith('"')) || (raw.startsWith("'") && raw.endsWith("'"))) {
      raw = raw.slice(1, -1);
    }

    const creds = JSON.parse(raw);
    const projectId = creds.project_id;

    return new vision.ImageAnnotatorClient({
      credentials: {
        client_email: creds.client_email,
        private_key: creds.private_key,
      },
      projectId,
    });
  }

  return null;
}

function isGeminiConfigured() {
  return !!(process.env.GEMINI_API_KEY && process.env.GEMINI_API_KEY.trim().length > 0);
}

function isVisionConfigured() {
  return !!(process.env.GOOGLE_APPLICATION_CREDENTIALS || process.env.GOOGLE_CLOUD_SERVICE_ACCOUNT_JSON);
}

// Health check endpoint
app.get('/', (req, res) => {
  res.json({
    status: 'ok',
    message: 'Golf Scorecard Analyzer Server (GCV OCR + Gemini)',
    version: '2.0.0',
    gemini_model: GEMINI_MODEL,
    GEMINI_API_KEY: isGeminiConfigured() ? 'Configured' : 'NOT CONFIGURED',
    VISION: isVisionConfigured() ? 'Configured' : 'NOT CONFIGURED',
  });
});

// Scorecard analysis endpoint
app.post('/api/scorecard', async (req, res) => {
  try {
    const { base64Data, mimeType } = req.body;

    if (!base64Data) {
      return res.status(400).json({ error: 'No image data provided' });
    }
    if (!isVisionConfigured()) {
      return res.status(500).json({
        error: 'Google Cloud Vision not configured',
        hint: 'Set GOOGLE_APPLICATION_CREDENTIALS to a service-account JSON file path, or set GOOGLE_CLOUD_SERVICE_ACCOUNT_JSON.',
      });
    }
    if (!isGeminiConfigured()) {
      return res.status(500).json({
        error: 'GEMINI_API_KEY not configured',
        hint: 'Set GEMINI_API_KEY in your .env or environment variables.',
      });
    }

    const client = createVisionClient();
    if (!client) {
      return res.status(500).json({
        error: 'Failed to initialize Vision client',
      });
    }

    // Decode base64 to bytes buffer
    const imgBuffer = Buffer.from(base64Data, 'base64');

    // OCR with Vision: documentTextDetection is better for dense text/structured docs
    const [result] = await client.documentTextDetection({
      image: { content: imgBuffer },
    });

    const ocrText =
      (result.fullTextAnnotation && result.fullTextAnnotation.text) ||
      (result.textAnnotations && result.textAnnotations[0] && result.textAnnotations[0].description) ||
      '';

    if (!ocrText || ocrText.trim().length < 10) {
      return res.status(500).json({
        error: 'OCR returned insufficient text',
        debug: { mimeType: mimeType || 'image/jpeg' },
      });
    }

    // Ask Gemini to convert OCR text to the JSON structure your front-end expects
    const prompt = `You are given OCR text extracted from a golf scorecard. Extract course information and return ONLY valid JSON with this exact schema:

{
  "name": "Course Name",
  "location": "City/Location",
  "holes": 18,
  "par": [18 numbers],
  "distances_blue": [18 numbers],
  "distances_white": [18 numbers],
  "stroke_index": [18 numbers from 1 to 18]
}

Rules:
- Return ONLY JSON (no markdown, no backticks, no commentary).
- par values must be 3, 4, or 5.
- Distances must be numeric. If they look like yards, convert to meters (1 yard = 0.9144 m).
- stroke_index should be 1-18; if missing, infer the most likely indices or output a reasonable placeholder [1..18].
- If only one distance set exists, set it to distances_white and leave distances_blue as an empty array (or copy if clearly the same tee set).
- Ensure arrays are length 18.

OCR TEXT:
${ocrText}`;

    const model = genAI.getGenerativeModel({ model: GEMINI_MODEL });

    const genResult = await model.generateContent([prompt]);
    const response = await genResult.response;
    const text = response.text();

    // Parse JSON
    let courseData;
    try {
      const cleanText = text.replace(/```json\s*/g, '').replace(/```/g, '').trim();
      courseData = JSON.parse(cleanText);
    } catch (parseError) {
      console.error('JSON parse error:', parseError);
      console.error('Raw Gemini response:', text);
      return res.status(500).json({
        error: 'Failed to parse Gemini response as JSON',
        rawResponse: text.substring(0, 1500),
      });
    }

    // Normalize keys
    const normalized = {
      name: courseData.name || 'Unknown Course',
      location: courseData.location || '',
      holes: courseData.holes || 18,
      par: Array.isArray(courseData.par) ? courseData.par : [],
      distances_blue: courseData.distances_blue || courseData.distancesBlue || [],
      distances_white: courseData.distances_white || courseData.distancesWhite || [],
      stroke_index: courseData.stroke_index || courseData.strokeIndex || [],
    };

    return res.json(normalized);
  } catch (error) {
    console.error('Scorecard analysis error:', error);
    return res.status(500).json({
      error: 'Failed to analyze scorecard',
      message: error.message,
    });
  }
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error('Server error:', err);
  res.status(500).json({ error: 'Internal server error' });
});

// Start server
app.listen(PORT, () => {
  console.log(`🏌️ Golf Scorecard Analyzer Server (GCV OCR + Gemini) running on port ${PORT}`);
  console.log(`Using Gemini model: ${GEMINI_MODEL}`);
  console.log(`GEMINI_API_KEY: ${isGeminiConfigured() ? 'Configured' : 'NOT CONFIGURED'}`);
  console.log(`VISION: ${isVisionConfigured() ? 'Configured' : 'NOT CONFIGURED'}`);
});
