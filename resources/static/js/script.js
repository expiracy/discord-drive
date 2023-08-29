const dragDrop = document.getElementById('dragDrop');
const fileInput = document.getElementById('fileInput');
const searchBox = document.getElementById("search");
const directoryDiv = document.getElementById("directory");

console.log(window.location.pathname.split('/'))

const getGuild = () => {
    const pathName = window.location.pathname.split('/');
    return pathName[1];
};

const getDirectoryId =  () => {
    const pathName = window.location.pathname.split('/');
    return pathName[2];
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

const home = () => {
    window.location.href = `/${getGuild()}/0`;
};

const searchFolder = async () => {
    location.href = `${location.origin}/${getGuild()}/${getDirectoryId()}/search?substring=${searchBox.value}&scope=folder`;
};

const searchGuild = async () => {
    location.href = `${location.origin}/${getGuild()}/${getDirectoryId()}/search?substring=${searchBox.value}&scope=guild`;
};

const goTo = (pathName) => {
    window.location.href = `${location.origin}/${pathName}`;
}

const deleteDirectory = async (directoryId) => {
   if (!e) var e = window.event;
    e.cancelBubble = true;
    if (e.stopPropagation) e.stopPropagation();

    if (!window.confirm("Delete folder?")) return;

    try {
        let response =
            await fetch(`${location.href}/../${directoryId}`, {
                method: 'DELETE',
            });

        if (!response.ok) {
            console.error(`Error deleting folder ${directoryId}`);
            return;
        }

        document.getElementById(`directoryDiv${directoryId}`).remove();

    } catch (error) {
        console.error(error)
    }
};

const deleteFile = async (fileId) => {
   if (!e) var e = window.event;
    e.cancelBubble = true;
    if (e.stopPropagation) e.stopPropagation();
    console.log("FILE");

    if (!window.confirm("Delete file?")) return;

    try {
        let response =
            await fetch(`${location.href}/${fileId}`, {
                method: 'DELETE',
            });

        if (!response.ok) {
            console.error(`Error deleting file ${fileId}`);
            return;
        }

        document.getElementById(`fileDiv${fileId}`).remove();

    } catch (error) {
        console.error(error)
    }
};