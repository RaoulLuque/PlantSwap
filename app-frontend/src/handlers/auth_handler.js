import api from "../api";

export const handleLogin = async (event, onLoginClose, toast) => {
  event.preventDefault();

  const formData = new FormData(event.target);

  try {
    const params = new URLSearchParams();
    params.append('username', formData.get('username'));
    params.append('password', formData.get('password'));

    const response = await api.post('/login/token', params, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      withCredentials: true,
    });
    console.log(response)

    if (response.data.message === 'Login successful') {
      toast({
        title: 'Login successful',
        status: 'success',
        duration: 5000,
        isClosable: true,
      });
      onLoginClose();
    } else {
      toast({
        title: 'Login failed',
        description: 'Incorrect username or password',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  } catch (error) {
    toast({
      title: 'Login failed',
      description: error.response?.data?.detail || 'An error occurred',
      status: 'error',
      duration: 5000,
      isClosable: true,
    });
  }
};
