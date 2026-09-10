//define frontend pages shared helper functions

//get JWT token
function getToken() {
    return localStorage.getItem("token");
}

//save JWT token
function setToken(token) {
    localStorage.setItem("token", token);

    const payload = decodeJwt(token);

    if (payload && payload.role) {
        localStorage.setItem("role", payload.role);
    }
}

function getRole() {
    return localStorage.getItem("role");
}

//logout
function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
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

function decodeJwt(token) {
    try {
        const payload = token.split(".")[1];
        return JSON.parse(atob(payload));
    } catch {
        return null;
    }
}


function applyRoleNavigation() {
    const role = getRole();

    document.querySelectorAll("[data-roles]").forEach(function(element) {
        const allowedRoles = element
            .getAttribute("data-roles")
            .split(",");

        if (!allowedRoles.includes(role)) {
            element.style.display = "none";
        }
    });
}