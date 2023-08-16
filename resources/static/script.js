const dragDrop = document.getElementById('dragDrop');
const fileInput = document.getElementById('fileInput');
const searchBox = document.getElementById("search");
const directoryDiv = document.getElementById("directory");

const getGuild = () =>{
    const pathName = window.location.pathname.split('/');
    return pathName[pathName.length - 2];
};

const getDirectoryId =  () => {
    const pathName = window.location.pathname.split('/');
    return pathName[pathName.length - 1];
};

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

dragDrop.addEventListener('drop', async (e) => {
    e.preventDefault();
    e.stopPropagation();
    dragDrop.style.border = '2px dashed #ccc';
    const files = e.dataTransfer.files;
    await handleFiles(files);
});

dragDrop.addEventListener('click', () => {
    fileInput.click();
});

fileInput.addEventListener("change", async (e) => {
    const files = e.target.files;
    await handleFiles(files);
});

searchBox.addEventListener('keyup', async (e) => {
    if (e.key === 'Enter') {
        console.log(`${location.origin}/${getGuild()}/search?substring=${searchBox.value}`)
        location.href = `${location.origin}/${getGuild()}/search?substring=${searchBox.value}`
    }
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

        location.reload();
    } catch (e) {
        console.error(e);
    }
}

async function createFolder() {
    let folderName = prompt("Folder name:");

    if (folderName === '') return;

    console.log(folderName);
     try {
        let response = await fetch(`/api/create_folder${window.location.pathname}?name=${folderName}`)

        if (!response.ok) {
            alert("Error creating folder.");
            return;
        }

        console.log(response);

         location.reload();

    } catch (e) {
        console.error(e);
    }
}