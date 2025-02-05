import api from "../api";

export const handleCreatePlant = async (name, description, image, toast, onPlantModalClose, setIsCreatingPlant) => {
  setIsCreatingPlant(true);
  const formData = new FormData();
  formData.append('name', name);
  formData.append('description', description);
  if (image) {
    formData.append('image', image);
  } else {
    formData.append('image', "");
  }

  try {
    const response = await api.post('/plants/create', formData, {
      withCredentials: true
    });
    console.log(response)

    if (!response.status === 200) {
      toast({
        title: 'Plant creation unsuccessful',
        description: 'We have no idea what happened. Please try logging in again or reloading the webpage',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
      return;
    }

    const data = response.data;
    localStorage.setItem('toast', JSON.stringify({
        title: 'Plant created',
        description: `Plant "${data.name}" has been successfully created`,
        status: 'success',
        duration: 5000,
        isClosable: true,
      }));
    onPlantModalClose();
    window.location.reload();
  } catch (error) {
    if (error.status === 401) {
      toast({
        title: 'Unauthorized',
        description: 'You are not logged in',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
      return;
    }
    if (error.status === 500) {
      toast({
        title: 'Image upload not configured',
        description: 'The image upload has not been configured for this web app. Please remove the image from the ad',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
      return;
    }
    toast({
      title: 'Error creating plant',
      description: error.message,
      status: 'error',
      duration: 5000,
      isClosable: true,
    });
  } finally {
    setIsCreatingPlant(false);
  }
};

export const fetchMyPlants = async (toast, setMyPlants) => {
    try {
      const response = await api.get('/plants/own', {
      withCredentials: true
    });
      const filteredPlants = response.data.data;
      setMyPlants(filteredPlants);

      if (filteredPlants.length === 0) {
        toast({
          title: 'No Plants Found',
          description: 'You have not listed any plants yet.',
          status: 'info',
          duration: 5000,
          isClosable: true,
        });
      }
    } catch (error) {
      console.error('Error fetching plants:', error);
      toast({
        title: 'Error',
        description: 'Could not fetch your plants.',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
};

export const handleListMyPlants = (onMyPlantsOpen, toast, setMyPlants) => {
  onMyPlantsOpen();
  fetchMyPlants(toast, setMyPlants).then();
};

export const handleDeletePlant = async (plantId, toast, onDeletionSuccess) => {
  try {
    const response = await api.post(`/plants/${plantId}`, {},{
      withCredentials: true
    });

    if (response.status === 200) {
      toast({
        title: 'Plant deleted',
        description: 'The plant has been successfully deleted.',
        status: 'success',
        duration: 5000,
        isClosable: true,
      });
      onDeletionSuccess();
    } else {
      throw new Error('Failed to delete the plant');
    }
  } catch (error) {
    toast({
      title: 'Error deleting plant',
      description: error.response?.data?.detail || error.message,
      status: 'error',
      duration: 5000,
      isClosable: true,
    });
  }
};
