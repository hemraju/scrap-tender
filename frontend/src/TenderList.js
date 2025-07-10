import React, { useEffect, useState } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:8000';

export default function TenderList() {
  const [tenders, setTenders] = useState([]);
  const [category, setCategory] = useState('all');

  useEffect(() => {
    axios.get(`${API_URL}/tenders`).then(res => setTenders(res.data));
  }, []);

  const filtered = category === 'all' ? tenders : tenders.filter(t => t.category === category);
  const categories = Array.from(new Set(tenders.map(t => t.category)));

  return (
    <div>
      <h2>Tenders</h2>
      <label>Filter by category: </label>
      <select value={category} onChange={e => setCategory(e.target.value)}>
        <option value="all">All</option>
        {categories.map(cat => (
          <option key={cat} value={cat}>{cat}</option>
        ))}
      </select>
      <ul>
        {filtered.map(t => (
          <li key={t.id} style={{marginBottom: '1em'}}>
            <a href={t.url} target="_blank" rel="noopener noreferrer">{t.title}</a> [{t.category}]
            <br />{t.description.slice(0, 200)}...
            {t.document_path && (
              <div>
                <a href={`${API_URL}/files/${t.document_path}`} download>Download Document</a>
              </div>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}