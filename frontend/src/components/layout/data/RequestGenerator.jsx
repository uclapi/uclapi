export function getRequest(url, params, isDemo = false) {
  let now = new Date();

  // Setup the pythoncode code segment
  var pythoncode = `import requests\n`+`\n`+`params = {\n`;
  for(var key in params) {
    pythoncode += `\t "${key}": "${params[key]}",\n`;
  }
  pythoncode += `}\n` + `r = requests.get("${url}", params=params)\n` + `print(r.json())`;

  // Setup the javascriptcode code segment
  var javascriptcode = `fetch("${url}?`;
  var isFirst=true;
  for(var key in params) {
    if(isFirst) {javascriptcode += `${key}=${params[key]}`; isFirst=false;}
    else {javascriptcode += `&${key}=${params[key]}`;}
  }
  javascriptcode += `")\n` + `.then((response) => {\n` + `\t return response.json() \n` + `})\n` + `.then((json) => {\n`;
  javascriptcode += `\t console.log(json);\n` + `})`;

  // Setup the shellcode code segment
  var shellcode = `curl -G ${url} \ \n`
  for(var key in params) {
    shellcode += `\t -d ${key}=${params[key]}\n`;
  }

  if(isDemo) {
    return [
      {
        "name": "python",
        "code": pythoncode
      },
      {
        "name": "javascript",
        "code": javascriptcode
      },
      {
        "name": "shell",
        "code": shellcode
      },
    ];
  } else {
    return {
        python: pythoncode,
        javascript: javascriptcode,
        shell: shellcode
    };
  }
}