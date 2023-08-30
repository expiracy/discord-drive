# Discord Drive (Proof of Concept)

This app is a simple proof of concept for a file storage solution that utilizes a storage server hosted on Discord. It allows users to upload and download files of any size by breaking them into 8MB chunks for efficient storage and retrieval. The app is built using an async Quart web server and the Discord.py API for integration with Discord.

## Details

- **File Upload:** Users can upload files of any size to the storage server. The app automatically divides the files into 8MB chunks before uploading.
- **File Download:** When users download files, the app reassembles the chunks into the original file, ensuring data integrity.
- **Technology Stack:** The app is built using an async Quart web server for handling web requests and the Discord.py API for interacting with Discord servers.
- **Purpose:** This app is designed as a proof of concept to demonstrate the feasibility of using Discord as a platform for file storage and retrieval.

## Setup

1. **Navigate to Login/Register:** Access the app's URL and navigate to the login/register page.
2. **Register Bot:** Click on the register button to add the bot to your desired storage Discord server.
3. **Bot Registration:** Once the bot is added, type the command `/register_server {password}` in the Discord server to complete the registration.
4. **Login:** Log in to the app using your credentials.
5. **File Management:** After logging in, you can perform various file operations such as uploading, downloading, and creating folders as needed.

Please note that this app is a proof of concept and may not be suitable for production use. It showcases the core functionalities of chunked file upload, storage on Discord, and efficient retrieval.

## Images
![login](https://cdn.discordapp.com/attachments/1138939435044573378/1146385319869038643/image.png)
![main](https://cdn.discordapp.com/attachments/1138939435044573378/1146383670618378280/image.png)
