import React, { useState, useEffect } from 'react';

export default function ServiceTracker() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Vite catches '/api' and routes it to http://localhost:5000/api/services
    fetch('/api/services')
      .then((res) => {
        if (!res.ok) throw new Error('Network response was not ok');
        return res.json();
      })
      .then((payload) => {
        setData(payload);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Fetch error: ", err);
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Loading data...</p>;

  return (
    <div>
      {data.map((item) => (
        <p key={item.id}>{item.name}</p>
      ))}
    </div>
  );
}