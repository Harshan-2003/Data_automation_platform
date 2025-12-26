import { useState } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");

  const handleUpload = async () => {
    if (!file) {
      setMessage("Select a file first");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        setMessage(data.detail || "Upload failed");
      } else {
        setMessage("Upload successful: " + data.filename);
      }
    } catch (err) {
      setMessage("Backend not reachable");
    }
  };

  return (
    <div style={{ padding: "40px" }}>
      <h2>Upload File</h2>
      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
      />
      <br /><br />
      <button onClick={handleUpload}>Upload</button>
      <p>{message}</p>
    </div>
  );
}

export default App;
