/**
 * Paste in Chrome developer console to download links from a page to a CSV 
 * file. You'll have to clean out the ones that you don't want. 
 */
// Store link text and URL
let linksNodeList = document.querySelectorAll("a")
let linksArr = []
// NodeList doesn't have .map method
linksNodeList.forEach(l => {
    // Remove commas from title because CSV interprets it as next column
    linksArr.push([ l.textContent.replace(/[, ]+/g," ").trim(), l.href ])
})

// CSV format: https://stackoverflow.com/a/14966131
let csvContent = "data:text/csv;charset=utf-8," 
    + linksArr.map(l => l.join(",")).join("\n")

// Use encodeURI and an appended link to download CSV file
let encodedUri = encodeURI(csvContent)
let link = document.createElement("a")
link.setAttribute("href", encodedUri)
link.setAttribute("download", "links.csv")
document.body.appendChild(link)
link.click()
