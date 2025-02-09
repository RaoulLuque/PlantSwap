import {useCallback, useEffect, useState} from "react";
import api from "../api";
import {useToast} from "@chakra-ui/react";

export const ListAllPlantsHook = () => {
  const [plants, setPlants] = useState([]);
  const [owners, setOwners] = useState({});
  const [isLoading, setIsLoading] = useState(true);
  const toast = useToast();

  const fetchPlants = useCallback(async () => {
    setIsLoading(true);
    try {
      const response = await api.get("/plants/");
      const plantData = response.data.data;

      setPlants(plantData);

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
      const ownerMap = ownerData.reduce(
        (acc, owner) => ({ ...acc, [owner.id]: owner.name }),
        {}
      );

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
    } finally {
      setIsLoading(false);
    }
  }, [toast]);

  useEffect(() => {
    fetchPlants();
  }, [fetchPlants]);

  return {
    plants,
    owners,
    isLoading,
    refreshPlants: fetchPlants
  };
};
