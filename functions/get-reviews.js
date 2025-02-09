const express = require('express');
const app = express();
const port = process.env.PORT || 3001;
const Cloudant = require('@cloudant/cloudant');

// Initialize Cloudant connection with IAM authentication
async function dbCloudantConnect() {
    try {
        const cloudant = Cloudant({
            plugins: { iamauth: { iamApiKey: 'U-hxif2fOTgvdkWe7z_t5o_manJiacnrtXJGa1vQTqdM' } }, // Replace with your IAM API key
            url: 'https://776331ec-df96-4e33-b7d4-11afa91aa136-bluemix.cloudantnosqldb.appdomain.cloud', // Replace with your Cloudant URL
        });

        const db = cloudant.use('reviews');
        console.info('Connect success! Connected to DB');
        return db;
    } catch (err) {
        console.error('Connect failure: ' + err.message + ' for Cloudant DB');
        throw err;
    }
}

let db;

(async () => {
    db = await dbCloudantConnect();
})();

app.use(express.json());

// Define a route to get all reviews with optional state and ID filters
app.get('/reviews/get/:dealership', (req, res) => {
    const  dealership = req.query.dealership;

    // Create a selector object based on query parameters
    const selector = {};
    if (dealership) {
        selector.dealership = dealership;
    }
    
    /*if (id) {
        selector.id = parseInt(id); // Filter by "id" with a value of 1
    }*/

    const queryOptions = {
        selector,
        //limit: 10,  Limit the number of documents returned to 10
    };

    db.find(queryOptions, (err, body) => {
        if (err) {
            console.error('Error fetching reviews:', err);
            res.status(500).json({ error: 'An error occurred while fetching reviews.' });
        } else {
            const reviews = body.docs;
            res.json(reviews);
        }
    });
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});