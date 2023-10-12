import { Link, Outlet } from 'react-router-dom';

const MainPage = () => {
    return(
        <>
        <nav>
            <ul>
            <li>
                <Link to="/resources">Resources</Link>
            </li>
            <li>
                <Link to="/resource_types">Resource types</Link>
            </li>
            </ul>
        </nav>
        <hr />
        <Outlet />
        </>
    )
};

export default MainPage;
