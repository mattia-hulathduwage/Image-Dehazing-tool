document.getElementById('dehazeButton').addEventListener('click', () => {
    const fileInput = document.getElementById('imageInput');
    if (fileInput.files.length === 0) {
        alert('Please upload an image first.');
        return;
    }

    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('image', file);

    fetch('/dehaze', {
        method: 'POST',
        body: formData
    })
    .then(response => response.blob())
    .then(blob => {
        const imageURL = URL.createObjectURL(blob);
        document.getElementById('originalImage').src = URL.createObjectURL(file);
        document.getElementById('dehazedImage').src = imageURL;

        // Enable the save button
        const saveButton = document.getElementById('saveButton');
        saveButton.disabled = false;
        saveButton.dataset.imageUrl = imageURL; // Store the image URL for saving
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

document.getElementById('saveButton').addEventListener('click', () => {
    const saveButton = document.getElementById('saveButton');
    const imageURL = saveButton.dataset.imageUrl;
    
    if (imageURL) {
        const link = document.createElement('a');
        link.href = imageURL;
        link.download = 'dehazed_image.png'; // Set the default filename
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    } else {
        alert('No image to save.');
    }
});
