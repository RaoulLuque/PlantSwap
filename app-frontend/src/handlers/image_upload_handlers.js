export const handleDragOver = (e, setIsDragging) => {
  e.preventDefault();
  setIsDragging(true);
};

export const handleDragEnter = (e, setIsDragging) => {
  e.preventDefault();
  setIsDragging(true);
};

export const handleDragLeave = (e, setIsDragging) => {
  e.preventDefault();
  setIsDragging(false);
};

export const handleDrop = (e, setIsDragging, handleImageChange, toast) => {
  e.preventDefault();
  setIsDragging(false);
  const file = e.dataTransfer.files[0];
  if (file && file.type.startsWith('image/')) {
    handleImageChange(file);
  } else {
    toast({
      title: 'Invalid file type',
      description: 'Please upload an image file.',
      status: 'error',
      duration: 5000,
      isClosable: true,
    });
  }
};
