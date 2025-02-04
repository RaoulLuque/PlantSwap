import api from "../api";

export const handleCreatePlant = async (name, description, image, toast, onPlantModalClose) => {
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
  }
};
