import React from 'react';
import { Container } from 'react-bootstrap';
import ApplicationSearch from '../components/ApplicationSearch';
import Layout from '../components/Layout';
import '../styles/ApplicationSearch.css';

const Applications = () => {
    return (
        <Layout>
            <Container>
                <h1 className="mb-4">Application Search</h1>
                <p className="text-muted mb-4">
                    Search for applications across all departments and teams
                </p>
                <ApplicationSearch />
            </Container>
        </Layout>
    );
};

export default Applications;
