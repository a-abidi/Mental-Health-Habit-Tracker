import React from 'react';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import './Login.scss';

export default class Login extends React.Component {
    constructor(props){
        super(props);
    }

    render() {
        return (
            <div className="Main">
                <Form onSubmit={() => this.props.logIn()}>
                    <Form.Group>
                        <Form.Label>Username</Form.Label>
                        <Form.Control placeholder="Enter username" />
                    </Form.Group>
                    <Button variant="primary" type="submit">Log In</Button>
                </Form>
            </div>
        );
    }
}
