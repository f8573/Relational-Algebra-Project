const assert = require('assert')
const { detectAndBuildTable } = require('../src/components/resultParser.cjs')

function testSingleCharGrid(){
  const input = `(name:string)
----
G r e g
D e b
M i c h
t u e
2 rows` 
  const out = detectAndBuildTable(input)
  assert(out)
  assert.deepStrictEqual(out.cols, ['name : string'])
  const names = out.rows.map(r=> r[0])
  if (!names.some(n => n.includes('Greg') || n.includes('Gregory'))){
    console.error('Names did not merge as expected:', names)
    throw new Error('Name merge failed')
  }
}

function testMulticolConcat(){
  const input = `acctid : numbername : stringbalance : number
1001,John,2345.67
1002,Jane,1234.00` 
  const out = detectAndBuildTable(input)
  assert(out)
  assert.deepStrictEqual(out.cols, ['acctid : number','name : string','balance : number'])
  assert.strictEqual(out.rows.length, 2)
  assert.deepStrictEqual(out.rows[0], ['1001','John','2345.67'])
}

function testArrayOfObjects(){
  const arr = [ {a:1,b:2}, {a:3,b:4} ]
  const out = detectAndBuildTable(arr)
  assert(out)
  assert(out.cols.includes('a'))
  assert(out.cols.includes('b'))
  assert.strictEqual(out.rows.length, 2)
}

function runAll(){
  testSingleCharGrid();
  console.log('testSingleCharGrid OK')
  testMulticolConcat();
  console.log('testMulticolConcat OK')
  testArrayOfObjects();
  console.log('testArrayOfObjects OK')
}

runAll()
