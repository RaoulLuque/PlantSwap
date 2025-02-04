import api from "../api";

export const handleRegistration = async (event, onRegisterClose, toast) => {
  event.preventDefault();

  const formData = new FormData(event.target);

  try {
    const userData = {
      email: formData.get("email"),
      password: formData.get("password"),
      full_name: formData.get("full_name"),
    };

    const response = await api.post("/users/signup", userData);

    if (response.status === 200) {
      toast({
        title: "Registration successful",
        status: "success",
        duration: 5000,
        isClosable: true,
      });
      onRegisterClose();
    }
  } catch (error) {
    toast({
      title: "Registration failed",
      description: error.response?.data?.detail || "An error occurred",
      status: "error",
      duration: 5000,
      isClosable: true,
    });
  }
};
