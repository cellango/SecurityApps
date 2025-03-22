import React from 'react';
import { Container, Navbar, Nav } from 'react-bootstrap';
import { useAuth } from '../contexts/AuthContext';
import logo from '../assets/logo.svg';
import '../styles/Layout.css';

const Layout = ({ children }) => {
    const { token, logout } = useAuth();

    return (
        <div className="app-layout">
            <Navbar bg="dark" variant="dark" expand="lg" className="mb-4">
                <Container>
                    <Navbar.Brand href="/" className="d-flex align-items-center">
                        <div className="logo-container me-2">
                            <img
                                src={logo}
                                className="app-logo"
                                alt="AppSentinel Logo"
                            />
                        </div>
                        AppSentinel
                    </Navbar.Brand>
                    <Navbar.Toggle aria-controls="basic-navbar-nav" />
                    <Navbar.Collapse id="basic-navbar-nav">
                        <Nav className="ms-auto">
                            {token ? (
                                <>
                                    <Nav.Link href="/dashboard">Dashboard</Nav.Link>
                                    <Nav.Link href="/applications">Applications</Nav.Link>
                                    <Nav.Link onClick={logout}>Logout</Nav.Link>
                                </>
                            ) : (
                                <Nav.Link href="/login">Login</Nav.Link>
                            )}
                        </Nav>
                    </Navbar.Collapse>
                </Container>
            </Navbar>
            <Container className="mt-4">
                {children}
            </Container>
        </div>
    );
};

export default Layout;
