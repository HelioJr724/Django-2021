let searchForm = document.getElementById('searchForm')
let pageLinks = document.getElementsByClassName('page-link')
if (searchForm) {
for (let index = 0; pageLinks.length > index; index++) {
    pageLinks[index].addEventListener('click', function (e) {
    e.preventDefault()
    let page = this.dataset.page
    searchForm.innerHTML += `<input value=${page} name="page" hidden />`
    searchForm.submit()
    })
}
}