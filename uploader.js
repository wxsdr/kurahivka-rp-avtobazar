// uploader.js
async function uploadImageToImgBB(file) {
    const API_KEY = '7ef81dfc56bab94048936358f8fb9097'; // Встав сюди свій ключ
    const formData = new FormData();
    formData.append('image', file);

    try {
        const response = await fetch(`https://api.imgbb.com/1/upload?key=${API_KEY}`, {
            method: 'POST',
            body: formData
        });
        const result = await response.json();
        if (result.success) {
            return result.data.url;
        } else {
            throw new Error("Помилка завантаження");
        }
    } catch (error) {
        console.error(error);
        return null;
    }
}
