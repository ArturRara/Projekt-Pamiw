import axios from 'axios'

export const Register = newUser => {
    return axios
        .post('register', {
            login: newUser.login,
            password: newUser.password,
            email: newUser.email
        })
        .then(response => {
            console.log('Registered')
        })
}

export const Login = user => {
    return axios
        .post('', {
            login: user.login,
            password: user.password
        })
        .then(response => {
            localStorage.setItem('usertoken', response.data)
            return response.data
        })
        .catch(err => {
            console.log(err)
        })
}

export const getProfile = user => {
    return axios
        .get('profile', {
            //headers: { Authorization: ` ${this.getToken()}` }
        })
        .then(response => {
            console.log(response)
            return response.data
        })
        .catch(err => {
            console.log(err)
        })
}