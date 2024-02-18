import React, { useState } from 'react';
import './index.css';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleAnalysis = async () => {
    if (selectedFile) {
      const formData = new FormData();
      formData.append('image', selectedFile);

      try {
        const response = await fetch('http://127.0.0.1:5000/analyze', {
          method: 'POST',
          body: formData,
        });

        if (response.ok) {
          const result = await response.json();
          setAnalysisResult(result);
        } else {
          console.error('Error analyzing urine:', response.statusText);
        }
      } catch (error) {
        console.error('Error analyzing urine:', error.message);
      }
    }
  };

  return (
    <div className="App">
      <h1>Urine Analysis App</h1>
      <input type="file" accept="image/*" onChange={handleFileChange} />
      <button onClick={handleAnalysis}>Analyze</button>

      {analysisResult && (
        <div>
          <h2>Analysis Result</h2>
          <p>Status: {analysisResult.status}</p>
          <p>Predominant Color (RGB): {analysisResult.predominant_color_rgb.join(', ')}</p>
          <p>Brightened Color (HSV): {analysisResult.brightened_color_hsv.join(', ')}</p>
        </div>
      )}
    </div>
  );
}

export default App;
