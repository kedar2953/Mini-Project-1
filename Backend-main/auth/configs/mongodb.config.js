const mongoose = require('mongoose');
require('dotenv').config();
// exports.mongoConnect = mongoose
//     .connect(process.env.MONGO_URI, {
//         useNewUrlParser: true,
//         useUnifiedTopology: true,
//     }, () => {
//         console.log(`Auth-Service DB Connected`);
//     })

const mongoConnect=()=>{
    mongoose.connect(process.env.MONGO_URI, {
        useNewUrlParser: true,
        useUnifiedTopology: true,
    }).then(()=>{
        console.log("Connected ")
    }).catch((err)=>{
        console.err(err);
    })

}
module.exports=mongoConnect;

// mongoose.connection.on('connected', (err) => {
//     if (err) {
//         console.log("my error");
//         console.log(err);
//     }
//     console.log('Mongoose connected to db');
// })

// mongoose.connection.on('error', (err) => {
//     console.log('error',err.message)
// })

// mongoose.connection.on('disconnected', () => {
//     console.log('Mongoose connection is disconnected.')
// })

// process.on('SIGINT', async () => {
//     await mongoose.connection.close()
//     process.exit(0)
// })