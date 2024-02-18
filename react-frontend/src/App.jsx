import React, { useState } from "react";
import "./index.css";
import logo from "../src/CroppedLogo.png"




function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);




  const handleFileChange = (event) => {
    const file = event.target.files[0];
  setSelectedFile(file);


  // Load image
  const reader = new FileReader();


  reader.onload = function (e) {
    const uploadedImage = document.getElementById("uploadedImage");
    if (uploadedImage) {
      console.log("Image loaded successfully:", e.target.result);
      uploadedImage.src = e.target.result;
    } else {
      console.error("Error: uploadedImage element not found");
    }
  };


  reader.readAsDataURL(file);
 };


  const handleAnalysis = async () => {
    if (selectedFile) {
      const formData = new FormData();
      formData.append("image", selectedFile);


      try {
        const response = await fetch("http://127.0.0.1:5000/analyze", {
          method: "POST",
          body: formData,
        });


        if (response.ok) {
          const result = await response.json();
          setAnalysisResult(result);
        } else {
          console.error("Error analyzing urine:", response.statusText);
        }
      } catch (error) {
        console.error("Error analyzing urine:", error.message);
      }
    }
  };


  return (
    <>
      <nav>
        <figure className="nav__img--wrapper">
          <img src={logo} alt="" className="nav__img" />
        </figure>
        <h1 className="nav__header">Whizzard</h1>
      </nav>


      <div id="landing-page">
        <div className="fullwidth">
          <div className="left">
            <h2 className="left__header2">Whizzard Analysis</h2>
            <input
              className="inputField"
              type="file"
              accept="image/*"
              onChange={handleFileChange}
            />
            <div id="imageContainer">
              <img src="" alt="" id="uploadedImage" />
            </div>
            <button className="btn" onClick={handleAnalysis}>
              Analyze
            </button>
          </div>
          {analysisResult && (
            <div className="right lp__right--results">
              <div className="border-around">
                <h2>Analysis Results:</h2>
                <p>{analysisResult.status}</p>
              </div>
            </div>
          )}
        </div>


      </div>
    </>
  );
}


export default App;




