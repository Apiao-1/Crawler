const utils = require("./utils")
const cheerio = require('cheerio')
const v = require('voca')
const mongo = require('./mongo')
const fs = require('fs')
const log = require('./log')

const host = "http://chinadxscy.csu.edu.cn/"
const firstListPage = "http://chinadxscy.csu.edu.cn/entre/info/hot/"

const urlRecordFilename = './data/daxuesheng_chuangye_wang_url.json'

utils.co(function* () {
    "use strict"

    let urlRecords = require(urlRecordFilename)

    try {
        yield* mongo.gInit()

        let c = mongo.db().collection('OutArticle')

        let unFetchPageUrls = yield* gGetPagesUrls(urlRecords)

        for (let i = 0; i < 100; i++) {
            let pageUrl = unFetchPageUrls[i]
            if (urlRecords[pageUrl.href]) continue
            try {
                let r = yield* gGetPageContent(pageUrl)
                r.link = pageUrl.href
                yield c.insert(r)
                urlRecords[pageUrl.href] = pageUrl.label
            } catch (e) {
                console.error(e)
            }
        }
    } catch (e) {
        console.error(e)
    } finally {
        fs.writeFile(urlRecordFilename, JSON.stringify(urlRecords))

        yield* mongo.gDispose()
    }
})

function* gGetPagesUrls(urlRecords) {
    "use strict"
    let unFetchPageUrls = []
    let pageContent = yield* utils.gGetPage(firstListPage)
    // console.log(pageContent)
    const $ = cheerio.load(pageContent)
    let a = $('.page_no a').last()
    let href = a.attr('href')
    let parts = /list_(\d+)/.exec(href)
    if (!(parts && parts.length)) throw "bad page num href: " + href
    let pageNum = parseInt(parts[1], 10)
    console.log(pageNum)

    pageNum = 10

    for (let pageNo = 1; pageNo <= pageNum; pageNo++) {
        let pagUrl = `http://chinadxscy.csu.edu.cn/entre/info/hot/list_${pageNo}.html`
        console.log("Fetch List", pagUrl)
        let pageContent = yield* utils.gGetPage(pagUrl)
        const $ = cheerio.load(pageContent)
        $('.center_box .list_box a').each((index, ele) => {
            let $this = $(ele)
            let href = host + $this.attr('href')
            if (!urlRecords[href]) {
                let label = $this.text()
                unFetchPageUrls.push({href: href, label: label})
            }
        })
    }

    console.log("unFetchPageUrls", unFetchPageUrls.length)
    return unFetchPageUrls
}

function* gGetPageContent(pageUrl) {
    "use strict"
    console.log("Fetch Page", pageUrl.href)
    let pageContent = yield* utils.gGetPage(pageUrl.href)
    const $ = cheerio.load(pageContent)
    let title = $('.view_box .view_title').text()
    let msg = $('.view_box .view_msg').text()
    let parts = /发布时间：(\d+)年(\d+)月(\d+)日/.exec(msg)
    if (!(msg && msg.length)) throw "bad msg: " + msg + "|" + pageUrl.href
    let year = parseInt(parts[1], 10)
    let month = parseInt(parts[2], 10)
    let day = parseInt(parts[3], 10)
    let body = $('.view_box .view_body')
    let images = body.find("img")
    let imageCount = Math.min(images.length, 4)
    let figures = []
    for (let i = 0; i < imageCount; i++) {
        let img = images.get(i)
        let src = $(img).attr('src')
        if (!v.startsWith(src, "http")) src = host + src
        figures.push(src)
    }
    let abstract = body.text().substring(0, 100)
    abstract = abstract.replace(/(\s)/g, '')
    abstract = v.trim(abstract)
    let date = year * 10000 + month * 100 + day
    let category = 'top'
    return {category, title, date, year, month, day, body: body.html(), figures, abstract, _createdOn: new Date()}
}