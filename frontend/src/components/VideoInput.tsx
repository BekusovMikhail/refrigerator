import { useState, useRef } from 'react';
import { Button } from "@chakra-ui/react";

const VideoInput = () => {
    const inputRef = useRef<any>();

    const [source, setSource] = useState<string>();
    const [file, setFile] = useState<File>()

    const handleFileChange = (event: any) => {
        const file = event.target.files[0];
        const url = URL.createObjectURL(file);
        setSource(url);
        setFile(file)
    };

    const handleChoose = () => {
        inputRef.current.click();
    };

    const submitFile = () => {

    }
    
    return(
        <div className="box-2">
            <h1>Video upload</h1>
            <div className="VideoInput">
                <input
                    ref={inputRef}
                    className="VideoInput_input"
                    type="file"
                    onChange={handleFileChange}
                    accept=".mov,.mp4"
                />
                {!source && <button onClick={handleChoose}>Choose</button>}
                {source && (
                    <video
                    className="VideoInput_video"
                    width={1150}
                    controls
                    src={source}
                    />
                )}
                {/* <div className="VideoInput_footer">{source || "Nothing selectd"}</div> */}
                <Button onClick={submitFile}>Загрузить</Button>
            </div>
        </div>
    )
}

export default VideoInput;