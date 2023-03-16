import React, { useState } from "react";
import config from "./config";

const ImageUpload = () => {
  const [prediction, setPrediction] = useState("");
  const [uploadedImage, setUploadedImage] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();
    const fileInput = event.target.elements.file;
    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    try {
      const response = await fetch(`${config.API_BASE_URL}/predict`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        setPrediction("Prediction: " + data.product);
        setUploadedImage(data.user_image);
      } else {
        alert("Error occurred while predicting the image: " + data.error);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Error occurred while uploading the image.");
    }
  };

  return (
    <div>
      <h1>Dress ME Up</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" name="file" id="file" required />
        <button type="submit">Predict</button>
      </form>
      <h2>{prediction}</h2>
      {uploadedImage && <img src={uploadedImage} alt="Uploaded" />}
    </div>
  );
};

export default ImageUpload;
