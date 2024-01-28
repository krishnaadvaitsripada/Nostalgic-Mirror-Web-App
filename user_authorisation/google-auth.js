const axios = require('axios');
const config = require('../config/config.json').web;

function getNewLoginUrl() {
    const url = `https://accounts.google.com/o/oauth2/v2/auth?
    client_id=${config.google.client_id}&
    redirect_uri=${config.google.redirect_uris[0]}&
    access_type=offline&
    response_type=code&
    scope=https://www.googleapis.com/auth/photoslibrary.readonly&
    state=new_access_token&
    include_granted_scopes=true&
    prompt=consent`;
    return axios.get(url);
}

function getNewRefreshToken(code) {
    var data = {
        client_id: config.client_id,
        client_secret: config.client_secret,
        code,
        redirect_uri: config.google.redirect_uris[0],
        grant_type: 'authorization_code'
    };
    const axiosConfig = {
        method: "post",
        url: "https://oauth2.googleapis.com/token",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        params: data,
    };
    return axios(axiosConfig);
}

function getAccessToken(refreshToken) {
    var params = {
        client_id: config.client_id,
        client_secret: config.client_secret,
        refresh_token: refreshToken,
        grant_type: 'refresh_token'
    };
    const apiConfig = {
        method: "post",
        url: "https://oauth2.googleapis.com/token",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        params,
    };
    return axios(apiConfig);

}

module.exports = {
    getNewLoginUrl,
};