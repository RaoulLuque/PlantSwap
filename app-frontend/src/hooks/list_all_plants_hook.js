import {useCallback, useEffect, useState} from "react";
import api from "../api";
import {useToast} from "@chakra-ui/react";

export const ListAllPlantsHook = () => {
  const [plants, setPlants] = useState([]);
  const [owners, setOwners] = useState({});
  const toast = useToast();

  const fetchPlants = useCallback(async () => {
    try {
      const response = await api.get("/plants/");
      const plantData = response.data.data;

      console.log("Fetched Plants:", plantData);
      setPlants(plantData);

      // Fetch owners for all plants
      const ownerPromises = plantData.map((plant) =>
        api
          .get(`/users/${plant.owner_id}`)
          .then((res) => ({
            id: plant.owner_id,
            name: res.data.full_name,
          }))
          .catch((err) => {
            console.error(`Error fetching owner for ID ${plant.owner_id}:`, err);
            return { id: plant.owner_id, name: "Unknown" };
          })
      );

      const ownerData = await Promise.all(ownerPromises);
      console.log("Fetched Owners:", ownerData);

      // Create a map of owner IDs to names
      const ownerMap = ownerData.reduce(
        (acc, owner) => ({ ...acc, [owner.id]: owner.name }),
        {}
      );

      console.log("Owner Map:", ownerMap);
      setOwners(ownerMap);
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
  }, [toast]);

  useEffect(() => {
    fetchPlants().then();
  }, [fetchPlants]);

  return { plants, owners };
};
