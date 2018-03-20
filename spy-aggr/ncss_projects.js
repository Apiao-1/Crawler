const utils = require("./utils")
const cheerio = require('cheerio')
const v = require('voca')
const mongo = require('./mongo')
const fs = require('fs')
const log = require('./log')

const host = "http://cy.ncss.org.cn/"

const urlRecordFilename = './data/ncss_projects.json'

utils.co(function* () {
    "use strict"

    let urlRecords = require(urlRecordFilename)

    try {
        yield* mongo.gInit()

        let c = mongo.db().collection('OutArticle')

        let unFetchPageUrls = yield* gGetPagesUrls(urlRecords)

        for (let i = 0; i < 500; i++) {
            let pageInfo = unFetchPageUrls[i]
            if (urlRecords[pageInfo.href]) continue
            try {
                let r = yield* gGetPageContent(pageInfo)
                r.link = pageInfo.href
                // console.log(r)
                yield c.insert(r)
                urlRecords[pageInfo.href] = pageInfo.label
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

    let pageContent = yield* utils.gGetPage("http://cy.ncss.org.cn/search/projectcount")
    let total = parseInt(pageContent, 10)
    console.log("total", total)

    const pageSize = 20
    // const pageNum = Math.ceil(total / pageSize)

    const pageNum = 40

    for (let pageIndex = 0; pageIndex < pageNum; pageIndex++) {
        let pagUrl = `http://cy.ncss.org.cn/search/projectlist?pageIndex=${pageIndex}&pageSize=${pageSize}`
        console.log("Fetch List", pagUrl)
        let pageContent = yield* utils.gGetPage(pagUrl)
        const $ = cheerio.load(pageContent)
        $('.search-list-item').each((index, ele) => {
            let $this = $(ele)
            let imageSrc = $this.find('.project-list-face img').first().attr('src')
            if (imageSrc && !v.startsWith(imageSrc, "data:image/")) imageSrc = host + imageSrc

            let href = $this.find('.project-list-info a').first().attr('href')
            href = host + href

            let title = $this.find('.project-list-item-title').first().text()
            title = v.trim(title)

            let $info = $this.find('.project-list-item-tags-text')
            let infoSpans = $info.find('span')
            let school = $(infoSpans.get(0)).text()
            let area = $(infoSpans.get(1)).text()

            $info = $this.find('.project-list-item-tags-img').first()
            let tags = []
            $info.find('span').each((i2, ele) => tags.push(v.trim($(ele).text())))

            let abstract = $this.find('.project-list-item-desc').first().text()
            abstract = v.trim(abstract)

            if (!urlRecords[href]) {
                unFetchPageUrls.push({href: href, label: title, school, area, tags, abstract, imageSrc})
            }
        })
    }

    console.log("unFetchPageUrls", unFetchPageUrls.length)
    for (let i = 0; i < 10; i++) {
        console.log(unFetchPageUrls[i])
    }

    return unFetchPageUrls
}

function* gGetPageContent(pageInfo) {
    "use strict"
    console.log("Fetch Page", pageInfo.href)
    let pageContent = yield* utils.gGetPage(pageInfo.href)
    const $ = cheerio.load(pageContent)

    let html = ""
    let $bs = $('.project-block')
    let $d = $($bs.get(0)).find('.project-block-content div').first()
    html += v.trim($d.html())
    html += v.trim($d.next().html())

    $d = $($bs.get(1)).find('.project-block-content div').first()
    html += v.trim($d.html())
    html += v.trim($d.next().html())

    let category = 'project'

    let figures = [pageInfo.imageSrc]
    return {
        category, title: pageInfo.label, body: html, abstract: pageInfo.abbr, _createdOn: new Date(),
        tags: pageInfo.tags, area: pageInfo.area, school: pageInfo.school, figures
    }
}