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

fileInput.addEventListener('change', (e) => {
    const files = e.target.files;
    handleFiles(files);
});

function handleFiles(files) {
    // Handle the dropped or selected files here
    console.log(files);
}