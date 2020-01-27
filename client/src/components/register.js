import React, { Component } from 'react'
import { Register } from './UserFunctions'


function validate(login, password, email) {
    const errors = [];

    if (login.length === 0) {
        errors.push("Name can't be empty");
    }

    if (email.length < 5) {
        errors.push("Email should be at least 5 charcters long");
    }
    if (email.split("").filter(x => x === "@").length !== 1) {
        errors.push("Email should contain a @");
    }
    if (email.indexOf(".") === -1) {
        errors.push("Email should contain at least one dot");
    }

    if (password.length < 4) {
        errors.push("Password should be at least 4 characters long");
    }

    return errors;
}

class register extends Component {
    constructor() {
        super()
        this.state = {
            login: '',
            password: '',
            email: '',
            errors: {}
        }

        this.onChange = this.onChange.bind(this)
        this.onSubmit = this.onSubmit.bind(this)
    }

    onChange(e) {
        this.setState({ [e.target.name]: e.target.value })
    }
    onSubmit(e) {
        e.preventDefault()

        const newUser = {
            login: this.state.login,
            password: this.state.password,
            email: this.state.email
        }
        const errors = validate(newUser.login, newUser.password, newUser.email);
        if (errors.length > 0) {
            this.setState({ errors });
            return;
        }

        Register(newUser).then(res => {
            this.props.history.push(`/`)
        })
    }

    render() {
        return (
            <div className="container">
                <div className="row">
                    <div className="col-md-6 mt-5 mx-auto">
                        <form noValidate onSubmit={this.onSubmit}>
                            <h1 className="h3 mb-3 font-weight-normal">Register</h1>
                            <div className="form-group">
                                <label htmlFor="login">Login</label>
                                <input
                                    type="text"
                                    className="form-control"
                                    name="login"
                                    placeholder="Enter your login"
                                    value={this.state.login}
                                    onChange={this.onChange}
                                />
                            </div>

                            <div className="form-group">
                                <label htmlFor="password">Password</label>
                                <input
                                    type="password"
                                    className="form-control"
                                    name="password"
                                    placeholder="Password"
                                    value={this.state.password}
                                    onChange={this.onChange}
                                />
                                <div className="form-group">
                                    <label htmlFor="email">Email address</label>
                                    <input
                                        type="email"
                                        className="form-control"
                                        name="email"
                                        placeholder="Enter email"
                                        value={this.state.email}
                                        onChange={this.onChange}
                                    />
                                </div>
                            </div>
                            <button
                                type="submit"
                                className="btn btn-lg btn-primary btn-block"
                            >
                                Register!
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        )
    }
}

export default register
