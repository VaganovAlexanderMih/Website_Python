function deleteFile(file_id) {
  fetch("/delete-file", {
    method: "POST",
    body: JSON.stringify({ file_id: file_id }),
  }).then((_res) => {
    window.location.href = "/encryption";
});
}

function get_url() {
  return window.location.href;
}