const dragDrop = document.getElementById('dragDrop');
const fileInput = document.getElementById('fileInput');

dragDrop.addEventListener('dragover', (e) => {
    e.preventDefault();
    e.stopPropagation();
    dragDrop.style.border = '2px dashed #999';
});

dragDrop.addEventListener('dragleave', (e) => {
    e.preventDefault();
    e.stopPropagation();
    dragDrop.style.border = '2px dashed #ccc';
});

dragDrop.addEventListener('drop', (e) => {
    e.preventDefault();
    e.stopPropagation();
    dragDrop.style.border = '2px dashed #ccc';
    const files = e.dataTransfer.files;
    handleFiles(files);
});

dragDrop.addEventListener('click', () => {
    fileInput.click();
});

fileInput.addEventListener('change', async (e) => {
    const files = e.target.files;
    await handleFiles(files);
});

async function handleFiles(files) {
    // Handle the dropped or selected files here

    console.log(files);

    const formData = new FormData();

    for (let i = 0; i < files.length; i++)
        formData.append('files', files[i]);

    try {
        let response =
            await fetch(`/api/upload_files${window.location.pathname}`, {
                method: 'POST',
                body: formData
            });

        let text = await response.text();

        if (!response.ok) {
            console.error(text);
            return;
        }

        console.log(text);

    } catch (e) {
        console.error(e);
    }
}