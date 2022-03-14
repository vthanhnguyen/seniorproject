import React from 'react'; //we need this for JSX

import Title from "./components/Title";
import Body from './components/Body';
import Footer from "./components/Footer";
import Get_Profile from "./components/getProfileTable"

function App(){
    return(
        <div>
            <Title/> 
            <Get_Profile/> 
            <Footer/>
        </div>
    )
}

export default App