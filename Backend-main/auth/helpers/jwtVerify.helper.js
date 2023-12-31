const jsonwebtoken = require("jsonwebtoken");
const fs = require("fs");
// const PATH_TO_PRIV = __dirname + "/../private.pem";
require('dotenv').config();
// const PATH_TO_PRIV=process.env.JWT_SECRET;
// const PRIV_KEY = fs.readFileSync(PATH_TO_PRIV, "utf8");
const PRIV_KEY=process.env.JWT_SECRET
const verifyJWT = async (accessToken) => {
  return new Promise((resolve, reject) => {
    if (accessToken)
      jsonwebtoken.verify(accessToken, PRIV_KEY, (error, payload) => {
        if (error) {
          reject(error);
          return;
        }
        resolve(payload);
        return;
      });
    else reject("Access Token not provided");
  });
};

module.exports = {
  verifyJWT,
};
