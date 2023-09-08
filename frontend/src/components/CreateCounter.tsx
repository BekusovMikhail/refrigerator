import { Flex, Stack, Input, Button, HStack, Text } from "@chakra-ui/react";
import { useState, useEffect } from 'react';

const CreateCounter = ({closeModal, cameraId}: {closeModal: any, cameraId: number}) => {
    const [name, setName] = useState('')
    const addCounter = (productId: number) => {
        fetch("http://localhost:8001/api/add_counter/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({"camera_id": cameraId, "product_id": productId})
        }).then((res) => res.json())
        .then((data) => {console.log(data)})
        closeModal()
    }

    const handleAdd = () => {
        fetch("http://localhost:8000/api/product_id_by_name/" + name)
        .then((res) => res.json())
        .then((data) => addCounter(data["product_id"]))
    }

    return(
        <Flex
            flexDirection="column"
            width="100wh"
            height="100vh"
            justifyContent="center"
            alignItems="center"
        >
            <Stack
                width="20%"
                height="30vh"
                justifyContent="center"
                alignItems="left"
                bg='white'
                style={{border: "1px solid black"}}
            >
                <HStack mx='20px'>
                    <Text>Название: </Text>
                    <Input onChange={(e: any) => {setName(e.target.value)}}></Input>
                </HStack>
                <HStack>
                    <Button onClick={closeModal}>Отменить</Button>
                    <Button 
                        onClick={handleAdd} 
                        m={5}
                        width={100}
                        >Создать
                    </Button>
                </HStack>
            </Stack>
        </Flex>
    )
}

export default CreateCounter;