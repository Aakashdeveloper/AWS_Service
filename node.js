const express = require('express');
const app = express();
const port = 8900;
const Pool = require('pg').Pool;
const bodyParser = require('body-parser');

const pool = new Pool({
    user:'postgres',
    host:'localhost',
    database:'postgres',
    password:'docker',
    port:5432
});

app.use(bodyParser.urlencoded({extended:false}));
app.use(bodyParser.json())


app.get('/user', (req,res) => {
    pool.query('SELECT * FROM employee', (err,result) => {
        if(err){
            throw err
        }else{
            res.status(200).send(result.rows)
        }
    })
})

app.post('/addUser', (req,res) => {
    const {city,name,phone} = req.body;
    pool.query('INSERT INTO employee (city,name,phone) VALUES ($1,$2,$3)' [city,name,phone],(err,result) => {
        if(err){
            throw err;
        }else{
            res.status(200).send('data inserted')
        }

    })
})

app.listen(port, () => {
    console.log(`Server is running on port ${port}`)
}) 