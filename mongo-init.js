// mongo-init.js is the file that will be executed when the container is started.

// Create a new database
db.getSiblingDB('admin').auth(
    process.env.MONGO_USERNAME,
    process.env.MONGO_PASSWORD
);
db = db.getSiblingDB(process.env.MONGO_DB);

// Create a new collection
db.createCollection('users');

// Create a new user
db.createUser({
    user: process.env.MONGO_USERNAME,
    pwd: process.env.MONGO_PASSWORD,
    roles: [
        {
            role: 'readWrite',
            db: process.env.MONGO_DB
        }
    ]
});

