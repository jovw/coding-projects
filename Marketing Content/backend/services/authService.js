const axios = require('axios');
const { v4: uuidv4 } = require('uuid');
const { OAuth2Client } = require('google-auth-library');
const userCollection = require('../services/userCollection');

const CLIENT_ID = process.env.CLIENT_ID;
const CLIENT_SECRET = process.env.CLIENT_SECRET;
const REDIRECT_URI = process.env.REDIRECT_URI;
const client = new OAuth2Client(CLIENT_ID);

exports.handleLogin = async (req, res) => {
    const state = uuidv4().substring(0, 10);
    const authUrl = `https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id=${CLIENT_ID}&redirect_uri=${REDIRECT_URI}&scope=https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile&state=${state}&access_type=offline&prompt=consent`;

    res.redirect(authUrl);
};

exports.handleOAuth = async (req, res) => {
    try {
        const code = req.query.code;
        if (!code) {
            return res.status(400).send('Authorization code not found');
        }

        const tokens = await postAccessToken({ code });
        if (!tokens) {
            return res.status(500).send('Failed to retrieve tokens');
        }

        const payload = await verifyToken(tokens.id_token);
        if (payload && payload.sub) {
            const userInfo = await getUserInfo(tokens.access_token);
            let userStatus;
            const existingUser = await userCollection.getUserBySubService(payload.sub);

            if (!existingUser) {
                await userCollection.addUser(userInfo, payload.sub);
                userStatus = "User added";
            } else {
                userStatus = "User found";
            }
            // console.log(tokens)

            setAuthCookies(res, tokens.access_token, tokens.id_token, tokens.refresh_token);
            res.redirect('http://localhost:3000/profile');
        } else {
            res.status(500).json({ message: 'Failed to retrieve user info' });
        }
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Failed' });
    }
};

exports.handleLogout = async (req, res) => {
    try {
        const accessToken = req.cookies.access_token;
        const idToken = req.cookies.id_token;
        const refreshToken = req.cookies.refresh_token;

        if (!accessToken || !idToken || !refreshToken) {
            return res.status(401).json({ message: "Tokens not provided" });
        }

        if (accessToken) {
            try {
                await revokeToken(accessToken);
                res.status(200).json({ status: "Logged out successfully" });
            } catch (error) {
                console.error("Failed to revoke token:", error);
                try {
                    const newTokens = await refreshTokens(res, refreshToken);
                    const payload = await verifyToken(newTokens.id_token);
                    const userInfo = await getUserInfo(newTokens.access_token);
                    await revokeToken(newTokens.access_token);
                    res.status(200).json({ status: "Logged out successfully" });
                } catch (error) {
                    res.status(500).json({ message: 'Failed to revoke token', error: error.message });
                }
            }
        } else {
            console.log("No access token found, user possibly already logged out.");
            res.status(200).json({ status: "No active session found or user already logged out" });
        }

    } catch (error) {
        console.error("Error during logout process:", error);
        res.status(500).json({ message: 'Failed to process logout due to server error' });
    }
};

exports.handleAuthenticateToken = async (req, res, next) => {
    try {
        // console.log("handleAuthenticateToken")
        // console.log(req.cookies)
        const accessToken = req.cookies.access_token;
        const idToken = req.cookies.id_token;
        const refreshToken = req.cookies.refresh_token;

        if (!accessToken || !idToken || !refreshToken) {
            return res.status(401).json({ message: "Tokens not provided" });
        }

        try {
            const payload = await verifyToken(idToken);
            const userInfo = await getUserInfo(accessToken);

            req.user = { ...userInfo, sub: payload.sub };
            console.log("next()")
            next();
        } catch (error) {
            console.log("Token verification error:", error);
            try {
                const newTokens = await refreshTokens(res, refreshToken);
                const payload = await verifyToken(newTokens.id_token);
                const userInfo = await getUserInfo(newTokens.access_token);

                req.user = { ...userInfo, sub: payload.sub };
                next();
            } catch (refreshError) {
                console.error("Failed to refresh token:", refreshError);
                return res.status(401).json({ message: "Failed to refresh token" });
            }
        }
    } catch (error) {
        console.error("Authentication error:", error);
        res.status(500).json({ message: "Internal server error during authentication" });
    }
};

async function refreshTokens(res, refreshToken) {
    const newTokens = await postAccessToken({ refreshToken });

    if (newTokens && newTokens.access_token) {
        setAuthCookies(res, newTokens.access_token, newTokens.id_token, refreshToken);
        return newTokens;
    } else {
        throw new Error("Failed to refresh token");
    }
}

function setAuthCookies(res, access_token, id_token, refresh_token) {

    res.cookie('access_token', access_token, {
        httpOnly: false,
        secure: false,
        sameSite: 'Lax',
        path: '/',
        domain: 'localhost' // Adjust domain if needed
    });
    res.cookie('id_token', id_token, {
        httpOnly: false,
        secure: false,
        sameSite: 'Lax',
        path: '/',
        domain: 'localhost' // Adjust domain if needed
    });
    res.cookie('refresh_token', refresh_token, {
        httpOnly: false,
        secure: false,
        sameSite: 'Lax',
        path: '/',
        domain: 'localhost' // Adjust domain if needed
    });
}

async function getUserInfo(accessToken) {
    // console.log("accessToken: ", accessToken)
    const apiUrl = 'https://people.googleapis.com/v1/people/me?personFields=names,emailAddresses,photos';
    const headers = { 'Authorization': `Bearer ${accessToken}` };
    
    try {
        const response = await axios.get(apiUrl, { headers });
        return response.data;
    } catch (error) {
        console.error('Error fetching user info:', error);
        throw new Error('Invalid access token');
    }
}

async function postAccessToken({ code, refreshToken }) {
    const token_url = 'https://oauth2.googleapis.com/token';
    
    const data = new URLSearchParams(
        refreshToken ? {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'refresh_token': refreshToken,
            'grant_type': 'refresh_token'
        } : {
            'code': code,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'redirect_uri': REDIRECT_URI,
            'grant_type': 'authorization_code',
            'access_type': 'offline'
        }
    ).toString();

    try {
        const response = await axios.post(token_url, data, {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
        });
        return response.data;
    } catch (error) {
        console.error('Error fetching access token:', error);
        return null;
    }
}

async function verifyToken(token) {
    try {
        const ticket = await client.verifyIdToken({
            idToken: token,
            audience: CLIENT_ID,
        });
        const payload = ticket.getPayload();
        return payload;
    } catch (error) {
        console.error('Error verifying ID token:');
        throw new Error('Invalid ID token');
    }
}

async function revokeToken(accessToken) {
    const revokeUrl = `https://oauth2.googleapis.com/revoke?token=${accessToken}`;
    try {
        await axios.post(revokeUrl);
        console.log("Token revoked successfully.");
    } catch (error) {
        console.error("Failed to revoke token:", error);
        throw new Error("Failed to revoke token");
    }
}
