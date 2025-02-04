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
      localStorage.setItem('toast', JSON.stringify({
        title: 'Login successful',
        status: 'success',
        duration: 5000,
        isClosable: true,
      }));
      onLoginClose();
      window.location.reload();
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

export const handleLogout = async (toast) => {
  try {
    const response = await api.post("/logout", {}, { withCredentials: true });

    if (response.data.message === "Logout successful") {
      localStorage.setItem('toast', JSON.stringify({
        title: "Logout successful",
        status: "success",
        duration: 5000,
        isClosable: true,
      }));
      window.location.reload();
    }
  } catch (error) {
    toast({
      title: "Logout failed",
      description: error.response?.data?.detail || "An error occurred",
      status: "error",
      duration: 5000,
      isClosable: true,
    });
  }
};

export const checkUserLoggedIn = async () => {
  try {
    const response = await api.get('/users/me', { withCredentials: true });

    return response.status === 200;
  } catch (error) {
    if (!error.response?.status === 401) {
      console.error('Error checking user login status:', error);
    }
    return false;
  }
};
