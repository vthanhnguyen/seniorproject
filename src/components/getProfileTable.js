import React, {useState, useEffect} from "react";


function Get_profile(){
    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    var raw = JSON.stringify({
    "profileid": 3
    });

    var requestOptions = {
    method: 'GET',
    headers: myHeaders,
    redirect: 'follow'
    };
    
    const [plant, setPlant] = useState("");

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch('/getprofile', requestOptions)
                let data = await response.json();
                setPlant(data[0]);
            } catch (error) {
                console.log("error", error);
            }
        };
        fetchData();
    }, []);

    console.log(plant)

    return (
        <div>
            <p>ProfileID: {plant.profileid}</p>
            <p>ProfileName: {plant.profilename}</p>
            <p>PlantThreshold: {plant.threshold}</p>
        </div>)
}

export default Get_profile;