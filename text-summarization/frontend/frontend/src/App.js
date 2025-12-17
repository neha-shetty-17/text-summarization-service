import React, { useState, useEffect } from "react";
import { summarize, fetchHistory } from "./api";

function App() {
  const [text, setText] = useState("");
  const [summary, setSummary] = useState("");
  const [loading, setLoading] = useState(false);
  const [maxLen, setMaxLen] = useState(60);
  const [minLen, setMinLen] = useState(10);
  const [history, setHistory] = useState([]);
  const [latency, setLatency] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    loadHistory();
  }, []);

  async function loadHistory() {
    try {
      const hist = await fetchHistory(20);
      setHistory(hist);
    } catch (e) {
      console.error(e);
    }
  }

  async function handleSummarize(e) {
    e.preventDefault();
    setError("");
    if (!text.trim()) {
      setError("Please enter text to summarize.");
      return;
    }
    setLoading(true);
    setSummary("");
    const t0 = performance.now();
    try {
      const resp = await summarize(text, { max_length: maxLen, min_length: minLen });
      const t1 = performance.now();
      setLatency(((t1 - t0) / 1000).toFixed(3));
      setSummary(resp.summary);
      // update history
      loadHistory();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="container">
      <h1>Text Summarization Service</h1>

      <form onSubmit={handleSummarize}>
        <label>Paste text to summarize</label>
        <textarea value={text} onChange={(e) => setText(e.target.value)} rows={10} />

        <div className="controls">
          <label>Max length:
            <input type="number" value={maxLen} onChange={(e) => setMaxLen(Number(e.target.value))} />
          </label>
          <label>Min length:
            <input type="number" value={minLen} onChange={(e) => setMinLen(Number(e.target.value))} />
          </label>
          <button type="submit" disabled={loading}>
            {loading ? "Summarizing..." : "Summarize"}
          </button>
        </div>
      </form>

      {error && <div className="error">{error}</div>}

      <section className="result">
        <h2>Summary</h2>
        {latency && <div className="meta">Latency: {latency}s</div>}
        <textarea readOnly value={summary} rows={6} />
      </section>

      <section className="history">
        <h2>History (recent)</h2>
        <button onClick={loadHistory}>Refresh</button>
        <ul>
          {history.map((h) => (
            <li key={h.id}>
              <div><strong>{h.timestamp}</strong> — len: {h.input_length}, time: {h.execution_time.toFixed(3)}s</div>
              <div className="summaryPreview">{h.summary}</div>
            </li>
          ))}
          {history.length === 0 && <li>No history yet.</li>}
        </ul>
      </section>
    </div>
  );
}

export default App;
