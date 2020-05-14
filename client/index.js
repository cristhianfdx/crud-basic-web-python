const express = require('express');
const app = express();

const path = require('path');

//Settings
app.set('port', process.env.PORT || 3000);


//Static files
app.use(express.static(path.join(__dirname, 'public')));

//Server
app.listen(app.get('port'), ()=> {
    console.log('Listen on port', app.get('port'));
});