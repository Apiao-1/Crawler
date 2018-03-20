(function() {
  var bunyan, system;

  bunyan = require('bunyan');

  system = bunyan.createLogger({
    name: "system",
    level: "trace"
  });

  exports.system = system;

}).call(this);
