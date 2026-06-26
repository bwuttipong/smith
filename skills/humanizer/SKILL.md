# humanizer

> Humanize a value to human-readable format (e.g. bytes, ms).

## bin
`humanizer` → `/Users/Jeff/.npm-global/bin/humanizer`

## env
PATH includes `/Users/Jeff/.npm-global/bin`

## setup
```bash
npm install -g humanizer
mkdir -p ~/.npm-global/bin
cat > ~/.npm-global/bin/humanizer << 'SCRIPT'
#!/usr/bin/env node
var H = require('/Users/Jeff/.npm-global/lib/node_modules/humanizer');
var h = new H('B', 1)
  .unit('KB', 1024)
  .unit('MB', 1024*1024)
  .unit('GB', 1024*1024*1024)
  .unit('TB', 1024*1024*1024*1024);
h._sorter = function(a, b){ return b.value - a.value; };
h._selector = function(v){ return v >= 1 && v < 1000; };
h.setRound(function(v){ return Math.round(v*100)/100; });
var val = parseFloat(process.argv[2]) || 0;
var result = h.humanize(val);
console.log(result.join(' '));
SCRIPT
chmod +x ~/.npm-global/bin/humanizer
```

## usage
```bash
humanizer 1024      → 1 KB
humanizer 1048576   → 1 MB
humanizer 1536      → 1.5 KB
humanizer 1         → 1 B
```

## details
Wraps `humanizer@0.1.1` npm package by @fgribreau. Supports any unit/scales via Humanize class:
```javascript
var Humanize = require('humanizer').Humanize;
var h = new Humanize('ms', 1)
  .unit('sec', 1000)
  .unit('min', 60 * 1000)
  .unit('hour', 60 * 60 * 1000);
h.humanize(3600000) // [ 1, 'hour' ]
```
