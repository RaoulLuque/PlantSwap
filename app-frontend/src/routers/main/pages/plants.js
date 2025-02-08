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
import {PlantImageHandler} from "../../../handlers/plant_handlers";

const PlantTags = ({ marginTop = 0, tags }) => {
  const tagArray = tags.filter(tag => tag.trim() !== '').sort();
  return (
    <HStack spacing={2} marginTop={marginTop}>
      {tagArray.map((tag) => (
        <Tag size="md" variant="solid" colorScheme="green" key={tag}>
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

  const textColor = useColorModeValue("gray.700", "gray.200");
  const cardBg = useColorModeValue("white", "gray.700");

  return (
    <Container maxW={{ base: "100%", md: "7xl" }} p={{ base: 4, md: 4 }}>
      <Box
        mt={{ base: 12, md: 12 }}
        mb={{ base: 4, md: 4 }}
      >
        <Heading
          as="h1"
          fontSize={{ base: "2xl", md: "4xl" }}
        >
          Plants for Swapping
        </Heading>
      </Box>
      {isLoading ? (
        <Flex justify="center" align="center" minH="200px">
          <Spinner
            size="xl"
            thickness="4px"
            speed="0.65s"
            color="green.500"
            emptyColor="gray.200"
          />
        </Flex>
      ) : (
        <Flex direction="column" gap={6}>
          {plants.map((plant, index) => (
            <Box
              key={index}
              p={{ base: 4, md: 6 }}
              borderRadius="lg"
              boxShadow={{ base: "md", md: "xl" }}
              bg={cardBg}
              width="100%"
            >
              <Flex
                direction={{ base: "column", md: "row" }}
                gap={{ base: 4, md: 6 }}
              >
                {/* Image Section */}
                <Box
                  flexShrink={0}
                  width={{ base: "100%", md: "400px" }}
                >
                  <PlantImageHandler
                    imageUrl={plant.image_url}
                    plantId={plant.id}
                    borderRadius="lg"
                    width="100%"
                    height={{ base: "300px", md: "400px" }}
                    objectFit="cover"
                    transition="transform 0.2s"
                    _hover={{ transform: "scale(1.02)" }}
                  />
                </Box>

                {/* Content Section */}
                <Box flex={1} pl={{ md: 4 }}>
                  <PlantTags tags={plant.tags} marginTop={0} />
                  <Heading fontSize={{ base: "24px", md: "32px" }} mt={{ base: 2, md: 3 }} mb={2}>
                    {plant.name}
                  </Heading>
                  <Text
                    fontSize="md"
                    color={textColor}
                    noOfLines={{ base: 3, md: 4 }}
                  >
                    {plant.description}
                  </Text>
                  <PlantOwner name={owners[plant.owner_id] || "Unknown"} date={plant.creation_date} />

                  {isLoggedIn && (
                    <Button
                      colorScheme="green"
                      size="md"
                      width={{ base: "100%", md: "50%" }}
                      mt={4}
                      onClick={() => handleTradeRequestClick(plant.id, setIncomingPlantId, toast, setMyPlants, onTradeRequestOpen)}
                    >
                      Request Trade
                    </Button>
                  )}
                </Box>
              </Flex>
            </Box>
          ))}
        </Flex>
      )}

      {/* Trade Request Modal */}
      <Modal isOpen={isTradeRequestOpen} onClose={onTradeRequestClose} size="lg">
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
              onClick={() => handleCreateTradeRequest(selectedPlantId, incomingPlantId, message, onTradeRequestClose, toast)}
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
