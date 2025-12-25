import { useState } from "react";
import client from "../api/axiosClient";

export default function HybridSearch() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);

  const search = async () => {
    const res = await client.post("/hybrid/search", { query });
    setResults(res.data.results);
  };

  return (
    <div className="container">
      <div className="card">
        <h2>Hybrid Search</h2>

        <input placeholder="Search anything..." onChange={(e)=>setQuery(e.target.value)} />
        <button onClick={search}>Search</button>

        {results.map((r,i)=>(
          <div key={i} className="card">
            {r.text}
          </div>
        ))}
      </div>
    </div>
  );
}
