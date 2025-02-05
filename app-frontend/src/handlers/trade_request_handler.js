import {fetchMyPlants} from "./plant_handlers";
import api from "../api";

export const handleTradeRequestClick = (plantId, setIncomingPlantId, toast, setMyPlants, onTradeRequestOpen) => {
    setIncomingPlantId(plantId);
    fetchMyPlants(toast, setMyPlants).then();
    onTradeRequestOpen();
  };

export const handleCreateTradeRequest = async (selectedPlantId, incomingPlantId, message, onTradeRequestClose) => {
    try {
      const response = await api.post(`/requests/create/${selectedPlantId}/${incomingPlantId}`, {
        message: message,
      }, {
        withCredentials: true
      });

      if (response.status === 200) {
        onTradeRequestClose();
        // Optionally, show a success toast or refresh the page
      }
    } catch (error) {
      console.error('Error creating trade request:', error);
      // Optionally, show an error toast
    }
  };
