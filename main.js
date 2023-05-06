const fs = require("fs");
const path = require("path");
const { create } = require("xmlbuilder2");

// Get file info
function fFile(fPath) {
  if (!fs.existsSync(fPath)) {
    throw new Error(`${fPath} does not exist!`);
  }
  const file = fs.statSync(fPath);
  file.isDirectory = file.isDirectory();
  file.isFile = file.isFile();
  file.path = path.resolve(fPath);
  file.location = path.dirname(fPath);
  file.relativePath = path.relative(process.cwd(), fPath);
  file.name = path.basename(fPath);
  file.extention = path.extname(fPath);
  return file;
}

// Get folder info
function fFolder(fPath, folderStruct) {
  const folder = fFile(fPath);
  if (!folder.isDirectory) {
    throw new Error(`${fPath} is not a Directory!`);
  } else {
    folder.items = [];
  }
  const items = fs.readdirSync(fPath);
  items.forEach(item => {
    const itemPath = `${fPath}/${item}`;
    const stats = fs.lstatSync(itemPath);
    if (!stats.isSymbolicLink()) {
      if (stats.isDirectory()) {
        folder.items.push(fFolder(itemPath));
      } else if (stats.isFile()) {
        folder.items.push(fFile(itemPath));
      }
    }
  });
  return folder;
}

function sanitizeXMLName(name) {
  // Replace invalid characters with an underscore
  let sanitizedName = name.replace(/[^a-zA-Z0-9_\-]/g, '_');

  // Ensure the name starts with a letter or underscore
  if (!/^[a-zA-Z_]/.test(sanitizedName)) {
    sanitizedName = '_' + sanitizedName;
  }

  return sanitizedName;
}
// turn a file or folder info into an xml
function fXML(fFile, root) {
  if (root === undefined) {
    root = create({ version: '1.0' }).ele(`${sanitizeXMLName(fFile.name)}`);
  }

  for (let key in fFile) {
    if (fFile.hasOwnProperty(key)) {
      if (key === 'items') {
        let childRoot = root.ele(key);
        fFile[key].forEach(item => {
          let itemRoot = childRoot.ele(sanitizeXMLName(item.name));
          fXML(item, itemRoot);
        });
      } else {
        root.ele(sanitizeXMLName(key)).txt(fFile[key]).up();
      }
    }
  }
  return root;
}

if(process.argv[2] === undefined ){
    console.log(`please provide a path! `)
    process.exit(-1);
}else{
    console.log(fXML(fFolder(process.argv[2])).end({ prettyPrint: true}));
    process.exit(0);
}

