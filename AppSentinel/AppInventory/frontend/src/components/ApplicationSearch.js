import React, { useState } from 'react';
import AsyncSelect from 'react-select/async';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';
import { Table } from 'react-bootstrap';

const ApplicationSearch = () => {
    const { token } = useAuth();
    const [selectedApplication, setSelectedApplication] = useState(null);

    const loadOptions = async (inputValue) => {
        console.log('loadOptions called with:', inputValue);
        
        // Trim the input value to handle whitespace
        const trimmedInput = inputValue.trim();
        
        // Only search if we have at least 1 character
        if (trimmedInput.length === 0) {
            console.log('Empty input value, returning empty array');
            return [];
        }

        // Check authentication after allowing input
        if (!token) {
            console.error('No authentication token available');
            return [{ value: 'login', label: 'Please log in to search applications', isDisabled: true }];
        }

        try {
            const baseUrl = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';
            const searchUrl = `${baseUrl}/applications/search?q=${encodeURIComponent(trimmedInput)}`;
            console.log('Making API request to:', searchUrl);
            console.log('Request headers:', {
                'Authorization': `Bearer ${token.substring(0, 10)}...`,
                'Content-Type': 'application/json'
            });
            
            const response = await axios.get(searchUrl, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            });
            
            console.log('API response status:', response.status);
            console.log('API response data:', response.data);
            
            if (!response.data || !Array.isArray(response.data)) {
                console.error('Invalid response format:', response.data);
                return [];
            }
            
            // Ensure we have an array and transform it
            const options = response.data.map(app => ({
                value: app.id,
                label: `${app.name} (${app.department_name || 'No Department'})`,
                description: app.description,
                application: app
            }));
            
            console.log('Transformed options:', options);
            return options;
        } catch (error) {
            console.error('Error searching applications:', error);
            console.error('Error config:', error.config);
            if (error.response) {
                console.error('Response data:', error.response.data);
                console.error('Response status:', error.response.status);
                console.error('Response headers:', error.response.headers);
                if (error.response.status === 401) {
                    return [{ value: 'login', label: 'Session expired. Please log in again.', isDisabled: true }];
                }
            } else if (error.request) {
                console.error('No response received:', error.request);
            }
            return [{ value: 'error', label: 'Error searching applications', isDisabled: true }];
        }
    };

    const handleApplicationSelect = async (selectedOption) => {
        console.log('handleApplicationSelect called with:', selectedOption);
        if (!selectedOption) {
            setSelectedApplication(null);
            return;
        }

        try {
            const response = await axios.get(`/api/applications/${selectedOption.value}`, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });
            setSelectedApplication(response.data);
        } catch (error) {
            console.error('Error fetching application details:', error);
        }
    };

    return (
        <div className="application-search">
            <h2>Search Applications</h2>
            <div className="mb-4">
                <AsyncSelect
                    cacheOptions
                    defaultOptions
                    loadOptions={loadOptions}
                    onChange={handleApplicationSelect}
                    placeholder="Type to search applications..."
                    isClearable
                    className="basic-single"
                    classNamePrefix="select"
                    noOptionsMessage={({ inputValue }) => 
                        !inputValue ? "Type to search..." : 
                        "No applications found"
                    }
                    loadingMessage={() => "Searching..."}
                    debounceTimeout={300}
                    minInputLength={1}
                />
            </div>

            {selectedApplication && (
                <div className="application-details">
                    <h3>Application Details</h3>
                    <Table striped bordered hover>
                        <tbody>
                            <tr>
                                <td><strong>Name</strong></td>
                                <td>{selectedApplication.name}</td>
                            </tr>
                            <tr>
                                <td><strong>Description</strong></td>
                                <td>{selectedApplication.description || 'N/A'}</td>
                            </tr>
                            <tr>
                                <td><strong>Type</strong></td>
                                <td>{selectedApplication.application_type}</td>
                            </tr>
                            <tr>
                                <td><strong>Department</strong></td>
                                <td>{selectedApplication.department_name}</td>
                            </tr>
                            <tr>
                                <td><strong>Team</strong></td>
                                <td>{selectedApplication.team_name}</td>
                            </tr>
                            <tr>
                                <td><strong>Owner</strong></td>
                                <td>{selectedApplication.owner_email || 'N/A'}</td>
                            </tr>
                            <tr>
                                <td><strong>Test Score</strong></td>
                                <td>{selectedApplication.test_score ? `${selectedApplication.test_score.toFixed(1)}%` : 'N/A'}</td>
                            </tr>
                            <tr>
                                <td><strong>Last Security Review</strong></td>
                                <td>{selectedApplication.last_security_review ? new Date(selectedApplication.last_security_review).toLocaleDateString() : 'N/A'}</td>
                            </tr>
                        </tbody>
                    </Table>
                </div>
            )}
        </div>
    );
};

export default ApplicationSearch;
