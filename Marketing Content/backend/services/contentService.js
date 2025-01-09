const audienceRoutes = require('../routes/audienceRoutes');
const productCollection = require('./productCollection');
const audienceCollection = require('./audienceCollection');
const userCollection = require('./userCollection');
const openaiAssistantService = require('./api/openaiAssistantService');

exports.disperseContentInfo = async (req, res) => {
    try {
        const productId = req.body.productId
        const audienceIds = req.body.audienceIds
        const tone = req.body.tone
        const userId = req.user.sub;
        const platform = req.body.platform;

        try {
            // Use productId and audienceIds to fetch data
            const user = await userCollection.fetchUserBySub(userId);
            const userInfo = user.dataValues;
            const products = await productCollection.getProductByIdArg(userId, productId);
            const productData = products.dataValues;
            const audiences = await audienceCollection.getUserAudiencesByIds(userId, audienceIds)
            const audienceData = audiences.map(audience => audience.dataValues);

            //set productDescription and audienceDescriptions here to send to user prompt
            const productName = productData.productName;
            const productDescription = productData.productDescription;
            const audienceDescriptions = audienceData.map(audience => audience.description);
            //set imagePrompt here to send to user prompt
            const imagePrompt = productData.productDescription;

            console.log({
                "userInfo": userInfo,
                "tone": tone,
                "productData": productData,
                "audienceData": audienceData,
                "imagePrompt": imagePrompt
            })

            // Call openai service with the frontend user data
            // Updated to match predefined format and audience descriptions for user prompt use
            const requestData = {
                productId,
                tone,
                platform,
                productName,
                productDescription,
                audienceDescriptions,
                imagePrompt
            };
            const generatedResponse = await openaiAssistantService.generatePost(requestData);

            // Send generated post data to frontend
            res.json(generatedResponse);
        } catch (error) {
            console.error("Error getUserProductsId:", error);
            throw error;
        }
    } catch (error) {
        console.error("Error disperseContentInfo:", error);
        throw error;
    }
}

