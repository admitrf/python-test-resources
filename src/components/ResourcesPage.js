import axios from "axios";

import { useCallback, useEffect, useMemo, useState } from "react";

import ResourceEditForm from "./ResourceEditForm";

const API_URL = process.env.REACT_APP_API_URL + process.env.REACT_APP_API_PREFIX;

const ResourcesPage = () => {
    const emptyItem = useMemo(() => {
        return {
            id: 0,
            name: '',
            resource_type: 0,
            cur_speed: 0
        }
    }, []);

    const [data, setData] = useState(null);
    const [typesData, setTypesData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [curType, setCurType] = useState(0)
    const [refreshData, setRefreshData] = useState(0);
    const [refreshChild, setRefreshChild] = useState(0);
    const [edited, setEdited] = useState(emptyItem)

    const checkedIds = [];

    const getData = useCallback(async () => {
        setEdited(emptyItem);
        setLoading(true);
        try {
            let url = API_URL + '/resources' + (curType ? '?resource_type=' + curType :'');
            let response = await axios.get(url);
            setData(response.data);
            url = API_URL + '/resource_types'
            response = await axios.get(url);
            setTypesData(response.data);
            setError(null);
        } catch (err) {
            if (err.response?.data) {
                setError(err.response.data.error);
            } else {
                setError(err.message);
            }
            setData(null);
        } finally {
            setLoading(false);
        }
    }, [curType, emptyItem]);
    
    useEffect(() => {
        getData();
    }, [curType, refreshData, getData]);

    const setResourceType = (event) => {
        setCurType(event.target.value)
        setRefreshData(refreshData + 1)
    }

    const isIdChecked = (id) => {
        return checkedIds.includes(id);
    }

    const onIdSelect = (e, id) => {
        if (e.target.checked) {
            if (!isIdChecked(id))
                checkedIds.push(id)
        } else {
            const index = checkedIds.indexOf(id);
            if (index > -1) {
                checkedIds.splice(index, 1);
            }
        }
    }

    const onEditItem = (id, name, resource_type, cur_speed) => {
        setEdited({
            'id': id,
            'name': name,
            'resource_type': resource_type.id,
            'cur_speed': cur_speed
        });
    }

    const onAddNew = () => {
        setEdited(emptyItem);
        setRefreshChild(refreshChild + 1);
    }

    const onDeleteItem = async (id) => {
        try {
            let url = API_URL + '/resources/' + id;
            const response = await axios.delete(url);
            setError(null);
            const index = checkedIds.indexOf(id);
            if (index > -1) {
                checkedIds.splice(index, 1);
            }
            if (response.data?.deleted > 0){
                setRefreshData(refreshData + 1);
            }
        } catch (err) {
            if (err.response?.data) {
                setError(err.response.data.error);
            } else {
                setError(err.message);
            }
        }
    }

    const onDeleteSelected = async () => {
        if (checkedIds.length === 0) {
            return;
        }
        try {
            let url = API_URL + '/resources?ids=' + checkedIds.join(',');
            const response = await axios.delete(url);
            setError(null);
            checkedIds.length = 0;
            if (response.data?.deleted > 0){
                setRefreshData(refreshData + 1);
            }
        } catch (err) {
            if (err.response?.data) {
                setError(err.response.data.error);
            } else {
                setError(err.message);
            }
        }
    }

    const showData = () => {
        if (loading) {
            return <div>A moment please...</div>
        };
        if (error) {
            return <div>{`There is a problem fetching the post data - ${error}`}</div>
        }
        return <>
                <div>
                    Resource type:
                    <select value={curType} onChange={setResourceType}>
                        <option value={0}>--not selected--</option>
                        {typesData.map(row => 
                            <option key={row.id} value={row.id}>{row.name}</option>
                        )}
                    </select>
                    <p/>
                </div>
                <table border={1}>
                    <thead>
                        <tr>
                            <th>&nbsp;</th>
                            <th>Resource name</th>
                            <th>Resource type</th>
                            <th>Current speed</th>
                            <th>Speed excess, %</th>
                            <th>&nbsp;</th>
                            <th>&nbsp;</th>
                        </tr>
                    </thead>
                    <tbody>
                        {data.map(row => 
                            <tr key={row.id}>
                                <td><input type="checkbox" onChange={(e) => onIdSelect(e, row.id)} /></td>
                                <td>{row.name}</td>
                                <td>{row.resource_type.name}</td>
                                <td>{row.cur_speed}</td>
                                <td>{row.speed_excess}</td>
                                <td><button onClick={(e) => onEditItem(row.id, row.name, row.resource_type, row.cur_speed)}>edit</button></td>
                                <td><button onClick={(e) => onDeleteItem(row.id)}>delete</button></td>
                            </tr>
                        )}
                    </tbody>
                </table>
                <div>
                    <button onClick={(e) => onDeleteSelected()}>Delete selected</button>
                    <button onClick={(e) => onAddNew()}>Add new</button>
                </div>
                <p/>
                <ResourceEditForm data={{'edited': edited, 'resource_types': typesData, 'refreshChild': refreshChild}} onSave={(e) => setRefreshData(refreshData + 1)} />
            </>
        
    }

    return (
        <div>
            <h1>Resources</h1>
            {showData()}
        </div>
    );
}

export default ResourcesPage;