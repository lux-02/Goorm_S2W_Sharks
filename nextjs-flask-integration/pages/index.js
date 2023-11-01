import { useState } from 'react';
import styles from '@/styles/Home.module.css';
import wellKnownPorts from '@/pages/wellKnownPorts';

export default function Home() {
  const [ip, setIp] = useState('');
  const [results, setResults] = useState([]);
  const [detail, setDetail] = useState(null);

  const handleScan = async () => {
    try {
      const response = await fetch('http://localhost:5001/scan', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          target_ip: ip,
        }),
      });
      const data = await response.json();
      setResults(data.results);
    } catch (error) {
      console.error('Failed to fetch:', error);
    }
  };

  function showDetail(port, banner) {
    setDetail({ port, banner });
  }

  return (
    <div className={`${styles.wrap}`}>
      <h1 className={`${styles.title}`}>SHARKS SCANNER</h1>
      <div className={`${styles.inputWrap}`}>
        <input
          type="text"
          value={ip}
          onChange={(e) => setIp(e.target.value)}
          placeholder="Enter IP"
        />
        <button onClick={handleScan}>START</button>
      </div>
      <div className={styles.results}>
        {results.map((result, index) => (
          <div key={index} className={styles["result-item"]} onClick={() => showDetail(result[0], result[1])}>
            <strong>{result[0]}: </strong>
            <span>{parseBanner(result[0], result[1])}</span>
          </div>
        ))}
      </div>
      {
        detail && (
          <div className={styles.detail}>
            <div className={styles.detailBox}>
              <h3>Port: {detail.port}</h3>
              <p>{detail.banner}</p>
            </div>
          </div>
        )
      }
    </div >
  );
}

function parseBanner(port, banner) {
  if (wellKnownPorts[port]) {
    return wellKnownPorts[port];
  }
  return banner;
}
