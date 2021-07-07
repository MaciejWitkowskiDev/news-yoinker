const Examples = () => {
    let response = ""
    
    var axios = require("axios").default;

    var options = {
    method: 'GET',
    url: 'https://api.nasa.gov/insight_weather/',
    params: {
        api_key: '4OhRgtV01G0mbJlc5Q8dekZjCrwI0Go3C5bCqU5O',
        feedtype: 'json',
        version: 1.0
    }
    };

    axios.request(options).then(function (response) {
        console.log(response.data);
    }).catch(function (error) {
        console.error(error);
    });

    return(
        <>
            {response}
        </>
    );

    
}

export default Examples;