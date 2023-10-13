import axios from "axios";

import { useCallback, useEffect, useMemo, useState } from "react";

import ResourceTypeEditForm from "./ResourceTypeEditForm";

const API_URL = process.env.REACT_APP_API_URL + process.env.REACT_APP_API_PREFIX;

const ResourceTypesPage = () => {
    const emptyItem = useMemo(() => {
        return {
            id: 0,
            name: '',
            max_speed: 0
        }
    }, []);

    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [refreshData, setRefreshData] = useState(0);
    const [refreshChild, setRefreshChild] = useState(0);
    const [edited, setEdited] = useState(emptyItem)

    const checkedIds = [];

    const getData = useCallback(async () => {
        setEdited(emptyItem);
        setLoading(true);
        try {
            const response = await axios.get(API_URL + `/resource_types`);
            setData(response.data);
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
    }, [emptyItem]);
    
    useEffect(() => {
        getData();
    }, [refreshData, getData]);

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

    const onEditItem = (id, name, max_speed) => {
        setEdited({
            'id': id,
            'name': name,
            'max_speed': max_speed
        });
    }

    const onAddNew = () => {
        setEdited(emptyItem);
        setRefreshChild(refreshChild + 1);
    }

    const onDeleteItem = async (id) => {
        try {
            let url = API_URL + '/resource_types/' + id;
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
            let url = API_URL + '/resource_types?ids=' + checkedIds.join(',');
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
                <table border={1}>
                    <thead>
                        <tr>
                            <th>&nbsp;</th>
                            <th>Type name</th>
                            <th>Maximum speed</th>
                            <th>&nbsp;</th>
                            <th>&nbsp;</th>
                        </tr>
                    </thead>
                    <tbody>
                        {data.map(row => 
                            <tr key={row.id}>
                                <td><input type="checkbox" onChange={(e) => onIdSelect(e, row.id)} /></td>
                                <td>{row.name}</td>
                                <td>{row.max_speed}</td>
                                <td><button onClick={(e) => onEditItem(row.id, row.name, row.max_speed)}>edit</button></td>
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
                <ResourceTypeEditForm data={{'edited': edited, 'refreshChild': refreshChild}} onSave={(e) => setRefreshData(refreshData + 1)} />
            </>
        
    }

    return (
        <div>
            <h1>Resource types</h1>
            {showData()}
        </div>
    );
}

export default ResourceTypesPage;