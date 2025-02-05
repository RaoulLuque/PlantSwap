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
} from '@chakra-ui/react';
import {ListAllPlantsHook} from "../../../hooks/list_all_plants_hook";

const PlantTags = ({ marginTop = 0, tags }) => {
  return (
    <HStack spacing={2} marginTop={marginTop}>
      {tags.map((tag) => (
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
        src="https://e7.pngegg.com/pngimages/84/165/png-clipart-united-states-avatar-organization-information-user-avatar-service-computer-wallpaper-thumbnail.png"
        alt={`Avatar of ${name}`}
      />
      <Text fontWeight="medium">{name}</Text>
      <Text>—</Text>
      <Text>{new Date(date).toLocaleDateString()}</Text>
    </HStack>
  );
};

function PlantList() {
    const { plants, owners } = ListAllPlantsHook()

    const lightGradient = useColorModeValue(
        "radial(orange.600 1px, transparent 1px)",
        "radial(orange.300 1px, transparent 1px)"
    );
    const textColor = useColorModeValue("gray.700", "gray.200");

    return (
    <Container maxW="7xl" p="12">
      <Heading as="h1">Plants for Swapping</Heading>
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
                  src={plant.image_url}
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
            <PlantTags tags={['Plant', 'Testing']} />
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
            <PlantOwner name={owners[plant.owner_id] || "Unknown"} date="2021-04-06T19:01:27Z" />
          </Box>
        </Box>
      ))}
    </Container>
  );
}

export default PlantList;
