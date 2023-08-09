const usernameField = document.getElementById("username");
const passwordField = document.getElementById("password");


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