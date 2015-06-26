var config = process.argv[2],
input = process.argv[3],
OpenCC = require('opencc'),
opencc = new OpenCC(config),
converted = opencc.convertSync(input);

process.stdout.write(converted)