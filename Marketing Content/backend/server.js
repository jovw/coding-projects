require('dotenv').config();
const express = require('express');
const cors = require('cors');
const bodyParser = require("body-parser");
const cookieParser = require('cookie-parser');
const sequelize = require('./models/dbconfig/syncModelsServices');
//api services
const googleAuthRoutes = require('./routes/googleAuthRoutes');
const userRoutes = require('./routes/userRoutes')
const productRoutes = require('./routes/productRoutes');
const audienceRoutes = require('./routes/audienceRoutes');
const contentRoutes = require('./routes/contentRoutes');

const openaiRoutes = require('./routes/openaiRoutes');

const app = express();
app.use(cors({
    origin: 'http://localhost:3000',
    methods: ['GET', 'POST', 'PUT', 'DELETE'],
    credentials: true
}));
app.use(bodyParser.json());

app.use(cookieParser());



app.use((req, res, next) => {
    console.log(`Incoming request: ${req.method} ${req.url}`);
    // // Log authorization header (if present)
    // if (req.headers.authorization) {
    //     console.log('Authorization Header:', req.headers.authorization);
    // } else {
    //     console.log('No Authorization Header present');
    // }
    // console.log(req.cookies)
    next();
});

app.use('/auth/google', googleAuthRoutes);
app.use('/', userRoutes);
app.use('/', productRoutes);
app.use('/', audienceRoutes);
app.use('/', contentRoutes);
app.use('/', openaiRoutes);

const port = process.env.PORT || 8080;
app.listen(port, () => console.log('App listening on port ' + port));
