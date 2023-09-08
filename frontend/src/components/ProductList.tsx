import { 
    Stack, 
    Select, 
    Flex,
    IconButton,
} from "@chakra-ui/react";
import { confirmAlert } from 'react-confirm-alert'
import { AddIcon } from '@chakra-ui/icons'
import { useState } from 'react';
import { useParams } from 'react-router-dom'
import Modal from 'react-modal';
import {
    useQuery
  } from '@tanstack/react-query'
import CreateCamera from "./CreateCamera";
import Counters from "./Counters";

const getCameras = async (username: string | undefined) => {
    if (!username){
        return []
    }
    const response = await fetch("http://localhost:8000/api/cameras_by_username/" + username, {
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

function useCameras(username: string | undefined) {
    return useQuery({
        queryKey: ['cameras'],
        queryFn: () => getCameras(username),
    })
}

const ProductList = ({cameraId, setCameraId}: {cameraId: number, setCameraId: any}) => {
    const { username } = useParams()
    const { status, data, isFetching } = useCameras(username)

    const submit = () => {

        confirmAlert({
          title: 'Удалить',
          message: 'Уверены, что хотите удалить точку наблюдения?',
          buttons: [
            {
              label: 'Да',
              onClick: () => deleteCamera()
            },
            {
              label: 'Нет',
            }
          ]
        });
      }
    //const data = [{"name": "Белый холодильник", "id": 1}, {"name": "Чёрный холодильник", "id": 2}]
    // const counters_dict = [
    //     {"camera": 1, "counters": ["Молоко: 3", "Сыр: 2", "Колбаса: 1"], "counter_id": [1, 2, 3]}, 
    //     {"camera": 2, "counters": ["Яйцо: 10", "Помидор: 4"], "counter_id": [4, 5]}
    // ]
    //const [counters, setCounters] = useState<string[]>(["Молоко: 3", "Сыр: 2", "Колбаса: 1"])
    //const [counter_ids, setCounterIds] = useState<number[]>([1, 2, 3])
    //const status: string = "success"
    const [modalIsOpen, setModalIsOpen] = useState(false);
    //const [cameraId, setCameraId] = useState<number>(0)

    useEffect(() => {
        if (data && data.length){
            setCameraId(data[0][0])
        }
    }, [data])
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
                    <IconButton aria-label='Delete' size='sm' m={1} icon={<DeleteIcon/>} onClick={deleteCamera}/>
                </Flex>
                <Counters camera_id={cameraId} />
            </Stack>         
        </div>
    )
}

export default ProductList