import React from 'react';

function LiveStream() {
    return (
        <div>
            <h1>Live Video Stream</h1>
            {/* <img> 태그의 src 속성에 Flask에서 제공하는 스트림 URL을 설정 */}
            <img
                src="http://192.168.0.196:8000/"
                alt="Live Stream"
                style={{ width: '50%', height: 'auto' }}
            />
        </div>
    );
}

export default LiveStream;
