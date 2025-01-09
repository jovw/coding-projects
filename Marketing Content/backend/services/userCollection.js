//import data models for GET POST requests
const User = require('../models/User');
const Product = require('../models/Product');
const Audience = require('../models/Audience');
const Content = require('../models/Content');
const authService = require('./authService');


exports.addUser = async (userInfo, sub) => {
    try {
        // console.log(userInfo, sub)
        const { firstName, lastName, email, profilePicUrl, companyName = "", companyDescription = "" } = extractUserInfo(userInfo);
        const user = await User.create({
            firstName: firstName,
            lastName: lastName,
            email: email,
            profilePicUrl: profilePicUrl,
            googlesub: sub,
            companyName: companyName,
            companyDescription: companyDescription
        });
        return null
    } catch (error) {
        console.error('Error adding user:', error);
        throw new Error('Server side user data not found error');
    }
};


exports.getAllUsers = async (req, res) => {
    console.log("getAllUsers")
    User.findAll().then(users => {
        res.json(users);
    }) 
}

exports.getUserBySubHttp = async (req, res) => {
    try {
        const user = await exports.fetchUserBySub(req.user.sub);
        if (user) {
            res.json(user);
        } else {
            res.status(404).json({ error: 'User not found' });
        }
    } catch (error) {
        console.error('Error retrieving user:', error);
        res.status(500).json({ message: 'Server error while retrieving user data.' });
    }
};


exports.getUserBySubService = async (sub) => {
    try {
        const user = await exports.fetchUserBySub(sub);
        return user;  // Return user or null
    } catch (error) {
        throw new Error(error.message);  // Propagate the error
    }
};


exports.addUserCompany = async (req, res) => {
    console.log("addUserCompany", req.user.sub)
    try {
        let user = await User.findOne({ where: { googlesub: req.user.sub } });
        // console.log(user)
        if (user) {
            const { companyName, companyDescription } = req.body;
            await user.update({
                companyName: companyName,
                companyDescription: companyDescription
            });
            res.json(user);
        } else {
            res.status(404).json({ error: 'User not found' });
        }
    } catch (error) {
        console.error('Error updating user with company data', error);
        res.status(500).json({ error: 'Server side user data cannot be updated error' });
    }
}


exports.getUserCompany = async (req, res) => {
    console.log("getUserCompany");
    try {
        const user = await exports.fetchUserBySub(req.user.sub);
        if (user) {
            // Extract only the company information to send back
            const { companyName, companyDescription } = user;
            res.json({ companyName, companyDescription });
        } else {
            res.status(404).json({ error: 'User not found or does not have company details.' });
        }
    } catch (error) {
        console.error('Error fetching user company:', error);
        res.status(500).json({ message: 'Server error while retrieving company data.' });
    }
};


exports.fetchUserBySub = async (sub) => {
    // Assuming User model includes company details or related entities
    return User.findOne({
        where: { googlesub: sub },
        attributes: ['firstName', 'lastName', 'email', 'profilePicUrl', 'companyName', 'companyDescription']
    });
}

function extractUserInfo(userInfo) {
    const firstName = userInfo.names[0].givenName || '';
    const lastName = userInfo.names[0].familyName || '';
    const email = userInfo.emailAddresses[0].value || ''; 
    const profilePicUrl = userInfo.photos[0].url || '';
    return { firstName, lastName, email, profilePicUrl };
}
