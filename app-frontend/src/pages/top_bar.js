import React, {useState} from 'react';
import {
  Box,
  Flex,
  Avatar,
  HStack,
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
  AlertDialog,
  AlertDialogBody,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogContent,
  AlertDialogOverlay,
} from '@chakra-ui/react';
import {AddIcon} from '@chakra-ui/icons';
import {handleLogin, handleLogout} from "../handlers/auth_handler";
import {
  handleCreatePlant,
  handleDeletePlant,
  handleListMyPlants,
  handleMyPlantsClose
} from "../handlers/plant_handlers";
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
  const {
  isOpen: isDeleteDialogOpen,
  onOpen: onDeleteDialogOpen,
  onClose: onDeleteDialogClose,
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
  const [tags, setTags] = useState('');
  const [selectedPlantId, setSelectedPlantId] = useState(null);
  const cancelRef = React.useRef();
  const [hasDeleted, setHasDeleted] = useState(false);

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
          <HStack spacing={8} alignItems={'center'}>
            <Flex
              alignItems="center"
              cursor="pointer"
              onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
            >
              <Image
                src="images/logo512.png"
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
              onClick={onPlantModalOpen}
              w={{ base: '140px', md: 'auto' }}
            >
              Add a Plant Ad
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
                  src="/images/default_avatar.png"
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

      {/* Login Modal */}
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

      {/* Register Modal */}
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

      {/* Create Plant Modal */}
      <Modal isOpen={isPlantModalOpen} onClose={onPlantModalClose} size="lg">
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
                <FormLabel>Tags (comma-separated)</FormLabel>
                <Input
                  placeholder="e.g., Indoor, Succulent, Grown"
                  value={tags}
                  onChange={(e) => setTags(e.target.value)}
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
                handleCreatePlant(name, description, tags, image, toast, onPlantModalClose, setIsCreatingPlant).then();
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

      {/* My Plants Modal */}
      <Modal isOpen={isMyPlantsOpen} onClose={() => {handleMyPlantsClose(onMyPlantsClose, hasDeleted, setHasDeleted)}} size="lg">
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
                      justifyContent="space-between"
                      width="100%"
                    >
                      <Flex alignItems="center" flex={1} overflow="hidden" mr={4}>
                        <Image
                          src={plant.image_url}
                          alt={plant.name}
                          borderRadius="md"
                          boxSize="150px"
                          objectFit="cover"
                          mr={4}
                        />
                        <Box flex={1} overflow="hidden">
                          <Text fontWeight="bold" fontSize="lg">
                            {plant.name}
                          </Text>
                          <Text
                            fontSize="md"
                            color="gray.600"
                            noOfLines={2}
                            overflow="hidden"
                            textOverflow="ellipsis"
                            whiteSpace="nowrap"
                          >
                            {plant.description}
                          </Text>
                        </Box>
                      </Flex>
                      <Button
                        colorScheme="red"
                        size="sm"
                        onClick={() => {
                          setSelectedPlantId(plant.id);
                          onDeleteDialogOpen();
                        }}
                      >
                        Delete
                      </Button>
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
      <AlertDialog
        isOpen={isDeleteDialogOpen}
        leastDestructiveRef={cancelRef}
        onClose={onDeleteDialogClose}
      >
        <AlertDialogOverlay>
          <AlertDialogContent>
            <AlertDialogHeader fontSize="lg" fontWeight="bold">
              Delete Plant
            </AlertDialogHeader>
            <AlertDialogBody>
              Are you sure you want to delete this plant? This action cannot be undone.
            </AlertDialogBody>
            <AlertDialogFooter>
              <Button ref={cancelRef} onClick={onDeleteDialogClose}>
                Cancel
              </Button>
              <Button
                colorScheme="red"
                onClick={async () => {
                  await handleDeletePlant(selectedPlantId, toast, () => {
                    setMyPlants(prevPlants => prevPlants.filter(p => p.id !== selectedPlantId));
                    setHasDeleted(true);
                  });
                  onDeleteDialogClose();
                }}
                ml={3}
              >
                Delete
              </Button>
            </AlertDialogFooter>
          </AlertDialogContent>
        </AlertDialogOverlay>
      </AlertDialog>
    </>
  );
}
