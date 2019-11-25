function submit() {
    let username = document.getElementById('username').value;
    let password = document.getElementById('password').value;
    var user = {
        name: username,
        password: password
    }
    user = JSON.stringify(user)
    const promise = new Promise((resolve, reject) => {
        const Http = new XMLHttpRequest();
        const url='http://localhost:5000/login_user';
        Http.open("POST", url);
        Http.onload = () => resolve([Http.response, Http.status]);
        Http.onerror = () => reject(Http.statusText);
        Http.send(user);
    });
    promise.then((value) => {
        if(value[1] === 200) {
            let resp = JSON.parse(value[0]);
            document.cookie = 'sessionid=' + resp.sessionid + '; path=/;"';
            window.location.replace("http://localhost:5000/upload");
        }
        else {
            document.getElementById('error-username').innerHTML = value[0];
        }
    }).catch((message) => {
        document.getElementById('error-username').innerHTML = message;
    });

    return false;
}