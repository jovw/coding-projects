
const OpenAI = require("openai");
const { addProductContent } = require('../contentCollection');
const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

async function createAssistant() {
    return await openai.beta.assistants.create({
        name: "Marketing Content Generator",
        instructions: "You are a personalized marketing content generator. Generate marketing content per requirements.",
        tools: [{ type: "code_interpreter" }],
        model: "gpt-4o"
    });
}

// Generate text post
async function generateTextPost(assistantId, user_input) {
    const thread = await openai.beta.threads.create();
    await openai.beta.threads.messages.create(
        thread.id,
        {
            role: "user",
            content: user_input
        }
    );
    const run = await openai.beta.threads.runs.create(thread.id, {
        assistant_id: assistantId,
        instructions: "Please provide the response in the following JSON format: { \"title\": \"Your Title Here\", \"caption\": \"Your Caption Here\" }",
    });
    console.log(run);
    return { threadId: thread.id, runId: run.id };
}

// Generate image via Dalle
async function generateImagePost(imagePrompt) {
    try {
        const image = await openai.images.generate({
            model: "dall-e-3",
            prompt: imagePrompt
        });
        console.log(image.data);
        const imageData = image.data[0];
        return imageData;
    } catch (error) {
        console.error("Error generating image:", error);
        throw error;
    }
}

async function checkStatus(threadId, runId) {
    let runStatus = await openai.beta.threads.runs.retrieve(threadId, runId);
    while (runStatus.status !== "completed") {
        console.log("Run is not completed. Waiting...");
        await new Promise(resolve => setTimeout(resolve, 5000));
        runStatus = await openai.beta.threads.runs.retrieve(threadId, runId);
    }
    return runStatus;
}

async function extractContent(threadId) {
    const messages = await openai.beta.threads.messages.list(threadId);
    for (const msg of messages.data) {
        if (msg.role === 'assistant') {
            console.log(msg);
            let content = msg.content[0].text.value;
            console.log(content);
            //Parse json response
            try {
                //clean up json file
                content = content.replace(/`/g, ''); // Remove backticks
                // Escape double quotes correctly
                content = content.replace(/\\n/g, '\\n')
                    .replace(/\\"/g, '\\\\"')
                    .replace(/\\'/g, '\\\'')
                    .replace(/""/g, '\\"')
                    .replace(/([a-zA-Z])"([a-zA-Z])/g, '$1\\"$2'); // Fix unescaped quotes

                console.log('Content before parsing:', content);
                //parse content
                let jsonResponse = JSON.parse(content);
                return jsonResponse;
            } catch (error) {
                console.error("Failed to parse JSON response:", error);
            }
        }

    }
    return null;
}

async function generatePost(requestData) {

    // get data from disperseContentInfo function inside contentService.js
    const tone = requestData.tone;
    const platform = requestData.platform;
    const productName = requestData.productName;
    const productDescription = requestData.productDescription;
    const audienceDescriptions = requestData.audienceDescriptions;
    const imagePrompt = requestData.imagePrompt;
    const productId = requestData.productId;

    try {
        const assistant = await createAssistant();

        const user_prompt = `I need to generate a new post title and a post caption for marketing. 
        Please use the following writing tone: ${tone} . Targeted platform: ${platform}. 
        Product name: ${productName}. Product description: ${productDescription}. Targeted audience: ${audienceDescriptions}.`;

        const { threadId, runId } = await generateTextPost(assistant.id, user_prompt);
        await checkStatus(threadId, runId);
        const postContent = await extractContent(threadId);
        if (!postContent || !postContent.title || !postContent.caption) {
            throw new Error("Title or caption not found in the content.");
        }
        console.log(`Extracted Generated Post Title: ${postContent.title} `);
        console.log(`Extracted Generated Post Caption: ${postContent.caption} `);

        // generate image based on imagePrompt from frontend
        const postImage = await generateImagePost(imagePrompt);
        console.log(`Post Image URL: ${postImage.url} `);
        console.log(`Post Image Description: ${postImage.revised_prompt} `);

        //save to backend
        let postInfo = {
            postTitle: postContent.title,
            postCaption: postContent.caption,
            image: postImage.url,
            imageDescription: postImage.revised_prompt,
            productId: productId //use actual product ID
        };
        await addProductContent(postInfo);
        console.log(`Saving post to backend successfully`);
        return postInfo;

    } catch (error) {
        console.error("Error generating and saving text:", error);
    }

}

module.exports = {
    generatePost
};
