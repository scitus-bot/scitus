const Discord = require("discord.js");
const client = new Discord.Client()


// as soon as it logs in
client.on("ready", () => {
    console.log(`Logged in as ${client.user.tag}!`); // backticks for easier concatanation???
})

client.on("message", msg => {
    if (msg.content === "ping") {
        msg.reply("pong");
    }
})


client.login("no auth code for you !");