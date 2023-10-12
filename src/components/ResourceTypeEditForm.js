import axios from "axios";

import { useState, useEffect } from "react";

const API_URL = process.env.REACT_APP_API_URL + process.env.REACT_APP_API_PREFIX;

const ResourceTypeEditForm = (props) => {
    const [error, setError] = useState(null);
    const [id, setId] = useState(props.data.edited.id);
    const [name, setName] = useState(props.data.edited.name);
    const [max_speed, setMaxSpeed] = useState(props.data.edited.max_speed);

    useEffect( () => {
        setError(false);
        setId(props.data.edited.id);
        setName(props.data.edited.name);
        setMaxSpeed(props.data.edited.max_speed);
    }, [props.data]); 

    const saveEdited = async (e) => {
        e.preventDefault();
        try {
            const data = { id, name, max_speed };
            let response;
            const headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            };
            if (id) {
                const url = API_URL + '/resource_types/' + id;
                response = await axios.put(url, data, {headers});
            } else {
                const url = API_URL + '/resource_types';
                response = await axios.post(url, data, {headers});
            }
            if (response.data.result === 'error') {
                throw new Error(response.data.error);
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
                <label>Maximum speed:&nbsp;
                    <input pattern="[0-9]*" value={max_speed} onChange={(e) => setMaxSpeed(e.target.value)} />
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

export default ResourceTypeEditForm;