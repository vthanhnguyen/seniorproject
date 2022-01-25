import React from 'react'; //we need this for JSX
import "../style.css"

function Body(){
    return(
        <div className='body'>
            <ul>
                <li>Humidity: </li>
                <li>Temperature:</li>
                <li>Sunlight:</li>
            </ul>
        </div>
    )
}

export default Body