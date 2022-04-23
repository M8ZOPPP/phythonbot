const mongo = require('mongodb').MongoClient;
const { Telegraf, session, Extra, Markup, Scenes } = require('telegraf');
const axios = require ("axios");
const ratelimit = require("ratelimit")
const { BaseScene, Stage } = Scenes
const { enter, leave } = Stage
const stage = new Stage()
const rateLimit = require('telegraf-ratelimit')
var bot_token = '2044018822:AAFlFaiUn_UYrBBdz1Lr5m-8jH0O4HbPvWE'; //YOUR BOT TOKEN HERE
const bot = new Telegraf(bot_token);
let db;
const balance = new BaseScene('balance')
stage.register(balance)
const referal = new BaseScene('refferal')
stage.register(referal)
const withdraw = new BaseScene('withdraw')
stage.register(withdraw)
const wallet = new BaseScene('wallet')
stage.register(wallet)
const onWithdraw = new BaseScene('onWithdraw')
stage.register(onWithdraw)
const broadcast = new BaseScene('broadcast')
stage.register(broadcast)
const refer = new BaseScene('refer')
stage.register(refer)
const mini = new BaseScene('mini')
stage.register(mini)
const chnl = new BaseScene('chnl')
stage.register(chnl)
const removechnl = new BaseScene('removechnl')
stage.register(removechnl)
const paychnl = new BaseScene('paychnl')
stage.register(paychnl)
const bon = new BaseScene('bonus')
stage.register(bon)
const botstat = new BaseScene('botstat')
stage.register(botstat)
const withstat = new BaseScene('withstat')
stage.register(withstat)
const tgid = new BaseScene('tgid')
stage.register(tgid)
const incr = new BaseScene('incr')
stage.register(incr)
const subwallet = new BaseScene('subwallet')
stage.register(subwallet)
const mkey = new BaseScene('mkey')
stage.register(mkey)
const mid = new BaseScene('mid')
stage.register(mid)
const comment = new BaseScene('comment')
stage.register(comment)
var regex = new RegExp('.*')
const buttonsLimit = {
    window: 1000,
    limit: 1,
    onLimitExceeded: (ctx, next) => {
      if ('callback_query' in ctx.update)
      ctx.answerCbQuery('You`ve pressed Buttons too often, Wait......', true)
        .catch((err) => sendError(err, ctx))
    },
    keyGenerator: (ctx) => {
      return ctx.callbackQuery ? true : false
    }
  }
  bot.use(rateLimit(buttonsLimit))

bot.use(session())
bot.use(stage.middleware())
//CONNECT TO MONGO
mongo.connect('mongodb+srv://DATA1:xixMhPpvLbKh24Ng@cluster0.qnjvk.mongodb.net/myFirstDatabase?retryWrites=true&w=majority', { useUnifiedTopology: true }, (err, client) => {
    if (err) {
        console.log(err);
    }
    db = client.db('Demot1');
    bot.telegram.deleteWebhook().then(success => {
        success && console.log('ðŸ¤– Bot Has Been SuccessFully Registered')
        bot.launch();
    })
})

//START WITH INVITE LINK
bot.hears(/^\/start (.+[1-9]$)/, async (ctx) => {
    try {
        let admin = await db.collection('admindb').find({ admin: "admin" }).toArray()
        if (admin.length == 0) {
            db.collection('admindb').insertOne({ admin: "admin", ref: 1, cur: 'INR', paychannel: '@jsjdkkdkdhsjdk', bonus: 0.1, minimum: 1, botstat: 'Active', withstat: 'ON', subwallet: 'NOT SET', MKEY: 'NOT SET', MID: 'NOT SET', channels: [] })
            ctx.replyWithMarkdown(
                '*ðŸ˜…Restart Bot With /start*'
            )
        }
        let currency = admin[0].cur
        let refer = admin[0].ref
        let bots = admin[0].botstat
        let channel = admin[0].channels
        if (bots == 'Active') {
            let data = await db.collection('allUsers').find({ userID: ctx.from.id }).toArray()
            if (data.length == 0 && ctx.from.id != +ctx.match[1]) { //IF USER IS NOT IN DATA
                db.collection('allUsers').insertOne({ userID: ctx.from.id, balance: 0.00, toWithdraw: 0.00 })
                db.collection('balance').insertOne({ userID: ctx.from.id, balance: 0.00,toWithdraw:0.00 })
                db.collection('pendingUsers').insertOne({ userID: ctx.from.id, inviter: +ctx.match[1] })
                bot.telegram.sendMessage(+ctx.match[1], "<b>ðŸš§ New User On Your Invite Link : <a href='tg://user?id=" + ctx.from.id + "'>" + ctx.from.id + "</a></b>", { parse_mode: 'html' })
            }
            bot.telegram.sendMessage(ctx.from.id,"*Â©Share Your Contact In Order To Start Using The Bot. This Is Just A Phone Number Verification\n\nâš ï¸Note : We Will Not Share Your Details With Anyone*",{parse_mode:"markdown",reply_markup:{keyboard: [[{text:"ðŸ’¢ Share Contact",request_contact:true}]],resize_keyboard: true}})
        } else {
            ctx.replyWithMarkdown('*â›” Bot Is Currently Off*')
        }
    } catch (error) {
        console.log(error)
    }

})
//START WITHOUT INVITE LINK
bot.start(async (ctx) => {
    try {
        let data = await db.collection('allUsers').find({ userID: ctx.from.id }).toArray()
        let admin = await db.collection('admindb').find({ admin: "admin" }).toArray()
        if (admin.length == 0) {
            db.collection('admindb').insertOne({ admin: "admin", ref: 1, cur: 'INR', paychannel: '@jsjdkkdkdhsjdk', bonus: 0.1, minimum: 1, botstat: 'Active', withstat: 'ON', subwallet: 'NOT SET', MKEY: 'NOT SET', MID: 'NOT SET', channels: [] })
            ctx.replyWithMarkdown(
                '*ðŸ˜…Restart Bot With /start*'
            )
        }
        let bots = admin[0].botstat
        if (bots == 'Active') {
            if (data.length == 0) { //IF USER IS NOT IN DATA
                db.collection('allUsers').insertOne({ userID: ctx.from.id, balance: 0 ,toWithdraw:0.00})
                db.collection('balance').insertOne({ userID: ctx.from.id, balance: 0 ,toWithdraw:0.00})
                db.collection('pendingUsers').insertOne({ userID: ctx.from.id })

            }
            let channel = admin[0].channels
            bot.telegram.sendMessage(ctx.from.id,"*Â©Share Your Contact In Order To Start Using The Bot. This Is Just A Phone Number Verification\n\nâš ï¸Note : We Will Not Share Your Details With Anyone*",{parse_mode:"markdown",reply_markup:{keyboard: [[{text:"ðŸ’¢ Share Contact",request_contact:true}]],resize_keyboard: true}})
        } else {
            ctx.replyWithMarkdown('*â›” Bot Is Currently Off*')
        }
    } catch (error) {
        console.log(error)
    }
})
bot.on("contact", async(ctx)=> {
  try {
    var cont = ctx.update.message.contact.phone_number
    if (ctx.update.message.forward_from){
      bot.telegram.sendMessage(ctx.from.id,"*âš ï¸Seems Like This Is Not Your Contact*",{parse_mode:"markdown"})
      db.collection('pendingUsers').insertOne({ userID: ctx.from.id, inviter: "" })
      return
    }
    if(cont.startsWith("91")){
      let admin = await db.collection('admindb').find({ admin: "admin" }).toArray()
        let refer = admin[0].ref
        let currency = admin[0].cur
        let bots = admin[0].botstat
        if (bots == 'Active') {
            let channel = admin[0].channels
            var flag = 0;
            for (i in channel) {
                let res = await bot.telegram.getChatMember(channel[i], ctx.from.id)
                let result = res.status
                if (result == 'creator' || result == 'administrator' || result == 'member') {
                    flag += 1
                } else {
                    flag = 0
                }
            }
            if (flag == channel.length) {
                ctx.replyWithMarkdown(
                    '*ðŸ¡ Welcome To Main Menu*', { reply_markup: { keyboard: [['ðŸ’° Balance'], ['ðŸ™ŒðŸ» Invite', 'ðŸŽ Bonus', 'ðŸ—‚ Wallet'], ['ðŸ’³ Withdraw', 'ðŸ“Š Statistics']], resize_keyboard: true } }
                )
                let userdata = await db.collection('pendingUsers').find({ userID: ctx.from.id }).toArray()
                let config = await db.collection('allUsers').find({ userID: ctx.from.id }).toArray()
                if (('inviter' in userdata[0]) && !('referred' in config[0])) {
                    let bal = await db.collection('balance').find({ userID: userdata[0].inviter }).toArray()
                    let cur = bal[0].balance * 1
                    let ref = refer * 1
                    let final = ref + cur
                    bot.telegram.sendMessage(userdata[0].inviter, "*ðŸ’°" + refer + " " + currency + " Added To Your Balance*", { parse_mode: 'markdown' })
                    bot.telegram.sendMessage(ctx.from.id, "*?? To Check Who Invited You, Click On 'âœ… Check'*", { parse_mode: 'markdown', reply_markup: { inline_keyboard: [[{ text: "âœ… Check", callback_data: "check" }]] } })
                    db.collection('allUsers').updateOne({ userID: ctx.from.id }, { $set: { inviter: userdata[0].inviter, referred: 'DONE' } }, { upsert: true })
                    db.collection('balance').updateOne({ userID: userdata[0].inviter }, { $set: { balance: final } }, { upsert: true })
                }
            } else {
                mustjoin(ctx)
            }
        } else {
            ctx.replyWithMarkdown('*â›” Bot Is Currently Off*')
        }
    } else {
      ctx.replyWithMarkdown('*âš ï¸You Are Not Allowed To Use The Bot\n\nâ˜˜ï¸Either You Are Not Indian Or This Contact Is Not Yours*')
      db.collection('pendingUsers').insertOne({ userID: ctx.from.id, inviter: "" })
    }
  } catch (err) {
    console.log(err)
  }
})
//BALANCE COMMAND
bot.hears('ðŸ’° Balance', async (ctx) => {
    try {
        let admin = await db.collection('admindb').find({ admin: "admin" }).toArray()
        let currency = admin[0].cur
        let bots = admin[0].botstat
        if (bots == 'Active') {
            let userbalance = await db.collection('balance').find({ userID: ctx.from.id }).toArray()
            let ub = userbalance[0].balance
            let channel = admin[0].channels
            var flag = 0;
            for (i in channel) {
                let res = await bot.telegram.getChatMember(channel[i], ctx.from.id)
                let result = res.status
                if (result == 'creator' || result == 'administrator' || result == 'member') {
                    flag += 1
                } else {
                    flag = 0
                }
            }
            if (flag == channel.length) {
                ctx.replyWithMarkdown(
                    '*ðŸ™ŒðŸ» User = ' + ctx.from.first_name + '\n\nðŸ’° Balance = ' + ub.toFixed(3) + ' ' + currency + '\n\nðŸª¢ Invite To Earn More*', { reply_markup: { keyboard: [['ðŸ’° Balance'], ['ðŸ™ŒðŸ» Invite', 'ðŸŽ Bonus', 'ðŸ—‚ Wallet'], ['ðŸ’³ Withdraw', 'ðŸ“Š Statistics']], resize_keyboard: true } }
                )
            } else {
                mustjoin(ctx)
            }
        } else {
            ctx.replyWithMarkdown('*â›” Bot Is Currently Off*')
        }
    } catch (error) {
        console.log(error)
    }
})
//INVITE COMMAND
bot.hears('ðŸ™ŒðŸ» Invite', async (ctx) => {
    try {
        let admin = await db.collection('admindb').find({ admin: "admin" }).toArray()
        let refer = admin[0].ref
        let currency = admin[0].cur
        let bots = admin[0].botstat
        if (bots == 'Active') {
            let channel = admin[0].channels
            var flag = 0;
            for (i in channel) {
                let res = await bot.telegram.getChatMember(channel[i], ctx.from.id)
                let result = res.status
                if (result == 'creator' || result == 'administrator' || result == 'member') {
                    flag += 1
                } else {
                    flag = 0
                }
            }
            if (flag == channel.length) {
                ctx.replyWithMarkdown(
                    '*ðŸ™ŒðŸ» User =* [' + ctx.from.first_name + '](tg://user?id=' + ctx.from.id + ')\n\n*ðŸ™ŒðŸ» Your Invite Link = https://t.me/' + ctx.botInfo.username + '?start=' + ctx.from.id + ' \n\nðŸª¢ Invite To ' + refer + ' ' + currency + ' Per Invite*', { reply_markup: { keyboard: [['ðŸ’° Balance'], ['ðŸ™ŒðŸ» Invite', 'ðŸŽ Bonus', 'ðŸ—‚ Wallet'], ['ðŸ’³ Withdraw', 'ðŸ“Š Statistics']], resize_keyboard: true } }
                )
            } else {
                mustjoin(ctx)
            }
        } else {
            ctx.replyWithMarkdown('*â›” Bot Is Currently Off*')
        }
    } catch (error) {
        console.log(error)
    }

})
//JOINED BUTTON
bot.hears('ðŸŸ¢ Joined', async (ctx) => {
    try {
        let admin = await db.collection('admindb').find({ admin: "admin" }).toArray()
        let refer = admin[0].ref
        let currency = admin[0].cur
        let bots = admin[0].botstat
        if (bots == 'Active') {
            let channel = admin[0].channels
            var flag = 0;
            for (i in channel) {
                let res = await bot.telegram.getChatMember(channel[i], ctx.from.id)
                let result = res.status
                if (result == 'creator' || result == 'administrator' || result == 'member') {
                    flag += 1
                } else {
                    flag = 0
                }
            }
            if (flag == channel.length) {
                ctx.replyWithMarkdown(
                    '*ðŸ¡ Welcome To Main Menu*', { reply_markup: { keyboard: [['ðŸ’° Balance'], ['ðŸ™ŒðŸ» Invite', 'ðŸŽ Bonus', 'ðŸ—‚ Wallet'], ['ðŸ’³ Withdraw', 'ðŸ“Š Statistics']], resize_keyboard: true } }
                )
                let userdata = await db.collection('pendingUsers').find({ userID: ctx.from.id }).toArray()
                let config = await db.collection('allUsers').find({ userID: ctx.from.id }).toArray()
                if (('inviter' in userdata[0]) && !('referred' in config[0])) {
                    let bal = await db.collection('balance').find({ userID: userdata[0].inviter }).toArray()
                    let cur = bal[0].balance * 1
                    let ref = refer * 1
                    let final = ref + cur
                    bot.telegram.sendMessage(userdata[0].inviter, "*ðŸ’°" + refer + " " + currency + " Added To Your Balance*", { parse_mode: 'markdown' })
                    bot.telegram.sendMessage(ctx.from.id, "*ðŸ’¹ To Check Who Invited You, Click On 'âœ… Check'*", { parse_mode: 'markdown', reply_markup: { inline_keyboard: [[{ text: "âœ… Check", callback_data: "check" }]] } })
                    db.collection('allUsers').updateOne({ userID: ctx.from.id }, { $set: { inviter: userdata[0].inviter, referred: 'DONE' } }, { upsert: true })
                    db.collection('balance').updateOne({ userID: userdata[0].inviter }, { $set: { balance: final } }, { upsert: true })
                }
            } else {
                mustjoin(ctx)
            }
        } else {
            ctx.replyWithMarkdown('*â›” Bot Is Currently Off*')
        }
    } catch (error) {
        console.log(error)
    }

})
//WALLET BUTTON
bot.hears('ðŸ—‚ Wallet', async (ctx) => {
    try {
        let admin = await db.collection('admindb').find({ admin: "admin" }).toArray()
        let currency = admin[0].cur
        let bots = admin[0].botstat
        if (bots == 'Active') {
            let data = await db.collection('allUsers').find({ userID: ctx.from.id }).toArray()
            let channel = admin[0].channels
            var flag = 0;
            for (i in channel) {
                let res = await bot.telegram.getChatMember(channel[i], ctx.from.id)
                let result = res.status
                if (result == 'creator' || result == 'administrator' || result == 'member') {
                    flag += 1
                } else {
                    flag = 0
                }
            }
            if (flag == channel.length) {
                if ('wallet' in data[0]) {
                    bot.telegram.sendMessage(ctx.from.id, "<b>ðŸ’¡ Your Currently Set " + currency + " Wallet Is</b>:\n<code>" + data[0].wallet + "</code>\n\nðŸ—‚<b> It Will Be Used For Future Withdrawals</b>", { parse_mode: 'html', reply_markup: { inline_keyboard: [[{ text: "ðŸš§ Change " + currency + " Wallet ðŸš§", callback_data: "wallet" }]] } })
                } else {
                    bot.telegram.sendMessage(ctx.from.id, "<b>ðŸ’¡ Your Currently Set " + currency + " Wallet Is</b>:\n<code>'none'</code>\n\nðŸ—‚<b> It Will Be Used For Future Withdrawals</b>", { parse_mode: 'html', reply_markup: { inline_keyboard: [[{ text: "ðŸš§ Set " + currency + " Wallet ðŸš§", callback_data: "wallet" }]] } })
                }
            } else {
                mustjoin(ctx)
            }
        } else {
            ctx.replyWithMarkdown('*â›” Bot Is Currently Off*')
        }
    } catch (error) {
        console.log(error)
    }
})
//WITHDRAW COMMAND
bot.hears('ðŸ’³ Withdraw', async (ctx) => {
    try {
        let admin = await db.collection('admindb').find({ admin: "admin" }).toArray()
        let mini_with = admin[0].minimum
        let currency = admin[0].cur
        let bots = admin[0].botstat
        let withs = admin[0].withstat
        if (bots == 'Active') {
            if (withs == 'ON') {
                let channel = admin[0].channels
                var flag = 0;
                for (i in channel) {
                    let res = await bot.telegram.getChatMember(channel[i], ctx.from.id)
                    let result = res.status
                    if (result == 'creator' || result == 'administrator' || result == 'member') {
                        flag += 1
                    } else {
                        flag = 0
                    }
                }
                if (flag == channel.length) {
                    let userbalance = await db.collection('balance').find({ userID: ctx.from.id }).toArray()
                    let ub = userbalance[0].balance
                    let data = await db.collection('allUsers').find({ userID: ctx.from.id }).toArray()
                    if (ub < mini_with) {
                        ctx.replyWithMarkdown(
                            '*âš ï¸ Must Own AtLeast ' + mini_with + ' ' + currency + ' To Make Withdrawal*', { reply_markup: { keyboard: [['ðŸ’° Balance'], ['ðŸ™ŒðŸ» Invite', 'ðŸŽ Bonus', 'ðŸ—‚ Wallet'], ['ðŸ’³ Withdraw', 'ðŸ“Š Statistics']], resize_keyboard: true } }
                        )
                    } else if (!data[0].wallet) {
                        ctx.replyWithMarkdown(
                            '*âš ï¸ Set Your Wallet Using : *`ðŸ—‚ Wallet`', { reply_markup: { keyboard: [['ðŸ’° Balance'], ['ðŸ™ŒðŸ» Invite', 'ðŸŽ Bonus', 'ðŸ—‚ Wallet'], ['ðŸ’³ Withdraw', 'ðŸ“Š Statistics']], resize_keyboard: true } }
                        )
                    } else {
                        await bot.telegram.sendMessage(ctx.from.id, "*ðŸ“¤ Enter Amount To Withdraw*", {
                            parse_mode: 'markdown', reply_markup: {
                                keyboard: [['â›” Cancel']], resize_keyboard: true
                            }
                        })
                        ctx.scene.enter('onWithdraw')
                    }
                } else {
                    mustjoin(ctx)
                }
            } else {
                ctx.replyWithMarkdown('*â›” Withdrawal Is Currently Off*')
            }
        } else {
            ctx.replyWithMarkdown('*â›” Bot Is Currently Off*')
        }
    } catch (error) {
        console.log(error)
    }
})
bot.hears('â›” Cancel', async (ctx) => {
    try {
        let admin = await db.collection('admindb').find({ admin: "admin" }).toArray()
        let bots = admin[0].botstat
        if (bots == 'Active') {
            let channel = admin[0].channels
            var flag = 0;
            for (i in channel) {
                let res = await bot.telegram.getChatMember(channel[i], ctx.from.id)
                let result = res.status
                if (result == 'creator' || result == 'administrator' || result == 'member') {
                    flag += 1
                } else {
                    flag = 0
                }
            }
            if (flag == channel.length) {
                ctx.replyWithMarkdown(
                    '*ðŸ¡ Welcome To Main Menu*', { reply_markup: { keyboard: [['ðŸ’° Balance'], ['ðŸ™ŒðŸ» Invite', 'ðŸŽ Bonus', 'ðŸ—‚ Wallet'], ['ðŸ’³ Withdraw', 'ðŸ“Š Statistics']], resize_keyboard: true } }
                )
            } else {
                mustjoin(ctx)
            }
        } else {
            ctx.replyWithMarkdown('*â›” Bot Is Currently Off*')
        }
    } catch (error) {
        console.log(error)
    }
})
// STATISTICS OF BOT
bot.hears('ðŸ“Š Statistics', async (ctx) => {
    try {
        let admin = await db.collection('admindb').find({ admin: "admin" }).toArray()
        let currency = admin[0].cur
        let bots = admin[0].botstat
        if (bots == 'Active') {
            let channel = admin[0].channels
            var flag = 0;
            for (i in channel) {
                let res = await bot.telegram.getChatMember(channel[i], ctx.from.id)
                let result = res.status
                if (result == 'creator' || result == 'administrator' || result == 'member') {
                    flag += 1
                } else {
                    flag = 0
                }
            }
            if (flag == channel.length) {
                let statdata = await db.collection('allUsers').find({ stats: "stats" }).toArray()
                let members = await db.collection('allUsers').find({}).toArray()
                if (statdata.length == 0) {
                    db.collection('allUsers').insertOne({ stats: "stats", value: 0 })
                    ctx.reply(
                        '<b>ðŸ“Š Bot Live Stats ðŸ“Š\n\nðŸ“¤ Total Payouts : 0 ' + currency + '\n\nðŸ’¡ Total Users: ' + members.length + ' Users\n\nðŸ”Ž Coded By: <a href="tg://user?id=1003376875">ROHIT_154</a></b>' , { parse_mode: 'html', reply_markup: { keyboard: [['ðŸ’° Balance'], ['ðŸ™ŒðŸ» Invite', 'ðŸŽ Bonus', 'ðŸ—‚ Wallet'], ['ðŸ’³ Withdraw', 'ðŸ“Š Statistics']], resize_keyboard: true } }
                    )
                } else {
                    let payout = statdata[0].value * 1
                    let memb = parseInt(members.length)
                    ctx.reply(
                        '<b>ðŸ“Š Bot Live Stats ðŸ“Š\n\nðŸ“¤ Total Payouts : ' + payout + ' ' + currency + '\n\nðŸ’¡ Total Users: ' + memb + ' Users\n\nðŸ”Ž Coded By: <a href="tg://user?id=1003376875">ROHIT_154</a></b>', { parse_mode: 'html', reply_markup: { keyboard: [['ðŸ’° Balance'], ['ðŸ™ŒðŸ» Invite', 'ðŸŽ Bonus', 'ðŸ—‚ Wallet'], ['ðŸ’³ Withdraw', 'ðŸ“Š Statistics']], resize_keyboard: true } }
                    )
                }
            } else {
                mustjoin(ctx)
            }
        } else {
            ctx.replyWithMarkdown('*â›” Bot Is Currently Off*')
        }
    } catch (error) {
        console.log(error)
    }
})
//ADMIN PANEL
bot.hears('/adminhelp', async (ctx) => {
    try {
        let admin = await db.collection('admindb').find({ admin: "admin" }).toArray()
        let currency = admin[0].cur
        let chnl = admin[0].channels
        var final = "\n\t\t\t\t";
        for (i in chnl) {
            final += chnl[i] + "\n\t\t\t\t";
        }
        let paychannel = admin[0].paychannel
        let bonusamount = admin[0].bonus
        let mini_with = admin[0].minimum
        let refer = admin[0].ref
        let stat = admin[0].botstat
        let withst = admin[0].withstat
        let swg = admin[0].subwallet
        let mkey = admin[0].MKEY
        let mid = admin[0].MID
        if (swg == 'NOT SET' && mkey == 'NOT SET' && mid == 'NOT SET') {
            var keys = 'âŒ NOT SET'
        } else {
            var keys = 'âœ… SET'
        }
        if (stat == 'Active') {
            var botstt = 'âœ… Active'
        } else {
            var botstt = 'ðŸš« Disabled'
        }
        if (withst == 'ON') {
            var with_stat = 'âœ… On'
        } else {
            var with_stat = 'ðŸš« Off'
        }
        if (ctx.from.id == 1003376875) {
            bot.telegram.sendMessage(ctx.from.id,
                "<b>ðŸ¡ Hey " + ctx.from.first_name + "\nðŸ¤˜ðŸ» Welcome To Admin Panel\n\nðŸ’¡ Bot Current Stats: \n\t\t\t\tðŸ“› Bot : @" + ctx.botInfo.username + "\n\t\t\t\tðŸ¤– Bot Status: " + botstt + "\n\t\t\t\tðŸ“¤ Withdrawals : " + with_stat + "\n\t\t\t\tðŸŒ² Channels: " + final + "ðŸ’° Refer: " + refer + "\n\t\t\t\tðŸ’° Minimum: " + mini_with + "\n\t\t\t\tðŸ’² Currency: " + currency + "\n\t\t\t\tðŸŽ Bonus: " + bonusamount + "\n\t\t\t\tðŸ“¤ Pay Channel: " + paychannel + "\n\t\t\t\tâœï¸ Paytm Keys :</b> <code>" + keys + "</code> "
                , { parse_mode: 'html', reply_markup: { inline_keyboard: [[{ text: "ðŸ’° Change Refer", callback_data: "refer" }, { text: "ðŸ’° Change Minimum", callback_data: "minimum" }], [{ text: "ðŸ¤– Bot : " + botstt + "", callback_data: "botstat" }], [{ text: "ðŸŒ² Change Channels", callback_data: "channels" }, { text: "ðŸŽ Change Bonus", callback_data: "bonus" }], [{ text: "ðŸ“¤ Withdrawals : " + with_stat + "", callback_data: "withstat" }], [{ text: "ðŸš¹ User Details", callback_data: "userdetails" }, { text: "ðŸ”„ Change Balance", callback_data: "changebal" }], [{ text: "âœï¸ Paytm Keys : " + keys + "", callback_data: "keys" }]] } })
        }
    } catch (error) {
        console.log(error)
    }

})
//BONUS BUTTON
bot.hears('ðŸŽ Bonus', async (ctx) => {
    try {
        let admin = await db.collection('admindb').find({ admin: "admin" }).toArray()
        let bonusamount = admin[0].bonus
        let bots = admin[0].botstat
        let currency = admin[0].cur
        if (bots == 'Active') {
            let channel = admin[0].channels
            var flag = 0;
            for (i in channel) {
                let res = await bot.telegram.getChatMember(channel[i], ctx.from.id)
                let result = res.status
                if (result == 'creator' || result == 'administrator' || result == 'member') {
                    flag += 1
                } else {
                    flag = 0
                }
            }
            if (flag == channel.length) {
                let bdata = await db.collection('BonusUsers').find({ userID: ctx.from.id }).toArray()
                var duration_in_hours;
                var time = new Date().toISOString();
                if (bdata.length == 0) {
                    db.collection('BonusUsers').insertOne({ userID: ctx.from.id, bonus: new Date() })
                    duration_in_hours = 24;
                } else {
                    duration_in_hours = ((new Date()) - new Date(bdata[0].bonus)) / 1000 / 60 / 60;
                }
                if (duration_in_hours >= 24) {
                    let userbal = await db.collection('balance').find({ userID: ctx.from.id }).toArray()
                    var cur = userbal[0].balance * 1
                    var balance = cur + bonusamount
                    db.collection('balance').updateOne({ userID: ctx.from.id }, { $set: { balance: balance } }, { upsert: true })
                    db.collection('BonusUsers').updateOne({ userID: ctx.from.id }, { $set: { bonus: time } }, { upsert: true })
                    ctx.replyWithMarkdown(
                        '*ðŸŽ Congrats , You Recieved ' + bonusamount + ' ' + currency + '\n\nðŸ”Ž Check Back After 24 Hours* '
                    )
                } else {
                    ctx.replyWithMarkdown(
                        '*â›” You Already Recieved Bonus In Last 24 Hours *'
                    )
                }
            } else {
                mustjoin(ctx)
            }
        } else {
            ctx.replyWithMarkdown('*â›” Bot Is Currently Off*')
        }
    } catch (error) {
        console.log(error)
    }
})
bot.hears('/broadcast', async (ctx) => {
    if (ctx.from.id == 1003376875) {
        ctx.replyWithMarkdown(
            '*ðŸ“¨ Enter Message To Broadcast*', { reply_markup: { keyboard: [['â›” Cancel']], resize_keyboard: true } }
        )
        ctx.scene.enter('broadcast')
    }
})
broadcast.hears(regex, async (ctx) => {
    try {
        if (ctx.message.text == 'â›” Cancel') {
            ctx.replyWithMarkdown(
                '*ðŸ¡ Welcome To Main Menu*', { reply_markup: { keyboard: [['ðŸ’° Balance'], ['ðŸ™ŒðŸ» Invite', 'ðŸŽ Bonus', 'ðŸ—‚ Wallet'], ['ðŸ’³ Withdraw', 'ðŸ“Š Statistics']], resize_keyboard: true } }
            )
            ctx.scene.leave('broadcast')
        } else {
            total = 0
            let users = await db.collection('allUsers').find({}).toArray()
            ctx.replyWithMarkdown(
                '*ðŸ“£ Broadcast Sent To: ' + users.length + ' Users*', { reply_markup: { keyboard: [['ðŸ’° Balance'], ['ðŸ™ŒðŸ» Invite', 'ðŸŽ Bonus', 'ðŸ—‚ Wallet'], ['ðŸ’³ Withdraw', 'ðŸ“Š Statistics']], resize_keyboard: true } }
            )
            users.forEach((element, i) => {
                if (total == 5) {
                    total -= total
                    sleep(5)
                }
                total += 1
                bot.telegram.sendMessage(element.userID, "*ðŸ“£ Broadcast*\n\n" + ctx.message.text, { parse_mode: 'markdown' }).catch((err) => console.log(err))
            })
            ctx.scene.leave('broadcast')
        }
    } catch (error) {
        console.log(error)
    }
})
wallet.hears(regex, async (ctx) => {
    try {
        let admin = await db.collection('admindb').find({ admin: "admin" }).toArray()
        let channel = admin[0].channels
        var flag = 0;
        for (i in channel) {
            let res = await bot.telegram.getChatMember(channel[i], ctx.from.id)
            let result = res.status
            if (result == 'creator' || result == 'administrator' || result == 'member') {
                flag += 1
            } else {
                flag = 0
            }
        }
        if (flag == channel.length) {
            db.collection('allUsers').updateOne({ userID: ctx.from.id }, { $set: { wallet: ctx.message.text } }, { upsert: true })
            if (ctx.message.text == 'â›” Cancel') {
                ctx.replyWithMarkdown(
                    '*ðŸ¡ Welcome To Main Menu*', { reply_markup: { keyboard: [['ðŸ’° Balance'], ['ðŸ™ŒðŸ» Invite', 'ðŸŽ Bonus', 'ðŸ—‚ Wallet'], ['ðŸ’³ Withdraw', 'ðŸ“Š Statistics']], resize_keyboard: true } }
                )
            } else {
                ctx.replyWithMarkdown(
                    '*ðŸ—‚ Wallet Address Set To: *\n`' + ctx.message.text + '`', { reply_markup: { keyboard: [['ðŸ’° Balance'], ['ðŸ™ŒðŸ» Invite', 'ðŸŽ Bonus', 'ðŸ—‚ Wallet'], ['ðŸ’³ Withdraw', 'ðŸ“Š Statistics']], resize_keyboard: true } }
                )
                console.log(/^[a-zA-Z0-9]+$/.test("0xErts"))
            }
        } else {
            mustjoin(ctx)
        }
        ctx.scene.leave('wallet')
    } catch (error) {
        console.log(error)
    }
})
onWithdraw.on('text', async (ctx) => {
    try {
        ctx.scene.leave('onWithdraw')
        let admin = await db.collection('admindb').find({ admin: "admin" }).toArray()
        let mini_with = admin[0].minimum
        let currency = admin[0].cur
        let pay = admin[0].paychannel
        let bots = admin[0].withstat
        if (bots == 'ON') {
            let channel = admin[0].channels
            var flag = 0;
            for (i in channel) {
                let res = await bot.telegram.getChatMember(channel[i], ctx.from.id)
                let result = res.status
                if (result == 'creator' || result == 'administrator' || result == 'member') {
                    flag += 1
                } else {
                    flag = 0
                }
            }
            if (flag == channel.length) {
                let userbalance = await db.collection('balance').find({ userID: ctx.from.id }).toArray()
                let guy = await db.collection('allUsers').find({ userID: ctx.from.id }).toArray()
                let inc = await db.collection('allUsers').find({ stats: "stats" }).toArray()
                let toinc = (inc[0].value * 1) + parseInt(ctx.message.text)
                let ub = userbalance[0].balance * 1
                let wallet = guy[0].wallet
                if (ctx.message.text == 'â›” Cancel'){
                  ctx.replyWithMarkdown(

                        '*â›” Withdrawal Cancelled*', { reply_markup: { keyboard: [['ðŸ’° Balance'], ['ðŸ™ŒðŸ» Invite', 'ðŸŽ Bonus', 'ðŸ—‚ Wallet'], ['ðŸ’³ Withdraw', 'ðŸ“Š Statistics']], resize_keyboard: true } }

                    )
                    ctx.scene.leave('onWithdraw')
                    return 0;
                } else if (isNaN(ctx.message.text)){
                    ctx.replyWithMarkdown(
                        '*â›” Only Numeric Value Allowed*', { reply_markup: { keyboard: [['ðŸ’° Balance'], ['ðŸ™ŒðŸ» Invite', 'ðŸŽ Bonus', 'ðŸ—‚ Wallet'], ['ðŸ’³ Withdraw', 'ðŸ“Š Statistics']], resize_keyboard: true } }
                    )
                    ctx.scene.leave('onWithdraw')
                    return 0;
                } else if (ctx.message.text > ub) {
                    ctx.replyWithMarkdown(
                        '*â›” Entered Amount Is Greater Than Your Balance*', { reply_markup: { keyboard: [['ðŸ’° Balance'], ['ðŸ™ŒðŸ» Invite', 'ðŸŽ Bonus', 'ðŸ—‚ Wallet'], ['ðŸ’³ Withdraw', 'ðŸ“Š Statistics']], resize_keyboard: true } }
                    )
                    ctx.scene.leave('onWithdraw')
                    return 0;
                } else if (ctx.message.text < mini_with) {
                    ctx.replyWithMarkdown(

                        '*âš ï¸ Minimum Withdrawal Is ' + mini_with + ' ' + currency + '*', { reply_markup: { keyboard: [['ðŸ’° Balance'], ['ðŸ™ŒðŸ» Invite', 'ðŸŽ Bonus', 'ðŸ—‚ Wallet'], ['ðŸ’³ Withdraw', 'ðŸ“Š Statistics']], resize_keyboard: true } }

                    )
                    ctx.scene.leave('onWithdraw')
                    return 0;
                } else if (ctx.message.text > 10){
                  ctx.replyWithMarkdown(

                        '*âš ï¸ Maximum Withdrawal Is 10 ' + currency + '*', { reply_markup: { keyboard: [['ðŸ’° Balance'], ['ðŸ™ŒðŸ» Invite', 'ðŸŽ Bonus', 'ðŸ—‚ Wallet'], ['ðŸ’³ Withdraw', 'ðŸ“Š Statistics']], resize_keyboard: true } }

                    )
                    ctx.scene.leave('onWithdraw')
                    return 0;
                } else {
                    bot.telegram.sendMessage(ctx.from.id,"*ðŸ¤˜Withdrawal Confirmation\n\nðŸ”° Amount : "+ctx.message.text+" "+currency+"\nðŸ—‚ Wallet :* `"+wallet+"`\n*âœŒï¸Confirm Your Transaction By Clicking On 'âœ… Approve'*",{parse_mode:'Markdown', reply_markup: {inline_keyboard: [[{text:"âœ… Approve",callback_data:"approve"},{text:"âŒ Cancel",callback_data:"cancel"}]]}})
                    }
                    db.collection('balance').updateOne({ userID: ctx.from.id }, { $set: { toWithdraw: ctx.message.text } }, { upsert: true })
                    ctx.scene.leave('onWithdraw')
                    return 0;
            } else {
                mustjoin(ctx)
            }
        } else {
            ctx.replyWithMarkdown('*â›” Bot Is Currently Off*')
        }
    } catch (error) {
        console.log(error)
    }
})
bot.action("approve",async(ctx) => {
  try{
    let admin = await db.collection('admindb').find({ admin: "admin" }).toArray()
    let mini_with = admin[0].minimum
    let currency = admin[0].cur
    let pay = admin[0].paychannel
    let bots = admin[0].withstat
    let userbalance = await db.collection('balance').find({ userID: ctx.from.id }).toArray()
    let toWith = userbalance[0].toWithdraw * 1
    let balan = userbalance[0].balance * 1
    let guy = await db.collection('allUsers').find({ userID: ctx.from.id }).toArray()
    let inc = await db.collection('allUsers').find({ stats: "stats" }).toArray()
    let toinc = (inc[0].value * 1) + parseInt(toWith)
    let ub = userbalance[0].balance * 1
    let wallet = guy[0].wallet
    if(toWith > balan){
      ctx.deleteMessage()
      ctx.replyWithMarkdown("*âŒ Withdrawal Failed*")
    }
    if(toWith == 0){
      ctx.deleteMessage()
      ctx.replyWithMarkdown("*âŒNo Amount Available For Withdrawal*")
      return 0;
    } else {
        var newbal = parseFloat(ub) - parseFloat(toWith)
        db.collection('balance').updateOne({ userID: ctx.from.id }, { $set: { balance: newbal } }, { upsert: true })
        db.collection('balance').updateOne({ userID: ctx.from.id }, { $set: { toWithdraw:0.00 } }, { upsert: true })
        db.collection('allUsers').updateOne({ stats: "stats" }, { $set: { value: parseFloat(toinc) } }, { upsert: true })
        ctx.deleteMessage()
        ctx.replyWithMarkdown( 
                        "*âœ… New Withdrawal Processed âœ…\n\nðŸš€Amount : " + toWith + " " + currency + "\nâ›” Wallet :* `" + wallet + "`\n*ðŸ’¡ Bot: @" + ctx.botInfo.username + "*", {parse_mode:'markdown', reply_markup: { keyboard: [['ðŸ’° Balance'], ['ðŸ™ŒðŸ» Invite', 'ðŸŽ Bonus', 'ðŸ—‚ Wallet'], ['ðŸ’³ Withdraw', 'ðŸ“Š Statistics']], resize_keyboard: true } } 
                    )
            bot.telegram.sendMessage(pay, "<b>âœ… New Withdrawal Requested âœ…\n\nðŸŸ¢ User : <a href='tg://user?id=" + ctx.from.id + "'>" + ctx.from.id + "</a>\n\nðŸš€Amount : " + toWith + " " + currency + "\nâ›” Address :</b> <code>" + wallet + "</code>\n\n<b>ðŸ’¡ Bot: @" + ctx.botInfo.username + "</b>", { parse_mode: 'html' })
             let swg = admin[0].subwallet
             let mkey = admin[0].mkey 
             let mid = admin[0].mid 
             let comment = admin[0].comment 
             let amount = toWith
             var url = 'https://job2all.xyz/api/index.php?mid='+mid+'&mkey='+mkey+'&guid='+swg+'&mob='+wallet+'&amount='+amount+'&info='+comment+'';
              axios.post(url)
              .then(res => {
                console.log("Result:\n"+res)
                
              })
              .catch(error => {
                console.error(error)
              })
             //paytm(wallet, amount, swg, mkey, mid, comment); 
    }
    ctx.scene.leave('onWithdraw')
  } catch(err) {
    console.log(err)
  }
})
bot.action("cancel",async(ctx)=> {
  try{
     db.collection('balance').updateOne({ userID: ctx.from.id }, { $set: { toWithdraw:0.00 } }, { upsert: true })
     ctx.deleteMessage()
     ctx.replyWithMarkdown( 

                        "*âŒ Withdrawal Cancelled *", {parse_mode:'markdown', reply_markup: { keyboard: [['ðŸ’° Balance'], ['ðŸ™ŒðŸ» Invite', 'ðŸŽ Bonus', 'ðŸ—‚ Wallet'], ['ðŸ’³ Withdraw', 'ðŸ“Š Statistics']], resize_keyboard: true } } 

                    )
     ctx.scene.leave('onWithdraw')
  } catch(err) {
    console.log(err)
  }
})
refer.hears(/^[+-]?([0-9]*[.])?[0-9]+/i, async (ctx) => {
    try {
        if (ctx.message.text == 'â›” Cancel') {
            ctx.replyWithMarkdown(
                '*ðŸ¡ Welcome To Main Menu*', { reply_markup: { keyboard: [['ðŸ’° Balance'], ['ðŸ™ŒðŸ» Invite', 'ðŸŽ Bonus', 'ðŸ—‚ Wallet'], ['ðŸ’³ Withdraw', 'ðŸ“Š Statistics']], resize_keyboard: true } }
            )
        } else {
            let final = ctx.message.text * 1
            db.collection('admindb').updateOne({ admin: "admin" }, { $set: { ref: final } }, { upsert: true })
            ctx.replyWithMarkdown(
                '*ðŸ—‚New Refer Amount Set To: *\n`' + ctx.message.text + '`', { reply_markup: { keyboard: [['ðŸ’° Balance'], ['ðŸ™ŒðŸ» Invite', 'ðŸŽ Bonus', 'ðŸ—‚ Wallet'], ['ðŸ’³ Withdraw', 'ðŸ“Š Statistics']], resize_keyboard: true } }
            )
        }
        ctx.scene.leave('refer')
    } catch (error) {
        console.log(error)
    }
})
mini.hears(/^[+-]?([0-9]*[.])?[0-9]+/i, async (ctx) => {
    try {
        if (ctx.message.text == 'â›” Cancel') {
            ctx.replyWithMarkdown(
                '*ðŸ¡ Welcome To Main Menu*', { reply_markup: { keyboard: [['ðŸ’° Balance'], ['ðŸ™ŒðŸ» Invite', 'ðŸŽ Bonus', 'ðŸ—‚ Wallet'], ['ðŸ’³ Withdraw', 'ðŸ“Š Statistics']], resize_keyboard: true } }
            )
        } else {
            let final = ctx.message.text * 1
            db.collection('admindb').updateOne({ admin: "admin" }, { $set: { minimum: final } }, { upsert: true })
            ctx.replyWithMarkdown(
                '*ðŸ—‚New Minimum Withdraw Set To: *\n`' + ctx.message.text + '`', { reply_markup: { keyboard: [['ðŸ’° Balance'], ['ðŸ™ŒðŸ» Invite', 'ðŸŽ Bonus', 'ðŸ—‚ Wallet'], ['ðŸ’³ Withdraw', 'ðŸ“Š Statistics']], resize_keyboard: true } }
            )
        }
        ctx.scene.leave('mini')
    } catch (error) {
        console.log(error)
    }
})
bon.hears(/^[+-]?([0-9]*[.])?[0-9]+/i, async (ctx) => {
    try {
        if (ctx.message.text == 'â›” Cancel') {
            ctx.replyWithMarkdown(
                '*ðŸ¡ Welcome To Main Menu*', { reply_markup: { keyboard: [['ðŸ’° Balance'], ['ðŸ™ŒðŸ» Invite', 'ðŸŽ Bonus', 'ðŸ—‚ Wallet'], ['ðŸ’³ Withdraw', 'ðŸ“Š Statistics']], resize_keyboard: true } }
            )
        } else {
            let final = ctx.message.text * 1
            db.collection('admindb').updateOne({ admin: "admin" }, { $set: { bonus: final } }, { upsert: true })
            ctx.replyWithMarkdown(
                '*ðŸ—‚New Daily Bonus Set To: *\n`' + ctx.message.text + '`', { reply_markup: { keyboard: [['ðŸ’° Balance'], ['ðŸ™ŒðŸ» Invite', 'ðŸŽ Bonus', 'ðŸ—‚ Wallet'], ['ðŸ’³ Withdraw', 'ðŸ“Š Statistics']], resize_keyboard: true } }
            )
        }
        ctx.scene.leave('bonus')
    } catch (error) {
        console.log(error)
    }
})
tgid.hears(/^[0-9]+$/, async (ctx) => {
    try {
        if (ctx.message.text == 'â›” Cancel') {
            ctx.replyWithMarkdown(
                '*ðŸ¡ Welcome To Main Menu*', { reply_markup: { keyboard: [['ðŸ’° Balance'], ['ðŸ™ŒðŸ» Invite', 'ðŸŽ Bonus', 'ðŸ—‚ Wallet'], ['ðŸ’³ Withdraw', 'ðŸ“Š Statistics']], resize_keyboard: true } }
            )
        } else {
            let user = parseInt(ctx.message.text)
            let data = await db.collection('allUsers').find({ userID: user }).toArray()
            let used = await db.collection('balance').find({ userID: user }).toArray()
            if (!data[0]) {
                ctx.replyWithMarkdown(
                    '*â›” User Is Not Registered In Our Database *', { reply_markup: { keyboard: [['ðŸ’° Balance'], ['ðŸ™ŒðŸ» Invite', 'ðŸŽ Bonus', 'ðŸ—‚ Wallet'], ['ðŸ’³ Withdraw', 'ðŸ“Š Statistics']], resize_keyboard: true } }
                )
            } else {
                let bal = used[0].balance
                let add = data[0].wallet
                let invite;
                if (!data[0].inviter) {
                    invite = 'Not Invited'
                } else {
                    invite = data[0].inviter
                }
                ctx.reply(
                    '<b>ðŸ«‚ User : <a href="tg://user?id=' + ctx.message.text + '">' + ctx.message.text + '</a>\nâ›” User Id</b> : <code>' + ctx.message.text + '</code>\n\n<b>ðŸ’° Balance : ' + bal + '\nðŸ—‚ Wallet : </b><code>' + add + '</code>\n<b>ðŸ™ŒðŸ» Inviter : </b><code>' + invite + '</code>', { parse_mode: 'html', reply_markup: { keyboard: [['ðŸ’° Balance'], ['ðŸ™ŒðŸ» Invite', 'ðŸŽ Bonus', 'ðŸ—‚ Wallet'], ['ðŸ’³ Withdraw', 'ðŸ“Š Statistics']], resize_keyboard: true } }
                )
            }
        }
        ctx.scene.leave('tgid')
    } catch (error) {
        console.log(error)
    }
})
subwallet.hears(regex, async (ctx) => {
    try {
        if (ctx.message.text == 'â›” Cancel') {
            ctx.replyWithMarkdown(
                '*ðŸ¡ Welcome To Main Menu*', { reply_markup: { keyboard: [['ðŸ’° Balance'], ['ðŸ™ŒðŸ» Invite', 'ðŸŽ Bonus', 'ðŸ—‚ Wallet'], ['ðŸ’³ Withdraw', 'ðŸ“Š Statistics']], resize_keyboard: true } }
            )
        } else {
            db.collection('admindb').updateOne({ admin: "admin" }, { $set: { subwallet: ctx.message.text } }, { upsert: true })
            ctx.replyWithMarkdown(
                '*ðŸ—‚ Subwallet Guid Set To : *\n`' + ctx.message.text + '`', { reply_markup: { keyboard: [['ðŸ’° Balance'], ['ðŸ™ŒðŸ» Invite', 'ðŸŽ Bonus', 'ðŸ—‚ Wallet'], ['ðŸ’³ Withdraw', 'ðŸ“Š Statistics']], resize_keyboard: true } }
            )
        }
        ctx.scene.leave('subwallet')
    } catch (error) {
        console.log(error)
    }
})
mkey.hears(regex, async (ctx) => {
    try {
        if (ctx.message.text == 'â›” Cancel') {
            ctx.replyWithMarkdown(
                '*ðŸ¡ Welcome To Main Menu*', { reply_markup: { keyboard: [['ðŸ’° Balance'], ['ðŸ™ŒðŸ» Invite', 'ðŸŽ Bonus', 'ðŸ—‚ Wallet'], ['ðŸ’³ Withdraw', 'ðŸ“Š Statistics']], resize_keyboard: true } }
            )
        } else {
            db.collection('admindb').updateOne({ admin: "admin" }, { $set: { mkey: ctx.message.text } }, { upsert: true })
            ctx.replyWithMarkdown(
                '*ðŸ—‚ Merchant Key Set To : *\n`' + ctx.message.text + '`', { reply_markup: { keyboard: [['ðŸ’° Balance'], ['ðŸ™ŒðŸ» Invite', 'ðŸŽ Bonus', 'ðŸ—‚ Wallet'], ['ðŸ’³ Withdraw', 'ðŸ“Š Statistics']], resize_keyboard: true } }
            )
        }
        ctx.scene.leave('mkey')
    } catch (error) {
        console.log(error)
    }
})
mid.hears(regex, async (ctx) => {
    try {
        if (ctx.message.text == 'â›” Cancel') {
            ctx.replyWithMarkdown(
                '*ðŸ¡ Welcome To Main Menu*', { reply_markup: { keyboard: [['ðŸ’° Balance'], ['ðŸ™ŒðŸ» Invite', 'ðŸŽ Bonus', 'ðŸ—‚ Wallet'], ['ðŸ’³ Withdraw', 'ðŸ“Š Statistics']], resize_keyboard: true } }
            )
        } else {
            db.collection('admindb').updateOne({ admin: "admin" }, { $set: { mid: ctx.message.text } }, { upsert: true })
            ctx.replyWithMarkdown(
                '*ðŸ—‚ Merchant Id Set To : *\n`' + ctx.message.text + '`', { reply_markup: { keyboard: [['ðŸ’° Balance'], ['ðŸ™ŒðŸ» Invite', 'ðŸŽ Bonus', 'ðŸ—‚ Wallet'], ['ðŸ’³ Withdraw', 'ðŸ“Š Statistics']], resize_keyboard: true } }
            )
        }
        ctx.scene.leave('mid')
    } catch (error) {
        console.log(error)
    }
})
comment.hears(regex, async (ctx) => {
    try {
        if (ctx.message.text == 'â›” Cancel') {
            ctx.replyWithMarkdown(
                '*ðŸ¡ Welcome To Main Menu*', { reply_markup: { keyboard: [['ðŸ’° Balance'], ['ðŸ™ŒðŸ» Invite', 'ðŸŽ Bonus', 'ðŸ—‚ Wallet'], ['ðŸ’³ Withdraw', 'ðŸ“Š Statistics']], resize_keyboard: true } }
            )
        } else {
            db.collection('admindb').updateOne({ admin: "admin" }, { $set: { comment: ctx.message.text } }, { upsert: true })
            ctx.replyWithMarkdown(
                '*ðŸ—‚ Payment Description Set To : *\n`' + ctx.message.text + '`', { reply_markup: { keyboard: [['ðŸ’° Balance'], ['ðŸ™ŒðŸ» Invite', 'ðŸŽ Bonus', 'ðŸ—‚ Wallet'], ['ðŸ’³ Withdraw', 'ðŸ“Š Statistics']], resize_keyboard: true } }
            )
        }
        ctx.scene.leave('comments')
    } catch (error) {
        console.log(error)
    }
})
incr.hears(regex, async (ctx) => {
    try {
        if (ctx.message.text == 'â›” Cancel') {
            ctx.replyWithMarkdown(
                '*ðŸ¡ Welcome To Main Menu*', { reply_markup: { keyboard: [['ðŸ’° Balance'], ['ðŸ™ŒðŸ» Invite', 'ðŸŽ Bonus', 'ðŸ—‚ Wallet'], ['ðŸ’³ Withdraw', 'ðŸ“Š Statistics']], resize_keyboard: true } }
            )
        } else {
            let message = ctx.message.text
            let data = message.split(" ")
            let user = data[0]
            let amount = data[1] * 1
            let already = await db.collection('balance').find({ userID: parseInt(user) }).toArray()
            let bal = already[0].balance * 1
            let final = bal + amount
            db.collection('balance').updateOne({ userID: parseInt(user) }, { $set: { balance: final } }, { upsert: true })
            ctx.reply(
                '<b>ðŸ’° Balance Of <a href="tg://user?id=' + user + '">' + user + '</a> Was Increased By ' + amount + '\n\nðŸ’° Final Balance = ' + final + '</b>', { parse_mode: 'html', reply_markup: { keyboard: [['ðŸ’° Balance'], ['ðŸ™ŒðŸ» Invite', 'ðŸŽ Bonus', 'ðŸ—‚ Wallet'], ['ðŸ’³ Withdraw', 'ðŸ“Š Statistics']], resize_keyboard: true } }
            )
            bot.telegram.sendMessage(user, "*ðŸ’° Admin Gave You A Increase In Balance By " + amount + "*", { parse_mode: 'markdown' })
        }
        ctx.scene.leave('incr')
    } catch (error) {
        console.log(error)
    }
})
chnl.hears(regex, async (ctx) => {
    try {
        let admin = await db.collection('admindb').find({ admin: "admin" }).toArray()
        if (ctx.message.text == 'â›” Cancel') {
            ctx.replyWithMarkdown(
                '*ðŸ¡ Welcome To Main Menu*', { reply_markup: { keyboard: [['ðŸ’° Balance'], ['ðŸ™ŒðŸ» Invite', 'ðŸŽ Bonus', 'ðŸ—‚ Wallet'], ['ðŸ’³ Withdraw', 'ðŸ“Š Statistics']], resize_keyboard: true } }
            )
        } else if (ctx.message.text[0] == "@") {
            let channel = admin[0].channels
            channel.push(ctx.message.text)
            db.collection('admindb').updateOne({ admin: "admin" }, { $set: { channels: channel } }, { upsert: true })
            ctx.reply(
                '<b>ðŸ—‚ Channel Added To Bot : ' + ctx.message.text + '</b>', { parse_mode: 'html', reply_markup: { keyboard: [['ðŸ’° Balance'], ['ðŸ™ŒðŸ» Invite', 'ðŸŽ Bonus', 'ðŸ—‚ Wallet'], ['ðŸ’³ Withdraw', 'ðŸ“Š Statistics']], resize_keyboard: true } }
            )
        } else {
            ctx.replyWithMarkdown(
                '*â›” Channel User Name Must Start With "@"*', { reply_markup: { keyboard: [['ðŸ’° Balance'], ['ðŸ™ŒðŸ» Invite', 'ðŸŽ Bonus', 'ðŸ—‚ Wallet'], ['ðŸ’³ Withdraw', 'ðŸ“Š Statistics']], resize_keyboard: true } }
            )
        }
        ctx.scene.leave('chnl')
    } catch (error) {
        console.log(error)
    }
})
removechnl.hears(regex, async (ctx) => {
    try {
        let admin = await db.collection('admindb').find({ admin: "admin" }).toArray()
        var chan = admin[0].channels
        if (ctx.message.text == 'â›” Cancel') {
            ctx.replyWithMarkdown(
                '*ðŸ¡ Welcome To Main Menu*', { reply_markup: { keyboard: [['ðŸ’° Balance'], ['ðŸ™ŒðŸ» Invite', 'ðŸŽ Bonus', 'ðŸ—‚ Wallet'], ['ðŸ’³ Withdraw', 'ðŸ“Š Statistics']], resize_keyboard: true } }
            )
        } else if (ctx.message.text[0] == "@") {
            if (contains("" + ctx.message.text + "", chan)) {
                var result = arrayRemove(chan, "" + ctx.message.text + "");
                db.collection('admindb').updateOne({ admin: "admin" }, { $set: { channels: result } }, { upsert: true })
                ctx.reply(
                    '<b>ðŸ—‚ Channel Removed From Bot : ' + ctx.message.text + '</b>', { parse_mode: 'html', reply_markup: { keyboard: [['ðŸ’° Balance'], ['ðŸ™ŒðŸ» Invite', 'ðŸŽ Bonus', 'ðŸ—‚ Wallet'], ['ðŸ’³ Withdraw', 'ðŸ“Š Statistics']], resize_keyboard: true } }
                )
            } else {
                ctx.reply(
                    '<b>â›” Channel Not In Our Database</b>', { parse_mode: 'html', reply_markup: { keyboard: [['ðŸ’° Balance'], ['ðŸ™ŒðŸ» Invite', 'ðŸŽ Bonus', 'ðŸ—‚ Wallet'], ['ðŸ’³ Withdraw', 'ðŸ“Š Statistics']], resize_keyboard: true } }
                )
            }
        } else {
            ctx.replyWithMarkdown(
                '*â›” Channel User Name Must Start With "@"*', { reply_markup: { keyboard: [['ðŸ’° Balance'], ['ðŸ™ŒðŸ» Invite', 'ðŸŽ Bonus', 'ðŸ—‚ Wallet'], ['ðŸ’³ Withdraw', 'ðŸ“Š Statistics']], resize_keyboard: true } }
            )
        }
        ctx.scene.leave('removechnl')
    } catch (error) {
        console.log(error)
    }
})
paychnl.hears(regex, async (ctx) => {
    try {
        let admin = await db.collection('admindb').find({ admin: "admin" }).toArray()
        if (ctx.message.text == 'â›” Cancel') {
            ctx.replyWithMarkdown(
                '*ðŸ¡ Welcome To Main Menu*', { reply_markup: { keyboard: [['ðŸ’° Balance'], ['ðŸ™ŒðŸ» Invite', 'ðŸŽ Bonus', 'ðŸ—‚ Wallet'], ['ðŸ’³ Withdraw', 'ðŸ“Š Statistics']], resize_keyboard: true } }
            )
        } else if (ctx.message.text[0] == "@") {
            db.collection('admindb').updateOne({ admin: "admin" }, { $set: { paychannel: "" + ctx.message.text + "" } }, { upsert: true })
            ctx.reply(
                '<b>ðŸ—‚ Pay Channel Set To : ' + ctx.message.text + '</b>', { parse_mode: 'html', reply_markup: { keyboard: [['ðŸ’° Balance'], ['ðŸ™ŒðŸ» Invite', 'ðŸŽ Bonus', 'ðŸ—‚ Wallet'], ['ðŸ’³ Withdraw', 'ðŸ“Š Statistics']], resize_keyboard: true } }
            )
        } else {
            ctx.replyWithMarkdown(
                '*â›” Channel User Name Must Start With "@"*', { reply_markup: { keyboard: [['ðŸ’° Balance'], ['ðŸ™ŒðŸ» Invite', 'ðŸŽ Bonus', 'ðŸ—‚ Wallet'], ['ðŸ’³ Withdraw', 'ðŸ“Š Statistics']], resize_keyboard: true } }
            )
        }
        ctx.scene.leave('paychnl')
    } catch (error) {
        console.log(error)
    }
})
bot.action('botstat', async (ctx) => {
    try {
        let admin = await db.collection('admindb').find({ admin: "admin" }).toArray()
        let currency = admin[0].cur
        let paychannel = admin[0].paychannel
        let bonusamount = admin[0].bonus
        let mini_with = admin[0].minimum
        let refer = admin[0].ref
        let stat = admin[0].botstat
        let withst = admin[0].withstat
        let swg = admin[0].subwallet
        let mkey = admin[0].MKEY
        let mid = admin[0].MID
        let chnl = admin[0].channels
        var final = "\n\t\t\t\t";
        for (i in chnl) {
            final += chnl[i] + "\n\t\t\t\t";
        }
        if (swg == 'NOT SET' && mkey == 'NOT SET' && mid == 'NOT SET') {
            var keys = 'âŒ NOT SET'
        } else {
            var keys = 'âœ… SET'
        }
        if (stat == 'Active') {
            var botstt = 'ðŸš« Disabled'
            db.collection('admindb').updateOne({ admin: "admin" }, { $set: { botstat: 'Disabled' } }, { upsert: true })
        } else {
            var botstt = 'âœ… Active'
            db.collection('admindb').updateOne({ admin: "admin" }, { $set: { botstat: 'Active' } }, { upsert: true })
        }
        if (withst == 'ON') {
            var with_stat = 'âœ… On'
        } else {
            var with_stat = 'ðŸš« Off'
        }
        if (ctx.from.id == 1003376875 ) {
            ctx.editMessageText("<b>ðŸ¡ Hey " + ctx.from.first_name + "\nðŸ¤˜ðŸ» Welcome To Admin Panel\n\nðŸ’¡ Bot Current Stats: \n\t\t\t\tðŸ“› Bot : @" + ctx.botInfo.username + "\n\t\t\t\tðŸ¤– Bot Status: " + botstt + "\n\t\t\t\tðŸ“¤ Withdrawals : " + with_stat + "\n\t\t\t\tðŸŒ² Channel:" + final + "\n\t\t\t\tðŸ’° Refer: " + refer + "\n\t\t\t\tðŸ’° Minimum: " + mini_with + "\n\t\t\t\tðŸ’² Currency: " + currency + "\n\t\t\t\tðŸŽ Bonus: " + bonusamount + "\n\t\t\t\tðŸ“¤ Pay Channel: " + paychannel + "\n\t\t\t\tâœï¸ Paytm Keys :</b> <code>" + keys + "</code> "
                , { parse_mode: 'html', reply_markup: { inline_keyboard: [[{ text: "ðŸ’° Change Refer", callback_data: "refer" }, { text: "ðŸ’° Change Minimum", callback_data: "minimum" }], [{ text: "ðŸ¤– Bot : " + botstt + "", callback_data: "botstat" }], [{ text: "ðŸŒ² Change Channels", callback_data: "channels" }, { text: "ðŸŽ Change Bonus", callback_data: "bonus" }], [{ text: "ðŸ“¤ Withdrawals : " + with_stat + "", callback_data: "withstat" }], [{ text: "ðŸš¹ User Details", callback_data: "userdetails" }, { text: "ðŸ”„ Change Balance", callback_data: "changebal" }], [{ text: "âœï¸ Paytm Keys : " + keys + "", callback_data: "keys" }]] } })
        }
    } catch (error) {
        console.log(error)
    }
})
bot.action('withstat', async (ctx) => {
    try {
        let admin = await db.collection('admindb').find({ admin: "admin" }).toArray()
        let currency = admin[0].cur
        let paychannel = admin[0].paychannel
        let bonusamount = admin[0].bonus
        let mini_with = admin[0].minimum
        let refer = admin[0].ref
        let stat = admin[0].botstat
        let withst = admin[0].withstat
        let swg = admin[0].subwallet
        let mkey = admin[0].MKEY
        let mid = admin[0].MID
        let chnl = admin[0].channels
        var final = "\n\t\t\t\t";
        for (i in chnl) {
            final += chnl[i] + "\n\t\t\t\t";
        }
        if (swg == 'NOT SET' && mkey == 'NOT SET' && mid == 'NOT SET') {
            var keys = 'âŒ NOT SET'
        } else {
            var keys = 'âœ… SET'
        }
        if (stat == 'Active') {
            var botstt = 'âœ… Active'
        } else {
            var botstt = 'ðŸš« Disabled'
        }
        if (withst == 'ON') {
            var with_stat = 'ðŸš« Off'
            db.collection('admindb').updateOne({ admin: "admin" }, { $set: { withstat: 'OFF' } }, { upsert: true })
        } else {
            var with_stat = 'âœ… On'
            db.collection('admindb').updateOne({ admin: "admin" }, { $set: { withstat: 'ON' } }, { upsert: true })
        }
        if (ctx.from.id == 1003376875) {
            ctx.editMessageText("<b>ðŸ¡ Hey " + ctx.from.first_name + "\nðŸ¤˜ðŸ» Welcome To Admin Panel\n\nðŸ’¡ Bot Current Stats: \n\t\t\t\tðŸ“› Bot : @" + ctx.botInfo.username + "\n\t\t\t\tðŸ¤– Bot Status: " + botstt + "\n\t\t\t\tðŸ“¤ Withdrawals : " + with_stat + "\n\t\t\t\tðŸŒ² Channel:" + first + "\n\t\t\t\tðŸ’° Refer: " + refer + "\n\t\t\t\tðŸ’° Minimum: " + mini_with + "\n\t\t\t\tðŸ’² Currency: " + currency + "\n\t\t\t\tðŸŽ Bonus: " + bonusamount + "\n\t\t\t\tðŸ“¤ Pay Channel: " + paychannel + "\n\t\t\t\tâœï¸ Paytm Keys :</b> <code>" + keys + "</code> "
                , { parse_mode: 'html', reply_markup: { inline_keyboard: [[{ text: "ðŸ’° Change Refer", callback_data: "refer" }, { text: "ðŸ’° Change Minimum", callback_data: "minimum" }], [{ text: "ðŸ¤– Bot : " + botstt + "", callback_data: "botstat" }], [{ text: "ðŸŒ² Change Channels", callback_data: "channels" }, { text: "ðŸŽ Change Bonus", callback_data: "bonus" }], [{ text: "ðŸ“¤ Withdrawals : " + with_stat + "", callback_data: "withstat" }], [{ text: "ðŸš¹ User Details", callback_data: "userdetails" }, { text: "ðŸ”„ Change Balance", callback_data: "changebal" }], [{ text: "âœï¸ Paytm Keys : " + keys + "", callback_data: "keys" }]] } })
        }
    } catch (error) {
        console.log(error)
    }
})
bot.action('refer', async (ctx) => {
    try {
        ctx.deleteMessage()
        ctx.reply(
            '*ðŸ’¡ Enter New Refer Bonus Amount*', { parse_mode: 'markdown', reply_markup: { keyboard: [['â›” Cancel']], resize_keyboard: true } }
        )
        ctx.scene.enter('refer')
    } catch (error) {
        console.log(error)
    }
})
bot.action('minimum', async (ctx) => {
    try {
        ctx.deleteMessage()
        ctx.reply(
            '*ðŸ’¡ Enter New Minimum Withdraw Amount*', { parse_mode: 'markdown', reply_markup: { keyboard: [['â›” Cancel']], resize_keyboard: true } }
        )
        ctx.scene.enter('mini')
    } catch (error) {
        console.log(error)
    }
})
bot.action('bonus', async (ctx) => {
    try {
        ctx.deleteMessage()
        ctx.reply(
            '*ðŸ’¡ Enter New Daily Bonus Amount*', { parse_mode: 'markdown', reply_markup: { keyboard: [['â›” Cancel']], resize_keyboard: true } }
        )
        ctx.scene.enter('bonus')
    } catch (error) {
        console.log(error)
    }
})
bot.action('userdetails', async (ctx) => {
    try {
        ctx.deleteMessage()
        ctx.reply(
            '*ðŸ’¡ Enter Users Telegram Id to Check His Info*', { parse_mode: 'markdown', reply_markup: { keyboard: [['â›” Cancel']], resize_keyboard: true } }
        )
        ctx.scene.enter('tgid')
    } catch (error) {
        console.log(error)
    }
})
bot.action('keys', async (ctx) => {
    try {
        let admin = await db.collection('admindb').find({ admin: "admin" }).toArray()
        let swg = admin[0].subwallet
        let mkey = admin[0].mkey
        let mid = admin[0].mid
        let com = admin[0].comment
        if (swg == 'NOT SET' && mkey == 'NOT SET' && mid == 'NOT SET') {
            var keys = 'âŒ NOT SET'
            ctx.editMessageText("*âœï¸ Your Paytm Keys: \n\nðŸ—ï¸ Subwallet Guid :* `" + keys + "`\n*ðŸ—ï¸ Merchant Key:* `" + keys + "`\n*ðŸ—ï¸ Merchant Id :* `" + keys + "`\n*ðŸ’¬ Comment :* `" + com + "`", { parse_mode: 'markdown', reply_markup: { inline_keyboard: [[{ text: "âœ… SUBWALLET GUID", callback_data: "subwallet" }, { text: "âœ… MERCHANT KEY", callback_data: "mkey" }], [{ text: "âœ… MERCHANT ID", callback_data: "mid" }, { text: "âœ… COMMENT", callback_data: "comment" }]] } })
        } else {
            ctx.editMessageText("*âœï¸ Your Paytm Keys: \n\nðŸ—ï¸ Subwallet Guid :* `" + swg + "`\n*ðŸ—ï¸ Merchant Key:* `" + mkey + "`\n*ðŸ—ï¸ Merchant Id :* `" + mid + "`\n*ðŸ’¬ Comment :* `" + com + "`", { parse_mode: 'markdown', reply_markup: { inline_keyboard: [[{ text: "âœ… SUBWALLET GUID", callback_data: "subwallet" }, { text: "âœ… MERCHANT KEY", callback_data: "mkey" }], [{ text: "âœ… MERCHANT ID", callback_data: "mid" }, { text: "âœ… COMMENT", callback_data: "comment" }]] } })
        }
    } catch (error) {
        console.log(error)
    }
})
bot.action('subwallet', async (ctx) => {
    try {
        ctx.deleteMessage()
        ctx.reply(
            '*ðŸ’¡ Send Your Subwallet GUID*', { parse_mode: 'markdown', reply_markup: { keyboard: [['â›” Cancel']], resize_keyboard: true } }
        )
        ctx.scene.enter('subwallet')
    } catch (error) {
        console.log(error)
    }
})
bot.action('mkey', async (ctx) => {
    try {
        ctx.deleteMessage()
        ctx.reply(
            '*ðŸ’¡ Send Your Merchant Key*', { parse_mode: 'markdown', reply_markup: { keyboard: [['â›” Cancel']], resize_keyboard: true } }
        )
        ctx.scene.enter('mkey')
    } catch (error) {
        console.log(error)
    }
})
bot.action('mid', async (ctx) => {
    try {
        ctx.deleteMessage()
        ctx.reply(
            '*ðŸ’¡ Send Your Merchant Id*', { parse_mode: 'markdown', reply_markup: { keyboard: [['â›” Cancel']], resize_keyboard: true } }
        )
        ctx.scene.enter('mid')
    } catch (error) {
        console.log(error)
    }
})
bot.action('comment', async (ctx) => {
    try {
        ctx.deleteMessage()
        ctx.reply(
            '*ðŸ’¡ Send Your Description For Payment*', { parse_mode: 'markdown', reply_markup: { keyboard: [['â›” Cancel']], resize_keyboard: true } }
        )
        ctx.scene.enter('comment')
    } catch (error) {
        console.log(error)
    }
})
bot.action('changebal', async (ctx) => {
    try {
        ctx.deleteMessage()
        ctx.reply(
            '*ðŸ’¡ Send User Telegram Id & Amount\n\nâš ï¸ Use Format : *`' + ctx.from.id + ' 10`', { parse_mode: 'markdown', reply_markup: { keyboard: [['â›” Cancel']], resize_keyboard: true } }
        )
        ctx.scene.enter('incr')
    } catch (error) {
        console.log(error)
    }
})
bot.action('channels', async (ctx) => {
    try {
        let admin = await db.collection('admindb').find({ admin: "admin" }).toArray()
        let chnl = admin[0].channels
        var final = "";
        if (chnl.length == 0) {
            final = "ðŸ“£ No Channels Set"
        } else {
            for (i in chnl) {
                final += chnl[i] + "\n\t\t\t\t";
            }
        }
        ctx.editMessageText("<b>ðŸ¡ Currently Set Channels:\n\t\t\t\t " + final + " </b>", { parse_mode: 'html', reply_markup: { inline_keyboard: [[{ text: "âž• Add Channels", callback_data: "chnl" }, { text: "âž– Remove Channel", callback_data: "removechnl" }], [{ text: "ðŸ“¤ Pay Channel", callback_data: "paychannel" }]] } })
    } catch (error) {
        console.log(error)
    }
})
bot.action('chnl', async (ctx) => {
    try {
        ctx.deleteMessage()
        ctx.reply(
            '*ðŸ’¡ Send New Username Of Channel*', { parse_mode: 'markdown', reply_markup: { keyboard: [['â›” Cancel']], resize_keyboard: true } }
        )
        ctx.scene.enter('chnl')
    } catch (error) {
        console.log(error)
    }
})
bot.action('removechnl', async (ctx) => {
    try {
        ctx.deleteMessage()
        ctx.reply(
            '*ðŸ’¡ Send Username Of Channel*', { parse_mode: 'markdown', reply_markup: { keyboard: [['â›” Cancel']], resize_keyboard: true } }
        )
        ctx.scene.enter('removechnl')
    } catch (error) {
        console.log(error)
    }
})
bot.action('paychannel', async (ctx) => {
    try {
        ctx.deleteMessage()
        ctx.reply(
            '*ðŸ’¡ Send Username Of Channel*', { parse_mode: 'markdown', reply_markup: { keyboard: [['â›” Cancel']], resize_keyboard: true } }
        )
        ctx.scene.enter('paychnl')
    } catch (error) {
        console.log(error)
    }
})
bot.action('check', async (ctx) => {
    try {
        let userdata = await db.collection('pendingUsers').find({ userID: ctx.from.id }).toArray()
        let invite = userdata[0].inviter
        ctx.editMessageText(
            "<b>ðŸ’¹ You Were Invited By <a href='tg://user?id=" + invite + "'>" + invite + "</a></b>", { parse_mode: 'html' }
        )
    } catch (error) {
        console.log(error)
    }
})
bot.action('wallet', async (ctx) => {
    try {
        ctx.deleteMessage()
        let admin = await db.collection('admindb').find({ admin: "admin" }).toArray()
        let currency = admin[0].cur
        ctx.reply(
            '*âœï¸ Now Send Your ' + currency + ' Wallet Address To Use It For Future Withdrawals*\n\nâš ï¸ _This Wallet Will Be Used For Future Withdrawals !!_', { parse_mode: 'markdown', reply_markup: { keyboard: [['â›” Cancel']], resize_keyboard: true } }
        )
        ctx.scene.enter('wallet')
    } catch (error) {
        console.log(error)
    }
})

async function mustjoin(ctx) {
    try {
        let admin = await db.collection('admindb').find({ admin: "admin" }).toArray()
        let chnl = admin[0].channels
        var final = '';
        for (i in chnl) {
            final += chnl[i] + "\n";
        }
        ctx.reply(
            "<b>â›” Must Join All Our Channel</b>\n\n" + final + "\n<b>âœ… After Joining, Click On 'ðŸŸ¢ Joined'</b>", { parse_mode: 'html', reply_markup: { keyboard: [['ðŸŸ¢ Joined']], resize_keyboard: true } }
        )
    } catch (error) {
        console.log(error)
    }
};
function sleep(in_sec) {
    return new Promise(resolve => setTimeout(resolve, in_sec * 1000));
};
function paytm(wallet, amount, subwallet, mkey, mid, comment) {
     const https = require('https');
     const PaytmChecksum = require('./PaytmChecksum');

     var id = between(10000000, 99999999);
     var order = "ORDERID_" + id

     var paytmParams = {};

     paytmParams["subwalletGuid"] = subwallet;
     paytmParams["orderId"] = order;
     paytmParams["beneficiaryPhoneNo"] = wallet;
     paytmParams["amount"] = parseInt(amount);
     paytmParams["comments"] = comment;

     var post_data = JSON.stringify(paytmParams);

     PaytmChecksum.generateSignature(post_data, mkey).then(function (checksum) {

         var x_mid = mid;
         var x_checksum = checksum;

         var options = {
             hostname: 'dashboard.paytm.com',
             path: '/bpay/api/v1/disburse/order/wallet/gratification',
             port: 443,
            method: 'POST',
            headers: {
                 'Content-Type': 'application/json',
                 'x-mid': x_mid,
                'x-checksum': x_checksum,
                 'Content-Length': post_data.length
            }
         };

         var response = "";
         var post_req = https.request(options, function (post_res) {
             post_res.on('data', function (chunk) {
                 response += chunk;
            });

             post_res.on('end', function () {
                 console.log(response)
             });
         });

         post_req.write(post_data);
         post_req.end();
     });
 };
 function between(min, max) {
     return Math.floor(
         Math.random() * (max - min) + min
     )
 }
function arrayRemove(arr, value) {

     return arr.filter(function (ele) {
         return ele != value;
     });
 }
 function contains(obj, list) {
     var i;
     for (i = 0; i < list.length; i++) {
         if (list[i] === obj) {
             return true;
        }
    }
    return false;
 }
