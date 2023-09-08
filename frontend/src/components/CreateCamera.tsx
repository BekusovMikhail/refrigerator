import { useState } from 'react';
import { Flex, Stack, Input, Button, HStack, Text } from "@chakra-ui/react";
import { useParams } from 'react-router-dom'

const CreateCamera = ({closeModal}: {closeModal: any}) => {
    const [url, setUrl] = useState('')
    const [name, setName] = useState('')
    const { username } = useParams()
    //const [username, setUsername] = useState('LuckyHorseshoe')

    const addCamera = () => {
        fetch("http://localhost:8001/api/create_camera/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({"name": name, "url": url, "username": username})
        })
        closeModal()
    }

    return (
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
                <HStack mx='20px'>
                    <Text>URL: </Text>
                    <Input onChange={(e: any) => {setUrl(e.target.value)}}></Input>
                </HStack>
                <HStack ml={10}>
                    <Button onClick={closeModal}>
                        Отменить
                    </Button>
                    <Button 
                        onClick={addCamera} 
                        m={5}
                        width={100}
                        >Создать
                    </Button>
                </HStack>
            </Stack>
        </Flex>
    )
}

export default CreateCamera;