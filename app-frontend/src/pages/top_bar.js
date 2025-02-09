import React, { useState } from 'react';
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
  Tag,
} from '@chakra-ui/react';
import { AddIcon } from '@chakra-ui/icons';
import { handleLogin, handleLogout } from "../handlers/auth_handler";
import {
  handleCreatePlant,
  handleDeletePlant,
  handleListMyPlants,
  handleMyPlantsClose,
  PlantImageHandler
} from "../handlers/plant_handlers";
import { handleRegistration } from "../handlers/user_handler";
import {
  handleDragEnter,
  handleDragLeave,
  handleDragOver,
  handleDrop,
  handleImageChange
} from "../handlers/image_upload_handlers";
import { IsLoggedInHook } from "../hooks/is_logged_in_hook";
import { showStoredToastAfterWindowReload } from "../utils";
import {
  handleAcceptTradeRequest, handleDeclineTradeRequest,
  handleDeleteTradeRequest,
  handleListTradeRequests
} from "../handlers/trade_request_handler";

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
  const {
    isOpen: isTradeRequestsOpen,
    onOpen: onTradeRequestsOpen,
    onClose: onTradeRequestsClose,
  } = useDisclosure();
  const {
  isOpen: isTradeDetailsOpen,
  onOpen: onTradeDetailsOpen,
  onClose: onTradeDetailsClose,
} = useDisclosure();

  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [image, setImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isCreatingPlant, setIsCreatingPlant] = useState(false);
  const [isLoggingIn, setIsLoggingIn] = useState(false);
  const [isLoggedIn, currentUserId] = IsLoggedInHook();
  const [myPlants, setMyPlants] = useState([]);
  const [tags, setTags] = useState('');
  const [selectedPlantId, setSelectedPlantId] = useState(null);
  const cancelRef = React.useRef();
  const [hasDeleted, setHasDeleted] = useState(false);
  const [tradeRequests, setTradeRequests] = useState([]);
  const [selectedTradeRequest, setSelectedTradeRequest] = useState(null);

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
                minW={0}
              >
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
                {isLoggedIn && (
                  <>
                    <MenuItem onClick={() => handleListMyPlants(onMyPlantsOpen, toast, setMyPlants)}>
                      My Plants
                    </MenuItem>
                    <MenuItem onClick={async () => {
                      handleListTradeRequests(onTradeRequestsOpen, toast, setTradeRequests);
                    }}>
                      My Trade Requests
                    </MenuItem>
                  </>
                )}
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
                    onChange={(e) =>
                      handleImageChange(e.target.files[0], toast, setImage, setImagePreview)
                    }
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
                    <Flex mt={4} justifyContent="center" alignItems="center">
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
                // Convert the comma-separated string into an array of trimmed strings
                const tagsArray = tags
                  .split(',')
                  .map((tag) => tag.trim())
                  .filter((tag) => tag !== '');
                handleCreatePlant(
                  name,
                  description,
                  tagsArray,
                  image,
                  toast,
                  onPlantModalClose,
                  setIsCreatingPlant
                ).then();
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
      <Modal isOpen={isMyPlantsOpen} onClose={() => { handleMyPlantsClose(onMyPlantsClose, hasDeleted, setHasDeleted) }} size="lg">
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
                        <PlantImageHandler
                          imageUrl={plant.image_url}
                          plantId={plant.id}
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

      {/* Trade Requests Modal */}
      <Modal isOpen={isTradeRequestsOpen} onClose={onTradeRequestsClose} size="xl">
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>My Trade Requests</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            {tradeRequests.length === 0 ? (
              <Text>No trade requests found.</Text>
            ) : (
              <Stack spacing={4}>
                {tradeRequests.map((tr, index) => {
                  // Determine if the current user is the receiver.
                  const isReceiver = currentUserId === tr.incoming_user_id;
                  return (
                    <Box key={index} borderWidth="1px" borderRadius="md" p={4}>
                      <Flex direction="column" gap={3}>
                        <Flex
                          direction={{ base: 'column', md: 'row' }}
                          gap={6}
                        >
                          {/* Left Box: The plant offered by the trade request creator */}
                          <Box flex={1}>
                            <Text fontWeight="bold" mb={2} fontSize="lg">
                              {isReceiver ? "You were offered:" : "Your Offer:"}
                            </Text>
                            <Flex align="center">
                              <PlantImageHandler
                                plantId={tr.outgoing_plant_id}
                                imageUrl={tr.outgoing_plant?.image_url}
                                boxSize="80px"
                                mr={3}
                              />
                              <Box>
                                <Text fontSize="md">
                                  {tr.outgoing_plant?.name || 'Plant not available'}
                                </Text>
                              </Box>
                            </Flex>
                          </Box>

                          {/* Right Box: The plant from the current user */}
                          <Box flex={1}>
                            <Text fontWeight="bold" mb={2} fontSize="lg">
                              {isReceiver ? "Your Plant:" : "Requested Plant:"}
                            </Text>
                            <Flex align="center">
                              <PlantImageHandler
                                plantId={tr.incoming_plant_id}
                                imageUrl={tr.incoming_plant?.image_url}
                                boxSize="80px"
                                mr={3}
                              />
                              <Box>
                                <Text fontSize="md">
                                  {tr.incoming_plant?.name || 'Plant not available'}
                                </Text>
                              </Box>
                            </Flex>
                          </Box>
                        </Flex>
                        <HStack justify="space-between" mt={2} width="100%">
                          <Tag colorScheme={tr.status === 'accepted' ? 'green' : 'orange'}>
                            {tr.status}
                          </Tag>
                          <Stack direction={{ base: 'column', md: 'row' }} spacing={4}>
                            <Button
                              colorScheme="red"
                              onClick={() => {
                                handleDeleteTradeRequest(
                                  tr.outgoing_plant_id,
                                  tr.incoming_plant_id,
                                  toast,
                                  () => {
                                    // Immediately filter out the deleted request
                                    setTradeRequests(prev => prev.filter(request =>
                                      request.outgoing_plant_id !== tr.outgoing_plant_id ||
                                      request.incoming_plant_id !== tr.incoming_plant_id
                                    ));
                                  }
                                );
                              }}
                            >
                              Delete Request
                            </Button>
                            <Button
                              colorScheme="blue"
                              onClick={() => {
                                onTradeRequestsClose();
                                setSelectedTradeRequest(tr);
                                onTradeDetailsOpen();
                              }}
                            >
                              Open Details
                            </Button>
                          </Stack>
                        </HStack>
                      </Flex>
                    </Box>
                  );
                })}
              </Stack>
            )}
          </ModalBody>
          <ModalFooter>
            <Button onClick={onTradeRequestsClose}>Close</Button>
          </ModalFooter>
        </ModalContent>
      </Modal>

      {/* Trade Details Modal */}
      {isTradeDetailsOpen && selectedTradeRequest && (
        <Modal
          isOpen={isTradeDetailsOpen}
          onClose={() => {
            onTradeDetailsClose();
            onTradeRequestsOpen();
          }}
          size="xl"
        >
          <ModalOverlay />
          <ModalContent>
            <ModalHeader>Trade Request Details</ModalHeader>
            <ModalCloseButton />
            <ModalBody>
              <Stack spacing={4}>
                {/* Plant Information */}
                <Flex direction={{ base: 'column', md: 'row' }} gap={6}>
                  <Box flex={1}>
                    <Text fontWeight="bold" mb={2}>Offered Plant:</Text>
                    <Flex align="center">
                      <PlantImageHandler
                        plantId={selectedTradeRequest.outgoing_plant_id}
                        imageUrl={selectedTradeRequest.outgoing_plant?.image_url}
                        boxSize="100px"
                        mr={3}
                      />
                      <Box>
                        <Text fontSize="lg" fontWeight="semibold">
                          {selectedTradeRequest.outgoing_plant?.name || 'Plant not available'}
                        </Text>
                        <Text fontSize="sm" color="gray.500">
                          {selectedTradeRequest.outgoing_plant?.description}
                        </Text>
                      </Box>
                    </Flex>
                  </Box>

                  <Box flex={1}>
                    <Text fontWeight="bold" mb={2}>Requested Plant:</Text>
                    <Flex align="center">
                      <PlantImageHandler
                        plantId={selectedTradeRequest.incoming_plant_id}
                        imageUrl={selectedTradeRequest.incoming_plant?.image_url}
                        boxSize="100px"
                        mr={3}
                      />
                      <Box>
                        <Text fontSize="lg" fontWeight="semibold">
                          {selectedTradeRequest.incoming_plant?.name || 'Plant not available'}
                        </Text>
                        <Text fontSize="sm" color="gray.500">
                          {selectedTradeRequest.incoming_plant?.description}
                        </Text>
                      </Box>
                    </Flex>
                  </Box>
                </Flex>

                {/* Messages */}
                <Box mt={4}>
                  <Text fontWeight="bold" mb={3}>Conversation:</Text>
                  <Stack spacing={3}>
                    {selectedTradeRequest.messages?.length > 0 ? (
                      selectedTradeRequest.messages.map((message, index) => (
                        <Box
                          key={index}
                          alignSelf={message.sender_id === currentUserId ? 'flex-end' : 'flex-start'}
                          bg={message.sender_id === currentUserId ? 'blue.50' : 'gray.100'}
                          p={3}
                          borderRadius="md"
                          maxWidth="80%"
                        >
                          <Text fontSize="sm">{message.content}</Text>
                          <Text fontSize="xs" color="gray.500" mt={1}>
                            {new Date(message.timestamp).toLocaleString()}
                          </Text>
                        </Box>
                      ))
                    ) : (
                      <Text color="gray.500">No messages yet</Text>
                    )}
                  </Stack>
                </Box>
              </Stack>
            </ModalBody>
            <ModalFooter>
              <HStack spacing={3}>
                {currentUserId === selectedTradeRequest.incoming_user_id && (
                  <>
                    <Button
                      colorScheme="green"
                      onClick={() => {
                        handleAcceptTradeRequest(
                          selectedTradeRequest.outgoing_plant_id,
                          selectedTradeRequest.incoming_plant_id,
                          toast,
                          () => {
                            setTradeRequests(prev => prev.map(tr =>
                              tr === selectedTradeRequest ? {...tr, status: 'accepted'} : tr
                            ));
                            onTradeDetailsClose();
                          }
                        );
                        onTradeDetailsClose();
                        onTradeRequestsOpen();
                      }}
                      isDisabled={selectedTradeRequest.status === 'accepted'}
                    >
                      Accept
                    </Button>
                    <Button
                      colorScheme="red"
                      variant="outline"
                      onClick={() => {
                        handleDeclineTradeRequest(
                          selectedTradeRequest.outgoing_plant_id,
                          selectedTradeRequest.incoming_plant_id,
                          toast,
                          () => {
                            setTradeRequests(prev => prev.map(tr =>
                              tr === selectedTradeRequest ? {...tr, status: 'declined'} : tr
                            ));
                            onTradeDetailsClose();
                          }
                        );
                        onTradeDetailsClose();
                        onTradeRequestsOpen();
                      }}
                    >
                      Decline
                    </Button>
                  </>
                )}
                <Button variant="ghost" onClick={() => {onTradeDetailsClose(); onTradeRequestsOpen();}}>
                  Close
                </Button>
              </HStack>
            </ModalFooter>
          </ModalContent>
        </Modal>
      )}

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
