import axios from "axios";

import { useState, useEffect } from "react";

const API_URL = process.env.REACT_APP_API_URL + process.env.REACT_APP_API_PREFIX;

const ResourceEditForm = (props) => {
    const [error, setError] = useState(null);
    const [id, setId] = useState(props.data.edited.id);
    const [name, setName] = useState(props.data.edited.name);
    const [cur_speed, setCurSpeed] = useState(props.data.edited.cur_speed);
    const [resource_type, setResourceType] = useState(props.data.edited.resourceType);

    useEffect( () => {
        setError(false);
        setId(props.data.edited.id);
        setName(props.data.edited.name);
        setCurSpeed(props.data.edited.cur_speed);
        setResourceType(props.data.edited.resource_type);
    }, [props.data]); 

    const resourceTypes = props.data.resource_types

    const saveEdited = async (e) => {
        e.preventDefault();
        try {
            const data = { id, name, cur_speed, resource_type };
            const headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            };
            if (id) {
                const url = API_URL + '/resources/' + id;
                await axios.put(url, data, {headers});
            } else {
                const url = API_URL + '/resources';
                await axios.post(url, data, {headers});
            }
            setError(null);
            props.onSave();
        } catch (err) {
            if (err.response?.data) {
                setError(err.response.data.error);
            } else {
                setError(err.message);
            }
        }
    }

    const showData = () => {
        if (error) {
            return <div>{`There is a problem with saving - ${error}`}</div>
        }
        return <>
            <form>
                <input type="hidden" value={id} /><br />
                <label>
                    Name:&nbsp;<input type="text" value={name}  onChange={(e) => setName(e.target.value)} />
                </label><br />
                <label>Type:&nbsp;
                    <select value={resource_type} onChange={(e) => setResourceType(e.target.value)}>
                        <option key="0" value="0">--not selected--</option>
                        {resourceTypes.map(row => 
                            <option key={row.id} value={row.id}>{row.name}</option>
                        )}
                    </select>
                </label><br />
                <label>Current speed:&nbsp;
                    <input pattern="[0-9]*" value={cur_speed} onChange={(e) => setCurSpeed(e.target.value)} />
                </label><br />
                <button onClick={saveEdited}>Save</button>
            </form>
        </>
    };

    return (
        <div>
            {showData()}
        </div>
    );
}

export default ResourceEditForm;