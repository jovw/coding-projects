//import data models for GET POST requests
const User = require('../models/User');
const Product = require('../models/Product');
const Audience = require('../models/Audience');
const Content = require('../models/Content');
const authService = require('./authService');


exports.initGen = async (req, res) => {
    console.log("addUserCompany")
    try{
        let user = await User.findOne({googlesub: req.user.sub});
        if(user){
            console.log(req.body)
            const {companyName, companyDescription} = req.body;
            await user.update({
                companyName: companyName,
                companyDescription: companyDescription
            });
            res.json(user);
        }else{
            res.status(404).json({error: 'User not found'});
        }
    }catch(error){
        console.error('Error updating user with company data', error);
        res.status(500).json({error: 'Server side user data cannot be updated error'});
    }
}
