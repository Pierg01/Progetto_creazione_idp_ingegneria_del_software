const express = require("express")
const fs = require("fs")
const path = require("path")
const jsonwebtoken = require("jsonwebtoken")
const {json} = require("express");

const app = express()


app.use("/",express.static(path.join(__dirname,"./Archivio/ResourceServer_files")))
app.use("/:token/:key",express.static(path.join(__dirname,"./Archivio/AccessoResourceServer_files")))

app.get("/",(req,res)=>{
    fs.readFile("./Archivio/ResourceServer.html",(err, data)=>{
        console.log(path.join(__dirname,"Archivio/ResourceServer_files"))
        res.write(data)
    })
})


app.use("/:token/:key",(req,res,next)=>{
    console.log("Sono entrato")
    const {token,key} = req.params
    const user = jsonwebtoken.decode(token,{
        key: key,
        algorithm:"HS256"
    })
    if (user === null){
        app.use("/token/:key",express.static(path.join("Archivio/AccessoFallito_files")))
        fs.readFile("Archivio/AccessoFallito.html",(err,data)=>{
            res.write(data)
        })
    }
    else if (user.exp > Date.now()+1){
        res.redirect("http://localhost:3000/refresh_token")
    }
    next()

})
app.use("/:token/:key",express.static(path.join(__dirname,"Archivio/AccessoResourceServer_files")))

app.get("/:token/:key",(req,res)=>{
    fs.readFile("./Archivio/AccessoResourceServer.html",(err,data)=>{
        if (err)
            console.log(err)
        res.write(data)
    })
})





app.listen(2000,()=>{
    console.log("Sto ascoltando")
})