import api from "../api";

export const handleRegistration = async (event, onRegisterClose, toast) => {
  event.preventDefault();

  const formData = new FormData(event.target);

  const password = formData.get("password");
  const confirmPassword = formData.get("confirmPassword");

  // Check if the passwords match
  if (password !== confirmPassword) {
    toast({
      title: "Passwords do not match",
      description: "Please ensure both password fields are identical.",
      status: "error",
      duration: 3000,
      isClosable: true,
    });
    return;
  }

  // Build the user data object for signup
  const userData = {
    email: formData.get("email"),
    password: password,
    full_name: formData.get("full_name"),
  };

  try {
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
