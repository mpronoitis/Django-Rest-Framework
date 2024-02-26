const contentContainer = document.getElementById('content-container');
const loginForm = document.getElementById('login-form');
const baseEndpont = "http://localhost:8000/api"
const loginButton = document.getElementById('login-form-submit');
if (loginForm) {
    loginForm.addEventListener('submit', handleLogin);
}

function handleLogin(event) {
    event.preventDefault(); // prevent the form from submitting
    const loginEndpoint = `${baseEndpont}/token/`;
    let loginFormData = new FormData(loginForm);
    let loginObjectData = Object.fromEntries(loginFormData);
    let loginData = JSON.stringify(loginObjectData);
    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: loginData
    };
    fetch(loginEndpoint, options)
        .then(response => response.json())
        .then(data => handleAuthData(data,getProductList))
        .catch(error => console.log(error));
}

    function handleAuthData(authData,callback) {
        localStorage.setItem('access', authData.access);
        localStorage.setItem('refresh', authData.refresh);
        if (callback) {
            callback();
        }
    }

    function writeToContainer(data) {
        contentContainer.innerHTML = "<pre>" + JSON.stringify(data) + "</pre>";
    }

    function getProductList() {
        const endpoint = `${baseEndpont}/products/`;
        const options = {
            method: 'GET',
            headers: {
                "Content-type": "application/json",
                "Authorization": `Bearer ${localStorage.getItem('access')}`
        } 
    };
        fetch(endpoint, options)
        .then(response => response.json())
        .then(data => writeToContainer(data))
        .catch(error => console.log(error));
    };






