(function () {
    const co = require('co')
    const Promise = require('bluebird')
    const request = require('request')
    const pRequestHead = Promise.promisify(request.head)
    const pRequestGet = Promise.promisify(request.get)

    exports.gGetPage = function *(url) {
        "use strict"
        let r = yield pRequestGet(url)
        if (!(r && r.statusCode === 200)) {
            console.log('statusCode:', r && r.statusCode)
            throw "Not 200, " + r.statusCode
        }
        return r.body
    }

    exports.co = function (generator) {
        "use strict"
        co(generator).catch(function (e) {
            console.error(e)
        })
    }
})()
