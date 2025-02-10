export function showStoredToastAfterWindowReload(toast) {
  // Check immediately in case the component mounted after load event
  const checkAndShowToast = () => {
    const toastData = localStorage.getItem('toast');
    if (toastData) {
      const { title, status, duration, isClosable } = JSON.parse(toastData);
      toast({
        title,
        status,
        duration,
        isClosable,
      });
      localStorage.removeItem('toast');
    }
  };

  // If document is already loaded, run immediately
  if (document.readyState === 'complete') {
    checkAndShowToast();
  } else {
    // Otherwise wait for load event
    window.addEventListener('load', checkAndShowToast);
  }
}
