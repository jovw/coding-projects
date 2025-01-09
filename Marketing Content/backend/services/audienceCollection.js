//import data models for GET POST requests
const User = require('../models/User');
const Product = require('../models/Product');
const Audience = require('../models/Audience');
const Content = require('../models/Content');
const authService = require('./authService');


exports.addUserAudiences = async (req, res) => {
    try {
        // Find the user by their Google sub
        const user = await User.findOne({ where: { googlesub: req.user.sub } });
        
        if (!user) {
            return res.status(404).json({ message: 'User not found' });
        }

        // Create the new audience associated with the user
        const newAudience = await Audience.create({
            audienceName: req.body.audienceName,
            audienceDescription: req.body.audienceDescription,
            userId: user.id  // Ensure the product is associated with the user
        });

        res.status(200).json(newAudience);
    } catch (error) {
        console.error('Error adding product:', error);
        res.status(500).json({ message: 'Server error while adding product.' });
    }
};

exports.editUserAudiencesById = async (req, res) => {
    try {
        const user = await User.findOne({ where: { googlesub: req.user.sub } });

        if (!user) {
            return res.status(404).json({ message: 'User not found' });
        }

        const audienceId = req.params.audienceId;
        const audience = await Audience.findOne({ where: { id: audienceId, userId: user.id } });

        if (!audience) {
            return res.status(404).json({ message: 'Audience not found or does not belong to the user' });
        }

        const { audienceName, audienceDescription } = req.body;

        await audience.update({
            audienceName: audienceName || audience.audienceName, // Keep existing name if not provided
            audienceDescription: audienceDescription || audience.audienceDescription // Keep existing description if not provided
        });
    
        res.status(200).json({ message: `Audience with ID ${audienceId} has been updated.`, audience });

    } catch (error) {
        console.error('Error deleting user audience:', error);
        res.status(500).json({ message: 'Server error while deleting user audience.' });
    }
};

exports.deleteAllAudiences = async (req, res) => {
    try {
        await Audience.destroy({ where: {} });
        res.status(200).json({ message: 'All audiences have been deleted.' });
    } catch (error) {
        console.error('Error deleting all audiences:', error);
        res.status(500).json({ message: 'Server error while deleting all audiences.' });
    }
};

exports.deleteUserAudienceById = async (req, res) => {
    try {
        const user = await User.findOne({ where: { googlesub: req.user.sub } });

        if (!user) {
            return res.status(404).json({ message: 'User not found' });
        }

        const audienceId = req.params.audienceId;
        const audience = await Audience.findOne({ where: { id: audienceId, userId: user.id } });

        if (!audience) {
            return res.status(404).json({ message: 'Audience not found or does not belong to the user' });
        }

        await Audience.destroy({ where: { id: audienceId } });
        res.status(200).json({ message: `Audience with ID ${audienceId} has been deleted.` });
    } catch (error) {
        console.error('Error deleting user audience:', error);
        res.status(500).json({ message: 'Server error while deleting user audience.' });
    }
};


exports.getAudiences = async (req, res) => {
    Audience.findAll().then(audiences => {
        res.json(audiences);
    }) 
}

exports.getUserAudiences = async (req, res) => {
    try {
        const user = await User.findOne({
            where: { googlesub: req.user.sub },
            include: { model: Audience, as: 'Audiences' }
        });

        if (!user) {
            return res.status(404).json({ message: 'User not found' });
        }
        res.json(user.Audiences);
    } catch (error) {
        console.error('Error fetching user audiences:', error);
        res.status(500).json({ message: 'Server error while retrieving products.' });
    }
};

exports.getUserAudiencesById = async (req, res) => {
    try {
        const user = await User.findOne({ where: { googlesub: req.user.sub } });

        if (!user) {
            return res.status(404).json({ message: 'User not found' });
        }

        const audienceId = req.params.audienceId;
        const audience = await Audience.findOne({ where: { id: audienceId, userId: user.id } });

        if (!audience) {
            return res.status(404).json({ message: 'Audience not found or does not belong to the user' });
        }

        res.json(audience);
    } catch (error) {
        console.error('Error deleting user audience:', error);
        res.status(500).json({ message: 'Server error while deleting user audience.' });
    }
};

exports.getUserAudiencesByIds = async (userId, audienceIds) => {
    try {
        const user = await User.findOne({ where: { googlesub: userId } });

        if (!user) {
            console.error('User not found');
            return null; // Return null or an appropriate error object
        }

        // Find audiences belonging to the user and matching the provided IDs
        const audiences = await Audience.findAll({
            where: {
                id: audienceIds,
                userId: user.id
            }
        });

        if (!audiences || audiences.length === 0) {
            console.error('Audiences not found or do not belong to the user');
            return null; // Return null or an appropriate error object
        }

        return audiences;
    } catch (error) {
        console.error('Error fetching user audiences:', error);
        throw error; // Or return a specific error object
    }
};

