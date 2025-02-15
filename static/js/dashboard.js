
function selectAsset(url, name) {
    document.getElementById('picture').value = window.location.origin + url;
    document.getElementById('selectAssetBtn').innerHTML = "Change selected asset (" + name + ")";
    document.getElementById('selectAssetBtn').style.backgroundColor = "#873319";
    var selectAssetEl = document.getElementById('selectAsset');
    var selectAsset = bootstrap.Modal.getInstance(selectAssetEl)
    selectAsset.hide();
}