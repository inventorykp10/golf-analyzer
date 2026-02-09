// Golf Scorecard Analyzer - Proxy Server
// This server receives scorecard images and uses Google Gemini AI to extract course information

const express = require('express');
const cors = require('cors');
const { GoogleGenerativeAI } = require('@google/generative-ai');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json({ limit: '10mb' }));

// Initialize Gemini AI
const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);

// Health check endpoint
app.get('/', (req, res) => {
  res.json({ 
    status: 'ok', 
    message: 'Golf Scorecard Analyzer Server',
    version: '1.0.0'
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

    // Prepare the image for Gemini
    const imageParts = [{
      inlineData: {
        data: base64Data,
        mimeType: mimeType || 'image/jpeg'
      }
    }];

    // Prompt for extracting scorecard information
    const prompt = `Analyze this golf scorecard image and extract the following information in JSON format:

{
  "name": "Course Name",
  "location": "City/Location",
  "holes": 18,
  "par": [4, 4, 3, 5, 4, 3, 4, 5, 4, 4, 3, 4, 5, 4, 4, 3, 5, 4],
  "distances_blue": [array of 18 distances in meters or yards],
  "distances_white": [array of 18 distances in meters or yards],
  "stroke_index": [array of 18 handicap stroke indices]
}

Important:
- Extract ALL 18 holes (front 9 + back 9)
- Par values should be 3, 4, or 5
- Distances should be numbers (convert yards to meters if needed: 1 yard = 0.9144 meters)
- Stroke index (also called handicap or index) is typically 1-18, indicating hole difficulty
- If you see "Blue", "Championship", or longer distances, use those for distances_blue
- If you see "White", "Regular", or shorter distances, use those for distances_white
- Return ONLY valid JSON, no markdown formatting, no backticks
- If any data is unclear, make reasonable estimates based on typical golf course layouts`;

    // Call Gemini API
    const model = genAI.getGenerativeModel({ model: 'gemini-1.5-flash' });
    const result = await model.generateContent([prompt, ...imageParts]);
    const response = await result.response;
    const text = response.text();

    // Parse the JSON response
    let courseData;
    try {
      // Remove markdown code blocks if present
      const cleanText = text.replace(/```json\n?/g, '').replace(/```\n?/g, '').trim();
      courseData = JSON.parse(cleanText);
    } catch (parseError) {
      console.error('JSON parse error:', parseError);
      console.error('Raw response:', text);
      return res.status(500).json({ 
        error: 'Failed to parse AI response',
        rawResponse: text.substring(0, 500)
      });
    }

    // Validate the response
    if (!courseData.par || !Array.isArray(courseData.par)) {
      return res.status(500).json({ error: 'Invalid course data structure' });
    }

    // Return the extracted data
    res.json(courseData);

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
  console.log(`✅ GEMINI_API_KEY: ${process.env.GEMINI_API_KEY ? 'Configured' : 'NOT CONFIGURED'}`);
});
