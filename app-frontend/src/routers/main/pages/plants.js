'use client'

import {
  Box,
  Heading,
  Image,
  Text,
  HStack,
  Tag,
  Container,
  useColorModeValue,
  Button,
  useDisclosure,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
  Select,
  Textarea,
  VStack,
  useToast,
  Flex,
  Spinner,
} from '@chakra-ui/react';
import { ListAllPlantsHook } from "../../../hooks/list_all_plants_hook";
import { IsLoggedInHook } from "../../../hooks/is_logged_in_hook";
import { useState } from 'react';
import { handleCreateTradeRequest, handleTradeRequestClick } from "../../../handlers/trade_request_handler";

const PlantTags = ({ marginTop = 0, tags }) => {
  const tagArray = typeof tags[0] === 'string' ? tags[0].split(',') : tags;
  return (
    <HStack spacing={2} marginTop={marginTop}>
      {tagArray.map((tag) => (
        <Tag size="md" variant="solid" colorScheme="orange" key={tag}>
          {tag}
        </Tag>
      ))}
    </HStack>
  );
};

const PlantOwner = ({ date, name }) => {
  return (
    <HStack marginTop="2" spacing="2" display="flex" alignItems="center">
      <Image
        borderRadius="full"
        boxSize="40px"
        src="/images/default_avatar.png"
        alt={`Avatar of ${name}`}
      />
      <Text fontWeight="medium">{name}</Text>
      <Text>—</Text>
      <Text>{new Date(date).toLocaleDateString()}</Text>
    </HStack>
  );
};

function PlantList() {
  const toast = useToast();

  const { plants, owners, isLoading } = ListAllPlantsHook();
  const isLoggedIn = IsLoggedInHook();
  const { isOpen: isTradeRequestOpen, onOpen: onTradeRequestOpen, onClose: onTradeRequestClose } = useDisclosure();
  const [selectedPlantId, setSelectedPlantId] = useState(null);
  const [myPlants, setMyPlants] = useState([]);
  const [message, setMessage] = useState('');
  const [incomingPlantId, setIncomingPlantId] = useState(null);

  const lightGradient = useColorModeValue(
    "radial(orange.600 1px, transparent 1px)",
    "radial(orange.300 1px, transparent 1px)"
  );
  const textColor = useColorModeValue("gray.700", "gray.200");

  return (
    <Container maxW="7xl" p="12">
      <Heading as="h1">Plants for Swapping</Heading>
      {/* Loading Indicator */}
      {isLoading ? (
        <Flex justify="center" align="center" minH="200px">
          <Spinner
            size="xl"
            thickness="4px"
            speed="0.65s"
            color="orange.500"
            emptyColor="gray.200"
          />
        </Flex>
          ) : (
            <>
              {plants.map((plant, index) => (
                <Box
                  key={index}
                  marginTop={{ base: '1', sm: '5' }}
                  display="flex"
                  flexDirection={{ base: 'column', sm: 'row' }}
                  justifyContent="space-between"
                >
              <Box
                display="flex"
                flex="1"
                marginRight="3"
                position="relative"
                alignItems="center"
              >
                <Box
                  width={{ base: '100%', sm: '85%' }}
                  zIndex="2"
                  marginLeft={{ base: '0', sm: '5%' }}
                  marginTop="5%"
                >
                  <Box textDecoration="none" _hover={{ textDecoration: 'none' }}>
                    <Image
                      borderRadius="lg"
                      src={plant.image_url ? plant.image_url : "/images/default_plant.jpg"}
                      alt="Image of the Plant"
                      boxSize="500px"
                      objectFit="cover"
                    />
                  </Box>
                </Box>
                <Box zIndex="1" width="100%" position="absolute" height="100%">
                  <Box
                    bgGradient={lightGradient}
                    backgroundSize="20px 20px"
                    opacity="0.4"
                    height="100%"
                  />
                </Box>
              </Box>
              <Box
                display="flex"
                flex="1"
                flexDirection="column"
                justifyContent="center"
                marginTop={{ base: '3', sm: '0' }}
              >
                <PlantTags tags={plant.tags} />
                <Heading marginTop="1">
                  <Text textDecoration="none" _hover={{ textDecoration: 'none' }}>
                    {plant.name}
                  </Text>
                </Heading>
                <Text
                  as="p"
                  marginTop="2"
                  color={textColor}
                  fontSize="lg"
                >
                  {plant.description}
                </Text>
                <PlantOwner name={owners[plant.owner_id] || "Unknown"} date={plant.creation_date} />
                {isLoggedIn && (
                  <Button
                    colorScheme="customGreen"
                    size="sm"
                    width="50%"
                    alignSelf="flex-start"
                    mt={4}
                    onClick={() => handleTradeRequestClick(plant.id, setIncomingPlantId, toast, setMyPlants, onTradeRequestOpen)}
                  >
                    Request Trade
                  </Button>
                )}
              </Box>
            </Box>
          ))}
        </>
      )}

      {/* Trade Request Modal */}
      <Modal isOpen={isTradeRequestOpen} onClose={onTradeRequestClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Create Trade Request</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <VStack spacing={4}>
              <Select
                placeholder="Select your plant to offer"
                onChange={(e) => setSelectedPlantId(e.target.value)}
              >
                {myPlants.map((plant) => (
                  <option key={plant.id} value={plant.id}>
                    {plant.name}
                  </option>
                ))}
              </Select>
              <Textarea
                placeholder="Optional message to the plant owner"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
              />
            </VStack>
          </ModalBody>
          <ModalFooter>
            <Button
              colorScheme="customGreen"
              size="sm"
              mr={3}
              onClick={() => handleCreateTradeRequest(selectedPlantId, incomingPlantId, message, onTradeRequestClose)}
            >
              Submit Request
            </Button>
            <Button
              variant="ghost"
              size="sm"
              onClick={onTradeRequestClose}
            >
              Cancel
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </Container>
  );
}

export default PlantList;
