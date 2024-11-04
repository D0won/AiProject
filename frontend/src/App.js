import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [videoFeedUrl] = useState('http://192.168.0.196:8000/video_feed'); // FastAPI 서버의 주소
  const [videoSrc, setVideoSrc] = useState('');

  useEffect(() => {
    // 이미지 태그의 src 속성을 비디오 스트리밍 URL로 설정
    setVideoSrc(videoFeedUrl);
  }, [videoFeedUrl]);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Video Stream</h1>
        <img id="video" src={videoSrc} alt="Video Stream" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
