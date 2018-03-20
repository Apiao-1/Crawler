(function() {
  var MongoClient, ObjectId, config, db, gInitIndex, log, mongodb;

  mongodb = require('mongodb');

  ObjectId = mongodb.ObjectId;

  MongoClient = mongodb.MongoClient;

  log = require('./log');

  config = require('./config');

  db = null;

  exports.gInit = function*() {
    if (db) {
      return db;
    }
    db = (yield MongoClient.connect(config.mongo));
    db.on('close', (function(_this) {
      return function() {
        db = null;
        return log.system.info("MongoDB closed");
      };
    })(this));
    db.on('error', (function(_this) {
      return function(e) {
        db = null;
        return log.system.error(e, "MongoDB error");
      };
    })(this));
    db.on('reconnect', (function(_this) {
      return function() {
        return log.system.info("Mongo DB reconnect");
      };
    })(this));
    yield* gInitIndex();
    return db;
  };

  exports.db = function() {
    return db;
  };

  exports.gDispose = function*() {
    var e;
    log.system.info("Closing mongodb ...");
    if (!db) {
      return;
    }
    try {
      return (yield db.close());
    } catch (error) {
      e = error;
      return log.system.error(e, "dispose mongodb");
    }
  };

  exports.getInsertedIdObject = function(r) {
    return (r != null ? r.insertedId : void 0) || null;
  };

  exports.getUpdateResult = function(r) {
    return {
      matchedCount: r.matchedCount,
      modifiedCount: r.modifiedCount
    };
  };

  exports.isIndexConflictError = function(e) {
    return e.code === 11000;
  };

  exports.stringToObjectId = function(string) {
    if (!string) {
      return null;
    }
    if (string instanceof ObjectId) {
      return string;
    } else {
      return new ObjectId(string);
    }
  };

  exports.stringToObjectIdSilently = function(string) {
    if (string instanceof ObjectId) {
      return string;
    }
    if (string == null) {
      return string;
    }
    try {
      return new ObjectId(string);
    } catch (error) {
      return void 0;
    }
  };

  exports.stringArrayToObjectIdArraySilently = function(strings) {
    var i, id, ids, len, s;
    if (strings == null) {
      return [];
    }
    ids = [];
    for (i = 0, len = strings.length; i < len; i++) {
      s = strings[i];
      id = exports.stringToObjectIdSilently(s);
      if (id != null) {
        ids.push(id);
      }
    }
    return ids;
  };

  exports.toDupKeyError = function(e, indexNamesToMessage) {
    var indexName, matches, message;
    matches = e.message.match(/index:\s(.+)\$(.+) dup key: (.+)/);
    if (matches) {
      indexName = matches[2];
      message = indexNamesToMessage[indexName];
      return {
        code: "DupKey",
        message: message,
        key: indexName
      };
    } else {
      return {
        code: "DupKey",
        message: '值重复'
      };
    }
  };

  gInitIndex = function*() {
    var c, options;
    c = db.collection('User');
    options = {
      name: 'UserUsername'
    };
    options.unique = true;
    options.sparse = false;
    return (yield c.createIndex({
      username: 1
    }, options));
  };

}).call(this);
