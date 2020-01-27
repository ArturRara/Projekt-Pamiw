import React, {Component} from 'react'
import {Login} from './UserFunctions'


class login extends Component {
    constructor() {
        super()
        this.state = {
            login: '',
            password: '',
            errors: {}
        }

        this.onChange = this.onChange.bind(this)
        this.onSubmit = this.onSubmit.bind(this)
    }

    onChange(e) {
        this.setState({[e.target.name]: e.target.value})
    }

    onSubmit(e) {
        e.preventDefault()

        const user = {
            login: this.state.login,
            password: this.state.password
        }

        Login(user).then(res => {
                this.props.history.push(`/profile`)
        })
            .catch(err => {
                console.log(err)
            })
    }

    render() {
        return (
            <div className="container">
                <div className="row">
                    <div className="col-md-6 mt-5 mx-auto">
                        <form noValidate onSubmit={this.onSubmit}>
                            <h1 className="h3 mb-3 font-weight-normal">Please sign in</h1>
                            <div className="form-group">
                                <label htmlFor="login">Login</label>
                                <input
                                    type="login"
                                    className="form-control"
                                    name="login"
                                    placeholder="Enter login"
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
                                    placeholder="password"
                                    value={this.state.password}
                                    onChange={this.onChange}
                                />
                            </div>
                            <button
                                type="submit"
                                className="btn btn-lg btn-primary btn-block"
                            >
                                Sign in
                            </button>
                        </form>
                        <br />
                        <div className="auth-buttons text-center">
                            <button bsStyle="primary" href= "/oauth">
                                Sign in with Twitter
                            </button>
                        </div>
                    </div>

                </div>
            </div>
        )
    }
}

export default login