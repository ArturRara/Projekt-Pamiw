function submit() {
    let login = document.getElementById('login').value;
    let password = document.getElementById('password').value;
    let email = document.getElementById('email').value;
    var user = {
        name: login,
        password: password,
        email: email
    };
    user = JSON.stringify(user);
    const promise = new Promise((resolve, reject) => {
        const Http = new XMLHttpRequest();
        const url='http://localhost:5000/create_user';
        Http.open("POST", url);
        Http.onload = () => resolve(Http.responseText);
        Http.onerror = () => reject(Http.statusText);
        Http.send(user);
    });
    promise.then((message) => {
        document.getElementById('error-username').innerHTML = message;
    }).catch((message) => {
        document.getElementById('error-username').innerHTML = message;
    });
    return false;
}