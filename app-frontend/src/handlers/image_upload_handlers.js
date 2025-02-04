export const handleImageChange = (eventOrFile, toast, setImage, setImagePreview) => {
    let file;
    if (eventOrFile.target) {
      // If it's an event object (from file input)
      file = eventOrFile.target.files[0];
    } else {
      // If it's a File object (from drag-and-drop)
      file = eventOrFile;
    }

    if (file && file.type.startsWith('image/')) {
      setImage(file);
      setImagePreview(URL.createObjectURL(file));
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

export const handleDrop = (e, setIsDragging, toast, setImage, setImagePreview) => {
  e.preventDefault();
  setIsDragging(false);
  const file = e.dataTransfer.files[0];
  if (file && file.type.startsWith('image/')) {
    handleImageChange(file, toast, setImage, setImagePreview);
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
