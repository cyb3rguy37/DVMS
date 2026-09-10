//define frontend pages shared helper functions

//get JWT token
function getToken() {
    return localStorage.getItem("token");
}

//save JWT token
function setToken(token) {
    localStorage.setItem("token", token);
}

//logout
function logout() {
    localStorage.removeItem("token");
    window.location.href = "/login";
}

//login protection
function requireLogin() {
    if (!getToken()) {
        window.location.href = "/login";
    }
}

//showing messages
function showMessage(elementId, type, message) {
    const element = document.getElementById(elementId);

    element.innerHTML = `
        <div class="alert alert-${type}">
            ${message}
        </div>
    `;
}