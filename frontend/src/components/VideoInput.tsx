import { useState, useRef } from 'react';
import { Button, HStack, Select, Text } from "@chakra-ui/react";
import axios from "axios";

const VideoInput = ({cameraId}: {cameraId: number}) => {
    const inputRef = useRef<any>();

    const [source, setSource] = useState<string>();
    const [name, setName] = useState<string>();
    const [file, setFile] = useState<File>();
    const [handDirection, setHandDirection] = useState('Hor')
    const [fridgeSide, setFridgeSide] = useState('Right')

    const handleFileChange = (event: any) => {
        const file = event.target.files[0];
        setName(file.name)
        const url = URL.createObjectURL(file);
        setSource(url);
        setFile(file)
    };

    const handleChoose = () => {
        inputRef.current.click();
    };

    const submitFile = () => {
        //const name = file ? file.name : ''
        //console.log(file)
        const formData = new FormData();
        if(file){
            formData.append("upload_file", file)
        }
        if(name){
            formData.append("name", name)
        }
        formData.append("camera", String(cameraId))
        formData.append("hand_direction", handDirection)
        formData.append("fridge_side", fridgeSide)
        axios.post("http://localhost:8001/api/upload_video/", formData, {headers: {"content-type": "multipart/form-data"}})
    }

    const selectHandDirection = (e: any) => {
        setHandDirection(e.target.value)
    }

    const selectFridgeSide = (e: any) => {
        setFridgeSide(e.target.value)
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
                <Button m={3} onClick={handleChoose}>Choose</Button>
                {/* {source && (
                    <video
                    className="VideoInput_video"
                    width={1000}
                    controls
                    src={source}
                    />
                )} */}
                <div className="VideoInput_footer">{name || "Nothing selected"}</div>
                <HStack m={3} spacing={3}>
                    <Text>Сторона холодильника:</Text>
                    <Select onChange={selectFridgeSide} defaultValue="Right">
                        <option value='Left'>Левая</option>
                        <option value='Right'>Правая</option>
                    </Select>
                    <Text>Направление руки: </Text>
                    <Select onChange={selectHandDirection} defaultValue="Hor">
                        <option value='Vert'>Вертикальное</option>
                        <option value='Hor'>Горизонтальное</option>
                    </Select>
                    <Button w={250} onClick={submitFile}>Загрузить</Button>
                </HStack>
            </div>
        </div>
    )
}

export default VideoInput;