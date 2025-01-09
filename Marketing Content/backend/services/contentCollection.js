//import data models for GET POST requests
const User = require('../models/User');
const Product = require('../models/Product');
const Audience = require('../models/Audience');
const Content = require('../models/Content');
const authService = require('./authService');

exports.addProductContent = async (postInfo) => {
    // Used in openaiAssistantService.js to save post to backend
    try {
        //Find the product to associate the content with
        let product = await Product.findOne({ where: { id: postInfo.productId } });
        if (!product) {
            throw new Error('Product not found');
        }

        //Create new Content
        const newContent = await Content.create({
            postTitle: postInfo.postTitle,
            postCaption: postInfo.postCaption,
            image: postInfo.image,
            imageDescription: postInfo.imageDescription,
            productId: postInfo.productId // Associate the content with the product
        });
        // Respond with the saved content
        return newContent;
    } catch (error) {
        console.error("Error in addProductContent:", error);
        throw error;
    }

};

exports.getProductContentByProductId = async (req, res) => {
    console.log("getProductContentByProductId");
    try {
        const productId = req.params.productId;
        const content = await Content.findAll({
            where: { productId: productId }
        });
        if (!content || content.length === 0) {
            return res.status(404).json({ error: 'Content not found for this product ID' });
        }
        res.json(content);
    } catch (error) {
        console.error("Error in getProductContentByProductId:", error);
        res.status(500).send({ error: 'An error occurred while fetching content for the specified product ID.' });
    }
};


// exports.getProductsContent = async (req, res) => {
//     console.log("getProductsContent")
//     try {
//         const user = await User.findOne({ where: { googlesub: req.user.sub } })
//         const products = await user.getProducts();
//         res.json(contents)
//     } catch (error) {
//         console.log("Error in getProductsContent:", error);
//         res.status(500).send({ error: 'An error occurred while fetching users products post content.' });
//     }
// };

exports.getContents = async (req, res) => {
    console.log("getContents")
    Content.findAll().then(contents => {
        res.json(contents);
    })
};

