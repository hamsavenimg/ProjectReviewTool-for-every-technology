import { useState } from "react";
import axios from "axios";

const AddProject = () => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  // const handleUpload = async () => {
  //   if (!file) {
  //     setMessage("Please select a .zip file first!");
  //     return;
  //   }

    const formData = new FormData();
    formData.append("file", file);

    // try {
    //   const response = await axios.post("http://localhost:8000/upload", formData, {
    //     headers: { "Content-Type": "multipart/form-data" },
    //   });

    //   setMessage(response.data.message);
    // } catch (error) {
    //   setMessage("Error uploading file.");
    // }


  return (
    <div>
      <h2>Upload Your Project (.zip)</h2>
      <input type="file" accept=".zip" onChange={handleFileChange} />
      <button>Upload</button>
      {message && <p>{message}</p>}
    </div>
  );
};

export default AddProject;
