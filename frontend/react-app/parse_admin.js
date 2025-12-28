const fs = require('fs');
const parser = require('@babel/parser');
const path = 'src/pages/admin/AdminDashboard.jsx';
const code = fs.readFileSync(path, 'utf8');
try{
  parser.parse(code, {
    sourceType: 'module',
    plugins: ['jsx', 'classProperties', 'optionalChaining', 'nullishCoalescingOperator']
  });
  console.log('Parsed OK')
}catch(e){
  console.error(e.message);
  console.error(e.loc);
  process.exit(1);
}
