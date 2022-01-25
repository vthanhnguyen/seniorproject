import React from 'react'; //we need this for JSX

import Title from "./components/Title";
import Body from './components/Body';
import Footer from "./components/Footer";

function App(){
    return(
        <div>
            <Title/>
            <Body/>
            <Footer/>
        </div>
    )
}

export default App