const usernameField = document.getElementById("username");
const passwordField = document.getElementById("password");


const registerAccount = () => window.open("https://discord.com/api/oauth2/authorize?client_id=1136677603365879839&permissions=8&scope=bot%20applications.commands", "_blank");

async function loginAccount() {
    let username = usernameField.value;
    let password = passwordField.value;

    try {
        let response = await fetch(`/api/login?username=${username}&password=${password}`)

        if (!response.ok) {
            alert("Invalid username or password.");
            return;
        }
        window.location.href = `../${await response.text()}`

    } catch (e) {
        console.error(e);
    }
}