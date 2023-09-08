import {
    useQuery
  } from '@tanstack/react-query'
import Modal from 'react-modal';
import { useState, useEffect } from 'react';
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
    HStack,
    Button
} from "@chakra-ui/react";
import { CheckIcon, CloseIcon, EditIcon, AddIcon, DeleteIcon } from '@chakra-ui/icons'
import CreateCounter from './CreateCounter';
import Product from './Product';

const getCounters = async (camera_id: number) => {
    const response = await fetch(`http://localhost:8000/api/counters_by_camera/${camera_id}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
    })
    return response.json()
}

function useCounters(camera_id: number) {
    return useQuery({
        queryKey: ['counters'],
        queryFn: () => getCounters(camera_id),
    })
}


function EditableControls() {
    const {
      isEditing,
      getSubmitButtonProps,
      getCancelButtonProps,
      getEditButtonProps,
    } = useEditableControls()

    return isEditing ? (
      <ButtonGroup justifyContent='center' size='sm'>
        <IconButton aria-label='Check' icon={<CheckIcon />} {...getSubmitButtonProps()} />
        <IconButton aria-label='Close' icon={<CloseIcon />} {...getCancelButtonProps()}/>
      </ButtonGroup>
    ) : (
      <Flex ml={1}>
        <IconButton aria-label='Edit' size='sm' icon={<EditIcon {...getEditButtonProps()} />} />
      </Flex>
    )
}

const Counters = ({camera_id}: {camera_id: number}) => {
    const { status, data, isFetching } = useCounters(camera_id)
    const [modalIsOpen, setModalIsOpen] = useState(false);
    const [count, setCount] = useState(0)

    const openModal = () => {
        setModalIsOpen(true);
    };
    
    const closeModal = () => {
        setModalIsOpen(false);
    };

    const deleteProduct = (counter_id: number) => () => {
        fetch("http://localhost:8000/api/delete_counter/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({"counter_id": counter_id})
        })
    }

    const handleChange = (counter_id: number) => (e: any) => {
        setCount(e.target.value)
        fetch("http://localhost:8000/api/put_counter/", {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({"counter_id": counter_id, "count": count})
        })
        console.log(count)
    }

    return(
        <div>
            <Modal isOpen={modalIsOpen} onRequestClose={closeModal} className='modal'>
                <CreateCounter closeModal={closeModal} cameraId={camera_id}/>
            </Modal>
            {status === 'loading' ? (
                'Loading...'
                ) : status === 'error' ? (
                <span>Error</span>
                ) : (
                    <List spacing={3}>
                        {data?.map((counter: string, i: number) => (
                            <ListItem key={counter[0]}>
                                <HStack>
                                    <Text>{counter[2]}</Text>
                                    {/* <Product id={Number(counter[3])}/> */}
                                    <Editable
                                        textAlign='center'
                                        defaultValue={String(counter[1])}
                                        isPreviewFocusable={false}
                                        >
                                            <Flex flexDirection="row" justifyContent='center' ml={1}>
                                                <EditablePreview />
                                                <Input as={EditableInput} onChange={handleChange(Number(counter[0]))} />
                                                <EditableControls />
                                            </Flex>
                                    </Editable>
                                    <IconButton aria-label='Delete' size='sm' m={1} icon={<DeleteIcon/>} onClick={deleteProduct(Number(counter[0]))}/>
                                </HStack>
                            </ListItem>
                        ))}
                        <ListItem key={0}>
                            <Button onClick={openModal}>Добавить</Button>
                        </ListItem>
                    </List>
                )}
        </div>
    )
}

export default Counters;