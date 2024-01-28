const axios = require('axios');

function getAllMedia(accessToken, pageToken, pageSize=2){
    let finalSet = [];
    return new Promise((resolve, reject) => {
        const params = {
            pageSize: pageSize,
            pageToken: pageToken,
        };
        const config = {
            method: "get",
            url: "https://photoslibrary.googleapis.com/v1/mediaItems",
            headers: {
                "Content-Type": "application/json",
                authorization: "Bearer" + accessToken
            },
            params: params,
        };
        axios(config)
            .then((response) => {
                const nextPageToken = response.data.nextPageToken;
                const mediaItems = response.data.mediaItems;
                mediaItems.forEach((item) => {
                    finalSet.push(item.baseUrl);
                });
                if(nextPageToken){
                    getAllMedia(accessToken, nextPageToken).then((data) => {
                        finalSet = finalSet.concat(data);
                        resolve(finalSet);
                    });
                } else {
                    resolve(finalSet);
                }
                
            })
            .catch((error) => {
                reject(error);
            });
    });
}