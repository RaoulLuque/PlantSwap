import React, {useState} from 'react';
import {
  Box,
  Flex,
  Avatar,
  HStack,
  IconButton,
  Button,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  MenuDivider,
  useDisclosure,
  useColorModeValue,
  Stack,
  Image,
  Text,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalCloseButton,
  ModalBody,
  ModalFooter,
  Input,
  useToast,
  FormControl,
  FormLabel,
  Textarea,
} from '@chakra-ui/react';
import {HamburgerIcon, CloseIcon, AddIcon} from '@chakra-ui/icons';
import {handleLogin, handleLogout} from "../handlers/auth_handler";
import {handleCreatePlant, handleListMyPlants} from "../handlers/plant_handlers";
import {handleRegistration} from "../handlers/user_handler";
import {
  handleDragEnter,
  handleDragLeave,
  handleDragOver,
  handleDrop,
  handleImageChange
} from "../handlers/image_upload_handlers";
import {IsLoggedInHook} from "../hooks/is_logged_in_hook";
import {showStoredToastAfterWindowReload} from "../utils";

export default function TopBar() {
  const toast = useToast();

  const { isOpen, onOpen, onClose } = useDisclosure();
  const {
    isOpen: isLoginOpen,
    onOpen: onLoginOpen,
    onClose: onLoginClose,
  } = useDisclosure();
  const {
    isOpen: isPlantModalOpen,
    onOpen: onPlantModalOpen,
    onClose: onPlantModalClose,
  } = useDisclosure();
  const {
    isOpen: isRegisterOpen,
    onOpen: onRegisterOpen,
    onClose: onRegisterClose,
  } = useDisclosure();
  const {
    isOpen: isMyPlantsOpen,
    onOpen: onMyPlantsOpen,
    onClose: onMyPlantsClose,
  } = useDisclosure();

  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [image, setImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isCreatingPlant, setIsCreatingPlant] = useState(false);
  const [isLoggingIn, setIsLoggingIn] = useState(false);
  const isLoggedIn = IsLoggedInHook();
  const [myPlants, setMyPlants] = useState([]);

  // Show toasts after reloading page
  showStoredToastAfterWindowReload(toast);

  return (
    <>
      <Box
        bg={useColorModeValue('gray.100', 'gray.900')}
        px={4}
        position="fixed"
        top={0}
        left={0}
        right={0}
        zIndex={1000}
      >
        <Flex h={16} alignItems={'center'} justifyContent={'space-between'}>
          <IconButton
            size={'md'}
            icon={isOpen ? <CloseIcon /> : <HamburgerIcon />}
            aria-label={'Open Menu'}
            display={{ md: 'none' }}
            onClick={isOpen ? onClose : onOpen}
          />
          <HStack spacing={8} alignItems={'center'}>
            <Flex alignItems="center">
              <Image
                src="/logo512.png"
                alt="PlantSwap Logo"
                boxSize="40px"
                objectFit="contain"
              />
              <Text fontWeight="bold" ml={2} fontSize="lg">
                PlantSwap
              </Text>
            </Flex>
          </HStack>
          <Flex alignItems={'center'}>
            <Button
              variant={'solid'}
              colorScheme={'customGreen'}
              size={'sm'}
              mr={4}
              leftIcon={<AddIcon />}
              onClick={onPlantModalOpen}>
              Create a Plant Ad
            </Button>
            <Menu>
              <MenuButton
                as={Button}
                rounded={'full'}
                variant={'link'}
                cursor={'pointer'}
                minW={0}>
                <Avatar
                  size={'sm'}
                  src="https://e7.pngegg.com/pngimages/84/165/png-clipart-united-states-avatar-organization-information-user-avatar-service-computer-wallpaper-thumbnail.png"
                />
              </MenuButton>
              <MenuList>
                {!isLoggedIn && <MenuItem onClick={onLoginOpen}>Login</MenuItem>}
                {isLoggedIn && <MenuItem onClick={() => handleLogout(toast)}>Logout</MenuItem>}
                <MenuDivider />
                {!isLoggedIn && <MenuItem onClick={onRegisterOpen}>Register</MenuItem>}
                {isLoggedIn && <MenuItem onClick={() => handleListMyPlants(onMyPlantsOpen, toast, setMyPlants)}>My Plants</MenuItem>}
              </MenuList>
            </Menu>
          </Flex>
        </Flex>
      </Box>
      <Modal isOpen={isLoginOpen} onClose={onLoginClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Login</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <form id="login-form" onSubmit={(e) => handleLogin(e, onLoginClose, toast, setIsLoggingIn)}>
              <Stack spacing={4}>
                <Input name="username" placeholder="Username" required />
                <Input name="password" type="password" placeholder="Password" required />
              </Stack>
            </form>
          </ModalBody>
          <ModalFooter>
            <Button
              colorScheme="customGreen"
              mr={3}
              type="submit"
              form="login-form"
              isLoading={isLoggingIn}
              disabled={isLoggingIn}
            >
              Create
            </Button>
            <Button variant="ghost" onClick={onLoginClose}>
              Cancel
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
      <Modal isOpen={isRegisterOpen} onClose={onRegisterClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Register</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <form id="register-form" onSubmit={(e) => handleRegistration(e, onRegisterClose, toast)}>
              <Stack spacing={4}>
                <Input name="full_name" placeholder="Full Name" required />
                <Input name="email" type="email" placeholder="Email" required />
                <Input name="password" type="password" placeholder="Password" required />
              </Stack>
            </form>
          </ModalBody>
          <ModalFooter>
            <Button colorScheme="customGreen" mr={3} type="submit" form="register-form">
              Register
            </Button>
            <Button variant="ghost" onClick={onRegisterClose}>
              Cancel
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>

      <Modal isOpen={isPlantModalOpen} onClose={onPlantModalClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Create a New Plant</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <Stack spacing={4}>
              <FormControl isRequired>
                <FormLabel>Name</FormLabel>
                <Input
                  placeholder="Plant name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                />
              </FormControl>
              <FormControl>
                <FormLabel>Description</FormLabel>
                <Textarea
                  placeholder="Description of the plant"
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                />
              </FormControl>
              <FormControl>
                <FormLabel>Image</FormLabel>
                <Box
                  border="2px dashed"
                  borderColor={isDragging ? 'customGreen.500' : 'gray.200'}
                  borderRadius="md"
                  p={4}
                  textAlign="center"
                  onDragOver={(e) => handleDragOver(e, setIsDragging)}
                  onDragEnter={(e) => handleDragEnter(e, setIsDragging)}
                  onDragLeave={(e) => handleDragLeave(e, setIsDragging)}
                  onDrop={(e) => handleDrop(e, setIsDragging, toast, setImage, setImagePreview)}
                  _hover={{ borderColor: 'customGreen.500' }}
                >
                  <input
                    type="file"
                    onChange={(e) => handleImageChange(e.target.files[0], toast, setImage, setImagePreview)}
                    accept="image/*"
                    style={{ display: 'none' }}
                    id="file-input"
                  />
                  <label htmlFor="file-input">
                    <Button as="span" colorScheme="customGreen" variant="outline">
                      Upload Image
                    </Button>
                  </label>
                  <Text mt={2} fontSize="sm" color="gray.500">
                    or drag and drop an image here
                  </Text>
                  {imagePreview && (
                    <Flex
                      mt={4}
                      justifyContent="center"
                      alignItems="center"
                    >
                      <Image
                        src={imagePreview}
                        alt="Plant Preview"
                        borderRadius="md"
                        boxSize="150px"
                        objectFit="cover"
                      />
                    </Flex>
                  )}
                </Box>
              </FormControl>
            </Stack>
          </ModalBody>
          <ModalFooter>
            <Button
              colorScheme="customGreen"
              mr={3}
              onClick={() => {
                handleCreatePlant(name, description, image, toast, onPlantModalClose, setIsCreatingPlant).then();
              }}
              isLoading={isCreatingPlant}
              disabled={isCreatingPlant}
            >
              Create
            </Button>
            <Button variant="ghost" onClick={onPlantModalClose}>
              Cancel
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
      <Modal isOpen={isMyPlantsOpen} onClose={onMyPlantsClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>My Plants</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
              <>
                {myPlants.length === 0 ? (
                  <Text>You have not listed any plants yet.</Text>
                ) : (
                  <Stack spacing={4}>
                    {myPlants.map((plant, index) => (
                      <Flex
                        key={index}
                        borderWidth="1px"
                        borderRadius="lg"
                        p={4}
                        alignItems="center"
                      >
                        <Image
                          src={plant.image_url}
                          alt={plant.name}
                          borderRadius="md"
                          boxSize="150px"
                          objectFit="cover"
                          mr={4}
                        />
                        <Box>
                          <Text fontWeight="bold" fontSize="lg">
                            {plant.name}
                          </Text>
                          <Text fontSize="md" color="gray.600">
                            {plant.description}
                          </Text>
                        </Box>
                      </Flex>
                    ))}
                  </Stack>
                )}
              </>
          </ModalBody>
          <ModalFooter>
            <Button colorScheme="customGreen" onClick={onMyPlantsClose}>
              Close
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </>
  );
}
