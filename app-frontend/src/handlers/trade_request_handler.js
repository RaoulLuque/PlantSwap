import {fetchMyPlants} from "./plant_handlers";
import api from "../api";

export const handleTradeRequestClick = (plantId, setIncomingPlantId, toast, setMyPlants, onTradeRequestOpen) => {
    setIncomingPlantId(plantId);
    fetchMyPlants(toast, setMyPlants).then();
    onTradeRequestOpen();
  };

export const handleCreateTradeRequest = async (selectedPlantId, incomingPlantId, message, onTradeRequestClose, toast) => {
    try {
      const response = await api.post(`/requests/create/${selectedPlantId}/${incomingPlantId}`, {
        message: message,
      }, {
        withCredentials: true
      });

      if (response.status === 200) {
        toast({
            title: 'Trade request created',
            description: 'The trade request has been successfully created',
            status: 'success',
            duration: 5000,
            isClosable: true,
        });
          onTradeRequestClose();
      }
    } catch (error) {
        if (error.status === 401) {
          toast({
            title: 'Unauthorized',
            description: 'You are not logged in or are trying to trade a plant that is not yours',
            status: 'error',
            duration: 5000,
            isClosable: true,
          });
        } else if (error.status === 418) {
          toast({
            title: 'You cannot trade with yourself',
            description: 'You are trying to trade a plant with yourself. The server refuses to brew coffee because it is, permanently, a teapot',
            status: 'error',
            duration: 5000,
            isClosable: true,
          });
        } else {
            console.error('Error creating trade request:', error);
            toast({
            title: 'Error while creating the request',
            description: 'An error occurred while creating the trade request. Please try again or try reloading the page/logging in again',
            status: 'error',
            duration: 5000,
            isClosable: true,
          });
        }
    }
  };
