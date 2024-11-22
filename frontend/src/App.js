import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Handle sending the query to the FastAPI backend
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const res = await axios.post('http://127.0.0.1:8000/api/v1/query/', {
        query_text: query
      });

      setResponse(res.data.response); // Set the chatbot's response
    } catch (err) {
      setError('Error fetching data from the server.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <h1>RAG Chatbot</h1>
      <form onSubmit={handleSubmit}>
        <textarea
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask the chatbot a question..."
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Loading...' : 'Submit'}
        </button>
      </form>

      {response && (
        <div className="response">
          <h2>Response:</h2>
          <p>{response}</p>
        </div>
      )}

      {error && <div className="error">{error}</div>}
    </div>
  );
}

export default App;
