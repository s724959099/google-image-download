let script = document.createElement('script')
script.src = "https://ajax.googleapis.com/ajax/libs/jquery/2.2.0/jquery.min.js"
document.getElementsByTagName('head')[0].appendChild(script)

let urls = $('.rg_di .rg_meta').map(function() { return JSON.parse($(this).text()).ou })

let textToSave = urls.toArray().join('\n')
let hiddenElement = document.createElement('a')
hiddenElement.href = 'data:attachment/text,' + encodeURI(textToSave)
hiddenElement.target = '_blank'
hiddenElement.download = 'urls.txt'
hiddenElement.click()