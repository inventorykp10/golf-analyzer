// Golf Scorecard Analyzer - Proxy Server (FIXED for new Gemini models)
// Updated model: gemini-2.0-flash

const express = require('express');
const cors = require('cors');
const { GoogleGenerativeAI } = require('@google/generative-ai');

const app = express();
const PORT = process.env.PORT || 3000;

// ===== CONFIG =====
const GEMINI_MODEL = 'gemini-2.0-flash'; // <-- 핵심 수정 포인트

// Middleware
app.use(cors());
app.use(express.json({ limit: '15mb' }));

// Initialize Gemini AI
const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);

// Health check endpoint
app.get('/', (req, res) => {
  res.json({ 
    status: 'ok', 
    message: 'Golf Scorecard Analyzer Server (Fixed)',
    version: '1.0.3',
    model: GEMINI_MODEL
  });
});

// Scorecard analysis endpoint
app.post('/api/scorecard', async (req, res) => {
  try {
    const { base64Data, mimeType } = req.body;

    if (!base64Data) {
      return res.status(400).json({ error: 'No image data provided' });
    }

    if (!process.env.GEMINI_API_KEY) {
      return res.status(500).json({ error: 'GEMINI_API_KEY not configured' });
    }

    const imageParts = [{
      inlineData: {
        data: base64Data,
        mimeType: mimeType || 'image/jpeg'
      }
    }];

    const prompt = `Analyze this golf scorecard image and extract the following information in JSON format:

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
- Return ONLY valid JSON (no markdown, no backticks, no commentary).
- Par must be 3, 4, or 5.
- Distances must be numeric.
- If distances look like yards, convert to meters (1 yard = 0.9144 m).
- If data is unclear, make reasonable estimates.`;

    const model = genAI.getGenerativeModel({ model: GEMINI_MODEL });

    const result = await model.generateContent([prompt, ...imageParts]);
    const response = await result.response;
    const text = response.text();

    // Clean and parse JSON
    let courseData;
    try {
      const cleanText = text
        .replace(/```json\n?/g, '')
        .replace(/```/g, '')
        .trim();

      courseData = JSON.parse(cleanText);
    } catch (parseError) {
      console.error('JSON parse error:', parseError);
      console.error('Raw response:', text);
      return res.status(500).json({ 
        error: 'Failed to parse AI response',
        rawResponse: text.substring(0, 1000)
      });
    }

    // Basic validation
    if (!courseData.par || !Array.isArray(courseData.par)) {
      return res.status(500).json({ error: 'Invalid course data structure (par missing)' });
    }

    // Normalize keys to match your front-end expectation
    const normalized = {
      name: courseData.name || 'Unknown Course',
      location: courseData.location || '',
      holes: courseData.holes || 18,
      par: courseData.par,
      distances_blue: courseData.distances_blue || courseData.distancesBlue || [],
      distances_white: courseData.distances_white || courseData.distancesWhite || [],
      stroke_index: courseData.stroke_index || courseData.strokeIndex || []
    };

    res.json(normalized);

  } catch (error) {
    console.error('Scorecard analysis error:', error);
    res.status(500).json({ 
      error: 'Failed to analyze scorecard',
      message: error.message 
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
  console.log(`🏌️ Golf Scorecard Analyzer Server running on port ${PORT}`);
  console.log(`Using model: ${GEMINI_MODEL}`);
  console.log(`GEMINI_API_KEY: ${process.env.GEMINI_API_KEY ? 'Configured' : 'NOT CONFIGURED'}`);
});
