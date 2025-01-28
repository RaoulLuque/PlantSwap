import React, { useState, useEffect } from "react";
import api from "../../../api";
import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Input,
  Text,
  Stack,
  Heading,
  List,
  ListItem,
  VStack,
  useToast,
} from "@chakra-ui/react"; // Import Chakra UI components

function PlantsPage() {
  const [plants, setPlants] = useState([]);
  const [newPlant, setNewPlant] = useState({ name: "", description: "", price: 0, quantity: 0 });
  const toast = useToast(); // For showing notifications

  // Fetch plants from the backend
  useEffect(() => {
    fetchPlants();
  }, []);

  // Function to fetch all plants
  const fetchPlants = async () => {
    try {
      const response = await api.get("/plants/");
      setPlants(response.data.data); // The plants call returns PublicPlants which has a field data containing the list of plants
    } catch (error) {
      console.error("Error fetching plants:", error);
      toast({
        title: "Error",
        description: "Could not fetch plants.",
        status: "error",
        duration: 5000,
        isClosable: true,
      });
    }
  };

  // Handle input changes in the form
  const handleInputChange = (e) => {
    setNewPlant({ ...newPlant, [e.target.name]: e.target.value });
  };

  // Add new plant to the backend
  const addPlant = async () => {
    try {
      await api.post("/plants/", newPlant);
      fetchPlants(); // Refresh the plants list
      setNewPlant({ name: "", description: "", price: 0, quantity: 0 }); // Reset form
      toast({
        title: "Plant Added",
        description: "Your new plant has been added.",
        status: "success",
        duration: 5000,
        isClosable: true,
      });
    } catch (error) {
      console.error("Error adding plant:", error);
      toast({
        title: "Error",
        description: "Could not add the plant.",
        status: "error",
        duration: 5000,
        isClosable: true,
      });
    }
  };

  // Delete a plant from the backend
  const deletePlant = async (id) => {
    try {
      await api.delete(`/plants/${id}`);
      fetchPlants(); // Refresh plants list
      toast({
        title: "Plant Deleted",
        description: "The plant has been deleted.",
        status: "success",
        duration: 5000,
        isClosable: true,
      });
    } catch (error) {
      console.error("Error deleting plant:", error);
      toast({
        title: "Error",
        description: "Could not delete the plant.",
        status: "error",
        duration: 5000,
        isClosable: true,
      });
    }
  };

  return (
    <Box p={5}>
      <Heading as="h2" mb={5}>
        Plant List
      </Heading>
      <List spacing={3}>
        {plants.map((plant) => (
          <ListItem key={plant.id} p={3} border="1px" borderRadius="md" boxShadow="md">
            <VStack align="start" spacing={2}>
              <Text fontSize="xl" fontWeight="bold">
                {plant.name}
              </Text>
              <Text>{plant.description}</Text>
              <Button colorScheme="red" onClick={() => deletePlant(plant.id)}>
                Delete
              </Button>
            </VStack>
          </ListItem>
        ))}
      </List>

      <Heading as="h3" size="lg" mt={8} mb={5}>
        Add New Plant
      </Heading>
      <form
        onSubmit={(e) => {
          e.preventDefault();
          addPlant();
        }}
      >
        <Stack spacing={4}>
          <FormControl>
            <FormLabel htmlFor="name">Name</FormLabel>
            <Input
              type="text"
              name="name"
              id="name"
              placeholder="Name"
              value={newPlant.name}
              onChange={handleInputChange}
              required
            />
          </FormControl>
          <FormControl>
            <FormLabel htmlFor="description">Description</FormLabel>
            <Input
              type="text"
              name="description"
              id="description"
              placeholder="Description"
              value={newPlant.description}
              onChange={handleInputChange}
              required
            />
          </FormControl>
          <Button colorScheme="teal" type="submit">
            Add Plant
          </Button>
        </Stack>
      </form>
    </Box>
  );
}

export default PlantsPage;
