const jsonwebtoken = require("jsonwebtoken");
const fs = require("fs");
// const PATH_TO_PUB = __dirname + "/../private.pem";
// const PUB_KEY = fs.readFileSync(PATH_TO_PUB, "utf8");
require('dotenv').config();
const PATH_TO_PUB=process.env.JWT_SECRET;
// const PUB_KEY=fs.readFileSync(PATH_TO_PUB,"utf-8")
// const expiresIn = process.env.EXPIRATION_TIME;

const signJWT = async (payload) => {
  return new Promise((resolve, reject) => {
    if (payload?.userId) {
      jsonwebtoken.sign(
        payload,
        PATH_TO_PUB,
        { expiresIn: "24h" },
        (error, signedToken) => {
          if (error) {
            reject(error);
            return;
          }
          resolve(signedToken);
          return;
        }
      );
    } else reject("Payload not provided");
  });
};

module.exports = {
  signJWT,
};
