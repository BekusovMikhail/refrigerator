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
        headers: {
          'Content-Type': 'application/json',
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
    const [modalIsOpen, setModalIsOpen] = useState(false);

    useEffect(() => {
        if (data && data.length){
            setCameraId(data[0][0])
        }
    }, [data])

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