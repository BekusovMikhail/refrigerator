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
    Text
} from "@chakra-ui/react";
import { CheckIcon, CloseIcon, EditIcon } from '@chakra-ui/icons'

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

const ProductList = () => {
    return (
        <div className="box-3">
            <Stack
                flexDir="column"
                mb="2"
                justifyContent="center"
                alignItems="center"
            >
                <Select>
                    <option value='white'>Белый холодильник</option>
                    <option value='grey'>Серый холодильник</option>
                </Select>
                <List spacing={3}>
                    <ListItem>
                    <   Flex flexDirection="row" justifyContent='center'>
                            <Text>Молоко: </Text>
                            <Editable
                                textAlign='center'
                                defaultValue='1'
                                isPreviewFocusable={false}
                                >
                                    <Flex flexDirection="row" justifyContent='center' ml={1}>
                                        <EditablePreview />
                                        <Input as={EditableInput} />
                                        <EditableControls />
                                    </Flex>
                            </Editable>
                        </Flex>
                    </ListItem>
                    <ListItem>
                        <Flex flexDirection="row" justifyContent='center'>
                            <Text>Творог: </Text>
                            <Editable
                                textAlign='center'
                                defaultValue='1'
                                isPreviewFocusable={false}
                                >
                                    <Flex flexDirection="row" justifyContent='center' ml={1}>
                                        <EditablePreview />
                                        <Input as={EditableInput} />
                                        <EditableControls />
                                    </Flex>
                            </Editable>
                        </Flex>
                    </ListItem>
                    <ListItem>
                        <Flex flexDirection="row" justifyContent='center'>
                            <Text>Сыр: </Text>
                            <Editable
                                textAlign='center'
                                defaultValue='1'
                                isPreviewFocusable={false}
                                >
                                    <Flex flexDirection="row" justifyContent='center' ml={1}>
                                        <EditablePreview />
                                        <Input as={EditableInput} />
                                        <EditableControls />
                                    </Flex>
                            </Editable>
                        </Flex>
                    </ListItem>
                    <ListItem>
                        <Flex flexDirection="row" justifyContent='center'>
                            <Text>Колбаса: </Text>
                            <Editable
                                textAlign='center'
                                defaultValue='1'
                                isPreviewFocusable={false}
                                >
                                    <Flex flexDirection="row" justifyContent='center' ml={1}>
                                        <EditablePreview />
                                        <Input as={EditableInput} />
                                        <EditableControls />
                                    </Flex>
                            </Editable>
                        </Flex>
                    </ListItem>
                    <ListItem>
                        <Flex flexDirection="row" justifyContent='center'>
                            <Text>Кефир: </Text>
                            <Editable
                                textAlign='center'
                                defaultValue='1'
                                isPreviewFocusable={false}
                                >
                                    <Flex flexDirection="row" justifyContent='center' ml={1}>
                                        <EditablePreview />
                                        <Input as={EditableInput} />
                                        <EditableControls />
                                    </Flex>
                            </Editable>
                        </Flex>
                    </ListItem>
                </List>
            </Stack>         
        </div>
    )
}

export default ProductList