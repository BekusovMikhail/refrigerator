import { 
    Stack, 
    Select, 
    List,
    Editable,
    EditableInput,
    EditableTextarea,
    EditablePreview,
    Input,
    ListItem, 
    ButtonGroup,
    Flex,
    useEditableControls,
    IconButton,
    Text,
    HStack
} from "@chakra-ui/react";
import { CheckIcon, CloseIcon, EditIcon, AddIcon, DeleteIcon } from '@chakra-ui/icons'
import { useState, useEffect } from 'react';
import Modal from 'react-modal';
import {
    useQuery
  } from '@tanstack/react-query'
import axios from 'axios'
import CreateCamera from "./CreateCamera";
import Counters from "./Counters";

const getCameras = async () => {
    const response = await fetch("http://localhost:8000/api/cameras_by_username/LuckyHorseshoe", {
        method: 'GET',
        //mode: 'cors',
        headers: {
          'Content-Type': 'application/json',
        //   "Access-Control-Allow-Origin": "*",
        //   "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept, Authorization",
        //   "Access-Control-Allow-Methods": "GET, HEAD, OPTIONS, POST, PUT"
        }
    })
    return response.json()
}

function useCameras() {
    return useQuery({
        queryKey: ['cameras'],
        queryFn: () => getCameras(),
    })
}

const ProductList = () => {
    const { status, data, isFetching } = useCameras()
    //const data = [{"name": "Белый холодильник", "id": 1}, {"name": "Чёрный холодильник", "id": 2}]
    // const counters_dict = [
    //     {"camera": 1, "counters": ["Молоко: 3", "Сыр: 2", "Колбаса: 1"], "counter_id": [1, 2, 3]}, 
    //     {"camera": 2, "counters": ["Яйцо: 10", "Помидор: 4"], "counter_id": [4, 5]}
    // ]
    //const [counters, setCounters] = useState<string[]>(["Молоко: 3", "Сыр: 2", "Колбаса: 1"])
    //const [counter_ids, setCounterIds] = useState<number[]>([1, 2, 3])
    //const status: string = "success"
    const [modalIsOpen, setModalIsOpen] = useState(false);
    const [cameraId, setCameraId] = useState<number>(0)

    // useEffect(() => {
    //     fetch("http://localhost:8001/api/cameras_by_username/LuckyHorseshoe", {
    //         method: 'GET',
    //         headers: {
    //         'Content-Type': 'application/json',
    //         "Access-Control-Allow-Origin": "*",
    //         "Access-Control-Allow-Headers": "*",
    //         //   "Access-Control-Allow-Methods": "GET, HEAD, OPTIONS, POST, PUT"
    //             }
    //     })
    //     .then((res) => res.json())
    //     .then((data) => {
    //         console.log(data);
    //      })
    //     .catch((err) => {
    //         console.log(err.message);
    //     });
    // }, [])

    // useEffect(() => {
    //     for (let i = 0; i < counters_dict.length; i++){
    //         if(counters_dict[i]["camera"] == cameraId){
    //             setCounters(counters_dict[i]["counters"])
    //             setCounterIds(counters_dict[i]["counter_id"])
    //         }
    //     }
    // }, [cameraId])

    const selectCamera = (e: any) => {
        setCameraId(e.target.value)
    }
    const deleteCamera = () => {
        fetch("http://localhost:8001/api/delete_camera/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({"id": cameraId})
        })
    }
    const openModal = () => {
        setModalIsOpen(true);
    };
    
    const closeModal = () => {
        setModalIsOpen(false);
    };

    return (
        <div className="box-3">
            <Modal isOpen={modalIsOpen} onRequestClose={closeModal} className='modal'>
                <CreateCamera closeModal={closeModal}/>
            </Modal>
            <Stack
                flexDir="column"
                mb="2"
                justifyContent="center"
                alignItems="center"
            >
                <Flex>
                {status === 'loading' ? (
                    'Loading...'
                    ) : status === 'error' ? (
                    <span>Error</span>
                    ) : (
                        <Select onChange={selectCamera}>
                            {data?.map((row: any, i: number) => (
                                    <option key={i} value={row[0]}>
                                        {row[1]}
                                        {/* <IconButton aria-label='Delete' size='sm' m={1} icon={<DeleteIcon/>} onClick={deleteCamera}/> */}
                                    </option>
                                    )
                            )}
                        </Select>
                    )}
                    <IconButton aria-label='Add' size='sm' m={1} icon={<AddIcon/>} onClick={openModal}/>
                </Flex>
                <Counters camera_id={cameraId} />
            </Stack>         
        </div>
    )
}

export default ProductList