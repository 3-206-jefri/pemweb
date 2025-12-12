import { useState, useEffect } from "react";
import axios from "axios";

function App() {
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [reviews, setReviews] = useState([]);

  async function fetchReviews() {
    try {
      const res = await axios.get("/api/reviews");
      setReviews(res.data.reviews || []);
    } catch (err) {
      console.error(err);
    }
  }

  useEffect(() => {
    fetchReviews();
  }, []);

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const res = await axios.post("/api/analyze-review", { text });
      setResult(res.data.result);
      setText("");
      fetchReviews();
    } catch (err) {
      setError(err.response?.data || "Something went wrong");
    }

    setLoading(false);
  }

  return (
    <div style={{ padding: 20, maxWidth: 700, margin: "0 auto" }}>
      <h1>Product Review Analyzer</h1>

      <form onSubmit={handleSubmit}>
        <textarea
          rows={5}
          style={{ width: "100%", marginBottom: 10 }}
          placeholder="Masukkan product review..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />

        <button disabled={loading || !text.trim()}>
          {loading ? "Analyzing..." : "Analyze"}
        </button>
      </form>

      {error && (
        <pre style={{ color: "red", marginTop: 10 }}>
          {JSON.stringify(error, null, 2)}
        </pre>
      )}

      {result && (
        <div style={{ marginTop: 20 }}>
          <h2>Hasil Analisis</h2>
          <p><b>Sentiment:</b> {result.sentiment}</p>

          <p><b>Key Points:</b></p>
          <ul>
            {(result.key_points || []).map((p, i) => (
              <li key={i}>{p}</li>
            ))}
          </ul>
        </div>
      )}

      <h2 style={{ marginTop: 40 }}>Riwayat Analisis</h2>
      <ul>
        {reviews.map((r) => (
          <li key={r.id} style={{ marginBottom: 15 }}>
            <div><small>{new Date(r.created_at).toLocaleString()}</small></div>
            <div><b>Review:</b> {r.text}</div>
            <div><b>Sentiment:</b> {r.sentiment}</div>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
