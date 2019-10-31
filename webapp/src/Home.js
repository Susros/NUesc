import React, { Component } from 'react';
import io from 'socket.io-client';
import axios from 'axios';

const socket = io(process.env.REACT_APP_API_URL);

class Home extends Component {

    constructor(props) {
        super(props);

        this.state = {
            sound_list: [],
            isloading: true
        }
    }

    componentDidMount() {
        axios.get(process.env.REACT_APP_API_URL + '/soundclass', {
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        }).then(({ data }) => {
            this.setState({ sound_list: data.data, isloading: false });
        }).catch(err => {
            console.log(err);
            this.setState({ isloading: false });
        });

        socket.on('webapp_detected', data => {
            document.getElementById("detected").innerHTML = data.data.sound_event + " Detected !";

            setTimeout(() => {
                document.getElementById("detected").innerHTML = "";
            }, 3000);
        });

        socket.on('webapp_status', data => {
            document.getElementById("pi-status").innerHTML = data;
        });
    }

    onSubmit = (event) => {
        event.preventDefault();

        const soundIndex = event.target.sound.value;

        socket.emit('webapp_setsound', soundIndex);

        document.getElementById("pi-status").innerHTML = "Loading...";

    }

    render() {

        if (this.state.isloading) {
            return null;
        }

        return(
            <div>
                <nav className="navbar navbar-dark bg-dark">
                    <span className="navbar-brand">NUesc</span>

                    <span className="text-white">Prototype</span>
                </nav>

                <div className="container-fluid mt-3">
                    <div className="row">
                    <div className="col-4">
                        <h3 className="text-center">Sound List</h3>
                        <hr/>

                        <form onSubmit={ this.onSubmit }>
                        <div className="form-group">
                            <select className="custom-select" name="sound">
                                { 
                                    this.state.sound_list.map( (sound, index) => 
                                        <option value={ index } key={ index }>{ sound }</option>    
                                    )
                                }
                            </select>
                        </div>

                        <div className="form-group">
                            <input type="submit" className="btn btn-success w-100" value="Set in Pi" id="set-btn"/>
                        </div>
                        </form>
                    </div>
                    <div className="col-8">
                        <h3 className="text-center">Raspberry Pi</h3>
                        <hr/>

                        <div className="container">
                        <div className="alert alert-success" role="alert">
                            <b>Status: </b> <span id="pi-status">Loading...</span>
                        </div>

                        <div className="text-center mt-5 text-danger">
                            <h1 id="detected"></h1>
                        </div>
                        </div>
                    </div>
                    </div>
                </div>
            </div>
        );
    }
}

export default Home;