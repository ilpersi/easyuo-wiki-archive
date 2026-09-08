function filterDocumentationLinks(a) {
    let href = a.getAttribute('href');

    return !href.startsWith('#');
}

function getPageTitle(a) {
    let href = 'http://wiki.easyuo.com' + a.getAttribute('href');
    let url = new URL(href);

    return url.searchParams.get('title') || '';
}

// This script is intended to be run on http://wiki.easyuo.com/index.php?title=Documentation
// We get all the links
var links = Array.from(document.querySelectorAll('td a, li a'))
links = links.filter(filterDocumentationLinks);
links = links.map(getPageTitle);

// We include the root documentation page
links.push('Documentation');

// We use a set to make sure page names are unique
var uniqueSet = new Set(links);

// We covert everything back to the originally array and sort it
links = Array.from(uniqueSet).sort();

// We copy everything into the clipboard
copy(links.join('\n'));