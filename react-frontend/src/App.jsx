import React, { useState } from "react";
import "./index.css";
import logo from "../src/CroppedLogo.png";
import placehold from "../src/placeholder.jpg";
import steth from "../src/Steth.png";
import manimg from "../src/Man.png";

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
      <div id="landing-page">
        <div className="row">
          <nav>
            <div className="nav__content">
              <figure className="nav__img--wrapper">
                <img src={logo} alt="" className="nav__img" />
              </figure>
              <h1 className="nav__header">WHIZZARD</h1>
            </div>
          </nav>

          <div className="fullwidth">
            <div className="top">
              <input
                className="inputField"
                type="file"
                accept="image/*"
                onChange={handleFileChange}
              />
              <div id="imageContainer">
                <img src={placehold} alt="" id="uploadedImage" />
              </div>
              <button className="btn" onClick={handleAnalysis}>
                <img className="btn__img" src={steth} alt="" />
                <p className="btn__text">Generate Analysis</p>
                <img className="btn__img" src={manimg} alt="" />
              </button>
            </div>
            <div className="bottom">
              {analysisResult && (
                <>
                  <div className="border-around">
                    <h2 className="result__header">Analysis Results:</h2>
                    {analysisResult.status &&
                      analysisResult.status.split("|").map((part, index) => (
                        <React.Fragment key={index}>
                          {index > 0 && <br />}{" "}
                          {/* Add <br> after the first part */}
                          <p className="result__text">{part}</p>
                        </React.Fragment>
                      ))}
                  </div>
                  <button className="btn">
                    <a
                      href="https://4yk7hw-5173.csb.app/"
                      className="btn__text"
                      target="_blank"
                      rel="noreferrer"
                    >
                      Get AI Help
                    </a>
                  </button>
                </>
              )}
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default App;
