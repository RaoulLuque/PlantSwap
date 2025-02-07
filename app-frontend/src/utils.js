export function showStoredToastAfterWindowReload(toast) {
  window.onload = function () {
    const toastData = localStorage.getItem('toast');

    if (toastData) {
      const { title, status, duration, isClosable } = JSON.parse(toastData);

      toast({
        title,
        status,
        duration,
        isClosable,
      });

      // Clear the stored toast information
      localStorage.removeItem('toast');
    }
  };
}
