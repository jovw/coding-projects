/*To use this script, following the steps below
0. replace access_token with your access  token.
1. npm start both frontend and backend servers
2. use frontend to log in  via google account, this will establish a cookie session.
3. add product, audience, and company info via frontend forms
4. open a new terminal, navigate to api folder, `node postGeneratedContentRequestTestScript.js` to run the following script.
*/
const http = require('http');

const data = JSON.stringify({
    productId: 5,
    audienceIds: [3, 4, 5],
    tone: ["gentle", "interesting", "bright"],
    platform: ["Facebook"]
});

const options = {
    hostname: 'localhost',
    port: 8080,
    path: '/contents/disperse',
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Cookie': 'access_token=YOUR_ACCESS_TOKEN',
        'Content-Length': data.length
    }
};

const req = http.request(options, (res) => {
    let responseBody = '';

    res.on('data', (chunk) => {
        responseBody += chunk;
    });

    res.on('end', () => {
        console.log('Response:', responseBody);
    });
});

req.on('error', (e) => {
    console.error(`Problem with request: ${e.message}`);
});

req.write(data);
req.end();
