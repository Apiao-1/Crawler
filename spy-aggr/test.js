(function () {
    "use strict"
    const request = require('request')
    const jsdom = require("jsdom")
    const {JSDOM} = jsdom
    const v = require('voca')
    const Promise = require('bluebird')
    const co = require('co')
    const fs = require('fs')
    const cheerio = require('cheerio')

    // const rootUrl = 'http://cy.ncss.org.cn'
    const rootUrl = 'http://www.jycypt.com'

    const visited = {}
    let visitedCount = 0
    const outLinks = {}
    const unvisited = [{link: rootUrl, label: 'root'}]

    let ignoreLinks = ['/', '', 'javascript:void(0);', "#", "about:blank#", "javascript", "javascript:;", "javascript:"]
    let ignorePrefixes = ['mailto:', "javascript"]

    let ignoreLinksCount = {}
    ignoreLinks.forEach((href) => ignoreLinksCount[href] = 1)
    ignorePrefixes.forEach((href) => ignoreLinksCount[href] = 1)

    const pRequestHead = Promise.promisify(request.head)
    const pRequestGet = Promise.promisify(request.get)

    co(function*() {
        while (unvisited.length && visitedCount < 30) {
            let unvisitedLink = unvisited[unvisited.length - 1]
            unvisited.length = unvisited.length - 1
            visited[unvisitedLink.link] = unvisitedLink
            visitedCount++
            console.log("Visit", visitedCount, unvisitedLink.link)

            try {
                let r = yield pRequestHead(unvisitedLink.link)

                let contentType = r.headers['content-type']
                console.log(contentType)
                if (contentType && !v.startsWith(contentType, 'text/html')) {
                    console.log("Ignore")
                    continue
                }

                if (!(r && r.statusCode === 200)) {
                    console.log('statusCode:', r && r.statusCode)
                }

                r = yield pRequestGet(unvisitedLink.link)

                let links = getAllTagAByCheerio(r.body)

                links.forEach(function (link) {
                    let href = v.trim(link.href)

                    if (ignoreLinksCount[href]) {
                        ignoreLinksCount[href]++
                        return
                    }

                    for (let i in ignorePrefixes) {
                        let ignorePrefix = ignorePrefixes[i]
                        if (v.startsWith(href, ignorePrefix)) {
                            ignoreLinksCount[ignorePrefix]++
                            return
                        }
                    }

                    if (!v.startsWith(href, 'http')) {
                        href = rootUrl + href
                    }

                    if (visited[href]) {
                        return
                    }

                    if (v.startsWith(href, "http") && !v.startsWith(href, rootUrl)) {
                        outLinks[href] = v.trim(link.label)
                        return
                    }

                    unvisited.push({link: href, inLabel: v.trim(link.label)})
                })

                console.log("=====")
            } catch (e) {
                throw e
            }
        }
    }).then(function () {
        fs.writeFile('visited', JSON.stringify(visited, null, 4))
        // console.log(visited)
        console.log("======\n======ignoreLinksCount")
        console.log(ignoreLinksCount)
        console.log("======\n======outLinks")
        console.log(outLinks)
        console.log("======\n======")
        console.log("unvisited", unvisited.length)
    }).catch(function (e) {
        console.error(e)
    })


    function getAllTagAByJsDom(text) {
        const dom = new JSDOM(text)
        let links = []
        dom.window.document.querySelectorAll("a").forEach((e) => links.push({href: e.href, label: e.textContent()}))
        return links
    }

    function getAllTagAByCheerio(text) {
        const $ = cheerio.load(text)
        let links = []
        let a = $("a")
        a.each((index, ele) => {
            let $this = $(ele)
            links.push({href: $this.attr('href'), label: $this.text()})
        })
        return links
    }
})()

