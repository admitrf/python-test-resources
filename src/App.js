import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'

import MainPage from './components/MainPage'
import ResourcesPage from './components/ResourcesPage'
import ResourceTypesPage from './components/ResourceTypesPage'

function App() {
    return (
        <div className="App">
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<MainPage />} >
                    <Route index element={<Navigate to="resources" />} />
                    <Route path="resources" element={<ResourcesPage />} />
                    <Route path="resource_types" element={<ResourceTypesPage />} />
                </Route>
            </Routes>
        </BrowserRouter>
        </div>
    );
}

export default App;
