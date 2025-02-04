import React, { useState } from 'react';
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
import { HamburgerIcon, CloseIcon, AddIcon } from '@chakra-ui/icons';
import {handleLogin, handleLogout} from "../handlers/auth_handler";
import { handleCreatePlant } from "../handlers/plant_handlers";

const Links = [];

const NavLink = (props) => {
  const { children } = props;
  return (
    <Box
      as="a"
      px={2}
      py={1}
      rounded={'md'}
      _hover={{
        textDecoration: 'none',
        bg: useColorModeValue('gray.200', 'gray.700'),
      }}
      href={'#'}>
      {children}
    </Box>
  );
};

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

  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [image, setImage] = useState(null);

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
            <HStack as={'nav'} spacing={4} display={{ base: 'none', md: 'flex' }}>
              {Links.map((link) => (
                <NavLink key={link}>{link}</NavLink>
              ))}
            </HStack>
          </HStack>
          <Flex alignItems={'center'}>
            <Button
              variant={'solid'}
              colorScheme={'teal'}
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
                <MenuItem onClick={onLoginOpen}>Login</MenuItem>
                <MenuItem onClick={() => handleLogout(toast)}>Logout</MenuItem>
                <MenuDivider />
                <MenuItem>Link 3</MenuItem>
              </MenuList>
            </Menu>
          </Flex>
        </Flex>

        {isOpen ? (
          <Box pb={4} display={{ md: 'none' }}>
            <Stack as={'nav'} spacing={4}>
              {Links.map((link) => (
                <NavLink key={link}>{link}</NavLink>
              ))}
            </Stack>
          </Box>
        ) : null}
      </Box>
      <Modal isOpen={isLoginOpen} onClose={onLoginClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Login</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <form id="login-form" onSubmit={(e) => handleLogin(e, onLoginClose, toast)}>
              <Stack spacing={4}>
                <Input name="username" placeholder="Username" required />
                <Input name="password" type="password" placeholder="Password" required />
              </Stack>
            </form>
          </ModalBody>
          <ModalFooter>
            <Button colorScheme="teal" mr={3} type="submit" form="login-form">
              Login
            </Button>
            <Button variant="ghost" onClick={onLoginClose}>
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
                <Input
                  type="file"
                  onChange={(e) => setImage(e.target.files[0])}
                />
              </FormControl>
            </Stack>
          </ModalBody>
          <ModalFooter>
            <Button colorScheme="teal" mr={3} onClick={() => handleCreatePlant(name, description, image, toast, onPlantModalClose)}>
              Create
            </Button>
            <Button variant="ghost" onClick={onPlantModalClose}>
              Cancel
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </>
  );
}
