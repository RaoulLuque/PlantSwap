import {fetchMyPlants} from "./plant_handlers";
import api from "../api";

const handleTradeError = (error, toast) => {
  const status = error.response?.status;
  const defaultMessage = error.response?.data?.detail || 'An unexpected error occurred';

  const errorConfigs = {
    401: {
      title: 'Unauthorized',
      description: 'You need to be logged in to perform this action',
    },
    403: {
      title: 'Forbidden',
      description: 'You do not have permission for this action',
    },
    404: {
      title: 'Not Found',
      description: 'The requested resource was not found',
    },
    409: {
      title: 'Conflict',
      description: 'Trade request already exists',
    },
    418: {
      title: 'Teapot',
      description: 'Cannot trade with yourself',
    },
    default: {
      title: 'Error',
      description: defaultMessage,
    }
  };

  const { title, description } = errorConfigs[status] || errorConfigs.default;

  toast({
    title,
    description,
    status: 'error',
    duration: 5000,
    isClosable: true,
  });
};

export const handleListTradeRequests = async (onOpen, toast, setTradeRequests) => {
  try {
    const response = await api.get('/requests/all/', { withCredentials: true });

    if (!response.data?.data) {
      setTradeRequests([]);
      onOpen();
      return;
    }

    // Enrich with plant data
    const plantRequests = response.data.data.flatMap(tr => [
      api.get(`/plants/${tr.outgoing_plant_id}`, { withCredentials: true }),
      api.get(`/plants/${tr.incoming_plant_id}`, { withCredentials: true })
    ]);

    const plantResponses = await Promise.all(plantRequests);
    const plantMap = new Map();

    plantResponses.forEach(response => {
      if (response.data) {
        plantMap.set(response.data.id, response.data);
      }
    });

    // Map integer status to its string representation
    const statusMapping = {
      0: 'pending',
      1: 'accepted',
      2: 'declined'
    };

    const enrichedRequests = response.data.data.map(tr => ({
      ...tr,
      outgoing_plant: plantMap.get(tr.outgoing_plant_id),
      incoming_plant: plantMap.get(tr.incoming_plant_id),
      status: statusMapping[tr.status] || 'unknown'
    }));

    setTradeRequests(enrichedRequests);
    onOpen();

  } catch (error) {
    handleTradeError(error, toast);
  }
};

export const handleDeleteTradeRequest = async (outgoingId, incomingId, toast, onSuccess) => {
  try {
    await api.post(
      `/requests/delete/${outgoingId}/${incomingId}`,
      {},
      { withCredentials: true }
    );

    toast({
      title: 'Request Deleted',
      description: 'Trade request has been successfully removed',
      status: 'success',
      duration: 5000,
      isClosable: true,
    });

    onSuccess();

  } catch (error) {
    handleTradeError(error, toast);
  }
};

export const handleAcceptTradeRequest = async (outgoingId, incomingId, toast, onSuccess) => {
  try {
    await api.post(
      `/requests/accept/${outgoingId}/${incomingId}`,
      {},
      { withCredentials: true }
    );

    toast({
      title: 'Request Accepted',
      description: 'Trade request has been successfully accepted',
      status: 'success',
      duration: 5000,
      isClosable: true,
    });

    onSuccess();

  } catch (error) {
    handleTradeError(error, toast);
  }
};

export const handleDeclineTradeRequest = async (outgoingId, incomingId, toast, onSuccess) => {
  try {
    await api.post(
      `/requests/reject/${outgoingId}/${incomingId}`,
      {},
      { withCredentials: true }
    );

    toast({
      title: 'Request Accepted',
      description: 'Trade request has been successfully declined',
      status: 'success',
      duration: 5000,
      isClosable: true,
    });

    onSuccess();

  } catch (error) {
    handleTradeError(error, toast);
  }
};

export const handleTradeRequestClick = (plantId, setIncomingPlantId, toast, setMyPlants, onTradeRequestOpen) => {
  setIncomingPlantId(plantId);
  fetchMyPlants(toast, setMyPlants).then();
  onTradeRequestOpen();
};

export const handleCreateTradeRequest = async (selectedPlantId, incomingPlantId, message, onTradeRequestClose, toast, setIsSubmittingTradeRequest) => {
  setIsSubmittingTradeRequest(true);
  try {
    await api.post(
      `/requests/create/${selectedPlantId}/${incomingPlantId}`,
      { message },
      { withCredentials: true }
    );

    toast({
      title: 'Trade Request Created',
      description: 'Your trade request has been successfully submitted',
      status: 'success',
      duration: 5000,
      isClosable: true,
    });

    onTradeRequestClose();
    setIsSubmittingTradeRequest(false);
  } catch (error) {
    handleTradeError(error, toast);
    setIsSubmittingTradeRequest(false);
  }
};
